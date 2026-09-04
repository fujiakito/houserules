# houserules

**A portable agent layer for a repository — the part that does not ship with your agent, and does not
die when you switch.**

Most of the software lifecycle is already built into modern coding agents: planning, parallel
implementation, verification, review, security scanning, maintenance. That is why this is small. It
carries only the two things a vendor cannot give you:

1. **What is true about *this* repository** — the non-obvious rules an agent cannot read off the code
2. **What survives an agent switch** — because most mature adopters run more than one agent, and a
   sizeable share have already dropped one *(figures from an unpublished prior scan; see
   `research/PORTABILITY.md` §0)*

The name is what an entry has to answer before it goes in: **does this earn its place?**

> **Supported today: Claude Code and Codex.** Those are the two run against real installations,
> with versions recorded. Six more agents — Cursor, Copilot, Kiro, Antigravity, Goose, OpenCode —
> are covered from **official documentation only** and have never been executed here. `install.py`
> writes their skill directories, and that placement is unverified in practice. See the evidence
> grades in `research/MATRIX.md`.

---

## Install

**Requires Python 3.9+ and nothing else** — both scripts are standard library only, on purpose. A
check that needs an install step is a check that gets skipped.

Run these from *this* repository, pointing at the repository you are adopting it into:

```bash
python install.py --repo /path/to/your-project --check
```

`--check` writes nothing. It prints exactly what would change and **exits non-zero if anything is
missing or has drifted** — so on a repository that has never been installed into, it exits 1 and
lists what it would create. "Nothing to do" is the only green state, which is what makes it usable
in CI. Read that output, then:

```bash
python install.py --repo /path/to/your-project
python check.py --repo /path/to/your-project
```

Omit `--repo` to act on the current directory. **Do not copy these files in by hand** — the
installer is what avoids overwriting an `AGENTS.md`, a `CLAUDE.md` or a skill you already have.

Then, inside your agent — `/hr-onboard` on Claude Code, **`$hr-onboard` on Codex**, which uses `$`
for skills and `/` for session commands.

<details>
<summary><b>If <code>python</code> is not found</b></summary>

On Windows, the launcher is usually installed even when `python` is not on `PATH`:

```bash
py install.py --repo /path/to/your-project --check
```

Otherwise use the full path to your interpreter, or the one bundled with your editor. On macOS and
Linux, `python3` may be the name.
</details>

<details>
<summary><b>To remove it</b></summary>

There is no uninstaller, because there is nothing to unwind: delete `AGENTS.md`, the `@AGENTS.md`
line from `CLAUDE.md`, `check.py`, and the `hr-onboard` directory under each agent's skills path.
Everything this installs is a plain file.
</details>

## What it installs

| | |
|---|---|
| `AGENTS.md` | read natively by every surveyed agent **except Claude Code**. Verified by running Codex and Claude Code; the rest from official documentation, retrieved 2026-09-01 |
| `CLAUDE.md` containing `@AGENTS.md` | **required, not an adapter.** Without it Claude Code ignores `AGENTS.md` and raises no error |
| `hr-onboard` skill, in every agent's path | the `SKILL.md` format is portable; the location is not. **`.agents/skills/` is now the majority path** — six of eight vendors document support; only Claude Code and Kiro need their own. Three directories cover all eight on paper |
| `check.py` | the only portable enforcement: a script with an exit code binds regardless of which agent, or human, made the change |

## What it deliberately does not install

Hooks, subagent definitions, plugins, recipes — all per-vendor formats — and **anything that
duplicates a built-in**. `/init`, `/verify`, `/code-review`, `/doctor` already exist and are better
integrated than a reimplementation would be. Rebuilding them is the mistake the surveyed frameworks
made: measured adoption of every AI-native SDLC framework checked was essentially zero.

## The rule everything follows

> A capability that must survive an agent switch can be expressed as exactly three things:
> **text in `AGENTS.md`**, **an MCP server**, or **a CI check**.
>
> Everything else is vendor-local convenience. Use it. Do not depend on it.

## Files

```
docs/GUIDE.md              the AI-native SDLC: 12 stages + 3 cross-cutting concerns — for you
docs/agents/claude-code.md the full Claude Code inventory: surfaces, bundled skills, subagents,
                           hooks, permission modes, artifacts, scheduling, plugins, limits
docs/agents/codex.md       the full Codex inventory: surfaces, commands, built-in skills,
                           marketplaces, AGENTS.md rules, hooks, config defaults, traps
research/MATRIX.md         8 agents x 6 extension mechanisms, with check dates and a revision log
research/PORTABILITY.md    what dies on a switch, and what the portable layer must therefore carry
templates/AGENTS.md        mostly empty, with the inclusion test that keeps it that way
templates/CLAUDE.md        the required import line
templates/work/            cross-session, cross-agent wire format — handoff.md, findings.md
templates/skills/          hr-onboard — discovery by attempting, not by scanning
install.py                 one source of truth into every agent's path
check.py                   guards six failures that are otherwise silent
```

## Evidence

Claims here carry a source and a date, or are tagged `(unverified)`. Where a claim is testable
locally it is **tested, not cited** — vendor documentation and secondary write-ups in this field
contradict each other often enough that a citation is not evidence.

Two examples, both settled by running them rather than reading about them:

- Claude Code v2.1.251 does not read `AGENTS.md`; with both files present and no import, it is
  ignored **silently**
- A skill in `.agents/skills/` is invisible to Claude Code while the same skill in `.claude/skills/`
  is found

The platform surfaces this describes change monthly. `research/MATRIX.md` carries a `recheck_by`
date, and the local tests take minutes.
