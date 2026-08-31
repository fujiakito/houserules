# Claude Code

**Measured:** `v2.1.251`, 2026-08-31, by asking a session to enumerate its own skills and reading
its `/` picker. **Surfaces:** CLI (terminal), desktop app, web (`claude.ai/code`), IDE extensions
(VS Code, JetBrains) — **only the CLI/desktop session was checked**.
**Docs:** the published commands reference.

> Lower bound — see [README](README.md). Absence means "not recorded", not "not there".
>
> Availability varies by **feature flags and settings**: `/verify`, `/doctor`, `/debug`, `/batch`,
> `/deep-research` and `/run-skill-generator` appear in the published reference but did not all
> appear in this session's enumeration. Treat the published reference as the superset.

## 1. Commands

| Command | Does what |
|---|---|
| `/init` | write a starting **`CLAUDE.md`**. `CLAUDE_CODE_NEW_INIT=1` gives an interactive flow covering skills, hooks and memory |
| `/plan` | plan mode |
| `/batch` | **decompose into 5–30 units and run subagents in isolated git worktrees**, implementing, testing and opening PRs |
| `/subtask`, `/background` (`/bg`) | smaller splits; background work |
| `/verify` | **build and run the app to confirm a change does what it should** — without falling back to tests or type checks |
| `/run` | launch the app |
| `/run-skill-generator` | record the launch recipe once, as a skill, so every later run and every other agent follows it |
| `/code-review` (`/review`) | review a diff, branch, PR or path. Effort `low\|medium\|high\|xhigh\|max\|ultra`; `--fix` applies findings, `--comment` posts them to the PR |
| `/security-review` | single-pass vulnerability review |
| `/simplify` | cleanup-only pass — reuse, simplification, efficiency |
| `/debug` | turn on debug logging and work a runtime problem |
| `/doctor` (`/checkup`) | installation health, unused skills and MCP servers, slow hooks; **deduplicates and trims `CLAUDE.md`, and migrates guidance into skills** |
| `/deep-research` | fan out web searches, cross-check sources, return a cited report |
| `/loop` (`/proactive`), `/schedule` | run something on an interval; scheduled cloud agents |
| `/agents` | prints guidance — it no longer manages subagent definitions directly; ask Claude or edit the files |
| `/memory` | persistent memory |
| `/context` | **shows what actually loaded**, including a **Memory files** list. `/compact`, `/usage`, `/cost` for context and spend |
| `/model`, `/effort` | model and reasoning-effort selection |
| `/permissions` (`/allowed-tools`), `/config` (`/settings`), `/mcp`, `/hooks` | configuration |
| `/resume`, `/fork`, `/branch`, `/rewind`, `/clear` (`/reset`, `/new`) | session lifecycle |
| `/diff`, `/copy`, `/export`, `/status`, `/tasks`, `/feedback`, `/bug`, `/help` | utilities |
| `/artifacts` | list published artifacts |
| `/import` | bring a supported agent's config into Claude Code — appends `AGENTS.md` to the matching `CLAUDE.md`, carries over MCP servers, commands, subagents and skills (v2.1.213+) |

## 2. Built-in skills

Bare-named, as opposed to the `plugin:skill` form in section 4.

| Skill | Does what |
|---|---|
| `code-review`, `security-review`, `simplify` | the review family above |
| `init`, `run` | onboarding; launching the app |
| `claude-api` | reference for the Claude API and SDK — model ids, pricing, params, caching, tool use |
| `update-config` | edit `settings.json`: hooks, permissions, env vars |
| `keybindings-help` | customise `keybindings.json` |
| `fewer-permission-prompts` | scan transcripts for read-only calls you keep approving, write an allowlist |
| `loop`, `schedule` | recurring and scheduled work |
| `design` | multi-artboard visual design canvas |
| `dataviz` | charts, dashboards, palettes — load before writing any chart code |
| `artifact-design`, `artifact-diagramming`, `artifact-capabilities` | authoring published Artifacts |
| `agents`, `_remote-workflow` | agent and remote-workflow support |

## 3. Tools

Available to the model in a session: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `PowerShell`
(on Windows), `NotebookEdit`, `WebFetch`, `WebSearch`, `Agent` (subagents), `Task`/`Monitor`
controls, `Artifact` (publish a page), `Skill`, `ToolSearch`, `AskUserQuestion`, `SendUserFile`,
`Workflow`, `ScheduleWakeup`, `ReportFindings`, plus browser control and any MCP server tools.

