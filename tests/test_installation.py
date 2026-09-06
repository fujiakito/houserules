"""Run: python -m unittest discover -s tests -v

Fixtures are retained in the OS temp directory; no recursive cleanup is performed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

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
        # An operator reconciles the one known fixture file with the new source. No force,
        # directory replacement or recursive deletion is used to exercise the full upgrade.
        (self.repo / ".agents/skills/hr-onboard/SKILL.md").write_bytes(skill.read_bytes())
        self.install_ok("--agents", "codex,claude")
        self.assertFalse(self.sync().failed)
        self.assertEqual(check.read_manifest(self.repo)["skills"]["hr-onboard"]["sha256"],
                         check.tree_hash(skill.parent))
        self.assertEqual(self.run_install("--agents", "codex,claude", "--check").returncode, 0)
        result = subprocess.run(
            [sys.executable, str(self.repo / "check.py"), "--repo", str(self.repo)],
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

    def test_root_file_conflict_stops_before_skill_writes(self):
        (self.repo / "check.py").write_text("# user checker\n", encoding="utf-8")
        before = check.tree_hash(self.repo)
        outcomes = []
        for args in [("--check",), ()]:
            result = self.run_install("--agents", "codex", *args)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Changing --agents cannot resolve", result.stdout)
            self.assertNotIn("select only", result.stdout)
            outcomes.append(result.stdout.split("\n", 1)[1])
        self.assertEqual(outcomes[0], outcomes[1])
        self.assertEqual(check.tree_hash(self.repo), before)
        self.assertFalse((self.repo / ".agents").exists())

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

    def test_selection_is_additive_and_none_does_not_uninstall(self):
        self.install_ok("--agents", "codex", "--skills", "hr-tdd", "--work", "handoff")
        self.install_ok("--agents", "claude", "--skills", "hr-code-review", "--work", "review")
        self.install_ok("--agents", "codex", "--skills", "none", "--work", "none")
        self.assertEqual(set(check.read_manifest(self.repo)["skills"]), {"hr-tdd", "hr-code-review"})
        self.assertEqual(set(check.read_assets(self.repo)["files"]),
                         {"HOUSERULES.md", ".houserules/LICENSE", ".houserules/START.md",
                          ".houserules/workflow.py", ".houserules/work/README.md",
                          ".houserules/work/handoff.md", ".houserules/work/review.md"})

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
        self.assertEqual(len(check.read_assets(self.repo)["files"]), 11)
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
