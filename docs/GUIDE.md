# The AI-native SDLC, by stage

Seven stages. For each: what every agent has, which is better for what, and what to do when yours
has nothing.

**This file is for you, not for an agent.** It lives outside the instruction layer deliberately —
nothing here is loaded into a session, so it can be as long as it needs to be. Anything an agent
must act on belongs in `AGENTS.md`, a skill, or a check, expressed as a *trigger*, not as prose.

**Full inventories live in [`agents/`](agents/)** — one file per agent, listing what ships versus
what you install. This file only answers "what do I use at this stage".

**Checked 2026-08-31** — Claude Code v2.1.251, codex-cli 0.151.0-alpha.7.2. Recheck policy in
`../research/MATRIX.md`; these move monthly.

### How to read the tables

| Type | Means |
|---|---|
| **built-in** | ships with the agent, nothing to install |
| **install** | official, but you must install it first — see the agent's inventory |
| ⚠️ **gated** | install *plus* account or plan provisioning |
| **n/a** | verified absent — that agent has nothing for this |

> **Assume one agent, not two.** Every stage is answered so it works with whichever agent you
> already have. **Better for** is an observation for teams already running both — never a reason to
> install the other one.
>
> **Not yet inventoried:** Cursor, Copilot, Kiro, Antigravity, Goose, OpenCode. They appear in the
> mechanism matrix but no capability inventory exists, so they are absent from these tables rather
> than marked `n/a`. See [`agents/README.md`](agents/README.md).

---

## The starting position

**Most of the lifecycle already ships.** That is why the portable layer this repository installs is
small: it carries only what does *not* ship, and what does not survive an agent switch.

The mistake the surveyed frameworks made was rebuilding, as markdown scaffolding, what agents ship
as executable commands. Do not do that.

---

## 1. Onboard a repository

| Agent | Tool | Type | Does what |
|---|---|---|---|
| Claude Code | `/init` | built-in | writes a starting **`CLAUDE.md`**; `CLAUDE_CODE_NEW_INIT=1` adds an interactive flow |
| Codex | `/init` | built-in | writes a starting **`AGENTS.md`** |
| Codex | `$migrate-to-codex` | install | imports another agent's instruction files, skills, agents and MCP config |
| Claude Code | `/import` | built-in | the mirror image — appends a supported agent's `AGENTS.md` to `CLAUDE.md` and carries over MCP servers, commands, subagents and skills (v2.1.213+) |
| both | `/hr-onboard` (Codex: **`$hr-onboard`**) | this repo | finds the **non-discoverable** knowledge by attempting work and recording friction |

**Do this** — run your own agent's `/init`, then `python install.py`. Both agents produce a starting
file; they just produce different halves, and the installer squares it: it writes `AGENTS.md` if
there is none, and adds the `@AGENTS.md` import to `CLAUDE.md` if that is missing. **You reach the
same place from either side, with no second agent required.** Then `/hr-onboard` — `/init` produces
a description, `hr-onboard` produces what a description cannot contain: the command that only works
from a subdirectory, the test that is meant to fail.

**Better for** — nothing meaningful. The only difference is which file you get first, and
`install.py` fills in the other.

## 2. Plan

| Agent | Tool | Type | Does what |
|---|---|---|---|
| Claude Code | `/plan` | built-in | plan mode |
| Claude Code | `/deep-research` | built-in | fans out web searches, cross-checks sources, returns a cited report |
| Codex | `/plan mode` | built-in | plan mode |
| Codex | `/goal` | built-in | "set a goal to keep pursuing" — persists across turns |
| Codex | `$define-goal` | install | pin a concrete, measurable goal before work starts |

**Do this** — use your agent's plan mode; both have one. If the plan must outlive the session,
write it to `work/<id>/`. That is the part neither mode gives you.

**Better for** — Codex `/goal` for an objective spanning many turns; Claude Code `/deep-research`
before a decision resting on external behaviour, which in this field is usually contested. On Codex
alone, an MCP docs server covers most of what `/deep-research` does.

## 3. Build

| Agent | Tool | Type | Does what |
|---|---|---|---|
| Claude Code | `/batch` | built-in | decomposes into 5–30 units, runs subagents in **isolated git worktrees**, tests, opens PRs |
| Claude Code | `/subtask`, `/background` | built-in | smaller splits |
| Claude Code | `/debug` | built-in | debug logging for a runtime problem |
| Codex | `/new playground worktree` | built-in | runs **the current chat** in a fresh worktree |
| Codex | `.codex/agents/*.toml` | built-in | subagents with `sandbox_mode` (`read-only`, `workspace-write`, `danger-full-access`), capped by `agents.max_concurrent_threads_per_session` |
| Codex | `codex apply` | built-in | applies the latest diff from a Codex **cloud** task to the local tree |

