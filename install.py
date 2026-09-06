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
existing one is left alone unless --activate-workflow explicitly appends the routing block.
An edited routing block is preserved and reported for reconciliation. check.py is a *shipped
artifact* meant to be identical everywhere, so a byte difference is a conflict.

An existing skill directory is never replaced without --force. Adopting this layer into a
repository that already has its own skills must not cost the user one of them.
Successful installs record owned names, selected paths and source digests in
.houserules/skills.json. Later agent selections are additive; foreign skills are not enrolled.
Known conflicts are checked across all selected destinations before any installation write.

The default installs hr-onboard, a local HOUSERULES.md entry, START.md and workflow.py.
--activate-workflow appends a short instruction trigger; no hook or background process starts.
--skills and --work select
additional material; existing selections remain installed. --list shows the offline catalog.
The default `python check.py` path only reads;
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

from check import (MANIFEST, ASSET_MANIFEST, WORK_NAMES, read_manifest, tree_hash,
                   read_assets, asset_path, content_hash)

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

WORKFLOW_BLOCK = """<!-- houserules:workflow -->
For multi-step or usage-sensitive work, read `.houserules/START.md` before execution.
When resuming a task with `work/<id>/workflow.json`, run
`python .houserules/workflow.py status <id>` before reusing its verification.
<!-- /houserules:workflow -->"""


def workflow_activation(repo: Path) -> bytes | None:
    path = repo / 'AGENTS.md'
    if path.is_symlink() or not path.resolve().is_relative_to(repo):
        raise ValueError('Workflow activation cannot modify a linked AGENTS.md')
    current = path.read_bytes() if path.exists() else (HERE / 'templates/AGENTS.md').read_bytes()
    text = current.decode('utf-8')
    if '<!-- houserules:workflow -->' in text or '<!-- /houserules:workflow -->' in text:
        if WORKFLOW_BLOCK not in text.replace('\r\n', '\n'):
            raise ValueError('Preserve edited workflow instruction block; reconcile it before activation')
        return None
    return current + b'\n\n' + WORKFLOW_BLOCK.encode('utf-8') + b'\n'

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


def choose(value: str | None, available: set[str], default: set[str]) -> set[str]:
    if value is None:
        return default
    if value == "all":
        return available
    if value == "none":
        return set()
    selected = {part.strip() for part in value.split(",") if part.strip()}
    if not selected or selected - available:
        raise ValueError("choose from " + ", ".join(sorted(available)) + ", all or none")
    return selected


def start_page(skills: dict, work: set[str]) -> bytes:
    """Generated local entry point; no upstream checkout or network needed at use time."""
    lines = ["# Using houserules in this project", "",
             "Start with this project's AGENTS.md and existing task instructions.",
             "This page lists installed choices; it does not authorize external actions.", "",
             "## Start a task", "",
             "Tell your agent: **Read `.houserules/START.md` and use it for this task: <outcome>.**",
             "The [short execution protocol](.houserules/START.md) uses the installed",
             "[workflow tool](.houserules/workflow.py) to bound command attempts and execution time,",
             "save logs and detect stale verification. It does not cap surrounding chat usage.",
             "To load this protocol on relevant tasks automatically, install with --activate-workflow;",
             "that explicitly appends a small trigger to AGENTS.md, preserving existing content.", "",
             "## Installed skills", "",
             "Ask your agent to use a skill by name, or open its local SKILL.md below.",
             "Actual native discovery must be checked on your agent surface; files alone are not proof.", ""]
    for name, entry in sorted(skills.items()):
        links = ", ".join(f"[{rel}]({rel}/{name}/SKILL.md)" for rel in entry["paths"])
        state = "core" if name == "hr-onboard" else "optional / experimental"
        lines.append(f"- **{name}** ({state}): {links}")
    if not skills:
        lines.append("No skills selected.")
    lines += ["", "For test-first work use hr-tdd; for diagnosis use hr-diagnosing-bugs;",
              "for code review use hr-code-review, **only if listed above**. Matt Pocock adaptations",
              "carry their own NOTICE.md and MIT LICENSE beside SKILL.md. No companion skills,",
              "tracker account or parallel agents are required.",
              "houserules' own installed files are MIT; the notice is at",
              "[.houserules/LICENSE](.houserules/LICENSE) and your project's root LICENSE is untouched.",
              "", "## Carry work forward", ""]
    if work:
        lines += ["Read the [consumer protocol](.houserules/work/README.md) when passing work between sessions.",
                  "Copy only the needed template into the project's existing work location",
                  "(or work/<task-id>/); fill it there, leaving the installed originals intact.", ""]
        lines += [f"- [{name}](.houserules/work/{name}.md)" for name in sorted(work)]
    else:
        lines.append("No work templates selected. Use existing project records; templates are an optional install choice.")
    lines += ["", "A small task needs no document set. Record the target, next action and actual verification",
              "when another session needs them. Commit or explicitly transfer records to a fresh checkout;",
              "ignored local files do not travel automatically.", "", "## Verify and maintain", "",
              "Run `python check.py` here after installation or changes. It checks managed copies,",
              "instruction structure and selected work assets, not semantic correctness or runtime loading.",
              "Run this project's tests separately. Keep existing project-owned files and foreign skills.", "",
              "Re-run the houserules installer from its distribution for updates or additional selections;",
              "preview first with --check. Nothing updates over the network in the background.",
              "Keep HOUSERULES.md, .houserules manifests and installed material in Git; record your",
              "customizations in project work files. Modified managed files are reported and preserved",
              "until you reconcile them. Hooks and MCP connections are not installed by this layer.", ""]
    return "\n".join(lines).encode("utf-8")


