# Claude Code

**Measured:** `v2.1.251`, 2026-08-31, by asking a session to enumerate its own skills and reading its
`/` picker — **CLI/desktop session only**.
**Documentation:** `code.claude.com/docs`, `claude.com/docs`, `support.claude.com`. Pages read for
this file were retrieved **2026-08-29 to 2026-09-04**; each section names its date where it matters.
**Surfaces:** CLI, desktop app, mobile, IDE extensions (VS Code, JetBrains), web (`claude.ai/code`),
Agent SDK, Chrome extension.

## Evidence grades used in this file

| Grade | Means |
|---|---|
| **`tested`** | Run on a real installation here, surface and version recorded |
| **`documented`** | Official vendor page, retrieval date recorded. **Not run** |
| ⚠️ **`disputed`** | Two official pages disagree. Both readings kept, neither picked silently |
| `(unverified)` | Carried forward without a source |

> **Every list here is a lower bound.** Absence means "not recorded", not "not there". See
> [README](README.md).
>
> **A session enumeration cannot separate what ships from what the machine has installed.** For
> "is this bundled?", the enumerable source is the commands reference's own `Skill` marker, and
> that is what section 3 and `check.py`'s reserved-name set use. The `/` picker is used only where
> no documented list exists.
>
> **Availability varies by feature flag, plan, provider and version.** `/verify`, `/doctor`,
> `/debug`, `/batch`, `/deep-research` and `/run-skill-generator` appear in the published reference
> but did not all appear in this session's enumeration.

---

## 1. Surfaces

| Surface | What it is | Notes |
|---|---|---|
| **CLI** | `claude` in the terminal | The most complete surface for terminal-native work. **Scripting and the Agent SDK are CLI-only** |
| **Desktop** | The **Code** tab of the Claude app | Diff viewer, browser/preview pane, integrated terminal and file editor, parallel sessions with worktree isolation, computer use, Dispatch, iOS Simulator pane (macOS). macOS, Windows, Linux (beta), WSL. Windows needs Git for Windows |
| **Mobile** | Code tab of the Claude iOS/Android app | **A client, not a runtime.** Cloud sessions, Remote Control, Dispatch. Code never executes on the phone |
| **VS Code** | Extension | Inline diffs, `@`-mentions with line ranges, plan review, conversation history. **Exposes a subset of CLI commands and skills.** Needs no separate CLI install; also installs in VS Code forks via Open VSX |
| **JetBrains** | Plugin | Diff viewing, selection context, file-reference shortcuts, diagnostics. **Runs `claude` in the IDE's integrated terminal and does not bundle its own copy** — install both |
| **Web** | `claude.ai/code` | Cloud sessions on Anthropic-managed infra that continue after you disconnect |
| **Agent SDK** | Headless `--print`, SDK | Exposes skills, hooks, plugins, MCP, permissions |
| **Chrome extension** | Claude in Chrome | Separate install; drives your real Chrome with its logged-in state |

