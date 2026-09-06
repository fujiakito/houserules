# Agent inventories

One file per agent. What it ships with, what you have to install, and how to check on your own
machine.

## Choosing from an inventory

This is a reference for people comparing capabilities or adding agent support. [GUIDE.md](../GUIDE.md)
helps locate the stage; the relevant inventory supplies the details. These files are not installed
or automatically loaded as agent instructions.

| Question | Useful evidence |
|---|---|
| Which operation and artifact are involved? | The current task and its [work artifact](../../templates/work/README.md), when present |
| Does this option fit the active surface? | Agent, surface, version, capability section and known traps |
| Is it actually available here? | Installed/enabled/model-visible state, checked with the inventory's enumeration procedure; inaccessible state remains `unknown` |
| How do overlapping skills differ? | Actual source, trigger, outputs, dependencies and authority; similar names alone do not establish equivalence |
| Can the user's preferred skill do the job? | Required outputs/evidence and remaining gaps; project/global/plugin visibility may be incomplete |

An existing user skill can remain the selected implementation when it meets the contract. Comparing
options does not require replacing or disabling it. An agent asked to make this comparison can be
given the relevant inventory explicitly; no routing skill or automatic trigger is implied.

## Why one file per agent, and not one big table

The stage guide in `../GUIDE.md` answers *"at this stage, what do I use?"* — it needs every agent
side by side, so it puts **one row per agent** and grows downward. These files answer the other
question, *"what does this agent actually have?"*, which is reference data and belongs to one agent
at a time.

> **Adding an agent adds a file. It must never widen a table.**

Complete the change across the inventory, every GUIDE stage/concern table and MATRIX before
calling the agent mapped. Record surface, built-in versus installable status, source/date and
remaining runtime checks. `tests/test_documentation.py` guards GUIDE coverage; it cannot verify
vendor claims. See the [documentation map](../README.md) for the other consumers.

A column per agent stops being readable at about four. A row, or a file, does not. That rule is the
whole reason for this directory.

## The files

| | |
|---|---|
| [`claude-code.md`](claude-code.md) | Claude Code — CLI, desktop, mobile, IDE, web, SDK, Chrome |
| [`codex.md`](codex.md) | Codex — CLI, desktop app, IDE extension, cloud, mobile/Remote |
| [`antigravity.md`](antigravity.md) | Google Antigravity — four core products plus Remote Control, managed API and Enterprise; documentation inventory with installed 2.0/IDE presence, no capability execution |
| [`cursor.md`](cursor.md) | Cursor — IDE/CLI/cloud; documented capabilities, measured IDE launcher and Python installer acceptance |
| [`kiro.md`](kiro.md) | Kiro — IDE/CLI/Web/Mobile; documented capabilities, measured IDE launcher and unresolved custom-resource inheritance |
| [`_TEMPLATE.md`](_TEMPLATE.md) | copy this to add an agent |

**These five are the canonical inventories for this project.** Everything established about an
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

Cursor and Kiro have documentation inventories as of 2026-09-06. Their local version and installer
checks do not establish native discovery or execution; see the shared
[acceptance record](../../tests/workflows/cursor-kiro/README.md).

Not yet written: Copilot, Goose, OpenCode. They remain surveyed in
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
| **Cursor** | documented native review and extension-authoring skills | plugins, user/project skills and MCP; [dated inventory](cursor.md) |
| **Kiro** | Default/Plan agents and Specs, not relabeled as skills | Powers, user/project skills and MCP; [dated inventory](kiro.md) |
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
