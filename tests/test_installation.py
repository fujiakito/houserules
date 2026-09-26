"""Run: python -m unittest discover -s tests -v

Fixtures are retained in the OS temp directory; no recursive cleanup is performed.
"""
from __future__ import annotations

import io
import json
import os
import re
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

import check
import install


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="houserules-test-"))

    def run_install(self, *args):
        return subprocess.run(
            [sys.executable, str(getattr(self, "installer", install.HERE / "install.py")),
             "--repo", str(self.repo), *args],
            capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"},
        )

    def install_ok(self, *args):
        result = self.run_install(*args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def sync(self):
        report = check.Report()
        check.check_sync(self.repo, report)
        return report

    def foreign(self, name="foreign-example"):
        path = self.repo / ".claude/skills" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\nname: " + name + "\ndescription: User procedure\n---\nUser content\n",
                        encoding="utf-8")
        return path

    def test_foreign_skill_is_preserved_and_not_replicated(self):
        foreign = self.foreign()
        content = foreign.read_bytes()
        self.install_ok()
        self.assertFalse(self.sync().failed)
        self.assertEqual(foreign.read_bytes(), content)
        self.assertFalse((self.repo / ".agents/skills/foreign-example").exists())
        self.assertNotIn("foreign-example", check.read_manifest(self.repo)["skills"])

    def test_prefix_does_not_claim_ownership(self):
        self.foreign("hr-personal")
        self.install_ok()
        self.assertFalse(self.sync().failed)
        self.assertNotIn("hr-personal", check.read_manifest(self.repo)["skills"])

    def test_selected_agents_and_additive_install(self):
        self.install_ok("--agents", "claude")
        self.assertFalse(self.sync().failed)
        self.assertFalse((self.repo / ".agents").exists())
        self.install_ok("--agents", "codex")
        paths = check.read_manifest(self.repo)["skills"]["hr-onboard"]["paths"]
        self.assertEqual(paths, [".agents/skills", ".claude/skills"])
        self.assertFalse(self.sync().failed)

    def test_omitted_agents_adds_all_paths(self):
        self.install_ok('--agents', 'claude')
        before = check.tree_hash(self.repo)
        preview = self.run_install('--check')
        self.assertEqual(preview.returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)
        self.install_ok()
        self.assertEqual(set(check.read_manifest(self.repo)['skills']['hr-onboard']['paths']),
                         set(install.AGENT_SKILL_PATHS.values()))

    def test_managed_conflict_message_requires_recorded_path(self):
        self.install_ok('--agents', 'claude')
        owned = self.repo / '.claude/skills/hr-onboard/SKILL.md'
        owned.write_bytes(owned.read_bytes() + b'\nLocal edit\n')
        foreign = self.repo / '.agents/skills/hr-onboard/SKILL.md'
        foreign.parent.mkdir(parents=True)
        foreign.write_bytes(b'Foreign skill')
        before = check.tree_hash(self.repo)
        for flags in [('--check',), ()]:
            result = self.run_install('--agents', 'claude,codex', *flags)
            self.assertEqual(result.returncode, 1)
            lines = result.stdout.splitlines()
            self.assertTrue(any('.claude/skills/hr-onboard: CONFLICT - recorded installed copy'
                                in line for line in lines))
            self.assertTrue(any('.agents/skills/hr-onboard: CONFLICT - a different skill'
                                in line for line in lines))
            self.assertEqual(check.tree_hash(self.repo), before)

    def test_source_upgrade_requires_all_recorded_paths(self):
        source = Path(tempfile.mkdtemp(prefix="houserules-upgrade-source-"))
        for name in ["install.py", "check.py", "LICENSE"]:
            shutil.copy2(install.HERE / name, source / name)
        shutil.copytree(install.HERE / "templates", source / "templates")
        self.installer = source / "install.py"
        self.install_ok("--agents", "codex")
        skill = source / "templates/skills/hr-onboard/SKILL.md"
        skill.write_bytes(skill.read_bytes() + b"\nSource v2\n")
        before = check.tree_hash(self.repo)
        for args in [("--check",), (), ("--check", "--force"), ("--force",)]:
            result = self.run_install("--agents", "claude", *args)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("partial upgrade", result.stdout)
            self.assertIn(".agents/skills", result.stdout)
            self.assertEqual(check.tree_hash(self.repo), before)
            self.assertFalse(self.sync().failed)  # v1 baseline remains valid
        result = self.run_install('--agents', 'codex', '--check')
        self.assertEqual(result.returncode, 1)
        self.assertIn('recorded installed copy differs from current source', result.stdout)
        self.assertEqual(check.tree_hash(self.repo), before)
        # An operator reconciles the one known fixture file with the new source. No force,
        # directory replacement or recursive deletion is used to exercise the full upgrade.
        (self.repo / ".agents/skills/hr-onboard/SKILL.md").write_bytes(skill.read_bytes())
        self.install_ok("--agents", "codex,claude")
        self.assertFalse(self.sync().failed)
        self.assertEqual(check.read_manifest(self.repo)["skills"]["hr-onboard"]["sha256"],
                         check.tree_hash(skill.parent))
        self.assertEqual(self.run_install("--agents", "codex,claude", "--check").returncode, 0)
        result = subprocess.run(
            [sys.executable, str(self.repo / ".houserules/check.py"), "--repo", str(self.repo)],
            capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_absent_recorded_root_fails(self):
        self.install_ok("--agents", "claude")
        path = self.repo / check.MANIFEST
        data = check.read_manifest(self.repo)
        data["skills"]["hr-onboard"]["paths"].append(".cursor/skills")
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(self.sync().failed)
        self.assertIn(".cursor/skills/hr-onboard missing", str(self.sync().rows))

    def test_same_change_to_every_copy_is_still_drift(self):
        self.install_ok()
        for rel in check.SKILL_DIRS:
            path = self.repo / rel / "hr-onboard/SKILL.md"
            path.write_bytes(path.read_bytes() + b"\nUnrecorded change\n")
        self.assertTrue(self.sync().failed)

    def test_extra_support_file_is_drift(self):
        self.install_ok("--agents", "claude")
        (self.repo / ".claude/skills/hr-onboard/extra.txt").write_text("extra", encoding="utf-8")
        self.assertTrue(self.sync().failed)
        self.assertEqual(self.run_install("--agents", "claude", "--check").returncode, 1)

    def test_text_checkout_line_endings_do_not_invalidate_baseline(self):
        self.install_ok("--agents", "claude")
        target = self.repo / ".claude/skills/hr-onboard/SKILL.md"
        target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertFalse(self.sync().failed)
        self.assertEqual(self.run_install("--agents", "claude", "--check").returncode, 0)

    def test_binary_line_endings_remain_significant(self):
        target = self.repo / "binary.dat"
        for content in [b"\0\r\n", b"\xff\r\n"]:
            target.write_bytes(content)
            before = check.tree_hash(self.repo)
            target.write_bytes(content.replace(b"\r\n", b"\n"))
            self.assertNotEqual(check.tree_hash(self.repo), before)

    def test_same_name_conflict_is_never_owned_or_overwritten(self):
        foreign = self.foreign("hr-onboard")
        before = check.tree_hash(self.repo)
        result = self.run_install("--agents", "claude", "--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn('a different skill of this name', result.stdout)
        self.assertEqual(check.tree_hash(self.repo), before)
        content = foreign.read_bytes()
        result = self.run_install("--agents", "claude")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(foreign.read_bytes(), content)
        self.assertFalse((self.repo / check.MANIFEST).exists())

    def test_mixed_agent_conflict_stops_before_any_write(self):
        self.foreign("hr-onboard")
        before = check.tree_hash(self.repo)
        outcomes = []
        for args in [("--check",), ()]:
            result = self.run_install("--agents", "claude,codex", *args)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(check.tree_hash(self.repo), before)
            self.assertFalse((self.repo / ".agents").exists())
            self.assertFalse((self.repo / check.MANIFEST).exists())
            outcomes.append(result.stdout.split("\n", 1)[1])  # omit the mode banner only
        self.assertEqual(outcomes[0], outcomes[1])
        self.assertIn("Installation stopped before writes", outcomes[0])
        self.assertNotIn("would create", outcomes[0])

    def test_root_check_py_is_reported_and_never_touched(self):
        """The migration rule for a root check.py of ambiguous provenance: report, never write.

        Nothing recorded who wrote it - it was never in the asset manifest - so an old owned
        copy, a locally modified one and an unrelated user script are indistinguishable. All
        three take the same path: the file survives byte for byte, whatever CI runs it keeps
        working, and the installer says so once per run.
        """
        shipped = (install.HERE / "check.py").read_bytes()
        # In the distribution itself the root file is the source, not a leftover install.
        self.assertIsNone(install.legacy_root_checker(install.HERE))
        for kind, content in [("unrelated", b"# user checker\n"),
                              ("owned old copy", shipped),
                              ("modified old copy", shipped + b"\n# local edit\n")]:
            with self.subTest(kind=kind):
                self.repo = Path(tempfile.mkdtemp(prefix="houserules-test-"))
                root = self.repo / "check.py"
                root.write_bytes(content)
                result = self.run_install("--agents", "codex", "--check")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("left untouched", result.stdout)
                self.assertEqual(root.read_bytes(), content)
                self.install_ok("--agents", "codex")
                self.assertEqual(root.read_bytes(), content)
                self.assertTrue((self.repo / ".houserules/check.py").is_file())
                self.assertNotIn("check.py", check.read_manifest(self.repo)["skills"])
                self.assertIn(".houserules/check.py", check.read_assets(self.repo)["files"])
                # None of this is a pre-move installation, so a repeat run is ordinary and
                # the file at the root stays exactly as the adopter left it.
                repeat = self.run_install("--agents", "codex")
                self.assertEqual(repeat.returncode, 0, repeat.stdout)
                self.assertIn("left untouched", repeat.stdout)
                self.assertEqual(root.read_bytes(), content)

    def test_pre_move_checker_fails_against_the_new_manifest(self):
        """The concrete break the migration gate exists for, run with a real old checker.

        Preserving the root file's bytes does not preserve its behavior: its asset allowlist
        predates `.houserules/check.py`, so it rejects the manifest and exits 1. Asserted here
        rather than assumed, because an earlier version of this layer promised the opposite.
        """
        old = self.repo / "old_check.py"
        # The last revision before the checker moved. Skipped rather than faked where the
        # object is unreachable - a synthesized "old" checker would prove nothing.
        show = subprocess.run(["git", "-C", str(install.HERE), "show", "8ae9d31:check.py"],
                              capture_output=True, encoding="utf-8", errors="replace")
        if show.returncode != 0:
            self.skipTest("pre-move checker revision 8ae9d31 is not reachable here")
        old.write_bytes(show.stdout.encode("utf-8"))  # Preserve LF on Python 3.9 too.
        self.install_ok("--agents", "codex")
        result = subprocess.run([sys.executable, str(old), "--repo", str(self.repo)],
                                capture_output=True, text=True, encoding="utf-8",
                                env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("invalid managed asset: .houserules/check.py", result.stdout)
        # The checker shipped with this change reads the same repository without complaint.
        current = subprocess.run([sys.executable, str(self.repo / ".houserules/check.py"),
                                  "--repo", str(self.repo)], capture_output=True, text=True,
                                 encoding="utf-8",
                                 env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        self.assertEqual(current.returncode, 0, current.stdout + current.stderr)

    def pre_move_distribution(self):
        """A real pre-move distribution, extracted from the last revision before the move.

        Skipped rather than synthesized where that revision is unreachable: a hand-built "old"
        installer would only test this code's idea of the old layout, not the old layout.
        """
        archive = subprocess.run(["git", "-C", str(install.HERE), "archive",
                                  "--format=zip", "8ae9d31"], capture_output=True)
        if archive.returncode != 0:
            self.skipTest("pre-move revision 8ae9d31 is not reachable here")
        source = Path(tempfile.mkdtemp(prefix="houserules-pre-move-"))
        with zipfile.ZipFile(io.BytesIO(archive.stdout)) as bundle:
            bundle.extractall(source)
        return source / "install.py"

    def test_migration_gate_fires_once_and_never_for_a_completed_install(self):
        """The gate keys off recorded pre-move state, not off "a manifest exists".

        Treating any manifest as pre-move blocked ordinary re-runs forever, including the run
        immediately after a confirmed migration.
        """
        source = self.pre_move_distribution()
        self.installer = source
        self.install_ok("--agents", "codex")
        root = self.repo / "check.py"
        self.assertTrue(root.is_file(), "the pre-move installer places check.py at the root")
        original = root.read_bytes()
        self.assertNotIn(check.INSTALLED_CHECKER, check.read_assets(self.repo)["files"])

        del self.installer
        for flags in [("--check",), ()]:
            result = self.run_install("--agents", "codex", *flags)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("root check.py needs migrating first", result.stdout)

        self.install_ok("--agents", "codex", "--migrate-checker", "--force")
        self.assertIn(check.INSTALLED_CHECKER, check.read_assets(self.repo)["files"])
        self.assertEqual(root.read_bytes(), original)

        # Migration is recorded, so it must never be demanded again - not on a repeat preview,
        # not on a later selection change, and not with the root file still sitting there.
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 0)
        self.install_ok("--agents", "codex", "--skills", "hr-tdd")
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 0)
        self.assertEqual(root.read_bytes(), original)

    def test_unrelated_root_checker_never_triggers_the_migration_gate(self):
        """No manifest means no pre-move installation, whatever sits at the root."""
        root = self.repo / "check.py"
        root.write_bytes(b"# my own project checker\n")
        self.install_ok("--agents", "codex")
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 0)
        self.install_ok("--agents", "codex", "--work", "handoff")
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 0)
        self.assertEqual(root.read_bytes(), b"# my own project checker\n")

    def test_rendered_paths_round_trip_under_the_documented_shell_rules(self):
        """Backslashes are POSIX escapes, so a Windows path needs quoting with or without spaces."""
        separator = chr(92)
        cases = ["C:" + separator + "Projects" + separator + "demo",     # no space: the case
                 "C:" + separator + "hr review" + separator + "x.py",    # space too
                 "C:" + separator + "it's here" + separator + "x.py",    # embedded apostrophe
                 "/home/user/houserules/install.py", ".",
                 install.DISTRIBUTION]
        for value in cases:
            with self.subTest(path=value):
                quoted = install.shell_quote(value)
                self.assertEqual(shlex.split("python " + quoted)[1], value)
        # Ordinary POSIX paths stay unquoted, so the common case remains readable.
        self.assertEqual(install.shell_quote("/home/user/houserules/install.py"),
                         "/home/user/houserules/install.py")
        self.assertEqual(install.shell_quote("."), ".")
        # PowerShell doubles an embedded apostrophe instead; that is not claimed or tested.
        self.assertIn(separator + "''", install.shell_quote("C:" + separator + "it's here"))

    def test_follow_up_command_survives_paths_containing_spaces(self):
        """Rendered so a copy-paste reaches the intended directory, not two wrong ones."""
        distribution = Path(tempfile.mkdtemp(prefix="hr dist "))
        for name in ("install.py", "check.py", "LICENSE"):
            shutil.copy2(install.HERE / name, distribution / name)
        shutil.copytree(install.HERE / "templates", distribution / "templates")
        self.repo = Path(tempfile.mkdtemp(prefix="hr target "))
        self.installer = distribution / "install.py"
        result = self.run_install("--agents", "kiro")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        line = next(l.strip() for l in result.stdout.splitlines()
                    if l.strip().startswith("python "))
        argv = shlex.split(line)
        self.assertEqual(argv[1], str(distribution / "install.py"))
        self.assertEqual(argv[argv.index("--repo") + 1], str(self.repo))
        # The page's placeholder is quoted the same way, so filling it in keeps the command
        # whole. Asserted before the follow-up runs, which is what empties that section.
        self.assertIn("'<houserules distribution>/install.py'", self.page())
        argv[0] = sys.executable
        rerun = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                               env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
        self.assertEqual(set(check.read_manifest(self.repo)["skills"]),
                         {"hr-onboard", "hr-tdd", "hr-diagnosing-bugs", "hr-code-review"})


    def test_ci_workflow_triggers_match_what_the_page_promises(self):
        template = (install.HERE / "templates/ci/github-actions.yml").read_text(encoding="utf-8")
        triggers = template.split("on:", 1)[1].split("permissions:", 1)[0]
        self.assertIn("pull_request:", triggers)
        self.assertIn("push:", triggers)
        # A branches: filter here would silently exclude any project whose default branch is
        # named something else, while the generated page still promised every push.
        self.assertNotIn("branches:", triggers)
        self.install_ok("--agents", "codex", "--ci")
        self.assertIn("every push and pull request", self.page())

    def test_installed_checker_conflict_stops_before_skill_writes(self):
        """A destination occupied by something the installer does not own blocks every write."""
        (self.repo / ".houserules").mkdir()
        (self.repo / ".houserules/check.py").write_text("# user checker\n", encoding="utf-8")
        before = check.tree_hash(self.repo)
        outcomes = []
        for args in [("--check",), ()]:
            result = self.run_install("--agents", "codex", *args)
            self.assertEqual(result.returncode, 1)
            self.assertIn("preserve modified/unowned .houserules/check.py", result.stdout)
            outcomes.append(result.stdout.split("\n", 1)[1])
        self.assertEqual(outcomes[0], outcomes[1])
        self.assertEqual(check.tree_hash(self.repo), before)
        self.assertFalse((self.repo / ".agents").exists())

    def test_installed_checker_runs_from_the_project_root(self):
        """--repo resolves against the current directory, not against the script's location."""
        self.install_ok("--agents", "codex")
        checker = self.repo / ".houserules/check.py"
        self.assertEqual((install.HERE / "check.py").read_bytes(), checker.read_bytes())
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
        from_root = subprocess.run([sys.executable, str(checker)], cwd=self.repo,
                                   capture_output=True, text=True, encoding="utf-8", env=env)
        self.assertEqual(from_root.returncode, 0, from_root.stdout + from_root.stderr)
        # Run from inside .houserules/ it would check that directory instead, which is why the
        # shipped text says to run it from the root or pass --repo. Both are honest options.
        explicit = subprocess.run([sys.executable, "check.py", "--repo", str(self.repo)],
                                  cwd=self.repo / ".houserules", capture_output=True,
                                  text=True, encoding="utf-8", env=env)
        self.assertEqual(explicit.returncode, 0, explicit.stdout + explicit.stderr)

    def test_installed_checker_edit_is_preserved_and_reported(self):
        self.install_ok("--agents", "codex")
        checker = self.repo / ".houserules/check.py"
        edited = checker.read_bytes() + b"\n# local edit\n"
        checker.write_bytes(edited)
        report = check.Report()
        check.check_assets(self.repo, report)
        self.assertTrue(report.failed)
        before = check.tree_hash(self.repo)
        for flags in [(), ("--check",), ("--force",)]:
            result = self.run_install("--agents", "claude", *flags)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(check.tree_hash(self.repo), before)
        self.assertEqual(checker.read_bytes(), edited)

    def test_installed_checker_destination_may_not_be_a_symlink(self):
        elsewhere = self.repo / "user-checker.py"
        elsewhere.write_text("# user checker\n", encoding="utf-8")
        link = self.repo / ".houserules/check.py"
        link.parent.mkdir(parents=True)
        try:
            link.symlink_to(elsewhere)
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                self.skipTest(f"OS cannot create a symlink: {exc}")
            raise
        before = check.tree_hash(self.repo)
        result = self.run_install("--agents", "codex")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("symlink asset path", result.stdout)
        self.assertTrue(link.is_symlink())
        self.assertEqual(check.tree_hash(self.repo), before)

    def test_missing_manifest_with_shipped_name_fails_without_claiming_ownership(self):
        self.foreign("hr-onboard")
        before = check.tree_hash(self.repo)
        self.assertTrue(self.sync().failed)
        result = subprocess.run(
            [sys.executable, str(install.HERE / "check.py"), "--repo", str(self.repo)],
            capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(check.tree_hash(self.repo), before)
        self.assertFalse((self.repo / check.MANIFEST).exists())

    def test_standalone_shipped_name_catalog_matches_sources(self):
        self.assertEqual(check.SHIPPED_SKILL_NAMES, {s.name for s in install.discover_skills()})

    def test_matching_size_and_mtime_do_not_hide_different_bytes(self):
        self.install_ok("--agents", "claude")
        source = install.SKILL_SRC / "hr-onboard/SKILL.md"
        target = self.repo / ".claude/skills/hr-onboard/SKILL.md"
        original = target.read_bytes()
        target.write_bytes(original.replace(b"Onboard", b"Offload", 1))
        stamp = source.stat()
        os.utime(target, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
        self.assertEqual(source.stat().st_size, target.stat().st_size)
        self.assertFalse(install.same_tree(source.parent, target.parent))
        self.assertEqual(self.run_install("--agents", "claude", "--check").returncode, 1)

    def test_different_symlink_is_preserved(self):
        user_skill = self.repo / "user-skill"
        user_skill.mkdir()
        (user_skill / "SKILL.md").write_text("user content", encoding="utf-8")
        link = self.repo / ".claude/skills/hr-onboard"
        link.parent.mkdir(parents=True)
        try:
            link.symlink_to(user_skill, target_is_directory=True)
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                self.skipTest(f"OS cannot create a symlink: {exc}")
            raise
        result = self.run_install("--agents", "claude")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), user_skill)
        self.assertEqual((user_skill / "SKILL.md").read_text(encoding="utf-8"), "user content")
        self.assertFalse((self.repo / check.MANIFEST).exists())

    def test_dangling_symlink_is_preserved(self):
        # exists() follows the link and is false here; is_symlink() is the essential guard.
        missing = self.repo / 'missing-user-skill'
        link = self.repo / '.claude/skills/hr-onboard'
        link.parent.mkdir(parents=True)
        try:
            link.symlink_to(missing, target_is_directory=True)
        except OSError as exc:
            if os.name == 'nt' and getattr(exc, 'winerror', None) == 1314:
                self.skipTest(f'OS cannot create a symlink: {exc}')
            raise
        self.assertFalse(link.exists())
        result = self.run_install('--agents', 'claude')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.readlink(), missing)
        self.assertFalse(missing.exists())
        self.assertFalse((self.repo / check.MANIFEST).exists())

    def test_invalid_manifest_blocks_before_writes(self):
        self.install_ok("--agents", "claude")
        path = self.repo / check.MANIFEST
        data = check.read_manifest(self.repo)
        data["skills"]["hr-onboard"]["paths"] = ["../../outside"]
        path.write_text(json.dumps(data), encoding="utf-8")
        before = check.tree_hash(self.repo)
        self.assertTrue(self.sync().failed)
        self.assertEqual(self.run_install().returncode, 2)
        self.assertEqual(check.tree_hash(self.repo), before)

    def test_legacy_ownership_is_unknown_until_installer_runs(self):
        self.foreign()
        report = self.sync()
        self.assertFalse(report.failed)
        self.assertIn("ownership unknown", str(report.rows))
        self.install_ok()
        self.assertFalse(self.sync().failed)

    def test_preview_is_read_only_and_idempotent_after_install(self):
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install("--check").returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)
        self.install_ok()
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install("--check").returncode, 0)
        self.assertEqual(check.tree_hash(self.repo), before)


    def test_optional_selection_and_local_entry(self):
        self.install_ok("--agents", "codex")
        self.assertEqual(set(check.read_manifest(self.repo)["skills"]), {"hr-onboard"})
        self.assertFalse((self.repo / ".agents/skills/hr-tdd").exists())
        self.install_ok("--agents", "codex", "--skills", "hr-tdd,hr-code-review",
                        "--work", "handoff,verification")
        self.assertEqual(set(check.read_manifest(self.repo)["skills"]),
                         {"hr-onboard", "hr-tdd", "hr-code-review"})
        for name in ["SKILL.md", "LICENSE", "NOTICE.md", "tests.md", "mocking.md"]:
            self.assertTrue((self.repo / ".agents/skills/hr-tdd" / name).is_file())
        entry = (self.repo / "HOUSERULES.md").read_text(encoding="utf-8")
        self.assertIn(".agents/skills/hr-tdd/SKILL.md", entry)
        self.assertIn(".houserules/work/handoff.md", entry)
        self.assertFalse((self.repo / ".houserules/work/spec.md").exists())
        protocol = (self.repo / ".houserules/work/README.md").read_text(encoding="utf-8")
        self.assertNotIn("](spec.md)", protocol)
        self.assertNotIn("../../tests/workflows", protocol)
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 0)

    def page(self):
        return (self.repo / "HOUSERULES.md").read_text(encoding="utf-8")

    def test_generated_page_gives_one_first_action_for_each_onboarding_state(self):
        """The adopter reads their own repository, not the distribution, to know what to do."""
        self.install_ok("--agents", "codex")
        self.assertIn("use the `hr-onboard` skill", self.page())
        self.assertNotIn("onboarding is done", self.page())

        (self.repo / "AGENTS.md").write_text("# AGENTS.md\n\n## Commands\n\nmake test\n",
                                             encoding="utf-8")
        self.install_ok("--agents", "codex")
        self.assertIn("onboarding is done", self.page())
        self.assertNotIn("Ask your agent: **use the `hr-onboard` skill.**", self.page())

        self.repo = Path(tempfile.mkdtemp(prefix="houserules-test-"))
        self.install_ok("--agents", "codex", "--skills", "none")
        self.assertIn("`hr-onboard` was not selected", self.page())
        self.assertIn("--skills hr-onboard", self.page())

    def test_generated_page_answers_a_stage_question_locally(self):
        """A stage-level question is answered whether or not the skill for it was selected."""
        self.install_ok("--agents", "codex")
        for situation in ["New behaviour", "cannot yet reproduce", "before it lands",
                          "another agent takes it over"]:
            self.assertIn(situation, self.page())
        self.assertIn("Not installed. Write the failing test first", self.page())
        self.assertNotIn("(.agents/skills/hr-tdd/SKILL.md)", self.page())
        self.install_ok("--agents", "codex", "--skills", "hr-tdd", "--work", "handoff")
        self.assertIn("[hr-tdd](.agents/skills/hr-tdd/SKILL.md)", self.page())
        self.assertNotIn("Not installed. Write the failing test first", self.page())
        # The workflow walkthrough shows the loop, including the staleness signal.
        for step in ["workflow.py start demo", "workflow.py run demo", "workflow.py status demo",
                     "it exits **1**", "does not run an SDLC"]:
            self.assertIn(step, self.page())

    def test_generated_page_links_resolve_inside_the_adopting_repository(self):
        self.install_ok("--agents", "claude", "--skills", "all", "--work", "all")
        targets = re.findall(r"\]\(([^)\s]+)\)", self.page())
        self.assertTrue(targets)
        for target in targets:
            with self.subTest(link=target):
                self.assertTrue((self.repo / target.partition("#")[0]).exists(), target)

    def test_generated_page_records_no_machine_specific_path(self):
        """It is committed by the adopter and regenerated in this repository's own CI."""
        self.install_ok("--agents", "codex")
        self.assertNotIn(str(install.HERE), self.page())
        self.assertNotIn(str(self.repo), self.page())
        self.assertIn(install.DISTRIBUTION, self.page())

    def test_omissions_are_reported_by_the_installer_and_the_page(self):
        result = self.run_install("--agents", "kiro")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for expected in ["Not installed: skills hr-code-review, hr-diagnosing-bugs, hr-tdd",
                         "work templates findings, handoff, plan, review, spec, verification",
                         "--skills hr-code-review,hr-diagnosing-bugs,hr-tdd",
                         "--work findings,handoff,plan,review,spec,verification",
                         "Keep --agents kiro"]:
            self.assertIn(expected, result.stdout)
        self.assertIn(str(install.HERE / "install.py"), result.stdout)
        self.assertIn("hr-tdd", self.page())
        self.assertIn("Keep `--agents kiro`", self.page())

        # Additive second install: what is already here drops out of both reports.
        result = self.run_install("--agents", "claude", "--skills", "hr-tdd", "--work", "handoff")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Not installed: skills hr-code-review, hr-diagnosing-bugs"
                      " (optional, experimental); work templates findings, plan, review,"
                      " spec, verification", result.stdout)
        # --agents must cover both recorded paths, or the next source upgrade cannot complete.
        self.assertIn("Keep --agents claude,kiro", result.stdout)
        self.assertIn("Keep `--agents claude,kiro`", self.page())

        result = self.run_install("--agents", "claude,kiro", "--skills", "all", "--work", "all")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Not installed:", result.stdout)
        self.assertIn("Everything this installer ships is selected here.", result.stdout)
        self.assertIn("Everything this installer ships is already installed here.", self.page())

    def test_follow_up_agent_selection_covers_every_recorded_path(self):
        self.assertEqual(install.covering_agents(["kiro"], {".kiro/skills"}), ["kiro"])
        self.assertEqual(install.covering_agents(["kiro"], {".kiro/skills", ".claude/skills"}),
                         ["claude", "kiro"])
        # Every path covered means the shorthand is honest; anything less must be spelled out.
        # "all" is claimed on paths covered, not labels named: several agents share a
        # directory, so a subset of labels can already reach every path.
        self.assertEqual(install.covering_agents(list(install.AGENT_SKILL_PATHS), set()), ["all"])
        self.assertEqual(install.covering_agents(["claude"], set(install.AGENT_SKILL_PATHS.values())),
                         ["all"])
        self.assertEqual(install.covering_agents(["claude", "codex", "cursor", "kiro"], set()),
                         ["claude", "codex", "cursor", "kiro"])

    def test_selection_is_additive_and_none_does_not_uninstall(self):
        self.install_ok("--agents", "codex", "--skills", "hr-tdd", "--work", "handoff")
        self.install_ok("--agents", "claude", "--skills", "hr-code-review", "--work", "review")
        self.install_ok("--agents", "codex", "--skills", "none", "--work", "none")
        self.assertEqual(set(check.read_manifest(self.repo)["skills"]), {"hr-tdd", "hr-code-review"})
        self.assertEqual(set(check.read_assets(self.repo)["files"]),
                         {"HOUSERULES.md", ".houserules/LICENSE", ".houserules/START.md",
                          ".houserules/check.py", ".houserules/workflow.py",
                          ".houserules/work/README.md",
                          ".houserules/work/handoff.md", ".houserules/work/review.md"})

    def test_ci_template_is_opt_in_retained_and_leaves_other_workflows_alone(self):
        mine = self.repo / ".github/workflows/release.yml"
        mine.parent.mkdir(parents=True)
        mine.write_text("name: release\n", encoding="utf-8")
        self.install_ok("--agents", "codex")
        self.assertFalse((self.repo / check.CI_WORKFLOW).exists())
        self.assertIn("Re-install with --ci", self.page())

        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install("--agents", "codex", "--ci", "--check").returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)

        self.install_ok("--agents", "codex", "--ci")
        workflow = self.repo / check.CI_WORKFLOW
        self.assertEqual(workflow.read_bytes(),
                         (install.HERE / "templates/ci/github-actions.yml").read_bytes())
        self.assertIn("python .houserules/check.py", workflow.read_text(encoding="utf-8"))
        commands = [line for line in workflow.read_text(encoding="utf-8").splitlines()
                    if line.strip().startswith("run:")]
        self.assertTrue(commands)
        self.assertFalse([line for line in commands if "--fix" in line],
                         "--fix repairs instead of reporting; it must never be the gate")
        self.assertIn(check.CI_WORKFLOW, check.read_assets(self.repo)["files"])
        self.assertIn("branch protection settings", self.page())
        self.assertEqual(mine.read_text(encoding="utf-8"), "name: release\n")

        # Retained without the flag, and a repeat run is a no-op.
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 0)
        self.install_ok("--agents", "codex")
        self.assertTrue(workflow.is_file())

    def test_ci_path_conflict_stops_before_writes(self):
        target = self.repo / check.CI_WORKFLOW
        target.parent.mkdir(parents=True)
        target.write_text("name: mine\n", encoding="utf-8")
        before = check.tree_hash(self.repo)
        for flags in [("--check",), (), ("--force",)]:
            result = self.run_install("--agents", "codex", "--ci", *flags)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("preserve modified/unowned .github/workflows/houserules.yml",
                          result.stdout)
            self.assertEqual(check.tree_hash(self.repo), before)
        self.assertEqual(target.read_text(encoding="utf-8"), "name: mine\n")

    def test_unknown_selection_and_list_write_nothing(self):
        before = check.tree_hash(self.repo)
        for args in [("--skills", "tdd"), ("--work", "../spec"), ("--skills", "")]:
            self.assertEqual(self.run_install(*args).returncode, 2)
        self.assertEqual(self.run_install("--list").returncode, 0)
        self.assertEqual(check.tree_hash(self.repo), before)

    def test_workflow_activation_is_explicit_append_only_and_idempotent(self):
        agents = self.repo / 'AGENTS.md'
        original = b'# User instructions\r\n\r\nKeep my exact bytes.\r\n'
        agents.write_bytes(original)
        self.install_ok('--agents', 'codex')
        self.assertEqual(agents.read_bytes(), original)
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install('--agents', 'codex', '--activate-workflow', '--check').returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)
        self.install_ok('--agents', 'codex', '--activate-workflow')
        self.assertTrue(agents.read_bytes().startswith(original))
        after = agents.read_bytes()
        self.assertEqual(self.run_install('--agents', 'codex', '--activate-workflow', '--check').returncode, 0)
        self.install_ok('--agents', 'codex', '--activate-workflow')
        self.assertEqual(agents.read_bytes(), after)

    def test_modified_activation_and_runtime_stop_before_writes(self):
        self.install_ok('--agents', 'codex', '--activate-workflow')
        agents = self.repo / 'AGENTS.md'
        agents.write_text(agents.read_text().replace('before execution', 'after execution'))
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install('--agents', 'claude', '--activate-workflow').returncode, 2)
        self.assertEqual(check.tree_hash(self.repo), before)
        runtime = self.repo / '.houserules/workflow.py'
        runtime.write_bytes(runtime.read_bytes() + b'\n# User edit\n')
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install('--agents', 'claude').returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)

    def test_installed_workflow_runs_without_distribution(self):
        self.install_ok('--agents', 'cursor,kiro', '--activate-workflow')
        runtime = self.repo / '.houserules/workflow.py'
        target = self.repo / 'behavior.txt'
        target.write_text('expected')
        def execute(*args):
            return subprocess.run([sys.executable, str(runtime), '--repo', str(self.repo), *args],
                                  capture_output=True, text=True, encoding='utf-8')
        result = execute('start', 'local', '--task', 'Check behavior', '--target', 'behavior.txt')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = execute('run', 'local', '--', sys.executable, '-c',
                         "from pathlib import Path; assert Path('behavior.txt').read_text() == 'expected'")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(execute('status', 'local').returncode, 0)
        target.write_text('changed')
        self.assertEqual(execute('status', 'local').returncode, 1)

    def test_work_preview_is_read_only_then_converges(self):
        before = check.tree_hash(self.repo)
        args = ("--agents", "codex", "--skills", "all", "--work", "all")
        self.assertEqual(self.run_install(*args, "--check").returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)
        self.install_ok(*args)
        self.assertEqual(self.run_install(*args, "--check").returncode, 0)
        self.assertEqual(len(check.read_assets(self.repo)["files"]), 12)
        report = check.Report()
        check.check_assets(self.repo, report)
        self.assertFalse(report.failed)

    def test_untouched_work_assets_upgrade_from_recorded_baseline(self):
        source = self.repo / "distribution"
        source.mkdir()
        for name in ("install.py", "check.py", "LICENSE"):
            shutil.copy2(install.HERE / name, source / name)
        shutil.copytree(install.HERE / "templates", source / "templates")
        self.installer = source / "install.py"
        self.install_ok("--agents", "codex", "--work", "handoff")
        template = source / "templates/work/handoff.md"
        template.write_bytes(template.read_bytes() + b"\nUpstream extension\n")
        before = (self.repo / ".houserules/work/handoff.md").read_bytes()
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 1)
        self.assertEqual((self.repo / ".houserules/work/handoff.md").read_bytes(), before)
        self.install_ok("--agents", "codex")
        self.assertEqual((self.repo / ".houserules/work/handoff.md").read_bytes(), template.read_bytes())
        report = check.Report()
        check.check_assets(self.repo, report)
        self.assertFalse(report.failed)

    def test_first_party_notice_installs_without_touching_the_project_license(self):
        """MIT requires the notice to travel with the copies the installer makes."""
        own = self.repo / "LICENSE"
        own.write_bytes(b"Copyright (c) 2026 the adopting project. All rights reserved.\n")
        self.install_ok("--agents", "codex")
        notice = self.repo / ".houserules/LICENSE"
        self.assertEqual(notice.read_bytes(), (install.HERE / "LICENSE").read_bytes())
        self.assertEqual(own.read_bytes(), b"Copyright (c) 2026 the adopting project. All rights reserved.\n")
        # hr-onboard is first-party and is also copied on its own, outside .houserules/.
        self.assertTrue((self.repo / ".agents/skills/hr-onboard/LICENSE").is_file())
        manifest = json.loads((self.repo / check.ASSET_MANIFEST).read_text(encoding="utf-8"))
        self.assertIn(".houserules/LICENSE", manifest["files"])
        report = check.Report()
        check.check_assets(self.repo, report)
        self.assertFalse(report.failed)

    def test_untouched_notice_upgrades_and_a_modified_one_blocks_writes(self):
        source = self.repo / "distribution"
        source.mkdir()
        for name in ("install.py", "check.py", "LICENSE"):
            shutil.copy2(install.HERE / name, source / name)
        shutil.copytree(install.HERE / "templates", source / "templates")
        self.installer = source / "install.py"
        self.install_ok("--agents", "codex")
        upstream = source / "LICENSE"
        upstream.write_bytes(upstream.read_bytes() + b"\nRelicensed line\n")
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 1)
        self.install_ok("--agents", "codex")
        self.assertEqual((self.repo / ".houserules/LICENSE").read_bytes(), upstream.read_bytes())
        # A notice the adopter edited is preserved, and stops every write like any managed asset.
        target = self.repo / ".houserules/LICENSE"
        target.write_bytes(target.read_bytes() + b"\nLocal edit\n")
        before = check.tree_hash(self.repo)
        for flags in [(), ("--check",), ("--force",)]:
            self.assertEqual(self.run_install("--agents", "claude", *flags).returncode, 1)
            self.assertEqual(check.tree_hash(self.repo), before)

    def test_modified_assets_block_all_writes_even_force(self):
        self.install_ok("--agents", "codex", "--work", "handoff")
        target = self.repo / ".houserules/work/handoff.md"
        target.write_bytes(target.read_bytes() + b"\nUser customization\n")
        report = check.Report()
        check.check_assets(self.repo, report)
        self.assertTrue(report.failed)
        before = check.tree_hash(self.repo)
        for flags in [(), ("--check",), ("--force",)]:
            result = self.run_install("--agents", "claude", "--skills", "hr-tdd", *flags)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(check.tree_hash(self.repo), before)
        self.assertFalse((self.repo / ".claude/skills/hr-tdd").exists())

    def test_entry_collision_preserves_foreign_content(self):
        (self.repo / "HOUSERULES.md").write_text("Owned by user", encoding="utf-8")
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install().returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)

    def test_asset_manifest_rejects_escape_and_file_parent(self):
        parent = self.repo / ".houserules"
        parent.mkdir()
        manifest = parent / "assets.json"
        manifest.write_text(json.dumps({"schema_version": 1,
                                       "files": {"../outside": "a" * 64}}))
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install().returncode, 2)
        self.assertEqual(check.tree_hash(self.repo), before)
        manifest.write_text(json.dumps({"schema_version": 1, "files": {}}))
        (parent / "work").write_text("not a directory")
        before = check.tree_hash(self.repo)
        self.assertEqual(self.run_install("--work", "all").returncode, 1)
        self.assertEqual(check.tree_hash(self.repo), before)

    def test_asset_checkout_conversion_and_missing_file(self):
        self.install_ok("--agents", "codex", "--work", "handoff")
        target = self.repo / ".houserules/work/handoff.md"
        target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 0)
        # One explicit fixture file only; no directory cleanup.
        target.unlink()
        report = check.Report()
        check.check_assets(self.repo, report)
        self.assertTrue(report.failed)
        self.assertEqual(self.run_install("--agents", "codex", "--check").returncode, 1)
        self.install_ok("--agents", "codex")
        self.assertTrue(target.is_file())

    def test_nested_git_boundaries_do_not_hide_real_instruction_chains(self):
        (self.repo / "AGENTS.md").write_text("root rule")
        for name, gitfile in [("clone", False), ("worktree", True)]:
            nested = self.repo / name
            nested.mkdir()
            if gitfile:
                (nested / ".git").write_text("gitdir: /elsewhere")
            else:
                (nested / ".git").mkdir()
            (nested / "AGENTS.md").write_text("x" * check.MAX_INSTRUCTION_BYTES)
        report = check.Report()
        check.check_size(self.repo, report)
        self.assertFalse(report.failed)
        local = self.repo / "local"
        local.mkdir()
        (local / "AGENTS.md").write_text("x" * check.MAX_INSTRUCTION_BYTES)
        report = check.Report()
        check.check_size(self.repo, report)
        self.assertTrue(report.failed)


if __name__ == "__main__":
    unittest.main()