Also surfaces: **Slack** (`@Claude`, backed by Claude Code on the web), **Claude Tag** (the same as
your organization's shared identity, Team/Enterprise), and **CI/CD** (GitHub Actions, GitLab CI/CD).

**Desktop has three tabs** — Chat, **Cowork**, and Code. Cowork is a separate product sharing the
shell; see section 18.

### Third-party providers by surface — `documented`, 2026-09-02

| Surface | Bedrock | Google Agent Platform | Microsoft Foundry |
|---|---|---|---|
| CLI | ✅ | ✅ | ✅ |
| VS Code / JetBrains | ✅ | ✅ | ✅ |
| Desktop | via *Claude Desktop on 3P* | ✅ Enterprise, via managed settings; also *Claude Desktop on 3P* | via *Claude Desktop on 3P* |

The CLI is the **most complete** surface, not the only provider-capable one.

---

## 2. Commands

Built-in commands, from the published commands reference, retrieved **2026-09-02**. Rows marked
**Skill** are bundled skills and are listed separately in section 3.

| Command | Does what |
|---|---|
| `/init` | Write a starting **`CLAUDE.md`**. Reads Cursor rules (`.cursor/rules/`, `.cursorrules`) and Copilot rules (`.github/copilot-instructions.md`). `CLAUDE_CODE_NEW_INIT=1` adds an interactive flow covering skills, hooks and memory, and also reads `AGENTS.md`, `.devin/rules/`, `.windsurf/rules/`, `.clinerules`. **Offers to hand off to `/import`** when it finds a supported agent's config |
| `/import [codex\|gemini] [--dry-run] [--yes]` | Bring another agent's configuration in — appends its instruction file to the matching `CLAUDE.md`, carries over MCP servers, commands, subagents and skills. **v2.1.213+**. Not available on Bedrock, Agent Platform, Foundry or Claude Platform on AWS, nor with feature-flag fetching off |
| `/plan` | Plan mode |
| `/subtask`, `/background` (`/bg`), `/fork` | Side task reporting into this conversation; background session; copy the conversation into one |
| `/agents` | Prints guidance — it no longer manages subagent definitions directly |
| `/list-agents` (`/peers`) | Subagents, agent-team teammates and other sessions Claude can message. **v2.1.224+**; only where cross-session messaging is enabled |
| `/workflows` | Browse, watch and save dynamic workflow runs |
| `/worktree [create\|list\|switch\|delete]` | Manage git worktrees |
| `/memory` | List and edit `CLAUDE.md`, `CLAUDE.local.md` and the auto-memory folder; toggle auto memory |
| `/context [all]` | **Shows what actually loaded**, including a **Memory files** list. The documented way to confirm a `CLAUDE.md` or `@AGENTS.md` import took effect |
| `/compact`, `/autocompact`, `/usage`, `/cost`, `/status` | Context and spend |
| `/model`, `/effort` | Model and reasoning-effort selection. `/effort ultracode` = `xhigh` plus automatic workflow orchestration (**v2.1.203+**) |
| `/rewind [N\|--summary]` | Roll back to a checkpoint, or summarize part of the conversation without rolling back |
| `/resume [name]`, `/branch`, `/clear` (`/reset`, `/new`) | Session lifecycle. `/branch` tries a different direction without losing the conversation; `/fork` copies it into a background session and leaves you here; `/resume` keeps the project memory from the cleared conversation |
| `/rename [name]` | Rename the current session; the name also appears on the prompt bar. Naming a session replaces its default display name and generated title, and makes it resumable with `claude --resume <name>` or `/resume <name>`. **Available in non-interactive mode from v2.1.205.** Documented on both the commands reference and the sessions page, retrieved 2026-09-03 |
| `/permissions` (`/allowed-tools`), `/config` (`/settings`), `/mcp`, `/hooks`, `/keybindings`, `/statusline`, `/vim` | Configuration. `/statusline` and `/vim` need v2.1.208+ and v2.1.204+ |
| `/reload-skills`, `/reload-plugins` | Re-read skills or plugins from disk without restarting. `/reload-plugins` is v2.1.227+ |
| `/plugin` | Install and manage plugins |
| `/artifacts` | List artifacts you own and ones shared with you; `Enter` attaches one to the session (**v2.1.208+**; before v2.1.216 `Enter` opened the browser) |
| `/chrome`, `/ide`, `/add-dir`, `/cd` | Browser integration, IDE connection, working directories |
| `/remote-control` | Pair this session with another device (**v2.1.206+**; mobile app 1.14+) |
| `/voice [on\|off\|auto]` | Voice input. **v2.1.207+**, needs a claude.ai account and a compatible microphone |
| `/fast` | Fast mode |
| `/advisor` | Anthropic API and Console only |
| `/install-github-app`, `/install-slack-app`, `/autofix-pr` | Integrations; cloud session that watches and fixes PR feedback |
| `/login`, `/logout`, `/privacy-settings`, `/desktop`, `/mobile`, `/web-setup` | Account and surface setup |
| `/diff`, `/copy`, `/export`, `/tasks`, `/btw`, `/feedback`, `/bug`, `/help`, `/exit` | Utilities. `/tasks` also lists artifacts this session is watching |
| `/goal` | Keep the session working toward a condition, turn after turn |
| `/auto-mode-setup`, `/color`, `/focus`, `/insights`, `/passes`, `/powerup`, `/radio`, `/heapdump`, `/slash-commands`, `/pr-comments` | Assorted; `/pr-comments` was **removed in v2.1.91** |

> **`/rename` is the worked example of why every list in this file says "lower bound".**
>
> An earlier revision recorded it as "disputed, probably a confusion with Codex", on the strength of
> repeated searches of the commands reference alone. **That was wrong.** The sessions page documents
> it directly — *Name your sessions* gives `/rename auth-refactor` for "During a session", and the
> duplicate-name and `/clear` rules use it again.
>
> The mistake is the one this file warns about in its own header: **treating one enumerable page as
> the whole surface**, so *not found in the commands reference* became *not a Claude Code command*.
> A command lives wherever its feature is documented, and **repeating a search against the same page
> does not widen its scope.**
>
> **`/archive` remains unlisted** — no source found. It is reserved in `check.py` defensively, which
> costs nothing, but it is not claimed here as a Claude Code command.

> **Terminal-dialog commands** — `/permissions`, `/config`, `/doctor`, `/hooks` — open an
> interactive panel and are **not available on every surface**. Worth knowing before scripting
> around them.

---

## 3. Bundled skills

**Source: the commands reference's own `Skill` marker, retrieved 2026-09-02.** This is independent
of what any machine has installed. Bundled skills are prompt-based — they give Claude instructions
and let it orchestrate with its tools; most built-in commands instead execute fixed logic.

| Bundled skill | Does what |
|---|---|
| `/batch <instruction>` | Decompose a large change into 5–30 units, one background subagent per unit **in an isolated git worktree**; each implements, tests and opens a PR. Requires a git repo |
| `/claude-api [migrate\|upgrade\|managed-agents-onboard\|prompt-audit\|cost-optimize]` | Claude API and Managed Agents reference for your project's language |
| `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` | Review the diff, or a PR/branch/path. `--fix` applies, `--comment` posts inline PR comments, `ultra` runs a deep cloud review |
| `/dataviz [request]` | Chart and dashboard design guidance; validates palettes for colorblind safety and contrast with a bundled script |
| `/debug [description]` | Enable debug logging and work a runtime problem from the session log |
| `/design [brief]` | Draft UI mockups, screen flows, landing pages or posters as artboards on one canvas, published as an artifact. **Requires artifacts available, v2.1.234+** |
| `/design-sync [hint]` | Convert the repo's React design system and upload it to Claude Design |
| `/doctor` (`/checkup`) | Setup checkup: install health, unused skills and MCP servers, slow hooks; **trims a checked-in `CLAUDE.md`** and migrates guidance into skills. Trim check needs v2.1.206+ |
| `/fewer-permission-prompts` | Scan transcripts for read-only Bash and MCP calls you keep approving, write an allowlist into project `.claude/settings.json` |
| `/loop [interval] [prompt]` | Run a prompt repeatedly while the session stays open — see section 8 |
| `/run` | ⚠️ **disputed** — see below |
| `/run-skill-generator` | Generate a skill from a description or by recording interactions, then save and test it. Records a per-project launch recipe to `.claude/skills/run-<name>/` |
| `/sandbox [js\|python\|bash] [--timeout <s>]` | Run untrusted code in a sandboxed environment. Default timeout 30s. **v2.1.200+** |
| `/schedule <interval> <prompt>` (`/routines`) | Create a cloud **Routine** — see section 8 |
| `/security-review [--fix] [pr#\|branch\|path]` | Review the diff, or a PR/branch/path, for security vulnerabilities |
| `/simplify [--fix] [--comment] [pr#\|branch\|path]` | Simplification-only pass; similar to `/code-review` at effort `low` |
| `/verify` | ⚠️ **disputed** — see below |

Two more are bundled but are not rows in that table:

| | Kind | Notes |
|---|---|---|
| `/deep-research <question>` | bundled **workflow**, not a skill | The only one. Requires the WebSearch tool. Runs only when invoked |
| `/workflow-authoring` | bundled skill | Loads the script-writing reference before you edit a saved workflow. **v2.1.248+**, and unavailable when dynamic workflows are off |

### ⚠️ `/run` and `/verify` — two official pages disagree

Both retrieved 2026-09-02. Recorded rather than resolved, the same treatment `research/MATRIX.md`
§2 gives the Codex byte-budget dispute. **A citation stops being evidence when two citations
conflict.**

| | Skills page | Commands reference |
|---|---|---|
| `/run` | A bundled skill: *"Launch and drive your app to see a change working"*, inferring the launch from project type, README, `package.json` or `Makefile` | `/run <command>` — *"Execute a shell command, passing its output to Claude."* **Not marked as a Skill** |
| `/verify` | *"Build and run your app to confirm a code change does what it should, without falling back to tests or type checks."* Records its recipe to **`.claude/skills/verify/SKILL.md`** (v2.1.200+); at the repo root that recorded skill replaces the bundled `/verify` by design | *"Run a verification script … The script comes from your project's `CLAUDE.md` or a **`.claude/verify`** script."* Marked as a Skill |

Both agree `/verify` is a bundled skill and runs only when invoked (before v2.1.215 Claude could
also run it on its own). They disagree on **where the recorded recipe lives** — which decides
whether another session or another agent finds it. `docs/GUIDE.md` stage 6 depends on that answer.
**Settling it needs a run, not a re-read.**

### Turning bundled skills off

`disableBundledSkills` disables every bundled skill **except `/doctor`** (v2.1.205+; before that
`/doctor` was a built-in command). To hide `/doctor` too: `DISABLE_DOCTOR_COMMAND`, or
`skillOverrides: {"doctor": "off"}`.

**Repository-supplied, not bundled:** the `hr-onboard` skill is installed by this repository at
`.claude/skills/hr-onboard/SKILL.md`. It discovers non-obvious operating knowledge by attempting
real work; invoke it as `/hr-onboard`. Its own `SKILL.md` is the canonical procedure. `tested`,
Claude Code Desktop Code-tab session using bundled CLI 2.1.251, enumerated in the current checkout,
2026-09-03.

---

## 4. Subagents

Built in, no setup. `documented`, 2026-09-02.

| Subagent | Model | Tools | Purpose |
|---|---|---|---|
| **Explore** | **Inherits from the main conversation, capped at Opus on the Claude API**; inherits directly on every other provider | Read-only; Write and Edit denied | File discovery, code search. Claude passes a thoroughness level: *quick*, *medium*, *very thorough* |
| **Plan** | Inherits | Read-only; Write and Edit denied | Codebase research during plan mode |
| **general-purpose** | `CLAUDE_CODE_SUBAGENT_MODEL` if set, else the conversation's model | Every tool available to subagents | Complex research, multi-step operations, modification |
| `claude` | Follows the model order when spawned | Every tool available to subagents | Catch-all. Also the default agent for a dispatched background session |
| `statusline-setup` | Sonnet | — | When you run `/statusline` |
| `claude-code-guide` | Haiku | — | Questions about Claude Code features |

**As of v2.1.198 Explore inherits the conversation's model instead of always running on Haiku.** A
user or project subagent named `Explore` overrides the built-in and keeps its own `model` field, so
`model: haiku` is how you keep exploration cheap.

> **Explore and Plan skip your `CLAUDE.md` files and the parent session's git status** to stay fast.
> Every other built-in and custom subagent loads both, and **there is no frontmatter field or
> setting to change which agents skip them.** This is worth knowing before you put a load-bearing
> rule in `CLAUDE.md` and expect exploration to honour it.

**Custom:** `.claude/agents/` (project) or `~/.claude/agents/` (user), or programmatically in the
Agent SDK. Per-agent model, tool restrictions, permission modes, preloaded skills, persistent
memory and frontmatter hooks.

---

## 5. Tools

Available to the model in a session: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `PowerShell`
(on Windows), `NotebookEdit`, `WebFetch`, `WebSearch`, `Agent` (subagents), `Task`/`Monitor`
controls, `Artifact`, `Skill`, `ToolSearch`, `AskUserQuestion`, `SendUserFile`, `Workflow`,
`ScheduleWakeup`, `ReportFindings`, plus browser control and any MCP server tools.

Some are **deferred** — present, with schemas loaded on demand via `ToolSearch`, which keeps the
prompt small. That is a real difference from Codex, where the tool set is fixed per session.

---

## 6. Extension points

| | Path | Scope |
|---|---|---|
| Instruction file | **`CLAUDE.md` only** — `AGENTS.md` is **not** read natively. `@AGENTS.md` import required; without it `AGENTS.md` is ignored **and nothing says so**. `./CLAUDE.md` **and `./.claude/CLAUDE.md`** are both valid project locations | project, `~/.claude/CLAUDE.md`, `CLAUDE.local.md`, managed policy, `claudeMd` settings key |
| **Path-scoped rules** | **`.claude/rules/*.md`**. With a `paths:` frontmatter glob a rule loads **only when Claude reads a matching file**; without one it loads at launch with the same priority as `.claude/CLAUDE.md`. Discovered recursively; symlinks supported and cycles handled | project, `~/.claude/rules/` |
| Skills | `.claude/skills/<name>/SKILL.md`; `.claude/commands/<name>.md` still works (merged into skills) | project, `~/.claude/skills/`, plugin, enterprise, claude.ai account |
| MCP | `.mcp.json` (project), `~/.claude.json` (user/local); `/mcp` manages servers and OAuth | project, user, managed |
| Subagents | `.claude/agents/` | project, user |
| Hooks | `.claude/settings.json` — see section 7 | project, user, managed |
| Plugins | package skills, agents, commands, hooks and MCP together | marketplace |
| Workflows | `.claude/workflows/` (project, shared) or `~/.claude/workflows/` (personal). Project wins on a name clash; plugin workflows are namespaced `/<plugin>:<name>` | project, user, plugin |

The `@AGENTS.md` import is the single most important row here, and is why `check.py` guards it.

### `AGENTS.md`, verbatim

> *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`."* — memory documentation, retrieved 2026-09-02

The documented fix is a `CLAUDE.md` containing `@AGENTS.md`. A symlink also works where you need no
Claude-specific content, **but on Windows a symlink requires Administrator or Developer Mode, so
the docs direct you to the import** — which is what `install.py` writes. Confirm with `/context`
under **Memory files**.

### Size and loading limits — `documented`, 2026-09-02

| Limit | Value |
|---|---|
| `CLAUDE.md` target | **under 200 lines** — longer files consume more context and reduce adherence |
| `CLAUDE.md` hard cap | loaded in full up to **4 MiB**; a larger file is **skipped entirely** |
| Auto-memory `MEMORY.md` | first **200 lines or 25 KB**, whichever comes first |
| `@path` import depth | 4 hops |
| A rule's `paths:` brace expansion | **1,000 expanded patterns and 4 MiB**, shared across the rule's whole list. A pattern that would exceed it is used unexpanded and its literal braces match nothing |

**Loading order:** `CLAUDE.md` and `CLAUDE.local.md` load from cwd and every directory above it,
**concatenated root-first** so the closest file is read last; `CLAUDE.local.md` is appended after
`CLAUDE.md` at each level. Subdirectory files load **on demand** when Claude reads files there.
`claudeMdExcludes` skips files by glob. Managed-policy `CLAUDE.md` cannot be excluded.

**Block-level HTML comments in `CLAUDE.md` are stripped before injection**; comments inside code
blocks are preserved, and the Read tool shows them either way. This is why `templates/AGENTS.md`
tells you to delete its comment block — **Codex does not strip them**, so the same block is free on
one agent and billed on the other.

**Auto memory is on by default.** Stored per repository at
`~/.claude/projects/<project>/memory/`; `autoMemoryEnabled`, `autoMemoryDirectory`,
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Machine-local, excluded from the transcript retention sweep.
Not loaded into subagents except a fork.

---

## 7. Hooks

**Nothing is preconfigured — every hook is manual.** `documented`, event list and blocking set
re-read from the [official hooks reference](https://code.claude.com/docs/en/hooks), retrieved
2026-09-03.

**33 events:** `SessionStart` · `Setup` · `UserPromptSubmit` · `UserPromptExpansion` · `PreToolUse`
· `PermissionRequest` · `PermissionDenied` · `PostToolUse` · `PostToolUseFailure` · `PostToolBatch`
· `Notification` · `MessageDisplay` · `SubagentStart` · `SubagentStop` · `TaskCreated` ·
`TaskCompleted` · `Stop` · `StopFailure` · `TeammateIdle` · `InstructionsLoaded` · `ConfigChange` ·
`CwdChanged` · `DirectoryAdded` · `FileChanged` · `WorktreeCreate` · `WorktreeRemove` · `PreCompact`
· `PostCompact` · `PreModelSwitch` · `PostModelSwitch` · `Elicitation` · `ElicitationResult` ·
`SessionEnd`

**15 can block through process exit status:** `PreToolUse`, `UserPromptSubmit`,
`UserPromptExpansion`, `Stop`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`,
`ConfigChange`, `PostToolBatch`, `PreCompact`, `PreModelSwitch`, `Elicitation`,
`ElicitationResult`, and `WorktreeCreate`. The first 14 use exit code 2; `WorktreeCreate` aborts on
any non-zero exit. `PermissionRequest` does not honor exit code 2, but can deny through its
structured JSON decision.

**Command-hook failures are fail-open for most events.** Exit codes other than 0 or 2 (including a
missing or non-executable command, commonly 127) do not block unless valid structured JSON carries
a decision. A timed-out `command`, `http`, or `mcp_tool` `PreToolUse` hook also does not block; the
normal permission flow continues. Treat hook availability, executability, timeout, and output
parsing as part of the control, not as incidental diagnostics.

**5 handler types:**

| `type` | Does what |
|---|---|
| `command` | Shell command; JSON on stdin, result via exit code and stdout |
| `http` | POSTs the event JSON to a URL; result in the response body |
| `mcp_tool` | Calls a tool on an already-connected MCP server |
| `prompt` | Single-turn LLM evaluation; the model returns a JSON decision |
| `agent` | Spawns a subagent (experimental) that can use tools before deciding |

Hooks can also be declared in skill and subagent frontmatter, and run in the background
asynchronously. Controls: `disableAllHooks`, `allowManagedHooksOnly`, `allowedHttpHookUrls`,
`httpHookAllowedEnvVars`.

**`InstructionsLoaded`** fires when a `CLAUDE.md` or `.claude/rules/*.md` file loads — at session
start and on lazy load — with a load-reason matcher. It is the documented way to debug path-scoped
and lazily-loaded instruction files, and is finer-grained than anything Codex exposes.

---

## 8. Scheduling — three runtimes, not one feature

`documented`, 2026-09-02.

| | Cloud (**Routines**) | Desktop scheduled tasks | `/loop` + session cron |
|---|---|---|---|
| Created by | `/schedule` (alias `/routines`), claude.ai/code/routines, or Desktop → Routines → **Cloud** | Desktop → Routines → **Local** | `/loop`, or natural language |
| Runs on | Anthropic cloud, or your self-hosted environment | Your machine | Your machine |
| Machine on / session open | No / No | Yes / No | Yes / **Yes** |
| Local files | No — fresh clone | Yes | Yes |
| Skills it sees | Account skills + committed repo skills | **Local** skills | The session's own |
| Permission prompts | **None — runs autonomously** | Configurable per task | Inherits |
| Minimum interval | **1 hour** | 1 minute | 1 minute |
| Auth | **claude.ai required** | claude.ai | Any provider |

Plus **GitHub Actions** with a `schedule:` trigger — manual setup, any provider, and the only one
that needs no claude.ai account.

**Routines are in research preview.** Pro/Max/Team/Enterprise; Team and Enterprise Owners can
disable them org-wide, which from v2.1.227 also hides `/schedule` in the CLI. Triggers: schedule
(recurring or one-off), **API**, and **GitHub events** (pull request and release categories, with
filters on author, title, body, base/head branch, labels, draft and merged state). The API trigger
POSTs to a per-routine `fire` endpoint under the `experimental-cc-routine-2026-04-01` beta header;
its optional `text` arrives wrapped in a `<routine-fire-payload>` block **labelled as untrusted
data**, so the routine's own prompt must explicitly opt in to acting on it.

**Session cron:** session-scoped, **50 tasks per session**, recurring ones **expire 7 days after
creation** (firing once more, then deleting themselves). Jitter is deterministic from the task ID —
recurring up to 30 minutes late, or half the interval below hourly; one-shots at `:00`/`:30` up to
90 seconds early. `CLAUDE_CODE_DISABLE_CRON=1` disables the scheduler **and `/loop`**.

**`/loop` has three shapes:** interval + prompt runs on cron; prompt only lets Claude pick a delay
between one minute and one hour each iteration; neither runs the built-in maintenance prompt, or
your `.claude/loop.md` / `~/.claude/loop.md` if one exists (project wins; content past 25,000 bytes
is truncated). `Esc` stops a self-paced loop.

**A scheduled fire only runs skills Claude may invoke on its own.** Skills marked
`disable-model-invocation: true` — **including the bundled `/verify`** — plus built-in commands,
`skillOverrides`-hidden skills, `Skill` deny rules and MCP prompts all arrive as plain text instead
of executing.

**Provider fallback:** on Bedrock, Claude Platform on AWS, Agent Platform and Foundry, `/schedule`
is unavailable and the docs direct you to `/loop`. Dynamic `/loop` intervals and the maintenance
prompt need **v2.1.248+** on those providers.

---

## 9. Dynamic workflows

`/deep-research` is the **only** bundled workflow. `documented`, 2026-09-02.

**Availability:** all paid plans, with Anthropic API access, and on Bedrock, Agent Platform and
Foundry. **On Pro you must turn it on** from the Dynamic workflows row in `/config`. Available in
CLI, Desktop, IDE extensions, `claude -p` and the Agent SDK.

**Writing your own:** the keyword `ultracode`, or asking in your own words. **The keyword is an
opt-in only from human input** — it does not fire from `-p`, an unstamped SDK prompt, a scheduled
task, or a webhook/PR comment relayed into the conversation (before v2.1.210 it did). `/effort
ultracode` makes Claude plan a workflow for every substantive task.

**Runtime caps:**

| Cap | Value |
|---|---|
| Concurrent agents | **16**, fewer on fewer CPUs |
| Items per `parallel()` / `pipeline()` | **4,096** — a longer list is a hard error, not a silent truncation |
| Agents per run | **1,000** |
| Size guideline | `unrestricted` / `small` <5 / `medium` <15 / `large` <50. **Default `medium`** (v2.1.219+) |
| Large-run warning | >25 agents or projected >1.5M tokens. Advisory; suppressed under ultracode |

`Date.now()`, `Math.random()` and argless `new Date()` **throw** inside a script, so a relaunched
run repeats the same agent calls.

**Off:** `/config` → Dynamic workflows, `"disableWorkflows": true` (settings or managed), or
`CLAUDE_CODE_DISABLE_WORKFLOWS=1`. When off, bundled workflow commands and `/workflow-authoring`
disappear, the keyword stops triggering, and `ultracode` leaves the `/effort` menu.

---

## 10. Permission modes

`documented`, [permissions](https://code.claude.com/docs/en/permissions),
[sandboxing](https://code.claude.com/docs/en/sandboxing), [permission
modes](https://code.claude.com/docs/en/permission-modes), and [Desktop managed
settings](https://code.claude.com/docs/en/desktop), retrieved 2026-09-04. **This is the most
load-bearing default in this file** — in auto mode a
classifier reviews actions instead of you, so an artifact can publish and a workflow can launch
without a prompt you see.

| Mode | Runs without asking |
|---|---|
| `default` (shown as **Manual**; `manual` accepted as an alias) | Reads only |
| `acceptEdits` | Reads, file edits, common filesystem commands |
| `plan` | Reads, plus classifier-approved commands where auto mode is available |
| `auto` | Everything, with background safety checks by a classifier |
| `dontAsk` | Only pre-approved tools |
| `bypassPermissions` | Everything |

**The starting mode is `auto` on Pro, Max and Team in the terminal and VS Code** — requiring
**v2.1.228+** on macOS/Linux/WSL and **v2.1.233+ on native Windows**; earlier versions start in
Manual. Enterprise, API/third-party providers, headless SDK use, disabled feature-flag fetching,
first-run cases, and explicit settings fall back to or retain `default`/Manual. Managed
`disableAutoMode` removes Auto mode from the selector. On Bedrock, Agent Platform and Foundry the
starting mode is Manual and auto mode supports only Sonnet 5, Opus 4.7+ and the Fable models.

**No mode auto-approves** explicit ask rules, org-`ask` connector tools, `AskUserQuestion` and MCP
tools marked `requiresUserInteraction`, `rm`/`rmdir` against a critical path, or the cross-session
messaging safeguards. Writes to protected paths are never auto-approved outside
`bypassPermissions`.

### Enforcement boundary

Treat guidance, permission rules, and the OS sandbox as three different layers. `CLAUDE.md` and
skills are advisory. Permission `deny`/`ask` rules govern Claude Code tools, and hook `allow`
decisions cannot override them. The OS sandbox applies to Bash and its child processes; this
matters because Read/Edit deny rules do **not** stop a Python, Node, or other subprocess from opening
the same file.

Sandbox filesystem isolation protects Claude configuration, skills, agents, commands, hooks,
`.mcp.json`, workflow and scheduled-task definitions, and Git hooks/config as protected paths.
Command sandboxing supports macOS, Linux, and WSL2, **not native Windows**. Because sandbox startup
can otherwise fall back to an unsandboxed command, managed deployments that require the boundary
should set `failIfUnavailable: true` and `allowUnsandboxedCommands: false`.

> **A silently-denied shell call reads as a passing verification.** A mode that blocks Bash stops
> the agent running your tests, and it will "verify" by reading code instead. Nothing raises an
> error. `/fewer-permission-prompts` exists partly for this.

---

## 11. Artifacts

`documented`, 2026-09-02. **On by default where eligible.**

**Requirements — all must hold:**

| Requirement | Condition |
|---|---|
| Plan | Pro, Max, Team or Enterprise. **On Enterprise an Owner must enable it**; on Team it is on by default. Enterprise RBAC can scope it per role |
| Auth | claude.ai account via `/login`. API keys, gateway tokens and cloud-provider credentials **cannot publish**. Claude Tag publishes through the agent's identity |
| Provider | Anthropic API only |
| Org policy | CMEK, HIPAA and ZDR must not be enabled |
| Surface | CLI 2.1.183+ or Desktop 1.13576.0+. **Off by default in Agent SDK, GitHub Action and MCP-server contexts**, and when `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set. **Cloud sessions are not a publishing surface** |

**Page constraints:** one self-contained page under a strict CSP; no backend; `.html`, `.htm` or
`.md`; rendered page ≤ **16 MiB**.

**External hosts — narrower than it looks, and verified because it looks wrong.** The CSP allows
Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`) **plus four public CDN hosts for
scripts**: `cdnjs.cloudflare.com`, `cdn.jsdelivr.net` (selected paths such as `/npm/`),
`cdn.tailwindcss.com`, `code.jquery.com` — and no other external host. Every external image is
blocked, as are all other external scripts, stylesheets and fonts; `fetch`, XHR and WebSocket reach
only the page's own origin and the Google Fonts hosts. **A blocked font falls back; a blocked
library does not.**

**Live data:** an artifact can call claude.ai MCP connectors on view (v2.1.209+), through *the
viewing account's* connections, each viewer approving first. Local `.mcp.json` servers can supply
data while Claude builds the page but cannot be called from it. **A connector-backed artifact
cannot be shared to a public link on any plan.**

**Sharing, versions, comments:** a new artifact is private. Team/Enterprise can share within the
org or, once an Owner enables **External sharing**, publicly; on Pro/Max a public link is the only
route. Each publish is a **version**. Team/Enterprise can promote a viewer to **editor**.
**Comments** need v2.1.221+, Team/Enterprise and an org-shared artifact; Claude replies to or
resolves only a thread a person **activated**. From v2.1.228 a publishing session watches its
artifact and can auto-reply subject to permission mode, stopping after **60 sent comments or
activations per artifact per hour**. Public artifacts cannot take comments.

**Disable:** `"enableArtifact": false` is current; **`"disableArtifact": true` is deprecated** but
still works. Also `/config` → Artifacts, `CLAUDE_CODE_DISABLE_ARTIFACT=1`, or `Artifact` in
`permissions.deny`. Once off via `--settings`, the env var or managed settings, **no settings file
turns it back on** (v2.1.242+, which also added honouring the key in project settings, where `true`
never re-enables).

**Org:** retention set separately for private and shared artifacts; audit-log events under
`claude_artifact_*`; **Compliance API** endpoints to list, retrieve a version and delete. The
viewer loads each artifact from a sandboxed **`*.claudeusercontent.com`** origin — allowlist it
alongside `claude.ai` if you restrict outbound access.

`CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0` stops the browser opening on publish; `Ctrl+]` reopens the most
recent.

---

## 12. MCP, connectors and the IDE server

**Built in:** the MCP client, all four transports (stdio, HTTP, SSE, WebSocket), installation
scopes, tool search, elicitation handling, automatic reconnection, output limits. **Zero servers
preinstalled.**

Three things are effectively built-in servers:

| Server | Where | Setup |
|---|---|---|
| **`ide`** | **VS Code and JetBrains extensions** | Auto-connects — see below |
| `computer-use` | macOS CLI, appears under `/mcp` | Enable computer use |
| Claude Code itself | `claude mcp serve` | Exposes Claude Code as an MCP server to other clients |

**Manual:** `claude mcp add` (remote HTTP, remote SSE, local stdio, remote WebSocket); `.mcp.json`
(project), `~/.claude.json` (user/local); `claude mcp add-from-claude-desktop` (macOS, WSL);
plugin-provided servers; enterprise `managed-mcp.json` or policy (`allowedMcpServers`,
`deniedMcpServers`, `allowManagedMcpServersOnly`). **MCP prompts appear as commands**
(`/mcp__github__list_prs`).

### The `ide` MCP server — both IDEs, and hidden

> *"The server is named `ide` and is hidden from `/mcp` because there's nothing to configure. If
> your organization uses a `PreToolUse` hook to allowlist MCP tools, though, you'll need to know it
> exists."* — VS Code and JetBrains pages, retrieved 2026-09-02

| | VS Code | JetBrains |
|---|---|---|
| Tools hosted | about a dozen | several |
| **Visible to the model** | **two** | **one** — `mcp__ide__getDiagnostics` (read-only) |
| Code execution exposed | Jupyter cell execution | **none** |
| Listening interface | `127.0.0.1`, random port 10000–65535 | OS-assigned ephemeral port; an **`Accept connections from all network interfaces`** setting can bind it to the LAN |

Transport is unencrypted `ws://`, authenticated by a token in a lock file at
`~/.claude/ide/<port>.lock` (`$CLAUDE_CONFIG_DIR/ide/` when set), sent as
`X-Claude-Code-Ide-Authorization`. On loopback that is fine; **turning on JetBrains' all-interfaces
setting puts the session traffic and that token on the local network in cleartext.**

**Selection context is a data-egress path.** While connected, the CLI attaches your current editor
selection and the active file's path to every prompt. A matching **`Read` deny rule** suppresses
both.

**Connectors** are MCP servers with a graphical setup flow, requiring claude.ai as the *active* auth
method. Desktop's `+` button works in **local and SSH sessions only** — not WSL. In local and SSH
Desktop sessions the app delivers connectors to Claude Code directly, so **no MCP setting or
`managed-mcp.json` reaches them**; block them with organization connector tool controls instead.
Kill switch: `disableClaudeAiConnectors`.

**Desktop MCP precedence, which departs from the CLI:** the Code tab also loads
`claude_desktop_config.json`, and on a name clash **that definition wins**. For stdio servers
defined at the top level of `~/.claude.json` *and* in `.mcp.json`, the Code tab uses
**`~/.claude.json`** — the reverse of the CLI scope hierarchy. The standalone CLI does not read
`claude_desktop_config.json` at all.

**Provider caveat:** tool search is off by default when `ANTHROPIC_BASE_URL` points at a
non-first-party host, and unsupported on Agent Platform models earlier than Claude 4.5 and on
Foundry deployments hosted on Azure.

---

## 13. Installable — official

Claude Code addresses plugin skills as **`plugin:skill`**. The namespace is load-bearing: a project
skill named `pdf` **cannot** shadow `anthropic-skills:pdf`.

**The official marketplace (`claude-plugins-official`) is added automatically** the first time
Claude Code starts interactively. **Nothing is installed by default.** Fallback:
`/plugin marketplace add anthropics/claude-plugins-official`.

### Code intelligence — 11 LSP plugins

`clangd-lsp` · `csharp-lsp` · `gopls-lsp` · `jdtls-lsp` · `kotlin-lsp` · `lua-lsp` · `php-lsp` ·
`pyright-lsp` · `rust-analyzer-lsp` · `swift-lsp` · `typescript-lsp`

**You install the language-server binary yourself; the plugin does not.** They give automatic
post-edit diagnostics and code navigation. **Cloud sessions do not start plugin language servers**,
so there is no LSP tool there.

### Other official plugins

*Integrations (pre-configured MCP servers):* `github`, `gitlab` · `atlassian`, `asana`, `linear`,
`notion` · `figma` · `vercel`, `firebase`, `supabase` · `slack` · `sentry`
*Security:* `security-guidance` (per-edit, end-of-turn and pre-commit review), `claude-security`
(codebase scan and fix)
*Workflows:* `commit-commands`, `pr-review-toolkit`, `agent-sdk-dev`, `plugin-dev`, `skill-creator`
*Output styles:* `explanatory-output-style`, `learning-output-style`

> **`skill-creator` is not built in.** It is a plugin —
> `/plugin install skill-creator@claude-plugins-official`. It *is* pre-listed as an activatable
> example skill on claude.ai / Cowork, which is why the confusion is common.

### Marketplaces and scopes

| Marketplace | Add with | Notes |
|---|---|---|
| Official | *auto-added* | Auto-update on by default |
| Community | `/plugin marketplace add anthropics/claude-plugins-community` | Install with `@claude-community`; pinned to commit SHAs |
| Demo | `/plugin marketplace add anthropics/claude-code` | Example plugins |
| Your own | GitHub `owner/repo`, git URL, local path, or remote `marketplace.json` | Auto-update off by default |

**Scopes:** user, project (`.claude/settings.json`, shared), local (this repo, just you), managed
(admin-pushed, immutable). `/plugin` in the CLI; plugin browser UI in Desktop and VS Code;
`claude plugin install` for scripting. **Not available in cloud sessions, WSL sessions, or mobile**
— for cloud, declare under `enabledPlugins` in the repo's `.claude/settings.json`.

### Plugin skills seen in this session

`anthropic-skills:docx` · `xlsx` · `pptx` · `pdf` · `skill-creator` · `schedule` · `morning` ·
`consolidate-memory` · `import-memory` · `explain-usage` · `setup-cowork`

> **`schedule` exists in both tiers** — bare `schedule` *and* `anthropic-skills:schedule`. Two live
> skills under one bare name, which is evidence the bundled set is not curated against the plugin
> set.

---

## 14. Channels

**Nothing built in.** A channel is an MCP server that pushes external events into a running
session; you install one as a plugin and configure it with your own credentials.

Research preview: **Telegram, Discord, iMessage**, plus `fakechat` (an officially supported
localhost demo with nothing to authenticate). **Prerequisite: Bun** — the pre-built channel plugins
are Bun scripts. **Auth: claude.ai or Console API key only; not available on Bedrock, Claude
Platform on AWS, Agent Platform or Foundry.** Team and Enterprise must enable them
(`channelsEnabled`, `allowedChannelPlugins`). Each approved plugin keeps a sender allowlist;
Telegram and Discord bootstrap it by pairing. **Being in `.mcp.json` is not enough — the server
must also be named in `--channels`.**

---

## 15. Skill loading, precedence, and where it differs by surface

**Precedence:** enterprise > personal > project. Any of those overrides a bundled skill of the same
name **but not its aliases** — a project `code-review` skill replaces the bundled `/code-review`,
and typing `/review` never reaches yours. Plugin skills are namespaced so they never collide. Local
skills override claude.ai-synced skills, and Claude Code **skips** a synced skill whose name matches
any other command, **reserving its own built-in and bundled names even when they are unavailable in
the session**.

> This replacement is **silent**. It is what `check.py`'s `RESERVED_CLAUDE` set guards and why
> `AGENTS.md` requires the `hr-` prefix. The blocklist is a lower bound; **the prefix is the actual
> protection.**

**Per surface:**

- CLI, Desktop local/SSH, IDE — read the filesystem locations
- **Cowork, cloud sessions and routines do not read `~/.claude/skills/`.** They load the skills
  enabled for your claude.ai account, synced at session start; cloud sessions additionally load
  project skills from the cloned repo
- **Desktop scheduled tasks are the exception** — they run locally and see local skills
- Pull account skills down once with
  `CLAUDE_CODE_SYNC_SKILLS=1 claude -p "List the skills you have available"` → `~/.claude/skills/synced/`

**Frontmatter portability:** Claude Code accepts every field. claude.ai uploads, the Skills API and
`package_skill.py` accept only the six Agent Skills spec fields — `name`, `description`, `license`,
`compatibility`, `metadata`, `allowed-tools`. Anything else is a hard error on upload.

---

## 16. Availability by plan and provider

`documented`, 2026-09-02.

| Feature | Pro | Max | Team | Enterprise |
|---|---|---|---|---|
| Claude Code on the web | ✅ | ✅ | ✅ | ✅ premium or Chat + Code seat |
| Routines | ✅ | ✅ | ✅ | ✅ |
| Remote Control | ✅ | ✅ | Admin-enabled | Admin-enabled |
| Channels | ✅ | ✅ | Admin-enabled | Admin-enabled |
| Computer use | ✅ | ✅ | ❌ | ❌ |
| Dispatch | ✅ | ✅ | ❌ | ❌ |
| Code Review | ❌ | ❌ | ✅ | ✅ |
| Artifacts | ✅ | ✅ | ✅ | Admin-enabled |
| Analytics dashboard | ❌ | ❌ | ✅ | ✅ |
| Enterprise Analytics API | ❌ | ❌ | ❌ | ✅ |
| Server-managed settings | ❌ | ❌ | ✅ | ✅ |
| SSO | ❌ | ❌ | ✅ | ✅ |
| SCIM · Compliance API · ZDR | ❌ | ❌ | ❌ | ✅ |

**Requires a claude.ai login** — not reachable with a Console API key or a third-party provider:
Claude Code on the web, on mobile and in Slack; Claude Code Desktop; Routines; Ultrareview; Code
Review; Remote Control; the Chrome extension; computer use; Artifacts; voice dictation.

**Works on every provider:** CLI and Agent SDK; VS Code and JetBrains; subagents, hooks, commands
and skills; `CLAUDE.md` memory, plugins and MCP servers; checkpoints, sandboxing and **workflows**;
OpenTelemetry metrics and the managed settings file.

**Provider-specific differences:** claude.ai connectors load only when a claude.ai subscription is
the active auth method · Explore caps at Opus on the Claude API and inherits directly elsewhere ·
`/design-sync` and `/import` are unavailable on Bedrock, Agent Platform, Foundry and Claude Platform
on AWS · `/voice` needs claude.ai · `/list-agents` needs cross-session messaging.

**Cross-session messaging version floors:** v2.1.224+ on macOS/Linux/WSL2, **v2.1.234+ on native
Windows**, **v2.1.248+ on third-party providers**. Same-machine only on API keys and 3P providers.

---

## 17. Other built-ins, on by default

| Feature | Notes |
|---|---|
| Checkpoints / `/rewind` | Automatic file tracking; **does not cover bash changes, subagent edits, or external changes** |
| Sandboxing | OS-level filesystem and network isolation; `/sandbox` toggle |
| Worktree isolation | Automatic in Desktop; `--worktree` in CLI |
| Extended thinking | On |
| Auto-compaction | On; `/autocompact` tunes the window. **Project-root `CLAUDE.md` survives compaction** and is re-read from disk; nested files and path-scoped rules reload as Claude reads matching files |
| Prompt caching | On; `promptCacheTtl`. Workflow agents default to a 5-minute TTL — `subagentPromptCacheTtl: "1h"` changes it |
| Session recap, task list, `/btw` | On |

**Manual setup:** agent teams (must be enabled; **CLI only** `(unverified — not re-checked)`) ·
Code Review on every PR (GitHub App, Team/Enterprise) · GitHub Actions · GitLab CI/CD (**not on
Foundry**) · Slack · Remote Control · computer use (macOS Accessibility and Screen Recording
grants, Pro/Max) · voice · fast mode (Owner-enabled on Team/Enterprise, provisioned on Console,
**not on any 3P provider**) · advisor (Anthropic API and Console only) · self-hosted environments ·
LLM gateway · OpenTelemetry · status line · deep links.

---

## 18. Adjacent products, and where they diverge

Two Anthropic products sit next to Claude Code, share vocabulary with it, and behave differently.
Both are in scope for this file only where they touch a repository or a `.claude/` directory.

### Cowork

**Not Claude Code.** A sibling product in the same desktop shell. Built in: the tab, plus native
document production (Excel with functional formulas, PowerPoint, formatted documents).

**Everything else is opt-in through Customize**, which syncs through your claude.ai account and
**not from `~/.claude`**. To use a skill or plugin that exists only in `~/.claude`, add it in
Customize.

**Dispatch** bridges the two: development work spawns a Code session with a **Dispatch** badge;
research, document and spreadsheet work stays in Cowork. **Pro or Max only** — not Team or
Enterprise.

**Enterprise:** in a Cowork session on your machine Claude Code **never fetches admin-console
settings**, even signed in with a Team or Enterprise account. Remote Cowork sessions receive
neither device-deployed nor admin-console policy. Cowork also skips user-scope memory imports that
resolve outside the working directory, and a symlinked `~/.claude/CLAUDE.md`.

### Managed Agents — a consumer of `.claude/skills/` that is not a coding agent

`documented`, `platform.claude.com/docs/en/managed-agents/*`, retrieved 2026-09-02. Not Claude Code,
but it **reads the same skill directory this repository installs into**, which is why it is here.

**Skills reach an agent two ways, and only one of them needs configuring:**

| Path | Setup |
|---|---|
| **Attached** — an entry in the agent's `skills` array | `type` (`anthropic` or `custom`), `skill_id`, optional `version` defaulting to `latest`. Pre-built Anthropic skills (`pptx`, `xlsx`, `docx`, `pdf`) are **present in every workspace and need no upload**, but must still be attached |
| **Repository** — the mounted repo's root `.claude/skills` | *"No upload and no entry in the agent's `skills` array are required."* Scanned at session start |

A session supports up to **500 skills**, deduplicated across every agent in it; mounting more slows
sandbox start.

**Repository discovery is stricter than any coding agent's, and `install.py` already satisfies it:**

| Rule | Effect |
|---|---|
| Exactly `.claude/skills/<name>/SKILL.md`, **one level deep at the repo root** | A bare `SKILL.md`, anything nested deeper, or a `skills/` outside `.claude` is not discovered. A `.claude/skills` inside a package subdirectory is not announced at session start |
| Scanned **once, at session start** | Commits pushed mid-session are not picked up |
| Requires the toolset's **`read`** tool | An agent with `read` disabled loads no repository skills |
| **Cloud sandboxes only** | Self-hosted sandboxes do not support GitHub repository resources |
| Follows the **checked-out state** | The `checkout` branch or commit when the resource sets one, otherwise the repository's default branch. **A skill on `main` is not loaded by a session pinned to a tag** |
| Name clash with an attached skill | **Both stay available**, each announced with its own path |

> ⚠️ **Anthropic's own trust warning:** repository skills are agent instructions, so a mounted
> repository is part of the agent's trust boundary. Anyone who can commit to it — including through
> a merged external pull request — can add or change a skill, **the platform loads it at session
> start without a review step**, and session tools such as `bash` and `web_fetch` give those
> instructions real reach. Review `.claude/skills` before mounting a repository that accepts outside
> contributions.
>
> The portable-layer consequence — that this makes a ninth consumer of a checked-in `SKILL.md`, and
> what that does to the portability argument — is in `research/MATRIX.md` §2 and
> `research/PORTABILITY.md`. Not repeated here.

**The built-in toolset is `agent_toolset_20260401`, and every tool in it is on by default** when the
toolset is included in an agent's configuration:

| Tool | Name | Notes |
|---|---|---|
| Bash | `bash` | |
| Read | `read` | **Also what repository skill discovery depends on** |
| Write | `write` | |
| Edit | `edit` | |
| Glob | `glob` | |
| Grep | `grep` | |
| Web fetch | `web_fetch` | |
| Web search | `web_search` | |

**The default is on, so the safe pattern is to invert it.** `default_config: {"enabled": false}`
turns everything off and per-tool `configs` entries enable only what the agent needs.

`web_search` and `web_fetch` take `allowed_domains` / `blocked_domains` (1–64 entries, ASCII
hostnames, no path for `web_fetch`, the two mutually exclusive on one entry). **An environment's own
`networking` settings do not restrict them**, because both run on Anthropic's servers rather than in
the sandbox — the per-tool lists are the only control. Tool output over **100,000 characters** is
written to a sandbox file and the model gets a truncated preview with the path.

---

## 19. Surface gotchas

1. **The prompt/process split predicts most of it.** Anything that is *a prompt* — bundled skills,
   built-in subagents, `/deep-research` — ships and works on every provider. Anything touching *an
   external process or service* — LSP binaries, MCP servers, connectors, channels, the Chrome
   extension, Bun — is opt-in and usually carries a claude.ai or binary prerequisite.
2. **Local vs account configuration.** CLI, Desktop local/SSH and the IDEs read `~/.claude` and the
   project's `.claude/`. Cowork, cloud sessions and routines read your **claude.ai account**. A
   personal skill in `~/.claude/skills/` reports as not found when a routine invokes it.
3. **Desktop scheduled tasks ≠ routines.** Same sidebar, **Local** and **Cloud**; different runtime
   and different skills.
4. **Cloud sessions are the most restricted surface** — no plugin browser, no LSP servers, no
   artifacts, no `@mention` files, no file pane, no bypass-permissions mode, no `~/.claude` reads.
5. **WSL sessions are quietly limited** — no connector `+` button, no plugins, no `@mention`.
6. **Connectors bypass MCP policy in Desktop** local and SSH sessions.
7. **Third-party providers lose the whole claude.ai feature class**, but **Desktop is available**
   via *Claude Desktop on 3P* and, on Agent Platform, managed settings — the docs grade it
   **partial support**, not absent.
8. **Enterprise defaults differ from Team.** Artifacts on by default on Team, Owner-enabled on
   Enterprise where RBAC can also scope them per role.

---

## 20. How to enumerate this yourself

For **skills and commands** there is no command that prints the inventory. Ask the session directly
and read the `/` picker — weak evidence, since the model reports on itself and feature flags change
what is present. **For "is this bundled?", read the commands reference's `Skill` marker instead.**

For **instruction files** the tooling is better than Codex's:

- **`/context`** lists what loaded, under **Memory files**. The documented way to confirm a
  `CLAUDE.md` or `@AGENTS.md` import took effect.
- The **`InstructionsLoaded` hook** fires per instruction file with a load-reason matcher, so you
  can log exactly which file loaded, when, and **why**.
- **`/doctor`** reports installation health and unused skills, and proposes trims for a checked-in
  `CLAUDE.md`.