def plan_assets(repo: Path, previous: dict, skills: dict, work: set[str]) -> dict[str, bytes]:
    # MIT requires the notice to travel with copies. check.py, workflow.py, START.md and
    # hr-onboard are first-party, so an installation without this file would ship substantial
    # portions of the software with no notice. It is installed inside .houserules/ on purpose:
    # the adopting project's own root LICENSE is theirs and is never touched.
    notice = HERE / 'LICENSE'
    if not notice.is_file():
        raise ValueError("distribution is missing LICENSE; installing first-party files without "
                         "the notice would break the terms they ship under")
    files = {"HOUSERULES.md": start_page(skills, work),
             ".houserules/LICENSE": notice.read_bytes(),
             ".houserules/START.md": (HERE / 'templates/START.md').read_bytes(),
             ".houserules/workflow.py": (HERE / 'templates/workflow.py').read_bytes()}
    if work:
        for name in work | {"README"}:
            content = (HERE / "templates/work" / f"{name}.md").read_bytes()
            if name == "README":
                text = content.decode("utf-8")
                for omitted in WORK_NAMES - work:
                    text = text.replace(f"[{omitted}.md]({omitted}.md)", f"{omitted} (not selected)")
                text = text.replace("[worked pilot](../../tests/workflows/README.md)", "worked pilot in the houserules distribution")
                content = text.encode("utf-8")
            files[f".houserules/work/{name}.md"] = content
    # Every path and current user edit is checked before any installation write, even with --force.
    for rel, content in files.items():
        path = asset_path(repo, rel)
        for parent in path.parents:
            if parent == repo:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"CONFLICT - non-directory asset parent: {parent}")
        if path.exists():
            if not path.is_file():
                raise ValueError(f"CONFLICT - asset is not a file: {rel}")
            current = content_hash(path.read_bytes())
            if current not in {content_hash(content), previous["files"].get(rel)}:
                raise ValueError(f"CONFLICT - preserve modified/unowned {rel}; reconcile it before retrying")
    return files


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
    ap.add_argument("--skills", help="comma-separated skill names, all or none; default: hr-onboard and previously selected skills")
    ap.add_argument("--work", help="comma-separated work templates, all or none; default: keep previous selection")
    ap.add_argument("--list", action="store_true", help="list available skills and work templates; write nothing")
    ap.add_argument("--activate-workflow", action="store_true", help="append an idempotent execution trigger to AGENTS.md; preserve existing bytes")
    ap.add_argument("--link", action="store_true", help="symlink instead of copy where possible")
    ap.add_argument("--check", action="store_true", help="report only; write nothing")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing skill directory of the same name (destructive)")
    a = ap.parse_args()

    catalog = {p.name: p for p in discover_skills()}
    if a.list:
        print("Skills (optional skills require explicit selection):")
        for name in catalog:
            print(f"  {name}: " + ("core" if name == "hr-onboard" else "Matt Pocock adaptation; experimental; MIT; see NOTICE.md"))
        print("Work templates: " + ", ".join(sorted(WORK_NAMES)))
        return 0

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
        assets = read_assets(repo)
        skill_names = choose(a.skills, set(catalog),
                             {"hr-onboard"} | (set((previous or {}).get("skills", {})) & set(catalog)))
        prior_work = {Path(rel).stem for rel in assets["files"]
                      if rel.startswith(".houserules/work/") and Path(rel).stem in WORK_NAMES}
        work = prior_work | choose(a.work, WORK_NAMES, set())
        activation = workflow_activation(repo) if a.activate_workflow else None
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    skills = [catalog[name] for name in sorted(skill_names)]
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
    manifest = previous or {"schema_version": 1, "skills": {}}
    # Construct the prospective page/record without mutating the previous state used for checks.
    future_skills = {name: dict(entry) for name, entry in manifest["skills"].items()}
    for skill in skills:
        future_skills[skill.name] = {
            "paths": sorted(set(future_skills.get(skill.name, {}).get("paths", [])) | selected),
            "sha256": tree_hash(skill),
        }
    try:
        asset_files = plan_assets(repo, assets, future_skills, work)
    except (OSError, ValueError) as exc:
        print(f"Installation stopped before writes: {exc}")
        return 1
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
    if activation is not None:
        if a.check:
            outcome = 'would append workflow trigger'
        else:
            (repo / 'AGENTS.md').write_bytes(activation)
            outcome = 'appended workflow trigger'
        results.append(outcome)
        print(f"    workflow activation          {outcome}")
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
        for rel, content in sorted(asset_files.items()):
            path = asset_path(repo, rel)
            if path.is_file() and content_hash(path.read_bytes()) == content_hash(content):
                outcome = "unchanged"
            elif a.check:
                outcome = "would update" if path.exists() else "would create"
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                outcome = "written"
            results.append(outcome)
            print(f"{rel} : {outcome}")
        content = json.dumps({"schema_version": 1, "files": {
            rel: content_hash(data) for rel, data in asset_files.items()
        }}, indent=2, sort_keys=True) + "\n"
        path = asset_path(repo, ASSET_MANIFEST)
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            outcome = "unchanged"
        elif a.check:
            outcome = "would record work assets"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            outcome = "recorded work assets"
        results.append(outcome)
        print(f"{ASSET_MANIFEST} : {outcome}")
        print("\nStart here: HOUSERULES.md")
    if a.check:
        print()
        print("Nothing was written. Re-run without --check to apply.")

    print()
    print("To verify the installed layer - size, collisions with\nbuilt-in names, missing skill descriptions,"
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
