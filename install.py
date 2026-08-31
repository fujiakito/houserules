#!/usr/bin/env python3
"""Install portable agent instructions and skills into a repository.

The SKILL.md format is portable across agents. The path is not: seven agents surveyed use
four different locations (research/MATRIX.md section 2). This copies one source of truth
into each agent's own path, which is what the ecosystem's own skill collections do.

It also writes the CLAUDE.md import line, which is a correctness requirement rather than a
convenience: with AGENTS.md present and no import, Claude Code ignores it and raises no
error (research/MATRIX.md section 1, tested).

    python install.py --check          report what would change, write nothing
    python install.py                   install for every known agent
    python install.py --agents claude,codex
    python install.py --link            symlink instead of copy, where the OS allows it
    python install.py --force           replace an existing skill of the same name

Three things land at the repository root as well: AGENTS.md, the CLAUDE.md import line, and
check.py. They carry different overwrite rules, because they are different kinds of thing.
AGENTS.md is a *scaffold* - a repository that has filled it in has not drifted, so an
existing one is left alone and never reported as a conflict. check.py is a *shipped
artifact* meant to be identical everywhere, so a byte difference is a conflict.

An existing skill directory is never replaced without --force. Adopting this layer into a
repository that already has its own skills must not cost the user one of them.

This script writes; check.py only reads. Keeping them apart is deliberate - a check that
can repair what it is checking is not a check.

Paths verified 2026-08-31. Re-check them when an agent releases; see the recheck policy in
research/MATRIX.md.
"""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_SRC = HERE / "templates" / "skills"

# Where each agent looks for project-scoped skills. Verified 2026-08-31.
AGENT_SKILL_PATHS: dict[str, str] = {
    "claude": ".claude/skills",
    "codex": ".agents/skills",      # also read by Goose and Antigravity
    "goose": ".agents/skills",
    "antigravity": ".agents/skills",
    "cursor": ".cursor/skills",
    "kiro": ".kiro/skills",
    "opencode": ".opencode/skills",
}

IMPORT_LINE = "@AGENTS.md"

CLAUDE_MD_NOTE = """@AGENTS.md

<!--
  The import above is required. Tested on Claude Code v2.1.251: with AGENTS.md present and
  no import line, Claude Code reads only CLAUDE.md and ignores AGENTS.md, raising no error.
  Every other surveyed agent reads AGENTS.md natively.

  Keep project knowledge in AGENTS.md. Add below only what is genuinely Claude-Code-only.
-->
"""


def discover_skills() -> list[Path]:
    if not SKILL_SRC.is_dir():
        return []
    return sorted(p for p in SKILL_SRC.iterdir() if (p / "SKILL.md").is_file())


def same_tree(src: Path, dst: Path) -> bool:
    """True when dst already holds an identical copy of src."""
    if not dst.is_dir():
        return False
    cmp = filecmp.dircmp(src, dst)
    if cmp.left_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(same_tree(src / d, dst / d) for d in cmp.common_dirs)


def place(src: Path, dst: Path, link: bool, check: bool, force: bool) -> str:
    """Install src at dst.

    Refuses to replace a directory that already holds something different, because that
    would silently destroy a skill the user wrote. Adopting this layer into a repository
    that already has its own skills must never cost them one.
    """
    if same_tree(src, dst) or (link and dst.is_symlink() and dst.resolve() == src):
        return "unchanged"
    if dst.exists() and not dst.is_symlink() and not force:
        return ("CONFLICT - a different skill of this name is already here; "
                "rename yours or pass --force to overwrite it")
    if check:
        return "would replace (--force)" if dst.exists() else "would create"
    if dst.is_symlink() or dst.exists():
        (dst.unlink if dst.is_symlink() else lambda: shutil.rmtree(dst))()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if link:
        try:
            dst.symlink_to(src, target_is_directory=True)
            return "linked"
        except OSError:
            pass  # Windows without developer mode; fall through to copy
    shutil.copytree(src, dst)
    return "copied"


def place_file(src: Path, dst: Path, check: bool, force: bool) -> str:
    """Install a single file, never clobbering a different one already at dst.

    Used for check.py, which is meant to be the same script in every repository that
    adopts this layer — so a byte difference is a real conflict worth reporting.
    """
    if dst.is_file() and dst.read_bytes() == src.read_bytes():
        return "unchanged"
    if dst.exists() and not force:
        return ("CONFLICT - a different file of this name is already here; "
                "keep yours, or pass --force to overwrite it")
    if check:
        return "would replace (--force)" if dst.exists() else "would create"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return "copied"


