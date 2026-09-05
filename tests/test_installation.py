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
        for name in ["install.py", "check.py"]:
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


if __name__ == "__main__":
    unittest.main()
