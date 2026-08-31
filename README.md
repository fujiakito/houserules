# houserules

**A portable agent layer for a repository — the part that does not ship with your agent, and does not
die when you switch.**

Most of the software lifecycle is already built into modern coding agents: planning, parallel
implementation, verification, review, security scanning, maintenance. That is why this is small. It
carries only the two things a vendor cannot give you:

1. **What is true about *this* repository** — the non-obvious rules an agent cannot read off the code
2. **What survives an agent switch** — because 79% of mature adopters run two or more agents, and 31%
   have already dropped one

The name is what an entry has to answer before it goes in: **does this earn its place?**

---

## Install

```bash
python install.py --check     # report what would change
python install.py             # install
python check.py               # verify the layer is intact
```

Then, inside your agent:

```
/hr-onboard
```

## What it installs

| | |
|---|---|
| `AGENTS.md` | read natively by Codex, Cursor, Copilot, Kiro, Antigravity, OpenCode — **every surveyed agent except Claude Code** |
| `CLAUDE.md` containing `@AGENTS.md` | **required, not an adapter.** Without it Claude Code ignores `AGENTS.md` and raises no error |
| `hr-onboard` skill, in every agent's path | the `SKILL.md` format is portable; the location is not — seven agents, four different directories |
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
docs/GUIDE.md              which built-in at which stage, and what to do without it — for you
research/MATRIX.md         7 agents x 6 extension mechanisms, with check dates and a recheck policy
research/PORTABILITY.md    what dies on a switch, and what the portable layer must therefore carry
templates/AGENTS.md        mostly empty, with the inclusion test that keeps it that way
templates/CLAUDE.md        the required import line
templates/work/            cross-session, cross-agent wire format — handoff.md, findings.md
templates/skills/          hr-onboard — discovery by attempting, not by scanning
install.py                 one source of truth into five vendor paths
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
