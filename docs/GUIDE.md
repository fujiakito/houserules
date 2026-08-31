# Working guide

Which built-in to reach for at each stage, and what to do when your agent does not have it.

**This file is for you, not for an agent.** It lives outside the instruction layer deliberately —
nothing here is loaded into a session, so it can be as long as it needs to be. Anything an agent must
act on belongs in `AGENTS.md`, a skill, or a check, expressed as a *trigger*, not as prose.

Commands below are Claude Code unless noted. **Checked 2026-08-31**; see the recheck policy in
`research/MATRIX.md` — these move.

---

## The starting position

**Most of the lifecycle already ships.** That is why the portable layer this repository installs is
small: it carries only what does *not* ship, and what does not survive an agent switch.

The mistake the surveyed frameworks made was rebuilding, as markdown scaffolding, what agents ship as
executable commands. Do not do that.

---

## 1. Onboard a repository

| | |
|---|---|
| **Built-in** | `/init` — writes a starting `CLAUDE.md`. `CLAUDE_CODE_NEW_INIT=1` gives an interactive flow covering skills, hooks and memory |
| **This repo adds** | `/hr-onboard` — finds the **non-discoverable** knowledge by attempting work and recording the friction, rather than by scanning and describing |
| **Why both** | `/init` produces a description. `hr-onboard` produces the things a description cannot contain: the command that only works from a subdirectory, the test that is meant to fail |

```
/hr-onboard
```

Then `python install.py` to place skills in every agent's path, and `python check.py` to confirm the
layer is intact.

## 2. Plan

| | |
|---|---|
| **Built-in** | `/plan` — plan mode. Codex: `/goal` sets a persistent objective it works toward until verified |
| **When** | Anything you cannot hold in your head, and anything you would regret half-done |
| **Portable?** | No. If the plan must survive the session, write it to `work/<id>/` — see `templates/work/` |

A plan that lives only in a session dies with it. If a different session or a different agent will
pick this up, the plan is a handoff artifact, not a mode — see `templates/work/`.

**Also here:** `/deep-research` fans out web searches, cross-checks sources and returns a cited
report. Worth reaching for before a design decision that rests on how something outside the
repository actually behaves — which, in this field, is usually contested.

## 3. Build

| | |
|---|---|
| **Built-in** | `/batch` — decomposes into 5–30 units and runs subagents in isolated git worktrees, implementing, testing and opening PRs. `/subtask`, `/background` for smaller splits |
| **When** | `/batch` for a mechanical change across many files. `/subtask` for one bounded side quest |
| **Portable?** | No. Codex has its own subagent model (`.codex/agents/*.toml`, `max_threads`, sandbox modes) |

Worktree isolation is the part that matters — parallel agents editing one tree produces conflicts
that cost more than the parallelism saves.

**When something misbehaves at runtime rather than in the tests:** `/debug` turns on debug logging
and works the problem. Describe the symptom to focus it.

**If you are orchestrating several agents through stages** — the pipeline case this repository's
`work/` contract exists for — `/workflow-authoring` writes the orchestration. Available only when
dynamic workflows are enabled.

## 4. Verify

| | |
|---|---|
| **Built-in** | `/verify` — builds and runs the app to confirm a change does what it should, **without falling back to tests or type checks**. `/run` launches it. `/run-skill-generator` records the recipe once so every later run and every other agent follows it |
| **When** | Any change whose failure mode the test suite would not catch — most UI, most startup paths, most integration |
| **Portable?** | The command is not. **The recorded recipe is** — it lands in the repository as a skill, and `install.py` copies it to every agent's path |

This is the highest-value pairing in the whole set. Run `/run-skill-generator` once per project; after
that the launch procedure is repository knowledge instead of something each agent rediscovers.

```
/run-skill-generator
```

## 5. Review

