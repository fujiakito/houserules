#!/usr/bin/env python3
"""Verify the portable agent layer is intact. Exit 0 = pass, 1 = fail, 2 = usage error.

Every check here guards a failure that is **silent** — the repository looks fine, agents
behave differently, and nothing raises an error. That is why they belong in CI rather than
in an instruction telling an agent to remember.

    python check.py            run every check
    python check.py --fix      repair what is safely repairable, then re-check

CI must use the first form. The explicit --fix path mutates the repository and is a local repair
command, not a valid gate.

Run it in CI. A hook is a fine accelerator, but the check is the contract: it binds
regardless of which agent — or which human — made the change, and it validates state
rather than trusting anyone's claim that something was done.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# Codex's `project_doc_max_bytes` DEFAULT — configurable, not a hard ceiling.
#
# Two official pages disagree on what it bounds: the AGENTS.md discovery page says the
# COMBINED size of the concatenated chain, the configuration reference reads as per-file.
# This measures the chain total, the stricter reading — conservative rather than wrong if the
# other one is right. Both retrieved 2026-09-01. research/MATRIX.md section 2.
#
# Antigravity separately documents a 12,000-character limit for `.agents/rules/*.md`. Its current
# scope does not establish a limit for `AGENTS.md` or `GEMINI.md`, so it is recorded in MATRIX.md
# as a test item and deliberately does not change this Codex instruction-chain check.
MAX_INSTRUCTION_BYTES = 32 * 1024
WARN_AT = 8 * 1024  # long before the budget bites, brevity is the point

IMPORT_LINE = "@AGENTS.md"

# Per-directory precedence, highest first. Codex: "In each directory along the path, it checks
# for AGENTS.override.md, then AGENTS.md." The override replaces the plain file at its own
# level only — the chain continues through the directories above and below it.
#
# LIMIT: these two default names only. Codex also honours `project_doc_fallback_filenames`
# ("additional filenames to try when AGENTS.md is missing"), which can be set in
# ~/.codex/config.toml — outside the repository, so unknowable from here. A repo relying on
# that setting has instruction content this check does not see. research/MATRIX.md section 2.
INSTRUCTION_FILENAMES = ("AGENTS.override.md", "AGENTS.md")

# Skill directory names that collide with a built-in. A collision is silent: Claude Code
# replaces the bundled skill and never warns. research/MATRIX.md section 9.
# Lower bound — it grows with each release, which is why the rule is "prefix", not "blocklist".
#
# Sourced from the published commands reference, retrieved 2026-09-02 — NOT from enumerating a
# session. A live session cannot tell a bundled skill from one the user installed, so it is the
# wrong evidence for this set. See docs/agents/claude-code.md section 3.
#
# Bare-named BUNDLED skills and built-in commands only. Claude Code addresses plugin skills as
# `plugin:skill` (`anthropic-skills:pdf`), so a project skill named `pdf` cannot shadow one —
# which is why docx/xlsx/pptx are deliberately absent here.
RESERVED_CLAUDE = {
    # bundled skills — rows marked `Skill` in the commands reference
    "batch", "claude-api", "code-review", "dataviz", "debug", "design", "design-sync",
    "doctor", "fewer-permission-prompts", "loop", "run", "run-skill-generator", "sandbox",
    "schedule", "security-review", "simplify", "verify",
    # bundled workflow, and the skill that is present only when workflows are enabled
    "deep-research", "workflow-authoring",
    # documented aliases — an alias never reaches a project skill, so a name that only
    # matches an alias still costs you the bundled one
    "review", "checkup", "routines", "proactive", "peers", "bg", "reset", "new",
    "settings", "allowed-tools", "plugins",
    # built-in commands
    "add-dir", "advisor", "agents", "artifacts", "auto-mode-setup", "autocompact",
    "autofix-pr", "background", "branch", "btw", "bug", "cd", "chrome", "clear", "color",
    "compact", "config", "context", "copy", "cost", "design-login", "desktop", "diff",
    "effort", "exit", "export", "fast", "feedback", "focus", "fork", "goal", "heapdump",
    "help", "hooks", "ide", "import", "init", "insights", "install-github-app",
    "install-slack-app", "keybindings", "list-agents", "login", "logout", "mcp", "memory",
    "mobile", "model", "passes", "permissions", "plan", "plugin", "powerup", "pr-comments",
    "privacy-settings", "radio", "reload-plugins", "reload-skills", "remote-control",
    "resume", "rewind", "slash-commands", "status", "statusline", "subtask", "tasks",
    "usage", "vim", "voice", "web-setup", "workflows", "worktree",
    # documented in the commands reference and on the sessions page. An earlier revision wrongly
    # recorded it as absent after searching only the former: the commands reference is the biggest
    # enumerable list, not the whole surface.
    "rename",
    # observed in a session but absent from the commands reference; kept because this set is a
    # lower bound and reserving a name costs nothing
    "update-config", "keybindings-help", "artifact-design", "artifact-diagramming",
    "artifact-capabilities", "exec",
    # Reserved defensively, no source found on any page. Kept because this set's failure modes are
    # asymmetric: a MISSING name is a silent collision, while an EXTRA name only tells you to add
    # a prefix — which AGENTS.md requires regardless. Not claimed as a Claude Code command.
    "archive",
}

# Codex names, measured 2026-08-31 against codex-cli 0.151.0-alpha.7.2: bundled and curated
# plugin skills, the vendored openai/skills catalogue, and the documented slash commands.
# research/MATRIX.md section 9.
#
# The failure differs from Claude Code's and is why these are a separate set. Codex does not
# replace a bundled skill: a duplicate name produces BOTH entries in the selector, unmerged.
# Nothing is lost, so this is a warning — but `$pdf` matching two different skills is still a
# coin flip over which one runs, and `.agents/skills/` is shared by Codex, Goose and
# Antigravity, so a name chosen for one of them lands in all three.
RESERVED_CODEX = {
    # ~/.codex/skills/.system — the true built-ins, confirmed loaded via
    # `codex debug prompt-input` (docs/agents/codex.md)
    "imagegen", "openai-docs", "plugin-creator", "skill-creator", "skill-installer",
    "review-agent",
    # bundled + primary-runtime plugin skills
    "documents", "pdf", "presentations", "spreadsheets", "excel-live-control",
    "template-creator", "visualize", "control-chrome", "control-in-app-browser",
    "plugin-management", "computer-use", "latex", "browser", "chrome",
    # codex-security plugin — a gated add-on, so these only collide where it is provisioned.
    # Kept because this set is a lower bound and a prefix costs nothing.
    "security-scan", "deep-security-scan", "security-diff-scan", "threat-model",
    "finding-discovery", "attack-path-analysis", "validation", "triage-finding",
    "fix-finding", "track-findings",
    # vendored openai/skills catalogue
    "define-goal", "migrate-to-codex", "hatch-pet", "yeet", "screenshot", "speech",
    "transcribe", "playwright", "playwright-interactive", "cli-creator",
    "jupyter-notebook", "figma", "figma-use", "linear", "sentry", "aspnet-core",
    "chatgpt-apps", "winui-app", "gh-fix-ci", "gh-address-comments",
    "security-best-practices", "security-ownership-map", "security-threat-model",
    "vercel-deploy", "netlify-deploy", "render-deploy", "cloudflare-deploy",
    # slash commands — official reference plus the desktop app's own menu, 2026-08-31
    "ide", "keymap", "vim", "agent", "subagents", "apps", "plugins", "hooks",
    "rename", "archive", "delete", "title", "stop", "approvals", "undo",
    "goal", "init", "pet", "plan", "review", "chat", "reasoning", "worktree",
}

# Antigravity public slash commands and documented aliases. Official shared command page and CLI
# reference retrieved 2026-09-04; docs/agents/antigravity.md.
RESERVED_ANTIGRAVITY_COMMANDS = {
    "add-dir", "agents", "artifact", "boost", "browser", "btw", "clear", "codesearch",
    "config", "context", "copy", "credits", "diff", "exit", "fast", "feedback", "fork",
    "goal", "grill-me", "help", "hooks", "keybindings", "learn", "logout", "mcp", "model",
    "open", "permissions", "plan", "planning", "rename", "resume", "rewind", "schedule",
    "skills",
    "statusline", "tasks", "teamwork-preview", "title", "usage", "voice",
    # aliases in the official CLI reference
    "new", "settings", "quit", "branch", "switch", "conversation", "undo", "teamwork",
    "quota", "record",
}

# Confirmed built-in Skill names are a different namespace in the source material even though the
# CLI turns registered Skills into slash commands. Same-name resolution remains undocumented, so
# collisions warn rather than fail. Official changelog retrieved 2026-09-04.
RESERVED_ANTIGRAVITY_SKILLS = {"antigravity_guide", "migrate-workflows"}
RESERVED_ANTIGRAVITY = RESERVED_ANTIGRAVITY_COMMANDS | RESERVED_ANTIGRAVITY_SKILLS

# The canonical built-in-Skills table also contains a 2.0 display name that is not documented as
# a CLI invocation identifier. Track catalogue drift without claiming it is a collision name.
DOCUMENTED_ANTIGRAVITY_BUILTIN_SKILLS = {
    "antigravity guide", "antigravity_guide", "migrate-workflows",
}

SKILL_DIRS = [".claude/skills", ".agents/skills", ".cursor/skills",
              ".kiro/skills", ".opencode/skills"]
MANIFEST = ".houserules/skills.json"
# Standalone check.py cannot discover templates in adopting repositories. This catalogue
# detects ambiguous legacy installs, not ownership; tests keep it aligned with shipped sources.
SHIPPED_SKILL_NAMES = {"hr-onboard", "hr-tdd", "hr-diagnosing-bugs", "hr-code-review"}
ASSET_MANIFEST = ".houserules/assets.json"
WORK_NAMES = {"handoff", "spec", "plan", "review", "findings", "verification"}
ASSET_PATHS = {"HOUSERULES.md", ".houserules/LICENSE", ".houserules/START.md",
               ".houserules/workflow.py", ".houserules/work/README.md"} | {
    f".houserules/work/{name}.md" for name in WORK_NAMES
}

FAIL, WARN, OK = "FAIL", "warn", "ok"


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, level: str, name: str, detail: str) -> None:
        self.rows.append((level, name, detail))

    @property
    def failed(self) -> bool:
        return any(l == FAIL for l, _, _ in self.rows)

    def render(self) -> None:
        width = max((len(n) for _, n, _ in self.rows), default=0)
        for level, name, detail in self.rows:
            mark = {FAIL: "FAIL", WARN: "warn", OK: "  ok"}[level]
            print(f"  {mark}  {name:<{width}}  {detail}")


def check_import(repo: Path, r: Report, fix: bool) -> None:
    """CLAUDE.md must import AGENTS.md, or Claude Code ignores it and says nothing.

    Both `./CLAUDE.md` and `./.claude/CLAUDE.md` are documented project locations, so either
    satisfies this. Creating a second one when the other already exists would give the repo
    two competing project instruction files.
    """
    agents = repo / "AGENTS.md"
    if not agents.is_file():
        r.add(WARN, "AGENTS.md", "absent — nothing portable to carry")
        return

    candidates = [repo / "CLAUDE.md", repo / ".claude" / "CLAUDE.md"]
    existing = [p for p in candidates if p.is_file()]

    if not existing:
        if fix:
            candidates[0].write_text(IMPORT_LINE + "\n", encoding="utf-8")
            r.add(OK, "CLAUDE.md import", "created")
        else:
            r.add(FAIL, "CLAUDE.md import",
                  "no CLAUDE.md or .claude/CLAUDE.md — Claude Code reads nothing here"
                  " (--fix creates it)")
        return

    importing = [p for p in existing
                 if IMPORT_LINE in p.read_text(encoding="utf-8")]
    if importing:
        where = ", ".join(p.relative_to(repo).as_posix() for p in importing)
        r.add(OK, "CLAUDE.md import", f"present in {where}")
    elif fix:
        target = existing[0]
        target.write_text(IMPORT_LINE + "\n\n" + target.read_text(encoding="utf-8"),
                          encoding="utf-8")
        r.add(OK, "CLAUDE.md import", f"prepended to {target.relative_to(repo).as_posix()}")
    else:
        where = ", ".join(p.relative_to(repo).as_posix() for p in existing)
        r.add(FAIL, "CLAUDE.md import",
              f"'{IMPORT_LINE}' missing from {where}"
              " — Claude Code is SILENTLY ignoring AGENTS.md")


def check_size(repo: Path, r: Report) -> None:
    """Measure the AGENTS.md chain, not one file and not the whole repository.

    Codex concatenates one applicable file per directory from the repo root down to the working
    directory. Measuring only the root file passes a repository whose nested files push the
    chain over the budget; summing every file in the repository invents a total no session ever
    sees, because sibling directories are never in the same chain.

    What `project_doc_max_bytes` bounds is disputed: the discovery page says the combined chain,
    the configuration reference reads as per-file (both retrieved 2026-09-01, MATRIX.md section
    2). **This deliberately enforces the combined-chain reading** — the stricter one, so it is
    conservative rather than wrong if the other turns out to be correct.
    """
    # "In each directory along the path, it checks for AGENTS.override.md, then AGENTS.md."
    # The override replaces the plain file at ITS OWN level only; the chain continues past it.
    # Scanning only AGENTS.md makes a repository built on overrides look empty.
    dirs = set()
    for root, children, files in os.walk(repo, followlinks=False):
        directory = Path(root)
        # Independent clones/submodules/worktrees have their own instruction root.
        # A .git file is a boundary too. Prune before visiting their descendants.
        children[:] = [name for name in children
                       if name not in {".git", "templates"}
                       and not (directory / name).is_symlink()
                       and not (directory / name / ".git").exists()]
        if any(name in files for name in INSTRUCTION_FILENAMES):
            dirs.add(directory)
    if not dirs:
        return

    def applicable(d: Path) -> Path | None:
        return next((d / n for n in INSTRUCTION_FILENAMES if (d / n).is_file()), None)

    # A chain is one applicable file per directory level along a single root-to-cwd path.
    # Sibling directories are never in the same chain, so summing every file in the
    # repository invents a total no session ever sees. Measure the worst real path instead.
    sizes = {d: f.stat().st_size for d in dirs if (f := applicable(d)) is not None}
    worst, chain = 0, []
    for d in sizes:
        path = [a for a in (d, *d.parents)
                if a in sizes and (a == repo or repo in a.parents)]
        total = sum(sizes[a] for a in path)
        if total > worst:
            worst, chain = total, sorted(path, key=lambda a: len(a.parts))

    detail = f"{worst:,} B"
    if len(chain) > 1:
        detail += (" — deepest chain: "
                   + " + ".join(applicable(a).relative_to(repo).as_posix() for a in chain))

    if worst > MAX_INSTRUCTION_BYTES:
        r.add(FAIL, "AGENTS.md size",
              f"{detail} exceeds the {MAX_INSTRUCTION_BYTES:,} B default chain budget"
              " — Codex stops adding files at that point, so content is dropped")
    elif worst > WARN_AT:
        r.add(WARN, "AGENTS.md size",
              f"{detail} — every byte bills on every session; consider promoting rules to checks")
    else:
        r.add(OK, "AGENTS.md size", detail)


def check_empty_sections(repo: Path, r: Report) -> None:
    """A heading with nothing under it is cost with no return."""
    f = repo / "AGENTS.md"
    if not f.is_file():
        return
    # Strip HTML comments first. Checking only for a leading "<!--" catches the opening line
    # of a block and counts its body as content — which let the shipped scaffold, with every
    # section still empty, pass as "none empty".
    text = re.sub(r"<!--.*?-->", "", f.read_text(encoding="utf-8"), flags=re.S)
    lines = text.splitlines()
    heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
    empty = [
        lines[i][3:].strip() for n, i in enumerate(heads)
        if not any(l.strip()
                   for l in lines[i + 1:heads[n + 1] if n + 1 < len(heads) else len(lines)])
    ]
    if empty:
        r.add(WARN, "AGENTS.md sections", f"empty: {', '.join(empty)} — delete them")
    else:
        r.add(OK, "AGENTS.md sections", "none empty")


def check_names(repo: Path, r: Report) -> None:
    """A skill named like a built-in collides with it. Three vendors, three states:
    Claude Code replaces the bundled skill silently, Codex shows both entries unmerged, and
    Antigravity documents the shared slash namespace without documenting resolution. One project
    prefix prevents all three."""
    names: set[str] = set()
    for d in SKILL_DIRS:
        p = repo / d
        if p.is_dir():
            names |= {s.name.lower() for s in p.iterdir() if s.is_dir()}

    # Claude Code writes these itself: `/verify` records what worked to
    # `.claude/skills/verify/`, and `/run-skill-generator` writes `run-<name>/`. In both cases
    # replacing the bundled skill is the documented, intended outcome. Failing them would fail
    # the vendor's own workflow — and GUIDE.md stage 6 tells people to run it.
    generated = sorted(n for n in names
                       if n == "verify" or n.startswith("run-"))
    claude = sorted(names & RESERVED_CLAUDE - set(generated))
    codex = sorted((names & RESERVED_CODEX) - RESERVED_CLAUDE - set(generated))
    antigravity = sorted(
        (names & RESERVED_ANTIGRAVITY) - RESERVED_CLAUDE - RESERVED_CODEX - set(generated)
    )

    if claude:
        r.add(FAIL, "skill names",
              f"collide with Claude Code built-ins and SILENTLY replace them: "
              f"{', '.join(claude)} — add a project prefix")
    if generated:
        r.add(OK, "generated skills",
              f"{', '.join(generated)} — replaces a bundled skill by design"
              " (written by /verify or /run-skill-generator)")
    if codex:
        r.add(WARN, "skill names",
              f"collide with Codex built-ins: {', '.join(codex)}"
              " — Codex shows both entries unmerged, so which one runs is a coin flip")
    if antigravity:
        r.add(WARN, "skill names",
              f"collide with Antigravity commands or built-in Skills: {', '.join(antigravity)}"
              " — same-name resolution is undocumented; add a project prefix")
    if not claude and not codex and not antigravity:
        r.add(OK, "skill names", "no collisions with known built-in or public command names")


def tree_hash(root: Path) -> str:
    """Hash relative paths and content, normalizing CRLF in UTF-8 text only.

    An adopting repo may use core.autocrlf without our .gitattributes. A Git checkout must
    not invalidate the ownership baseline solely by converting text line endings. Binary
    content (NUL-containing or non-UTF-8) remains byte-exact. Follows skill symlinks.
    """
    h = hashlib.sha256()
    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(f.relative_to(root).as_posix().encode())
        h.update(b"\0")
        content = f.read_bytes()
        if b"\0" not in content:
            try:
                content.decode("utf-8")
            except UnicodeDecodeError:
                pass
            else:
                content = content.replace(b"\r\n", b"\n")
        h.update(content)
        h.update(b"\0")
    return h.hexdigest()


def read_manifest(repo: Path) -> dict | None:
    """Read explicit installer ownership; never infer it from a prefix or a directory union."""
    path = repo / MANIFEST
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if (not isinstance(data, dict) or data.get("schema_version") != 1
                or not isinstance(data.get("skills"), dict)):
            raise ValueError("expected schema_version 1 and a skills object")
        for name, entry in data["skills"].items():
            if not re.fullmatch(r"hr-[a-z0-9]+(?:-[a-z0-9]+)*", name):
                raise ValueError("invalid managed skill name")
            if not isinstance(entry, dict):
                raise ValueError(f"invalid entry for {name}")
            paths = entry.get("paths")
            if (not isinstance(paths, list) or not paths
                    or any(not isinstance(p, str) or p not in SKILL_DIRS for p in paths)
                    or len(paths) != len(set(paths))):
                raise ValueError(f"invalid paths for {name}")
            digest = entry.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise ValueError(f"invalid sha256 for {name}")
        return data
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError(f"{MANIFEST}: {exc}") from exc


def check_sync(repo: Path, r: Report) -> None:
    """Check only recorded installs, including absent roots and equally modified copies.

    Without a manifest ownership is unknown. Do not adopt user skills automatically; require
    the installer to establish a baseline. Other checks still inspect local names/frontmatter.
    """
    try:
        manifest = read_manifest(repo)
    except ValueError as exc:
        r.add(FAIL, "skill sync", str(exc))
        return
    if manifest is None:
        ambiguous = sorted(f"{rel}/{name}" for rel in SKILL_DIRS
                           for name in SHIPPED_SKILL_NAMES
                           if (repo / rel / name).exists() or (repo / rel / name).is_symlink())
        if ambiguous:
            r.add(FAIL, "skill sync",
                  "ownership unknown for shipped-name paths: " + ", ".join(ambiguous)
                  + " — inspect them, then run install.py with the intended --agents selection;"
                  " this does not claim ownership of user content")
        else:
            r.add(WARN, "skill sync",
                  "ownership unknown; no shipped-name paths found — user skills are not"
                  " compared across locations")
        return
    problems: list[str] = []
    copies = 0
    for name, entry in sorted(manifest["skills"].items()):
        for rel in entry["paths"]:
            path = repo / rel / name
            copies += 1
            if not (path / "SKILL.md").is_file():
                problems.append(f"{rel}/{name} missing SKILL.md")
            elif tree_hash(path) != entry["sha256"]:
                problems.append(f"{rel}/{name} differs from installed source")
    if problems:
        r.add(FAIL, "skill sync", " / ".join(problems)
              + " — inspect differences and run install.py --check before repairing")
    else:
        r.add(OK, "skill sync",
              f"{copies} managed copy/copies match installed source; foreign skills excluded")


def content_hash(content: bytes) -> str:
    """Normalize text checkout conversion; retain binary bytes."""
    if b"\0" not in content:
        try:
            content.decode("utf-8")
        except UnicodeDecodeError:
            pass
        else:
            content = content.replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


def asset_path(repo: Path, rel: str) -> Path:
    """Only known local asset files; never traverse a symlink in their ancestry."""
    if rel not in ASSET_PATHS | {ASSET_MANIFEST}:
        raise ValueError(f"invalid asset path: {rel}")
    path = repo / rel
    # Also catches Windows junctions, which need not be reported as symlinks.
    if not path.resolve().is_relative_to(repo.resolve()):
        raise ValueError(f"asset escapes repository: {rel}")
    current = repo
    for part in Path(rel).parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"symlink asset path: {rel}")
        if current != path and current.exists() and not current.is_dir():
            raise ValueError(f"non-directory asset parent: {current}")
    return path


def read_assets(repo: Path) -> dict:
    path = asset_path(repo, ASSET_MANIFEST)
    if not path.exists():
        return {"schema_version": 1, "files": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if (not isinstance(data, dict) or data.get("schema_version") != 1
                or not isinstance(data.get("files"), dict)):
            raise ValueError("expected schema_version 1 and files object")
        for rel, digest in data["files"].items():
            if rel not in ASSET_PATHS:
                raise ValueError(f"invalid managed asset: {rel}")
            asset_path(repo, rel)
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise ValueError(f"invalid digest for {rel}")
        return data
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError(f"{ASSET_MANIFEST}: {exc}") from exc


def check_assets(repo: Path, r: Report) -> None:
    try:
        manifest = read_assets(repo)
        problems = []
        for rel, digest in manifest["files"].items():
            path = asset_path(repo, rel)
            if not path.is_file() or content_hash(path.read_bytes()) != digest:
                problems.append(f"{rel} missing or modified")
        if problems:
            r.add(FAIL, "work assets", " / ".join(problems)
                  + " — preserve edits; reconcile with the installer before updating")
        elif manifest["files"]:
            r.add(OK, "work assets", f"{len(manifest['files'])} managed file(s) intact")
        elif (repo / "HOUSERULES.md").exists():
            r.add(WARN, "work assets", "ownership unknown; HOUSERULES.md is not enrolled")
    except (OSError, ValueError) as exc:
        r.add(FAIL, "work assets", str(exc))


def check_frontmatter(repo: Path, r: Report) -> None:
    """description is the trigger condition an agent matches on. Without it the skill
    is invisible to implicit invocation."""
    bad: list[str] = []
    seen: set[Path] = set()
    for d in SKILL_DIRS:
        p = repo / d
        if not p.is_dir():
            continue
        for s in p.iterdir():
            f = s / "SKILL.md"
            if not f.is_file() or f.resolve() in seen:
                continue
            seen.add(f.resolve())
            head = f.read_text(encoding="utf-8")[:2000]
            if not re.search(r"^---\s*$.*?^description:\s*\S", head, re.S | re.M):
                bad.append(f"{d}/{s.name}")
    if bad:
        r.add(FAIL, "skill frontmatter",
              f"no description field: {', '.join(bad)} — the agent cannot know when to use it")
    elif seen:
        r.add(OK, "skill frontmatter",
              f"{len(seen)} file(s) carry a description")
    else:
        r.add(OK, "skill frontmatter", "no skills present")


def check_reserved_drift(repo: Path, r: Report) -> None:
    """Guard the reserved-name sets against drifting from this repo's own inventories.

    RESERVED_CLAUDE is a lower bound transcribed by hand from the published commands reference,
    plus names found on other documentation pages. Two failure modes follow, and a review caught
    both: a name documented in `docs/agents/claude-code.md` can be missing from the set, and a name
    in the inventory can lack a source.

    `/rename` is the cautionary case. It is documented on the sessions page, and a first pass that
    searched only the commands reference concluded it did not exist. **The commands reference is
    the biggest enumerable list, not the whole surface** — a command lives wherever its feature is
    documented, and re-running the same search does not widen its scope.

    So this compares the two and WARNS rather than failing. A warning is correct here because the
    inventory is prose: it quotes other agents' commands, MCP prompt forms and shell examples, and
    a mismatch means "one of these two needs a look", not "the repository is broken".

    KNOWN LIMIT, and it is inherent rather than an oversight: this is a ONE-WAY check. It catches
    inventory names missing from the set. It cannot catch a command missing from BOTH, because
    nothing local knows the vendor's full list — and check.py is deliberately offline, standard
    library only, and shipped into other repositories. Closing that direction needs a fetch, which
    would make the check unrunnable in CI without network and is the wrong trade. Re-read the
    commands reference on the `recheck_by` date instead; research/MATRIX.md carries it.

    Antigravity uses independent one-way comparisons for public commands and confirmed built-in
    Skills. They cannot promote that inventory from documented to tested; they only prevent the
    offline sets from omitting names the checked-in inventory already records.

    Skipped entirely outside this repository — check.py ships into repos that have no docs/agents/.
    """
    inventory = repo / "docs" / "agents" / "claude-code.md"
    if inventory.is_file():
        text = inventory.read_text(encoding="utf-8")
        # Only backticked `/name` tokens: prose mentions and MCP prompt forms are noise.
        # `hr-` is the mandatory prefix for project-supplied skills, not a vendor command.
        found = {m.lower() for m in re.findall(r"`/([a-z][a-z0-9-]{1,30})`", text)
                 if not m.lower().startswith("hr-")}
        missing = sorted(found - RESERVED_CLAUDE)
        if missing:
            r.add(WARN, "reserved-name drift",
                  f"documented in docs/agents/claude-code.md but not in RESERVED_CLAUDE: "
                  f"{', '.join(missing)} — add them, or fix the inventory if the name is not "
                  f"Claude Code's")
        else:
            r.add(OK, "reserved-name drift",
                  f"{len(found)} command-shaped name(s) in the inventory, all reserved"
                  " (one-way check — see the docstring)")

    antigravity_inventory = repo / "docs" / "agents" / "antigravity.md"
    if not antigravity_inventory.is_file():
        return
    antigravity_text = antigravity_inventory.read_text(encoding="utf-8")
    antigravity_commands = {
        m.lower()
        for m in re.findall(r"`/([a-z][a-z0-9-]{1,30})`", antigravity_text)
        if not m.lower().startswith("hr-")
    }
    missing_commands = sorted(antigravity_commands - RESERVED_ANTIGRAVITY_COMMANDS)
    if missing_commands:
        r.add(WARN, "Antigravity command drift",
              "documented in docs/agents/antigravity.md but not reserved as commands: "
              f"{', '.join(missing_commands)} — add them, or fix the inventory")
    else:
        r.add(OK, "Antigravity command drift",
              f"{len(antigravity_commands)} command-shaped name(s), all reserved"
              " (documentation-only, one-way check)")

    marker = "### Built-in skills"
    if marker not in antigravity_text:
        r.add(WARN, "Antigravity built-in-skill drift",
              f"missing inventory heading: {marker}")
        return

    skill_section = antigravity_text.split(marker, 1)[1].split("\n## ", 1)[0]
    documented_skills: set[str] = set()
    for line in skill_section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in {"Surface", "---"}:
            continue
        skill_cell = cells[1]
        identifiers = re.findall(r"`([^`]+)`", skill_cell)
        if identifiers:
            documented_skills.update(name.casefold() for name in identifiers)
        else:
            display_name = skill_cell.strip("* ").casefold()
            if display_name:
                documented_skills.add(display_name)

    if not documented_skills:
        r.add(WARN, "Antigravity built-in-skill drift",
              "built-in Skills heading exists but its table has no parsable Skill rows")
        return

    untracked_skills = sorted(
        documented_skills - DOCUMENTED_ANTIGRAVITY_BUILTIN_SKILLS
    )
    if untracked_skills:
        r.add(WARN, "Antigravity built-in-skill drift",
              "documented in the built-in Skills table but not catalogued: "
              f"{', '.join(untracked_skills)}")
    else:
        r.add(OK, "Antigravity built-in-skill drift",
              f"{len(documented_skills)} table Skill name(s), all catalogued"
              " (documentation-only, one-way check)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--fix", action="store_true", help="repair what is safely repairable")
    a = ap.parse_args()

    repo = Path(a.repo).resolve()
    if not repo.is_dir():
        print(f"error: {repo} is not a directory", file=sys.stderr)
        return 2

    r = Report()
    check_import(repo, r, a.fix)
    check_size(repo, r)
    check_empty_sections(repo, r)
    check_names(repo, r)
    check_sync(repo, r)
    check_assets(repo, r)
    check_frontmatter(repo, r)
    check_reserved_drift(repo, r)

    print(f"portable agent layer — {repo}\n")
    r.render()
    print()
    if r.failed:
        print("FAILED. Each failure above is a silent one: nothing else would have told you.")
        return 1
    print("passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