def seed_file(src: Path, dst: Path, check: bool) -> str:
    """Write src to dst only if dst does not exist. Never a conflict, never an overwrite.

    Used for AGENTS.md, which is a *scaffold* rather than a shipped artifact: the version
    here is an empty skeleton carrying the inclusion test, and the whole point is that the
    adopting repository fills it with its own content. A repository whose AGENTS.md differs
    from this one is working correctly, not drifting — so this must never report CONFLICT.
    """
    if dst.exists():
        return "unchanged - this repository already has its own"
    if check:
        return "would create from the template"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return "created from the template"


def ensure_claude_import(repo: Path, check: bool) -> str:
    """CLAUDE.md must import AGENTS.md or Claude Code silently ignores it."""
    if not (repo / "AGENTS.md").is_file():
        return "skipped - no AGENTS.md in this repository"
    path = repo / "CLAUDE.md"
    if not path.is_file():
        if check:
            return "would create CLAUDE.md with the import"
        path.write_text(CLAUDE_MD_NOTE, encoding="utf-8")
        return "created CLAUDE.md"
    text = path.read_text(encoding="utf-8")
    if IMPORT_LINE in text:
        return "unchanged - import already present"
    if check:
        return "WOULD PREPEND the import - it is missing and AGENTS.md is being ignored"
    path.write_text(IMPORT_LINE + "\n\n" + text, encoding="utf-8")
    return "PREPENDED the import - AGENTS.md was being ignored"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".", help="target repository (default: current directory)")
    ap.add_argument("--agents", default="all",
                    help="comma-separated: " + ",".join(AGENT_SKILL_PATHS) + ", or 'all'")
    ap.add_argument("--link", action="store_true", help="symlink instead of copy where possible")
    ap.add_argument("--check", action="store_true", help="report only; write nothing")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing skill directory of the same name (destructive)")
    a = ap.parse_args()

    repo = Path(a.repo).resolve()
    if not repo.is_dir():
        print(f"error: {repo} is not a directory", file=sys.stderr)
        return 2

    names = list(AGENT_SKILL_PATHS) if a.agents == "all" else [
        n.strip() for n in a.agents.split(",") if n.strip()
    ]
    unknown = [n for n in names if n not in AGENT_SKILL_PATHS]
    if unknown:
        print(f"error: unknown agent(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"known: {', '.join(AGENT_SKILL_PATHS)}", file=sys.stderr)
        return 2

    skills = discover_skills()
    mode = "CHECK - nothing will be written" if a.check else "INSTALL"
    print(f"{mode}\n  repository : {repo}\n  skills     : "
          f"{', '.join(p.name for p in skills) if skills else '(none)'}\n")

    results: list[str] = []
    if skills:
        # One destination may serve several agents; do the work once and say who it covers.
        by_dest: dict[str, list[str]] = {}
        for n in names:
            by_dest.setdefault(AGENT_SKILL_PATHS[n], []).append(n)
        for rel, agents in sorted(by_dest.items()):
            print(f"{rel}  ({', '.join(agents)})")
            for s in skills:
                outcome = place(s, repo / rel / s.name, a.link, a.check, a.force)
                results.append(outcome)
                print(f"    {s.name:<28} {outcome}")
            print()

    # Repository root. AGENTS.md must land before ensure_claude_import runs, because that
    # step is a no-op when there is no AGENTS.md to import.
    print("repository root")
    print(f"    {'AGENTS.md':<28} "
          f"{seed_file(HERE / 'templates' / 'AGENTS.md', repo / 'AGENTS.md', a.check)}")
    outcome = place_file(HERE / "check.py", repo / "check.py", a.check, a.force)
    results.append(outcome)
    print(f"    {'check.py':<28} {outcome}")
    print()

    print(f"CLAUDE.md import : {ensure_claude_import(repo, a.check)}")

    conflicts = [r for r in results if r.startswith("CONFLICT")]
    if conflicts:
        print()
        print(f"{len(conflicts)} conflict(s) - nothing of yours was overwritten.")
    if a.check:
        print()
        print("Nothing was written. Re-run without --check to apply.")

    print()
    print("This reports what INSTALLING would change. To verify the layer is intact"
          " afterwards - size, collisions with\nbuilt-in names, missing skill descriptions,"
          " drift - run check.py. It is read-only by design, which is\nwhat makes it safe"
          " in CI: a check that can repair what it is checking is not a check.")
    # --check exits non-zero on a conflict too. A conflict is exactly how drift surfaces —
    # an installed copy that no longer matches its source reads as "a different file is
    # already here" — so without this, CI has no way to catch it from the exit code.
    return 1 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
