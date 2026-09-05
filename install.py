#!/usr/bin/env python3
"""Install portable agent instructions and skills into a repository.

The SKILL.md format is broadly portable across agents; paths and some surface-specific layouts are
not. The current coverage table lives only in research/MATRIX.md section 2. In particular,
Antigravity 2.0/IDE document nested `<name>/SKILL.md`, while Antigravity CLI documents flat `.md`
Skills. This installer does not synthesize the untested CLI variant.

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
Successful installs record owned names, selected paths and source digests in
.houserules/skills.json. Later agent selections are additive; foreign skills are not enrolled.
Known conflicts are checked across all selected destinations before any installation write.

This script installs the complete layer. The default `python check.py` path only reads;
`check.py --fix` is an explicit local repair mode and must not be used as a CI gate.

Paths verified 2026-09-01. Re-check them when an agent releases; see the recheck policy in
research/MATRIX.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

from check import MANIFEST, read_manifest, tree_hash

HERE = Path(__file__).resolve().parent
SKILL_SRC = HERE / "templates" / "skills"

# Where each agent looks for project-scoped nested SKILL.md skills. Rechecked through 2026-09-04.
# Cursor and OpenCode also read .agents/skills, so their entries here are redundant; kept
# until the topology change is decided (research/MATRIX.md section 2, open items).
AGENT_SKILL_PATHS: dict[str, str] = {
    "claude": ".claude/skills",
    "codex": ".agents/skills",      # also read by Goose and Antigravity 2.0/IDE
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
    # Compare bytes even when file size and mtime match. The same digest is recorded for
    # standalone check.py, so installer preview and later verification agree.
    return tree_hash(src) == tree_hash(dst)


def place(src: Path, dst: Path, link: bool, check: bool, force: bool) -> str:
    """Install src at dst.

    Refuses to replace a directory that already holds something different, because that
    would silently destroy a skill the user wrote. Adopting this layer into a repository
    that already has its own skills must never cost them one.
    """
    if same_tree(src, dst) or (link and dst.is_symlink() and dst.resolve() == src):
        return "unchanged"
    if (dst.exists() or dst.is_symlink()) and not force:
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


def ensure_claude_import(repo: Path, check: bool, agents_pending: bool = False) -> str:
    """CLAUDE.md must import AGENTS.md or Claude Code silently ignores it.

    `agents_pending` says AGENTS.md does not exist yet but this same run would create it.
    Without that, --check on an empty repository reports the import as skipped while a real
    run creates both files - a preview that contradicts the outcome it is previewing.
    """
    if not (repo / "AGENTS.md").is_file() and not agents_pending:
        return "skipped - no AGENTS.md in this repository"
    # Both ./CLAUDE.md and ./.claude/CLAUDE.md are documented project locations. Prefer an
    # existing one over creating a second, competing instruction file.
    path = next((p for p in (repo / "CLAUDE.md", repo / ".claude" / "CLAUDE.md")
                 if p.is_file()), repo / "CLAUDE.md")
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

    if not names:
        print("error: select at least one agent", file=sys.stderr)
        return 2
    try:
        previous = read_manifest(repo)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    skills = discover_skills()
    # Validate the intended ownership record before touching the target repository.
    if any(not re.fullmatch(r"hr-[a-z0-9]+(?:-[a-z0-9]+)*", s.name) for s in skills):
        print("error: shipped skill names must use the hr- prefix", file=sys.stderr)
        return 2
    mode = "CHECK - nothing will be written" if a.check else "INSTALL"
    print(f"{mode}\n  repository : {repo}\n  skills     : "
          f"{', '.join(p.name for p in skills) if skills else '(none)'}\n")

    # One source digest covers every recorded path. Do not advance it while leaving an
    # unselected path on an older source, even with --force. Ownership remains additive.
    selected = {AGENT_SKILL_PATHS[n] for n in names}
    partial_upgrades = []
    for skill in skills:
        entry = (previous or {}).get("skills", {}).get(skill.name)
        if entry and entry["sha256"] != tree_hash(skill):
            omitted = sorted(set(entry["paths"]) - selected)
            if omitted:
                partial_upgrades.append(f"{skill.name}: include recorded paths {', '.join(omitted)}")
    if partial_upgrades:
        print("Installation stopped before writes: partial upgrade would invalidate"
              " the shared source digest.")
        print("\n".join(partial_upgrades))
        print("Select agents covering all recorded paths for each changed skill (or --agents all),"
              " then inspect and reconcile any content conflicts before retrying.")
        return 1

    # Both modes preflight the full selection, including the shipped root checker. A preview
    # must describe the same refusal as installation, not advertise writes that will not run.
    # This prevents known conflicts; it is not rollback for I/O errors or concurrent edits.
    conflicts = []
    for rel in sorted(selected):
        for skill in skills:
            outcome = place(skill, repo / rel / skill.name, a.link, True, a.force)
            if outcome.startswith("CONFLICT"):
                conflicts.append(f"{rel}/{skill.name}: {outcome}")
    outcome = place_file(HERE / "check.py", repo / "check.py", True, a.force)
    root_conflict = outcome.startswith("CONFLICT")
    if root_conflict:
        conflicts.append(f"check.py: {outcome}")
    if conflicts:
        print("\n".join(conflicts))
        if root_conflict:
            print("Installation stopped before writes. Review root check.py and reconcile it"
                  " with the shipped source before retrying. Changing --agents cannot resolve"
                  " this root-file conflict.")
        else:
            print("Installation stopped before writes. Resolve conflicts or select only"
                  " the intended non-conflicting agents.")
        return 1

    results: list[str] = []
    if skills:
        # One destination may serve several agents; do the work once and say who it covers.
        by_dest: dict[str, list[str]] = {}
        for n in names:
            by_dest.setdefault(AGENT_SKILL_PATHS[n], []).append(n)
        for rel, agents in sorted(by_dest.items()):
            labels = ["antigravity 2.0/IDE" if n == "antigravity" else n for n in agents]
            print(f"{rel}  ({', '.join(labels)})")
            if rel == ".agents/skills" and "antigravity" in agents:
                print("    note: nested SKILL.md covers documented Antigravity 2.0/IDE;"
                      " CLI flat .md is not installed")
            for s in skills:
                outcome = place(s, repo / rel / s.name, a.link, a.check, a.force)
                results.append(outcome)
                print(f"    {s.name:<28} {outcome}")
            print()

    # Repository root. AGENTS.md must land before ensure_claude_import runs, because that
    # step is a no-op when there is no AGENTS.md to import.
    print("repository root")
    agents_pending = not (repo / "AGENTS.md").is_file()
    outcome = seed_file(HERE / 'templates' / 'AGENTS.md', repo / 'AGENTS.md', a.check)
    results.append(outcome)
    print(f"    {'AGENTS.md':<28} {outcome}")
    outcome = place_file(HERE / "check.py", repo / "check.py", a.check, a.force)
    results.append(outcome)
    print(f"    {'check.py':<28} {outcome}")
    print()

    outcome = ensure_claude_import(repo, a.check, agents_pending)
    results.append(outcome)
    print(f"CLAUDE.md import : {outcome}")

    conflicts = [r for r in results if r.startswith("CONFLICT")]
    if conflicts:
        print()
        print(f"{len(conflicts)} conflict(s) - nothing of yours was overwritten.")
    # A conflict must never bless a different user's skill. Preflight prevents known
    # partial writes; this guard also covers preview conflicts and a concurrent change.
    if not conflicts:
        manifest = previous or {"schema_version": 1, "skills": {}}
        for skill in skills:
            prior_paths = manifest["skills"].get(skill.name, {}).get("paths", [])
            manifest["skills"][skill.name] = {
                "paths": sorted(set(prior_paths) | selected),
                "sha256": tree_hash(skill),
            }
        content = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        path = repo / MANIFEST
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            outcome = "unchanged"
        elif a.check:
            outcome = "would update ownership record"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            outcome = "recorded managed skills"
        results.append(outcome)
        print(f"{MANIFEST} : {outcome}")
    if a.check:
        print()
        print("Nothing was written. Re-run without --check to apply.")

    print()
    print("This reports what INSTALLING would change. To verify the layer is intact"
          " afterwards - size, collisions with\nbuilt-in names, missing skill descriptions,"
          " drift - run check.py. Its default path is read-only; in CI, run it without"
          " --fix so the gate reports drift instead of repairing it.")
    # Exit non-zero for ANY pending change, not conflicts alone. A location that was never
    # installed reports "would create", which is not a conflict but still means the layer is
    # incomplete — and reporting success there let a repository missing a whole skill
    # directory pass both gates. "Nothing to do" is the only green state.
    pending = [r for r in results
               if r.lower().startswith("would") or r.startswith("CONFLICT")]
    return 1 if pending else 0


if __name__ == "__main__":
    raise SystemExit(main())
