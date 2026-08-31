#!/usr/bin/env python3
"""Verify the portable agent layer is intact. Exit 0 = pass, 1 = fail, 2 = usage error.

Every check here guards a failure that is **silent** — the repository looks fine, agents
behave differently, and nothing raises an error. That is why they belong in CI rather than
in an instruction telling an agent to remember.

    python check.py            run every check
    python check.py --fix      repair what is safely repairable, then re-check

Run it in CI. A hook is a fine accelerator, but the check is the contract: it binds
regardless of which agent — or which human — made the change, and it validates state
rather than trusting anyone's claim that something was done.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

# Codex truncates instruction files beyond this. The tightest documented limit found,
# so it is the one to design against. research/MATRIX.md section 1.
MAX_INSTRUCTION_BYTES = 32 * 1024
WARN_AT = 8 * 1024  # long before the hard limit, brevity is the point

IMPORT_LINE = "@AGENTS.md"

# Skill directory names that collide with a built-in. A collision is silent: Claude Code
# replaces the bundled skill and never warns. research/MATRIX.md section 9.
# Lower bound — it grows with each release, which is why the rule is "prefix", not "blocklist".
RESERVED = {
    "code-review", "review", "security-review", "simplify", "init", "run", "verify",
    "run-skill-generator", "doctor", "checkup", "debug", "batch", "loop", "proactive",
    "schedule", "deep-research", "claude-api", "update-config", "keybindings-help",
    "fewer-permission-prompts", "workflow-authoring", "design", "dataviz",
    "artifact-design", "artifact-diagramming", "artifact-capabilities",
    "plan", "memory", "clear", "reset", "new", "resume", "branch", "fork", "context",
    "compact", "model", "effort", "advisor", "tasks", "background", "bg", "subtask",
    "permissions", "allowed-tools", "mcp", "config", "settings", "usage", "cost",
    "status", "copy", "export", "rewind", "diff", "feedback", "bug", "help", "goal", "exec",
}

SKILL_DIRS = [".claude/skills", ".agents/skills", ".cursor/skills",
              ".kiro/skills", ".opencode/skills"]

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
    """CLAUDE.md must import AGENTS.md, or Claude Code ignores it and says nothing."""
    agents, claude = repo / "AGENTS.md", repo / "CLAUDE.md"
    if not agents.is_file():
        r.add(WARN, "AGENTS.md", "absent — nothing portable to carry")
        return
    if not claude.is_file():
        if fix:
            claude.write_text(IMPORT_LINE + "\n", encoding="utf-8")
            r.add(OK, "CLAUDE.md import", "created")
        else:
            r.add(FAIL, "CLAUDE.md import",
                  "CLAUDE.md missing — Claude Code reads nothing here (--fix creates it)")
        return
    if IMPORT_LINE in claude.read_text(encoding="utf-8"):
        r.add(OK, "CLAUDE.md import", "present")
    elif fix:
        claude.write_text(IMPORT_LINE + "\n\n" + claude.read_text(encoding="utf-8"),
                          encoding="utf-8")
        r.add(OK, "CLAUDE.md import", "prepended")
    else:
        r.add(FAIL, "CLAUDE.md import",
              f"'{IMPORT_LINE}' missing — Claude Code is SILENTLY ignoring AGENTS.md")


def check_size(repo: Path, r: Report) -> None:
    f = repo / "AGENTS.md"
    if not f.is_file():
        return
    n = f.stat().st_size
    if n > MAX_INSTRUCTION_BYTES:
        r.add(FAIL, "AGENTS.md size",
              f"{n:,} B exceeds the {MAX_INSTRUCTION_BYTES:,} B limit — Codex truncates it")
    elif n > WARN_AT:
        r.add(WARN, "AGENTS.md size",
              f"{n:,} B — every byte bills on every session; consider promoting rules to checks")
    else:
        r.add(OK, "AGENTS.md size", f"{n:,} B")


def check_empty_sections(repo: Path, r: Report) -> None:
    """A heading with nothing under it is cost with no return."""
    f = repo / "AGENTS.md"
    if not f.is_file():
        return
    lines = f.read_text(encoding="utf-8").splitlines()
    heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
    empty = [
        lines[i][3:].strip() for n, i in enumerate(heads)
        if not any(l.strip() and not l.strip().startswith("<!--")
                   for l in lines[i + 1:heads[n + 1] if n + 1 < len(heads) else len(lines)])
    ]
    if empty:
        r.add(WARN, "AGENTS.md sections", f"empty: {', '.join(empty)} — delete them")
    else:
        r.add(OK, "AGENTS.md sections", "none empty")


def check_names(repo: Path, r: Report) -> None:
    """A skill named like a built-in silently replaces it."""
    hits: set[str] = set()
    for d in SKILL_DIRS:
        p = repo / d
        if p.is_dir():
            hits |= {s.name for s in p.iterdir()
                     if s.is_dir() and s.name.lower() in RESERVED}
    if hits:
        r.add(FAIL, "skill names",
              f"collide with built-ins and SILENTLY replace them: {', '.join(sorted(hits))}"
              " — add a project prefix")
    else:
        r.add(OK, "skill names", "no collisions with known built-ins")


def tree_hash(root: Path) -> str:
    """Content hash of a directory — relative paths and file bytes, order-independent.
    Follows symlinks, so install.py --link and a plain copy hash identically."""
    h = hashlib.sha256()
    for f in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(f.relative_to(root).as_posix().encode())
        h.update(b"\0")
        h.update(f.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def check_sync(repo: Path, r: Report) -> None:
    """Skills drift two ways and both are silent: a location is missing a skill entirely,
    or it holds a *different version* of one. Comparing directory names catches only the
    first. The second is what a repository gets when it already had a skill of that name:
    install.py refuses to overwrite it, installs into the other vendor paths, and the repo
    is left with two different skills under one name — one agent reading each."""
    present = {d: {s.name for s in (repo / d).iterdir() if s.is_dir()}
               for d in SKILL_DIRS if (repo / d).is_dir()}
    if len(present) < 2:
        r.add(OK, "skill sync", "fewer than two skill locations in use")
        return
    union = set().union(*present.values())

    problems: list[str] = []
    drifted = {d: sorted(union - names) for d, names in present.items() if union - names}
    if drifted:
        problems.append("; ".join(f"{d} missing {', '.join(m)}" for d, m in drifted.items()))

    # Group the locations holding each skill by content. More than one group is a version split.
    for name in sorted(union):
        by_hash: dict[str, list[str]] = {}
        for d, names in present.items():
            if name in names:
                by_hash.setdefault(tree_hash(repo / d / name), []).append(d)
        if len(by_hash) > 1:
            groups = " vs ".join("+".join(v) for v in by_hash.values())
            problems.append(f"{name} differs between locations: {groups}")

    if problems:
        r.add(FAIL, "skill sync", " / ".join(problems) + " — re-run install.py --force")
    else:
        r.add(OK, "skill sync",
              f"{len(union)} skill(s) identical across {len(present)} location(s)")


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
        r.add(OK, "skill frontmatter", f"{len(seen)} skill file(s) carry a description")
    else:
        r.add(OK, "skill frontmatter", "no skills present")


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
    check_frontmatter(repo, r)

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
