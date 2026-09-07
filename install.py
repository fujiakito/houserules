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

Two things land at the repository root, because an agent has to find them there: AGENTS.md and
the CLAUDE.md import line. Everything else this installer owns goes under .houserules/, including
both executables - check.py and workflow.py. AGENTS.md is a *scaffold* - a repository that has
filled it in has not drifted, so an existing one is left alone unless --activate-workflow
explicitly appends the routing block. An edited routing block is preserved and reported for
reconciliation. The rest are *managed assets*: an edited one stops every write, including with
--force, and is reported for reconciliation instead of being overwritten.

A root check.py from an installation made before the checker moved is reported and left alone.
Its provenance was never recorded, so it is never deleted, moved or overwritten automatically -
but a pre-move checker cannot read the manifest this installer writes, so on an upgrade the run
stops until --migrate-checker says the adopter has repointed or removed it. A first install into
a repository that has its own root check.py is unaffected: that file is theirs.

An existing skill directory is never replaced without --force. Adopting this layer into a
repository that already has its own skills must not cost the user one of them.
Successful installs record owned names, selected paths and source digests in
.houserules/skills.json. Later agent selections are additive; foreign skills are not enrolled.
Known conflicts are checked across all selected destinations before any installation write.

The default installs hr-onboard, a local HOUSERULES.md entry, START.md, check.py and
workflow.py. --ci adds a GitHub Actions workflow that runs the installed checker; it writes only
its own file, and cannot gate template drift because the installer is never copied into a project.
--activate-workflow appends a short instruction trigger; no hook or background process starts.
--skills and --work select
additional material; existing selections remain installed. --list shows the offline catalog.
The default `python .houserules/check.py` path only reads; `--fix` is an explicit local repair
mode and must not be used as a CI gate. It resolves --repo against the current directory, so run
it from the adopting project's root or pass --repo explicitly.

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

from check import (MANIFEST, ASSET_MANIFEST, WORK_NAMES, CI_WORKFLOW, INSTALLED_CHECKER,
                   read_manifest, tree_hash, read_assets, asset_path, content_hash)

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


SCAFFOLD_MARKER = "Fill from observed repo friction using hr-onboard"
# The generated page is committed by the adopter, so it must not carry the installing
# machine's paths: this repository regenerates its own HOUSERULES.md in CI, and an absolute
# path would be reported as drift on every other machine. The adopter fills this in once.
DISTRIBUTION = "<houserules distribution>/install.py"


def is_scaffold(repo: Path) -> bool:
    """True when AGENTS.md still needs filling from real work.

    Called before the scaffold is seeded, so a missing file counts as one: this same run
    creates it. An unreadable file is treated as the adopter's own content, never as a
    scaffold to give onboarding advice about.
    """
    path = repo / "AGENTS.md"
    if not path.is_file():
        return True
    try:
        return SCAFFOLD_MARKER in path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def covering_agents(names: list[str], recorded: set[str]) -> list[str]:
    """Agent labels whose skill paths cover every recorded install path.

    A follow-up install that omits --agents defaults to every agent and silently widens the
    installation; one that names too few paths cannot complete a later source upgrade, because
    the recorded digest is shared across all of them. Keep this run's labels and add whatever
    else is needed to reach the recorded paths.
    """
    chosen = set(names)
    for rel in sorted(recorded - {AGENT_SKILL_PATHS[n] for n in chosen}):
        chosen.add(next(n for n in AGENT_SKILL_PATHS if AGENT_SKILL_PATHS[n] == rel))
    covered = {AGENT_SKILL_PATHS[n] for n in chosen}
    # Collapse on the paths, not the labels: several agents share a directory, so naming a
    # subset of them can still reach every path an install could write.
    return ["all"] if covered == set(AGENT_SKILL_PATHS.values()) else sorted(chosen)


def shell_quote(value: str) -> str:
    """POSIX-style quoting, applied only where the value needs it.

    The rendered commands sit in ```bash fences, so POSIX rules are the documented ones, and
    under those rules a backslash is an escape character rather than a path separator: an
    unquoted `C:\\Projects\\demo` parses as `C:Projectsdemo`. Every Windows path therefore gets
    quoted, whether or not it also contains a space. Inside single quotes a backslash is
    literal, which is what makes this correct rather than merely tidier.

    Scope, so the claim stays as narrow as what is tested: POSIX shells. PowerShell agrees for
    paths without an apostrophe, but escapes an embedded one by doubling it, not as `\'`;
    cmd.exe does not read single quotes at all. Neither is claimed or tested here.
    """
    if value and not re.search(r"[^\w@%+=:,./-]", value):
        return value
    return "'" + value.replace("'", "'\\''") + "'"


