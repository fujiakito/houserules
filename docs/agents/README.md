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
| [`_TEMPLATE.md`](_TEMPLATE.md) | copy this to add an agent |

**These two are the canonical inventories for this project.** Everything verified about either
agent lives in its file — surfaces, built-ins, installables, extension points, limits, and the
traps. Nothing else in the repository duplicates them; `../GUIDE.md` links into them per stage and
`../../research/MATRIX.md` compares one mechanism at a time across all eight agents.

**Both carry an evidence grade per claim** — `tested`, `documented` with a retrieval date, ⚠️
`disputed` where two official pages conflict, or `(unverified)`. The grades are not decoration: on
Codex, three enumerations that were `documented` turned out to disagree with the running build, and
the ⚠️ rows are cases nobody has settled yet.

Not yet written: Cursor, Copilot, Kiro, Antigravity, Goose, OpenCode. They are surveyed from
documentation only in `../../research/MATRIX.md`, where they are graded **`documented`** — sourced
and dated, but never run. **Writing an inventory from documentation alone would produce a file that
looks complete and was never checked**, which is exactly the failure these files exist to prevent.
Install the agent, run the enumeration step, then write the file.

## The two rules every file follows

**1. Separate what ships from what you install.** Both vendors blur this, and each has its own word
for it:

| | ships with the agent | you install it |
|---|---|---|
| **Codex** | `System` | `Personal` |
| **Claude Code** | bare name — `code-review` | `plugin:skill` — `anthropic-skills:pdf` |
| **this project** | **built-in** | **installable** |

"Agent X has a PDF skill" and "Agent X ships with a PDF skill" are different claims, and only the
second survives a fresh machine.

**2. Name the surface.** A vendor ships several — CLI, desktop app, IDE extension — and they do not
expose the same things. A local check measures the surface you ran it on and nothing else. Every
claim carries the surface and the version it was measured against.

## Every list here is a lower bound

Neither vendor exposes a complete machine-readable inventory, both ship monthly, and the built-in
set varies by platform and version — Codex's own documentation and this machine's `.system/`
directory list *different* skills, and both are right. **Read a name's absence as "not recorded
yet", never as "not there".**

This is why `check.py` enforces a **prefix rule** rather than a blocklist. A blocklist has to be
complete to work. A prefix does not.
