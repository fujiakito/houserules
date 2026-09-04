# Agent inventories

One file per agent. What it ships with, what you have to install, and how to check on your own
machine.

## Why one file per agent, and not one big table

The stage guide in `../GUIDE.md` answers *"at this stage, what do I use?"* — it needs every agent
side by side, so it puts **one row per agent** and grows downward. These files answer the other
question, *"what does this agent actually have?"*, which is reference data and belongs to one agent
at a time.

> **Adding an agent adds a file. It must never widen a table.**

A column per agent stops being readable at about four. A row, or a file, does not. That rule is the
whole reason for this directory.

## The files

| | |
|---|---|
| [`claude-code.md`](claude-code.md) | Claude Code — CLI, desktop, mobile, IDE, web, SDK, Chrome |
| [`codex.md`](codex.md) | Codex — CLI, desktop app, IDE extension, cloud, mobile/Remote |
| [`antigravity.md`](antigravity.md) | Google Antigravity — four core products plus Remote Control, managed API and Enterprise; documentation inventory with installed 2.0/IDE presence, no capability execution |
| [`_TEMPLATE.md`](_TEMPLATE.md) | copy this to add an agent |

**These three are the canonical inventories for this project.** Everything established about an
agent lives in its file — surfaces, built-ins, installables, extension points, limits, and the
traps. Nothing else in the repository duplicates them; `../GUIDE.md` links into them per stage and
`../../research/MATRIX.md` compares one mechanism at a time across all eight agents.

**Every file carries an evidence grade per claim** — `tested`, `documented` with a retrieval date, ⚠️
`disputed` where two official pages conflict, or `(unverified)`. The grades are not decoration: on
Codex, three enumerations that were `documented` turned out to disagree with the running build, and
the ⚠️ rows are cases nobody has settled yet.

Claude Code and Codex are `tested`; Antigravity is explicitly `documented`, not `tested`. Its
inventory exists because it records the official surface split, source-level conflicts, and the
exact local test still required — not because a documentation pass counts as support.

Not yet written: Cursor, Copilot, Kiro, Goose, OpenCode. They remain surveyed in
`../../research/MATRIX.md`. Before promoting one, either install and enumerate it or preserve the
same visible documentation-only boundary used by Antigravity.

## The two rules every file follows

**1. Separate what ships from what you install.** Vendors blur this, and each has its own word
for it:

| | ships with the agent | you install it |
|---|---|---|
| **Codex** | `System` | `Personal` |
| **Claude Code** | bare name — `code-review` | `plugin:skill` — `anthropic-skills:pdf` |
| **Antigravity** | lower bound: 2.0 **Antigravity Guide**; CLI `antigravity_guide`, `migrate-workflows` | enabled Google bundles and user plugins/skills |
| **this project** | **built-in** | **installable** |

"Agent X has a PDF skill" and "Agent X ships with a PDF skill" are different claims, and only the
second survives a fresh machine.

**2. Name the surface.** A vendor ships several — CLI, desktop app, IDE extension — and they do not
expose the same things. A local check measures the surface you ran it on and nothing else. Every
claim carries the surface and the version it was measured against.

## Every list here is a lower bound

No vendor here exposes a complete machine-readable inventory across every surface, all ship
frequently, and the built-in set varies by platform and version — Codex's own documentation and
this machine's `.system/` directory list *different* skills, and both are right. **Read a name's
absence as "not recorded yet", never as "not there".**

This is why `check.py` enforces a **prefix rule** rather than a blocklist. A blocklist has to be
complete to work. A prefix does not.