def follow_up(installer: str, repo: str, agents: str,
              skills: list[str], work: list[str]) -> str:
    """The exact command that adds unselected material, runnable where it is printed.

    A distribution or project path containing a space is otherwise split by the shell into two
    arguments, and the copied command targets the wrong directory or none.
    """
    command = f"python {shell_quote(installer)} --repo {shell_quote(repo)} --agents {agents}"
    if skills:
        command += " --skills " + ",".join(skills)
    if work:
        command += " --work " + ",".join(work)
    return command


def unselected(catalog: set[str], skills: dict, work: set[str]) -> tuple[list[str], list[str]]:
    """What this installer ships and this repository does not have.

    Computed from the retained selection rather than from one invocation, so an additive
    second install and `--skills none` both report what is actually absent. It cannot see
    global, user-scope or plugin skills, which is stated wherever the result is printed.
    """
    return sorted(catalog - set(skills)), sorted(WORK_NAMES - work)


def start_page(skills: dict, work: set[str], catalog: set[str],
               agents: list[str], scaffold: bool, ci: bool = False) -> bytes:
    """Generated onboarding page: what to do now, not only what was installed.

    No upstream checkout or network is needed at use time, and nothing machine-specific is
    written, so the adopter can commit it.
    """
    agents_arg = ",".join(agents)
    missing_skills, missing_work = unselected(catalog, skills, work)
    add = follow_up(DISTRIBUTION, ".", agents_arg, missing_skills, missing_work)
    lines = ["# Using houserules in this project", "",
             "This page is generated by the installer and describes this repository only.",
             "It lists installed choices; it does not authorize external actions.", "",
             "## Start here", ""]
    if "hr-onboard" in skills and scaffold:
        lines += ["Ask your agent: **use the `hr-onboard` skill.**",
                  "It fills AGENTS.md from friction it hits while attempting real work here, not from a",
                  "description of the codebase. Everything below assumes AGENTS.md has been filled.", "",
                  "Expect few rules. A well-documented project legitimately yields a short AGENTS.md, and a",
                  "line describing what the project *is* fails the inclusion test while costing tokens on",
                  "every session. Judge the result by the skill's report of accepted and rejected",
                  "candidates, not by how much it wrote."]
    elif "hr-onboard" in skills:
        lines += ["AGENTS.md already holds this project's own instructions, so onboarding is done.",
                  "Start your task from the map below.", "",
                  "Run `hr-onboard` again only when an agent keeps repeating a mistake this repository",
                  "never wrote down."]
    else:
        lines += ["`hr-onboard` was not selected, so nothing installed here fills AGENTS.md.",
                  "Write this project's non-obvious rules into AGENTS.md yourself — the ones an agent",
                  "cannot infer from the code — then start your task from the map below.", "",
                  "To add the skill instead, run this from this project's root:", "",
                  "```bash",
                  follow_up(DISTRIBUTION, ".", agents_arg, ["hr-onboard"], []),
                  "```"]
    lines += ["", "## Add more later", ""]
    if missing_skills or missing_work:
        described = []
        if missing_skills:
            described.append("skills " + ", ".join(missing_skills)
                             + " (optional and experimental — availability is not evidence that they"
                               " beat your agent's own procedure)")
        if missing_work:
            described.append("work templates " + ", ".join(missing_work))
        lines += ["Shipped by this installer and **not** installed here: " + "; ".join(described) + ".", "",
                  "Selections are additive: this adds to what is here and uninstalls nothing. Run it from",
                  "this project's root, replacing the placeholder with wherever you keep the houserules",
                  "distribution. That path is local to whoever installed, so it is deliberately not",
                  "recorded on a page you commit.", "",
                  "```bash", add, "```", "",
                  f"Keep `--agents {agents_arg}`. Omitting `--agents` installs for **every** supported agent."]
    else:
        lines += ["Everything this installer ships is already installed here.",
                  "Re-run it from the distribution only to pick up newer versions of these files."]
    lines += ["", "This covers what the installer ships. Skills your agent loads from a global, user-scope",
              "or plugin location are outside its view and are not listed anywhere on this page.", "",
              "## What to use, when", ""]
    rows = [("An agent keeps repeating a mistake this repository never wrote down",
             "hr-onboard", "Write the rule into AGENTS.md yourself, with a check where one is possible"),
            ("New behaviour, and you want a test to define it",
             "hr-tdd", "Write the failing test first, then run this project's own test command"),
            ("A reported bug you cannot yet reproduce",
             "hr-diagnosing-bugs", "Reproduce it, narrow to the smallest failing input, fix, then re-run it"),
            ("Reviewing a change before it lands",
             "hr-code-review", "Review against AGENTS.md and the task's stated criteria, not against taste")]
    lines += ["| Situation | Use |", "|---|---|"]
    for situation, skill, fallback in rows:
        if skill in skills:
            rel = sorted(skills[skill]["paths"])[0]
            lines.append(f"| {situation} | [{skill}]({rel}/{skill}/SKILL.md) — ask your agent for it by name |")
        else:
            lines.append(f"| {situation} | Not installed. {fallback} |")
    carry = ("[work templates](.houserules/work/README.md) — copy one into the task's own location"
             if work else
             "Record the target, the next action and the actual verification in this project's own records")
    lines += [f"| Work resumes in another session, or another agent takes it over | {carry} |",
              "| A claim that something passed has to survive later edits |"
              " [the workflow tool](.houserules/workflow.py) — walkthrough below |",
              "| Checking that the installed layer is still intact |"
              " `python .houserules/check.py` from this project's root |", "",
              "Your agent may have a **native** command for some of these, and a native route is",
              "usually the better one where it exists. This page cannot say which: nothing installed",
              "here inspects your agent. Check its own documentation; the houserules distribution",
              "keeps a dated capability map in docs/GUIDE.md and inventories under docs/agents/.", "",
              "## A first task, end to end", "",
              "Run this from this project's root, substituting a real check of your own:", "",
              "```bash",
              "python .houserules/workflow.py start demo --task \"<the outcome you need>\""
              " --target <a file that check reads>",
              "python .houserules/workflow.py run demo -- <your test command>",
              "python .houserules/workflow.py status demo",
              "```", "",
              "`run` saves that command's log, exit status and elapsed time under `work/demo/`.",
              "`status` exits 0 while the recorded evidence still matches the tree. Now edit the file you",
              "passed to `--target` and run `status demo` again: it exits **1**, because the recorded pass",
              "no longer describes these files. That staleness signal is the point of the tool.", "",
              "It bounds only the commands passed through `run` — three attempts and 300 seconds of command",
              "time by default; set `--max-runs`/`--max-seconds` at `start`. It does not run an SDLC, choose",
              "your tests, judge whether the outcome was met, or cap chat usage.", "",
              "[.houserules/START.md](.houserules/START.md) is that same protocol written for the agent.",
              "Point your agent at it for multi-step or resuming work; re-install with `--activate-workflow`",
              "to have a small trigger appended to AGENTS.md instead.", "",
              "## Installed skills", "",
              "Files on disk are not proof of loading; check discovery on your own agent surface.", ""]
    for name, entry in sorted(skills.items()):
        links = ", ".join(f"[{rel}]({rel}/{name}/SKILL.md)" for rel in entry["paths"])
        state = "core" if name == "hr-onboard" else "optional / experimental"
        lines.append(f"- **{name}** ({state}): {links}")
    if not skills:
        lines.append("No skills selected.")
    lines += ["", "Matt Pocock adaptations carry their own NOTICE.md and MIT LICENSE beside SKILL.md.",
              "No companion skills, tracker account or parallel agents are required.",
              "houserules' own installed files are MIT; the notice is at",
              "[.houserules/LICENSE](.houserules/LICENSE) and your project's root LICENSE is untouched.",
              "", "## Carry work forward", ""]
    if work:
        lines += ["Copy a template into the task's own location — the project's existing one, or",
                  "work/<task-id>/ — and fill it there, leaving these originals intact. The",
                  "[consumer protocol](.houserules/work/README.md) says what each record must carry.", ""]
        lines += [f"- [{name}](.houserules/work/{name}.md)" for name in sorted(work)]
    else:
        lines.append("No work templates selected. Use existing project records; templates are an optional install choice.")
    lines += ["", "A small task needs no document set. Commit or explicitly transfer any records you do",
              "keep: ignored local files do not travel to a fresh checkout.", "",
              "## Verify and maintain", "",
              "Run `python .houserules/check.py` from this project's root after installation or changes.",
              "It checks managed copies, instruction structure and selected work assets, not semantic",
              "correctness or runtime loading. `--repo` defaults to the current directory, so run it from",
              "the root or pass `--repo <path>` explicitly.",
              "Run this project's tests separately. Keep existing project-owned files and foreign skills.", "",
              ("The installed workflow at .github/workflows/houserules.yml runs that checker on"
               " every push and pull request. Whether it becomes a *required* check is your"
               " decision, in this repository's branch protection settings." if ci else
               "No CI workflow was installed for it. Re-install with --ci for a GitHub Actions"
               " workflow that runs the checker on every push and pull request; no existing"
               " workflow is touched."), "",
              "Re-run the houserules installer from its distribution for updates or additional selections;",
              "preview first with --check. Nothing updates over the network in the background.",
              "Keep HOUSERULES.md, .houserules manifests and installed material in Git; record your",
              "customizations in project work files. Modified managed files are reported and preserved",
              "until you reconcile them. Hooks and MCP connections are not installed by this layer.", ""]
    return "\n".join(lines).encode("utf-8")