Some are **deferred** — present but with schemas loaded on demand via `ToolSearch`, which keeps the
prompt small. That is a real difference from Codex, where the tool set is fixed per session.

## 4. Installable — official

Claude Code addresses plugin skills as **`plugin:skill`**. The namespace is load-bearing: a project
skill named `pdf` **cannot** shadow `anthropic-skills:pdf`.

| Plugin skill | Does what |
|---|---|
| `anthropic-skills:docx` | create, read and edit Word documents and templates |
| `anthropic-skills:xlsx` | spreadsheets — `.xlsx`, `.csv`, formulas, charts |
| `anthropic-skills:pptx` | PowerPoint decks — create, edit, render, export |
| `anthropic-skills:pdf` | read, create, merge, split, fill forms, OCR |
| `anthropic-skills:skill-creator` | create, edit and eval skills |
| `anthropic-skills:schedule` | create or update a scheduled task |
| `anthropic-skills:morning` | render a recurring morning brief |
| `anthropic-skills:consolidate-memory` | merge duplicate memories, prune the index |
| `anthropic-skills:import-memory` | import a memory export from another assistant |
| `anthropic-skills:explain-usage` | where this session's tokens went |
| `anthropic-skills:setup-cowork` | guided Cowork setup |

Managed with `/plugins`; more are available from marketplaces.

> **`schedule` exists in both tiers** — bare `schedule` *and* `anthropic-skills:schedule`. Two live
> skills under one bare name, which is evidence the bundled set is not curated against the plugin
> set.

## 5. Extension points

| | Path | Scope |
|---|---|---|
| Instruction file | **`CLAUDE.md` only** — `AGENTS.md` is **not** read natively. `@AGENTS.md` import required; without it `AGENTS.md` is ignored **and nothing says so**. `./CLAUDE.md` **and `./.claude/CLAUDE.md`** are both valid project locations | project, `~/.claude/CLAUDE.md`, managed policy, `claudeMd` settings key |
| **Path-scoped rules** | **`.claude/rules/*.md`**. With a `paths:` frontmatter glob a rule loads **only when Claude reads a matching file**; without one it loads at launch. Discovered recursively, symlinks supported | project, `~/.claude/rules/` |
| Skills | `.claude/skills/<name>/SKILL.md` | project, `~/.claude/skills/` |
| MCP | `.mcp.json` / settings; `/mcp` manages servers and OAuth | project, user |
| Subagents | `.claude/agents/` | project |
| Hooks | `.claude/settings.json` — **33 documented events**, ~10 of which can block. **5 handler types**: `command`, `http`, `mcp_tool`, `prompt` (decided by a model), `agent`. Includes **`InstructionsLoaded`**, which fires per instruction file with a load-reason matcher | project, user |
| Plugins | package skills, agents, commands, hooks and MCP together | marketplace |

The `@AGENTS.md` import is the single most important row here, and is why `check.py` guards it.

## 6. How to enumerate this yourself

For **skills and commands** there is no command that prints the inventory. Ask the session directly
— "list every skill and command you have" — and read the `/` picker. That is how this file was
produced, and it is weak evidence: the model reports on itself, and feature flags change what is
present.

For **instruction files** the tooling is better than Codex's:

- **`/context`** lists what loaded, under **Memory files**. This is the documented way to confirm a
  `CLAUDE.md` or `@AGENTS.md` import took effect.
- The **`InstructionsLoaded` hook** fires per instruction file with a reason matcher —
  `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` — so you can log
  exactly which file loaded, when, and **why**. Finer-grained than anything Codex exposes.
- **`/doctor`** reports installation health and unused skills, and proposes trims for a checked-in
  `CLAUDE.md`.

**Size thresholds:** target **under 200 lines** per `CLAUDE.md`; a file over **4 MiB** is skipped
entirely. Auto-memory's `MEMORY.md` loads only its first 200 lines or 25 KB.

## 7. Surface differences

Claude Code runs as a terminal CLI, a desktop app (Mac/Windows), a web app at `claude.ai/code`, and
IDE extensions for VS Code and JetBrains. **Only the CLI/desktop session was checked**; whether the
web and IDE surfaces expose the same skills and commands is **(unverified)**.

Terminal-dialog commands — `/permissions`, `/config`, `/doctor`, `/hooks` — open an interactive
panel and are **not available in every surface**, which is itself a surface difference worth knowing
before scripting around them.