**Do this** — isolate in a worktree before anything parallel. That isolation is the point in either
agent: parallel agents editing one tree produce conflicts costing more than the parallelism saves.

**Better for** — Claude Code, for wide mechanical changes. `/batch` fans out a decomposed 5–30 unit
job at once; Codex isolates one chat at a time.

## 4. Verify

| Agent | Tool | Type | Does what |
|---|---|---|---|
| Claude Code | `/verify` \* | built-in | **builds and runs the app** to confirm the change works — without falling back to tests or type checks |
| Claude Code | `/run` | built-in | launches the app |
| Claude Code | `/run-skill-generator` | built-in | records the launch recipe **as a skill**, once |
| Codex | — | **n/a** | no build-and-run-it-to-prove-it command exists |

**Do this** — on Claude Code, `/run-skill-generator` once per project. **On Codex, write the launch
procedure as a skill by hand** in `.agents/skills/` — that is exactly what the generator produces.
Either way `install.py` distributes it to every agent's path.

**Better for** — Claude Code, and this is the **widest gap in the set**: the only stage where the
other agent has nothing at all.

**Portable expression** — the command is not portable; **the recorded recipe is.** It lands in the
repository as a skill. This is the highest-value pairing on the page.

> ⚠️ **Where the recipe lands is disputed between two official pages.** The skills page says
> `/verify` writes to `.claude/skills/verify/SKILL.md` and `/run-skill-generator` to
> `.claude/skills/run-<name>/`; the commands reference says `/verify`'s script comes from
> `CLAUDE.md` or `.claude/verify`. The two pages also describe `/run` as two different features.
> **Which path it is decides whether another agent finds the recipe**, which is this stage's whole
> claim — so confirm it by running `/verify` once before relying on the pairing. See
> [`agents/claude-code.md`](agents/claude-code.md) section 3.

> \* **Availability varies by feature flag and settings.** `/verify`, `/doctor`, `/debug`, `/batch`,
> `/deep-research` and `/run-skill-generator` are in the published reference but did not all appear
> in the session used to build `agents/claude-code.md`. **This stage's verdict rests on `/verify`
> being present — check yours before relying on it.**

## 5. Review

| Agent | Tool | Type | Does what |
|---|---|---|---|
| Claude Code | `/code-review` | built-in | diff, branch, PR or path. Effort `low…ultra`; `--fix` applies, `--comment` posts to the PR |
| Claude Code | `/security-review` | built-in | single-pass vulnerability review |
| Claude Code | `/simplify` | built-in | cleanup-only pass |
| Codex | `codex review` | built-in | **non-interactive subcommand with an exit code** — `--uncommitted`, `--base`, `--commit`. Drops into CI |
| Codex | `codex-security` (10 skills) | ⚠️ gated | staged pipeline: threat-model → discovery → attack-path → validation → triage → fix → track. Needs Codex Security access |

**Do this** — run your agent's review before every PR, then **move anything that must never slip
into `check.py` or the test suite**. That is the half a review command cannot bind. For security,
use Claude Code's `/security-review`; it needs no provisioning.

**Better for** — `codex review` **in CI**, because it is a subcommand with an exit code while
`/code-review` is interactive-first. `/code-review` **interactively**, because its effort levels and
`--fix`/`--comment` have no Codex counterpart. This is the one stage where Codex is ahead on
something structural.

**Portable expression** — a review command is advisory and vendor-local; a CI check binds and is
universal. Use the review to *find*, the check to *bind*.

## 6. Commit and ship

| Agent | Tool | Type | Does what |
|---|---|---|---|
| Claude Code | — | **n/a** | nothing opinionated, and that is fine |
| Codex | `$yeet` | install | stage → commit → push → open PR, in one step |
| Codex | `codex apply` | built-in | applies the latest diff from a Codex **cloud** task |
| both | `python check.py` | this repo | guards the six silent failures of the portable layer |

**Do this** — wire `python check.py` into CI, alongside `python install.py --check`, which exits
non-zero when an installed copy has drifted from its source. That is the stage's actual requirement;
the rest is `git`.

**Better for** — Codex `$yeet`, marginally, on convenience. `codex apply` is **not** a local-workflow equivalent: it applies diffs from Codex **cloud** tasks. Neither is required.

**Portable expression** — ✅ a script with an exit code binds regardless of who or what made the
change. Optionally mirror it as a pre-commit hook for speed — but **if the hook and the check
disagree, the check wins**, because the check is what a reviewer and a different agent both see.

## 7. Maintain