| | |
|---|---|
| **Built-in** | `/code-review` — diff, branch, PR or path. Effort `low\|medium\|high\|xhigh\|max\|ultra`; `--fix` applies findings, `--comment` posts them to the PR. `/security-review` for vulnerabilities. `/simplify` for a cleanup-only pass. Codex has its own `review` |
| **When** | `/code-review` before every PR; `/security-review` before anything that touches auth, input handling or deploys |
| **Portable?** | No — and this is the case where the distinction bites |

**A review command is advisory and vendor-local. A CI check binds and is universal.** Use the review
to *find* things; move anything that must never slip into `check.py` or your test suite. The rule that
follows from this — validate state, never trust a claim that a check ran — is why `check.py` exists.

```
/code-review high
/security-review
```

## 6. Commit and ship

| | |
|---|---|
| **Built-in** | Nothing opinionated, and that is fine |
| **This repo adds** | `python check.py` — guards the six silent failures of the portable layer. Pair it with `python install.py --check`, which exits non-zero when an installed copy has drifted from its source |
| **Portable?** | ✅ Yes. It is a script with an exit code, so it binds regardless of who or what made the change |

Wire it into CI. Optionally mirror it as a pre-commit hook for faster feedback — but **if the hook and
the check disagree, the check wins**, because the check is what a reviewer and a different agent both
see.

## 7. Maintain

| | |
|---|---|
| **Built-in** | `/doctor` — installation health, unused skills and MCP servers, slow hooks, **deduplicates and trims `CLAUDE.md`, and migrates guidance into skills**. `/loop` and `/schedule` for recurring work. `/usage`, `/cost`, `/context` for what it is costing |
| **When** | `/doctor` every few weeks, and any time the instruction file has grown |

`/doctor` already performs the maintenance move this layer cares about: **guidance that has become a
procedure should leave the always-loaded file and become an on-demand skill.** Let it.

**Two more worth knowing:**

- **`/fewer-permission-prompts`** scans your transcripts for read-only commands you keep approving
  and writes an allowlist into `.claude/settings.json`. Reach for it when approvals are interrupting
  you — and note the failure it prevents. A permission mode that silently denies shell calls will
  stop an agent running your tests, and the agent will "verify" by reading code instead. Nothing
  raises an error. That is a real hazard, not a hypothetical.
- **`/claude-api cost-optimize`** profiles spend and suggests savings; **`prompt-audit`** flags
  instructions written for an older model. Both are relevant here because the instruction layer's
  cost is unconditional — over 20% more inference per session whether or not it helps.

---

## The three-tier rule

Everything above resolves into one decision. When you learn something about this repository, ask
where it belongs:

| Tier | Cost | Fires | Put here |
|---|---|---|---|
| **`AGENTS.md`** | **every session, every agent, everyone** | always | short, non-standard, non-obvious instructions |
| **A skill** | metadata always, body on match | the agent decides, from `description` | procedures and reference material |
| **A check** | on event | **cannot be skipped** | anything that must not be missed |

> **Push everything down as far as it will go: prose → skill → check.**

A rule enforced by CI does not need a sentence in `AGENTS.md`. Delete the sentence — it is costing you
on every session for a job something else is already doing.

## When *not* to reach for a built-in

| Situation | Do this instead |
|---|---|
| The team uses more than one agent | Whatever the built-in does for you, the knowledge belongs in `AGENTS.md` so the other agent has it too |
| The thing must never be skipped | A check, not a command. Commands need someone to type them |
| You keep typing the same prompt | A skill — with a project prefix, so it cannot silently replace a built-in |
| You are about to write a framework | Read `research/PORTABILITY.md` first. Four-plus projects have written it; adoption of every one of them measured at essentially zero |

## Naming

Prefix every skill this repository ships. A skill named `review` **silently replaces** Claude Code's
bundled `/code-review`, and its alias never reaches yours. Codex behaves differently again — both
appear, unmerged. `check.py` catches collisions against a known list, but the list is a lower bound;
the prefix is the actual protection.