def plan_assets(repo: Path, previous: dict, page: bytes, work: set[str],
                ci: bool = False) -> dict[str, bytes]:
    # MIT requires the notice to travel with copies. check.py, workflow.py, START.md and
    # hr-onboard are first-party, so an installation without this file would ship substantial
    # portions of the software with no notice. It is installed inside .houserules/ on purpose:
    # the adopting project's own root LICENSE is theirs and is never touched.
    notice = HERE / 'LICENSE'
    if not notice.is_file():
        raise ValueError("distribution is missing LICENSE; installing first-party files without "
                         "the notice would break the terms they ship under")
    # Both installed executables live in .houserules/. check.py is a managed asset like every
    # other one here, so an adopter's edit to it is preserved and reported rather than
    # overwritten, and the checker verifies its own installed copy's digest.
    files = {"HOUSERULES.md": page,
             ".houserules/LICENSE": notice.read_bytes(),
             ".houserules/START.md": (HERE / 'templates/START.md').read_bytes(),
             INSTALLED_CHECKER: (HERE / 'check.py').read_bytes(),
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
    if ci:
        files[CI_WORKFLOW] = (HERE / "templates/ci/github-actions.yml").read_bytes()
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


def place(src: Path, dst: Path, link: bool, check: bool, force: bool,
          managed: bool = False) -> str:
    """Install src at dst.

    Refuses to replace a directory that already holds something different, because that
    would silently destroy a skill the user wrote. Adopting this layer into a repository
    that already has its own skills must never cost them one.
    """
    if same_tree(src, dst) or (link and dst.is_symlink() and dst.resolve() == src):
        return "unchanged"
    if (dst.exists() or dst.is_symlink()) and not force:
        if managed:
            return ("CONFLICT - recorded installed copy differs from current source "
                    "(older version or local modification); compare and preserve local changes "
                    "before using --force to overwrite it")
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


def legacy_root_checker(repo: Path, upgrading: bool = False) -> str | None:
    """Report, never touch, a `check.py` at the adopter's root.

    Installations before the checker moved into .houserules/ left one there, and nothing
    recorded its ownership - it was not in the asset manifest, so "same name" never meant
    "ours". A file whose provenance is ambiguous is not deleted, moved or overwritten here.

    Leaving the bytes alone is not the same as leaving the behaviour alone, which an earlier
    version of this code claimed. A checker from before the move rejects the manifest this
    installation writes - `invalid managed asset: .houserules/check.py`, reproduced against the
    8ae9d31 checker on 2026-09-07 - so a CI job still invoking it goes red on its next build.
    On an upgrade that is a blocking migration, handled by the caller; on a first install the
    root file is the adopter's own and nothing of theirs is about to change.
    """
    path = repo / "check.py"
    if not (path.is_file() or path.is_symlink()) or repo == HERE:
        return None  # In the distribution itself that root file is the source, not a leftover.
    if not upgrading:
        return ("left untouched - it is yours. The installed checker is .houserules/check.py,"
                " which does not replace or read this file.")
    return ("left untouched - the installed checker is now .houserules/check.py. Nothing"
            " records who wrote this root file, so it is never removed automatically."
            " A pre-move checker FAILS against the manifest written below; repoint or delete"
            " it.")


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
    ap.add_argument("--ci", action="store_true",
                    help="add a GitHub Actions workflow running the installed checker; other workflows are untouched")
    ap.add_argument("--migrate-checker", action="store_true",
                    help="confirm that a root check.py left by an earlier install has been repointed or removed")
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
        # Retained like every other selection: once added it stays until the adopter removes it.
        ci = a.ci or CI_WORKFLOW in assets["files"]
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
    agent_labels = covering_agents(names, {rel for entry in future_skills.values()
                                           for rel in entry["paths"]})
    try:
        page = start_page(future_skills, work, set(catalog), agent_labels,
                          is_scaffold(repo), ci)
        asset_files = plan_assets(repo, assets, page, work, ci)
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

    # An upgrade out of the pre-move layout leaves that root checker broken - silently as far
    # as this run is concerned, loudly on the adopter's next CI build. Refuse until they say
    # they have dealt with it.
    #
    # "Pre-move" is a recorded fact, not a guess: a manifest that already names the installed
    # checker was written after the move, so its migration is done and this must never fire
    # again. A first install is exempt too - there is no manifest, so that root file is the
    # adopter's own and nothing of theirs is about to change.
    installed = (repo / ASSET_MANIFEST).is_file() or previous is not None
    upgrading = installed and INSTALLED_CHECKER not in assets["files"]
    if upgrading and legacy_root_checker(repo, True) and not a.migrate_checker:
        print("Installation stopped before writes: root check.py needs migrating first.")
        print("  This installation records .houserules/check.py in the asset manifest. A checker"
              " from before the move rejects that manifest outright - it reports"
              " 'invalid managed asset: .houserules/check.py' and exits 1 - so any CI job still"
              " running root check.py fails on its next build.")
        print("  Repoint that job at .houserules/check.py (run from the project root, or pass"
              " --repo), or delete the root file. Then re-run with --migrate-checker.")
        print("  Nothing at your root is deleted by this installer, with or without that flag.")
        return 1

    # Both modes preflight the full selection. A preview must describe the same refusal as
    # installation, not advertise writes that will not run. The installed checker is preflighted
    # with the other managed assets in plan_assets above, which already returned.
    # This prevents known conflicts; it is not rollback for I/O errors or concurrent edits.
    conflicts = []
    for rel in sorted(selected):
        for skill in skills:
            managed = rel in (previous or {}).get("skills", {}).get(skill.name, {}).get("paths", [])
            outcome = place(skill, repo / rel / skill.name, a.link, True, a.force, managed)
            if outcome.startswith("CONFLICT"):
                conflicts.append(f"{rel}/{skill.name}: {outcome}")
    if conflicts:
        print("\n".join(conflicts))
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
                managed = rel in (previous or {}).get("skills", {}).get(s.name, {}).get("paths", [])
                outcome = place(s, repo / rel / s.name, a.link, a.check, a.force, managed)
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
    legacy = legacy_root_checker(repo, upgrading)
    if legacy:
        print(f"    {'check.py':<28} {legacy}")
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
        # Naming only the entry page let an adopter finish an install without ever learning
        # that --skills and --work exist. The same retained selection drives the generated
        # page, so stdout and HOUSERULES.md cannot disagree. Here the real paths are printed:
        # this text is not committed anywhere, so it can be pasted as-is.
        missing_skills, missing_work = unselected(set(catalog), future_skills, work)
        print()
        if missing_skills or missing_work:
            described = []
            if missing_skills:
                described.append("skills " + ", ".join(missing_skills)
                                 + " (optional, experimental)")
            if missing_work:
                described.append("work templates " + ", ".join(missing_work))
            print("Not installed: " + "; ".join(described)
                  + ". Selections are additive; this uninstalls nothing:")
            print("  " + follow_up(str(HERE / "install.py"), str(repo),
                                   ",".join(agent_labels), missing_skills, missing_work))
            print(f"  Keep --agents {','.join(agent_labels)}."
                  " Omitting --agents installs for every supported agent.")
            print("  Global, user-scope and plugin skills are outside this installer's view.")
        else:
            print("Everything this installer ships is selected here.")
        print("\nStart here: HOUSERULES.md")
    if a.check:
        print()
        print("Nothing was written. Re-run without --check to apply.")

    print()
    print("To verify the installed layer - size, collisions with\nbuilt-in names, missing skill descriptions,"
          " drift - run .houserules/check.py from the project root. Its default path is"
          " read-only; in CI, run it without --fix so the gate reports drift instead of"
          " repairing it.")
    # Exit non-zero for ANY pending change, not conflicts alone. A location that was never
    # installed reports "would create", which is not a conflict but still means the layer is
    # incomplete — and reporting success there let a repository missing a whole skill
    # directory pass both gates. "Nothing to do" is the only green state.
    pending = [r for r in results
               if r.lower().startswith("would") or r.startswith("CONFLICT")]
    return 1 if pending else 0


if __name__ == "__main__":
    raise SystemExit(main())