| Agent | Tool | Type | Does what |
|---|---|---|---|
| Claude Code | `/doctor` | built-in | installation health, unused skills and MCP servers, slow hooks; **trims `CLAUDE.md` and migrates guidance into skills** |
| Claude Code | `/fewer-permission-prompts` | built-in | writes an allowlist for read-only calls you keep approving |
| Claude Code | `/claude-api cost-optimize` | built-in | profiles spend; `prompt-audit` flags instructions written for an older model |
| Claude Code | `/loop`, `/schedule` | built-in | recurring work |
| Codex | `codex plugin list`, `/plugins`, `/hooks` | built-in | **print** what is installed and active |
| Codex | `.codex/hooks.json` | built-in | repo- and user-level lifecycle hooks, incl. a **blocking `PreToolUse`** |
| Codex | `codex debug prompt-input` | built-in | renders **what the model actually sees**, including every skill and its root |
| Codex | `/doctor` equivalent | **n/a** | nothing acts on what it finds |

**Do this** — on Claude Code, `/doctor` every few weeks and whenever the instruction file has grown.
**On Codex the equivalent is manual**: `codex plugin list` and `/hooks` to see what is active, then
trim `AGENTS.md` by hand against the inclusion test.

**Better for** — roughly even, and both can answer "what is actually loaded". Codex has `codex
debug prompt-input`; Claude Code has **`/context`**, which lists the **Memory files** that loaded,
and the **`InstructionsLoaded`** hook, which fires per instruction file with a reason matcher
(`session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`) — finer-grained than
Codex's. Only Claude Code has a `/doctor` that then *acts* on what it finds.

`/doctor` already performs the maintenance move this layer cares about: **guidance that has become a
procedure should leave the always-loaded file and become an on-demand skill.** Let it.

> **One hazard worth naming.** A permission mode that silently denies shell calls will stop an agent
> running your tests, and the agent will "verify" by reading code instead. Nothing raises an error.
> `/fewer-permission-prompts` exists partly for this.

---

## What has no counterpart at all

Neither of these maps onto a stage.

**Codex only** — `codex sandbox` and per-project `trust_level`, where an **untrusted project skips every
`.codex/` project-scoped layer** · ~45 curated third-party plugins · `computer-use`, `latex` ·
`$screenshot`, `$speech`, `$transcribe` · `$security-ownership-map` (people-to-file security
ownership from git history) · `$hatch-pet` — the clearest example of a vendor-local convenience no
portable layer should try to carry.

**Claude Code only** — Artifacts · workflow orchestration · deferred tool loading · prompt-based
hooks decided by a model.

---

## The three-tier rule

Everything above resolves into one decision. When you learn something about this repository, ask
where it belongs:

| Tier | Cost | Fires | Put here |
|---|---|---|---|
| **`AGENTS.md`** | **every session, every agent, everyone** | always | short, non-standard, non-obvious instructions |
| **A path-scoped rule** | only when a matching file is touched | Claude Code reads a file matching `paths:` | instructions that apply to one part of the tree |
| **A skill** | metadata always, body on match | the agent decides, from `description` | procedures and reference material |
| **A check** | on event | **cannot be skipped** | anything that must not be missed |

> **Push everything down as far as it will go: prose → path-scoped rule → skill → check.**

**The second tier is Claude-Code-only and worth knowing about.** `.claude/rules/*.md` with a `paths:`
frontmatter glob loads *only* when Claude reads a matching file — so a rule about `src/api/**` costs
nothing on a session that never opens it. It attacks exactly the cost problem this table exists for,
and it is **not portable**: Codex has no equivalent. Keep the portable statement in `AGENTS.md`; use
a rule as the vendor-local accelerator, the same way a hook mirrors a check.

A rule enforced by CI does not need a sentence in `AGENTS.md`. Delete the sentence — it is costing
you on every session for a job something else is already doing.

## When *not* to reach for a built-in

| Situation | Do this instead |
|---|---|
| The team uses more than one agent | Whatever the built-in does for you, the knowledge belongs in `AGENTS.md` so the other agent has it too |
| The thing must never be skipped | A check, not a command. Commands need someone to type them |
| You keep typing the same prompt | A skill — with a project prefix, so it cannot silently replace a built-in |
| You are about to write a framework | Read `../research/PORTABILITY.md` first. Four-plus projects have written it; adoption of every one measured at essentially zero |

## Naming

Prefix every skill this repository ships. A skill named `review` **silently replaces** Claude Code's
bundled `/code-review`, and its alias never reaches yours. Codex behaves differently again — both
appear, unmerged. `check.py` catches collisions against known lists, but those lists are lower
bounds; **the prefix is the actual protection.**

```
✗  review/          shadows Claude Code's bundled /code-review, silently
✓  hr-review/       cannot collide; reads as local in every selector
```
