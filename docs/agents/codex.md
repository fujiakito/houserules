# Codex

**Measured:** `codex-cli 0.151.0-alpha.7.2`, 2026-08-31, on **CLI** (`codex --help`,
`codex plugin list`, `codex debug prompt-input`, `ls $CODEX_HOME/skills/.system/`) and the
**desktop app** (its own `/` and `$` pickers). **IDE extension: not checked.**
**Documentation:** `learn.chatgpt.com/docs`, `help.openai.com`, `developers.openai.com`,
`github.com/openai/plugins`. Pages read for this file were retrieved **2026-08-31 to 2026-09-02**;
each section names its date where it matters.

## Evidence grades used in this file

| Grade | Means |
|---|---|
| **`tested`** | Run on the installation above, version recorded |
| **`documented`** | Official vendor page, retrieval date recorded. **Not run** |
| ⚠️ **`disputed`** | Two official pages disagree. Both readings kept, neither picked silently |
| `(unverified)` | Carried forward without a source |

> **Every list here is a lower bound.** Absence means "not recorded", not "not there". See
> [README](README.md).
>
> **The binary is versioned.** `bin/codex.exe` reported `0.130.0-alpha.5` on this machine while the
> live one under `bin/<hash>/codex.exe` was `0.151.0-alpha.7.2`. Check the hashed path.
>
> **Reading is not running, and here it mattered three times.** `codex review`, `codex apply` and
> `codex debug prompt-input` are **not on the official CLI page**; the `.system/` skill set and the
> contents of `openai-bundled` both differ from what the documentation and the issue tracker
> report. Every one of those was settled by running the tool.

### The documentation moved, and not by a uniform rule

`developers.openai.com/codex/*` issues a **308** into `learn.chatgpt.com`, which is canonical. It is
**not** a prefix swap — measured 2026-09-02:

| From | To |
|---|---|
| `developers.openai.com/codex/cli` | `learn.chatgpt.com/docs/**codex**/cli` — gains a segment |
| `developers.openai.com/codex/plugins` | `learn.chatgpt.com/docs/plugins` — does not |

`learn.chatgpt.com/docs/codex/plugins` returns **404**. Follow each redirect; do not rewrite by
pattern. Markdown versions exist by appending `.md`; the index is at `learn.chatgpt.com/llms.txt`.

---

## 1. Surfaces

Codex is a mode inside the unified ChatGPT desktop app, alongside Chat and Work. `documented`.

| Surface | What it is | Notes |
|---|---|---|
| **Desktop (Codex mode)** | The broadest native surface | Repositories, integrated terminal, Git UX, in-app Browser, Local Environments, managed Worktrees, plugins, skills, Pets, optional Computer Use. macOS, Windows, Linux. **Bundles its own CLI** |
| **CLI** | Terminal-native agent, Apache-2.0 | Repository context, shell execution, skills, plugins, MCP, web search, hooks, non-interactive automation |
| **IDE extension** | VS Code-compatible; JetBrains and Xcode integrations exist | Same agent and the same `~/.codex/config.toml` as the CLI. **Plugins are not available here** — see section 5 |
| **Cloud / web** | `chatgpt.com/codex` | Parallel cloud chats against a connected repo |
| **Mobile / Remote** | Codex interface inside the ChatGPT apps | **A remote client, not a runtime.** Reaches Codex work running on a connected host; project files, shell, plugins and tests stay there |
| **SDK / App Server** | TypeScript `@openai/codex-sdk` (Node 18+), Python `openai-codex` (3.10+) | Drive the local app-server over JSON-RPC |
| **Browser extension** | Chromium companion | Separate install; uses your existing profile, tabs and sessions. **Distinct from the desktop in-app Browser** |

**Install (CLI):** `curl -fsSL https://chatgpt.com/codex/install.sh | sh` · PowerShell `irm
https://chatgpt.com/codex/install.ps1 | iex` · `npm i -g @openai/codex` · `brew install --cask codex`

**Alternative backend — Amazon Bedrock.** Supports local CLI, desktop and IDE workflows but **drops**
image generation, voice transcription for input, the cloud plugin store, cloud configuration and
policy management, and **all Codex cloud agents** (review, security, web). MCP namespace tools and
tool search are also unavailable, limiting tool discovery.

---

## 2. Commands

### Slash commands (in-session)

Descriptions marked **app** are read off the desktop app's own menu; the official reference names
these commands but does not describe them. `tested` unless noted.

| Command | Does what |
|---|---|
| `/init` | **"Create an `AGENTS.md` file with instructions for Codex"** (app) |
| `/goal` | "Set a goal to keep pursuing" — persists across turns (app). `features.goals` is on by default |
| `/code review` | "Review uncommitted changes or compare against a branch" (app) |
| `/plan mode` | "Turn plan mode on" (app) |
| `/new playground worktree` | "Run this chat in a new worktree" (app) |
| `/skills` | List available skills. `documented` — the skills page pairs it with `$` mention |
| `/pet`, `/pets` | Open the pet picker; `/pets <name>` chooses directly, `/pets off` disables. **Not in the official command reference at all**, but documented on the Pets page |
| `/chat` | "Don't work in a project" (app) |
| `/model`, `/reasoning` | Model and reasoning-effort selection (app) |
| `/agent`, `/subagents` | Switch the active agent thread |
| `/plugins` | Browse installed and discoverable plugins |
| `/hooks` | View, manage and **trust** lifecycle hooks |
| `/apps` | Browse connectors and insert them into a prompt |
| `/mcp` | Show MCP server status |
| `/permissions` | Set what Codex can do without asking |
| `/personality` | Personality selection; `features.personality` is on by default |
| `/ide` | Include open files, selection and other IDE context |
| `/keymap`, `/vim` | Remap TUI shortcuts; toggle Vim mode |
| `/setup-default-sandbox` | Set up the elevated agent sandbox (**Windows only**) |
| `/sandbox-add-read-dir` | Grant sandbox read access to an extra directory |
| `/clear`, `/rename`, `/archive`, `/delete` | Session lifecycle |
| `/resume`, `/title`, `/copy`, `/stop`, `/status`, `/feedback`, `/help` | Session utilities |

**Skills are invoked with `$`, session commands with `/`.** `$skill-installer`, not
`/skill-installer`. In ChatGPT Work the same skill is `@skill-creator`.

### CLI subcommands

`tested` — **`codex review`, `codex apply` and `codex debug` are not on the official CLI page.**

| Command | Does what |
|---|---|
| `codex exec` (`e`) | Run Codex non-interactively. `--json` JSONL streaming; read-only by default, `--full-auto` for edits, `--sandbox danger-full-access` for networked commands. Needs a Git repo unless `--skip-git-repo-check` |
| `codex review` | **Code review as a non-interactive subcommand** — `--uncommitted`, `--base <BRANCH>`, `--commit <SHA>`, `--title`, plus free-text instructions. **Has an exit code, so it drops into CI.** Delegates to the `review-agent` built-in skill |
| `codex apply` (`a`) | "Apply the latest diff generated by a Codex **cloud** chat to your local working tree." Takes a cloud task ID — **not** a local-session diff |
| `codex sandbox` | Run arbitrary commands inside Codex's sandbox |
| `codex mcp` | **Manage external MCP servers** — add local or remote servers, authenticate, inspect the tools available to the session |
| ~~`codex mcp-server`~~ | **Deprecated** — "Use the Codex app server instead." This was the one that exposed Codex *as* an MCP server; for existing integrations the docs point to the Codex plugin for Claude Code |
| `codex plugin` | `add`, `list`, `remove`, `marketplace …` |
| `codex features` | Inspect feature flags |
| `codex debug` | `models`, `app-server`, **`prompt-input`** — see section 12 |
| `codex doctor` | Diagnostics for startup, connectivity, performance |
| `codex resume`, `codex fork` | Resume or fork a previous session |
| `codex cloud` | Browse Codex Cloud tasks and apply results locally (experimental) |
| `codex app-server`, `remote-control`, `exec-server` | Headless and remote operation (experimental). App server is a stateful JSON-RPC 2.0 process hosting agent threads; it backs the VS Code extension and JetBrains plugin |
| `codex login`/`logout`, `update`, `completion`, `app` | Account, updates, shell completion, launch the desktop app |

**GitHub Action:** `openai/codex-action@v1` — installs the CLI, starts a Responses API proxy, runs
`codex exec` under specified permissions. Use `CODEX_API_KEY` scoped to the single invocation.

---

## 3. Built-in skills

Bundled by OpenAI. On disk at `$CODEX_HOME/skills/.system/`, stamped with a
`.codex-system-skills.marker` — **that marker, not the directory, is how you tell a built-in from
something you installed.** `tested`.

| Skill | Does what |
|---|---|
| `skill-creator` | Create or update a skill. Ships `init_skill.py`, `package_skill.py`, `quick_validate.py` |
| `skill-installer` | Install curated skills from `openai/skills` or another repo |
| `plugin-creator` | Scaffold a plugin directory and marketplace entry |
| `openai-docs` | OpenAI and Codex documentation, including Codex's own self-knowledge |
| `imagegen` | Generate or edit raster images |
| `review-agent` | Read-only, defect-first review of a change. **Not user-invocable** — its own description says to use it when another agent **delegates** review, and it does not appear in the model-visible skill list. **It is what `codex review` delegates to** |

Also bundled, installed on demand: **`hatch-pet`** — creating a custom Pet *"installs the bundled
`hatch-pet` skill, reloads skills, and opens a new chat"*. `documented`, 2026-09-02.

> **Three sources give three different lists, and all three are right.**
>
> | Source | Reports |
> |---|---|
> | Official documentation | Skill Creator, Skill Installer, **Atlas Control (macOS)**, **Exec Plan**, **GitHub Fix CI**, **Linear**, OpenAI Docs |
> | This measured Windows install | imagegen, openai-docs, plugin-creator, review-agent, skill-creator, skill-installer |
> | The issue tracker | a third, shorter set |
>
> **Only three names overlap.** The set varies by platform and version, so none is canonical and
> the disagreement is not an error in any of them. Check the machine you care about:
> `ls $CODEX_HOME/skills/.system/`. **`skill-creator` alone is documented as present by default.**

**Not built in:** `linear`, `gh-fix-ci`, `yeet`, `exec-plan`, `atlas-control` and similar names
appear in the docs as *examples of what a Skills page can contain*, not as defaults. Curated ones
install via `$skill-installer`; others arrive through plugins or a hand-written `SKILL.md`.

---

## 4. Tools

Not documented as a list. **`codex debug prompt-input` renders the model-visible prompt including
tool definitions**, which is the way to see them. `features.shell_tool` (the default `shell` tool)
and `features.unified_exec` (PTY-backed, **on except Windows**) are the core execution tools. MCP
servers add tools on top; this installation had `context7` (HTTP) and `node_repl` (local) in
`config.toml`.

---

## 5. Installable — official

Nothing here is available until installed, **however pre-installed it looks**. The desktop app
marks all of it `Personal`, as opposed to `System`.

### Plugins

`/plugins` in-session, or `codex plugin add <name>@<marketplace>`. `tested` unless noted.

| Marketplace | Plugins | Default state |
|---|---|---|
| `openai-primary-runtime` | `documents` (Word/Google Docs), `pdf`, `spreadsheets` (Excel/Sheets, plus `excel-live-control` for a live workbook), `presentations` (PowerPoint/Slides), `template-creator` | **Ship enabled on a normal install** — but still *installed*, not built in |
| `openai-bundled` | `browser` (in-app browser), `chrome` (your real Chrome, with its logged-in state), `visualize` (charts, maps, diagrams, 3D, UI previews), `codex-app-tools`, `computer-use`, `latex` (Tectonic + TeX Live) | Shipped, **not automatically active**. `computer-use` and `latex` were **not installed** on this machine |
| `openai-curated` | ~45 third-party: `linear`, `github`, `slack`, `figma`, `stripe`, `vercel`, `netlify`, `sentry`, `notion`, `posthog`, `shopify`, `glean`, `atlassian-rovo`, `expo`, `zoom`, `box`, `digitalocean`, `hugging-face` … | Mostly MCP wrappers; manual install |
| `openai-curated` | **`codex-security`** | ⚠️ **gated** — see below |

**Three states, not two.** A plugin can be *shipped in the package*, *installed*, and *enabled*, and
only the last means its skills reach the model.

> **⚠️ Plugins are not available in the IDE extension.** *"Plugins aren't available in the IDE
> extension. To browse and install plugins for Codex, use the ChatGPT desktop app or Codex CLI."*
> `documented`, 2026-09-02. The IDE **does** read skills and shares `~/.codex/config.toml` with the
> CLI, so a capability packaged as a plugin can often be delivered there as a plain
> `.agents/skills/<name>/SKILL.md` instead — which is the portable form anyway.

> **A documented startup race.** Codex has been observed to first write a marketplace containing
> only `latex`, uninstall the other bundled plugins as "not in bundled marketplace plugin names",
> then rewrite the full marketplace and reinstall `browser` and `chrome` — **sometimes skipping
> `computer-use`**. Recovery: `codex plugin add computer-use@openai-bundled`. `(unverified)` — from
> the issue tracker, not a documentation page.

**`codex-security`** ⚠️ is the deepest capability either agent has at any stage, and the hardest to
get. Ten skills forming a pipeline: entry points `security-scan`, `deep-security-scan`,
`security-diff-scan`; stages `threat-model` → `finding-discovery` → `attack-path-analysis` →
`validation` → `triage-finding` → `fix-finding`; and `track-findings`, which writes results into
Linear, Jira, GitHub issues or a draft GitHub security advisory.

> **"Running scans requires Codex Security access."** Installing the plugin is not enough. On this
> machine `codex plugin list` reported it `installed, enabled` while its skills were **never
> exposed to the model** — typing `$security-scan` did nothing. Install via the desktop app's
> plugin list, or the separate npm package `npx @openai/codex-security`.

**Enterprise plugin controls.** Admins set a plugin to **Available** (members install it) or
**Installed** (installed by default for that role). These apply across ChatGPT web, mobile, desktop
and Codex; **there is no separate per-surface toggle**. A plugin requiring an app needs that app
enabled for the member's role first.

### Curated skills

`$skill-installer <name>`, or `$skill-installer <owner>/<repo>/<skill>` for a community one. ~40 in
the catalogue, including:

| Skill | Does what |
|---|---|
| `define-goal` | Pin a concrete, measurable goal before work starts |
| `migrate-to-codex` | **Import another agent's instruction files, skills, agents and MCP config** |
| `yeet` | Stage → commit → push → open a PR, in one step |
| `gh-fix-ci`, `gh-address-comments` | Debug failing GitHub Actions; address PR review comments |
| `playwright`, `playwright-interactive` | Browser automation; persistent interactive debugging |
| `screenshot`, `speech`, `transcribe` | Desktop screenshot; text-to-speech; audio transcription with diarization |
| `security-best-practices`, `security-threat-model`, `security-ownership-map` | Language-specific security review; threat modelling; **people-to-file ownership topology from git history** |
| `cli-creator` | Build a composable CLI from API docs or an OpenAPI spec |
| `jupyter-notebook`, `openai-docs`, `aspnet-core`, `winui-app`, `chatgpt-apps` | Stack-specific workflows |
| `vercel-deploy`, `netlify-deploy`, `render-deploy`, `cloudflare-deploy` | Deployment |
| `figma-*` (8), `notion-*` (4), `linear`, `sentry` | Integrations |

> **The catalogue repository is deprecated.** `github.com/openai/skills` now directs users to
> [`openai/plugins`](https://github.com/openai/plugins). A vendored clone (this machine had one at
> `~/.codex/vendor_imports/skills/`, commit `49f948f`, 2026-06-23) may be stale by design.

---

## 6. Extension points

| | Path | Scope |
|---|---|---|
| Instruction file | `AGENTS.md` — see section 7 | project + `~/.codex/AGENTS.md` |
| Skills | `.agents/skills/` | project, user (`~/.agents/skills`), admin (`/etc/codex/skills`) |
| MCP | `[mcp_servers.<name>]` in `config.toml` | project `.codex/config.toml`, user `~/.codex/config.toml` |
| Subagents | `.codex/agents/*.toml` — `name`, `description`, `developer_instructions`, `model`, `sandbox_mode` (`read-only`, `workspace-write`, `danger-full-access`). Built-in types `default`, `worker`, `explorer`. Capped by **`agents.max_concurrent_threads_per_session`** (legacy alias `agents.max_threads`). `max_depth` and `job_max_runtime_seconds` are **not** in the current configuration reference — `(unverified)` | project |
| Hooks | `<repo>/.codex/hooks.json`, `~/.codex/hooks.json`, inline `[hooks]` in either `config.toml`, plus plugin-bundled — see section 8 | project, user, plugin |
| Plugins | `.codex-plugin/plugin.json` + optional `skills/`, `commands/`, `agents/`, **`hooks/hooks.json`**, `.mcp.json`, `.app.json`, `assets/` | marketplace |

### Skills — `.agents/skills/`, and the path Codex authored

`documented`, 2026-09-02. **Precedence, highest first:**

`$CWD/.agents/skills` → parent folders → `$REPO_ROOT/.agents/skills` → `$HOME/.agents/skills` →
`/etc/codex/skills` → built-in.

**`.agents/skills/` is the vendor-neutral path**, and Codex authored the convention — six of eight
agents surveyed in `research/MATRIX.md` §2 now read it.

> **Same-named skills are not merged. Both appear in the selector.** This is the opposite of Claude
> Code, where a project skill silently *replaces* a bundled one. Nothing is lost on Codex, but which
> one runs is a coin flip — and because `.agents/skills/` is shared with Goose and Antigravity, a
> name chosen for one lands in all three. The protection is a **project prefix**; `check.py` guards
> the known names, but the list is a lower bound.

**A skill is a folder with `SKILL.md` carrying `name` and `description` frontmatter.**
Instruction-only is the default shape; scripts are optional. Codex follows symlinked skill folders.
**The `description` is a trigger, not a title** — it decides whether the model selects the skill.
Write it as *use when…*.

### Configuration precedence, and the trust boundary that overrides it

CLI flags and `--config` → profile → project `.codex/config.toml` root-to-cwd → user →
`/etc/codex/config.toml` → defaults. Profiles live at `$CODEX_HOME/profile-name.config.toml`,
selected with `--profile`.

> **A project marked untrusted skips every project-scoped `.codex/` layer** — config, hooks,
> subagents, all of it. **Claude Code has no equivalent boundary**, and it means a `trust_level`
> setting can silently disable extension machinery you assume is loaded.

**Project config cannot override** keys that redirect credentials, alter host-owned app request
metadata, change provider auth, select profiles, or run machine-local notification/telemetry
commands. Ignored project-local keys: `openai_base_url`, `chatgpt_base_url`,
`apps_mcp_product_sku`, `model_provider`, `model_providers`, `notify`, `profile`, `profiles`,
`experimental_realtime_ws_base_url`, `otel`.

---

## 7. `AGENTS.md`

**Codex reads `AGENTS.md` natively — Claude Code does not.** That asymmetry is why this repository
exists; see `research/MATRIX.md` §1.

| Rule | Behaviour |
|---|---|
| Discovery | Every directory level from repo root down to cwd, plus `~/.codex/AGENTS.md` globally |
| Combination | Files **concatenate** — a subdirectory *adds to* the root rather than overriding it |
| Override | `AGENTS.override.md` replaces `AGENTS.md` **at its own level only**; the chain continues above and below |
| Fallbacks | `project_doc_fallback_filenames` — *"Additional filenames to try when `AGENTS.md` is missing"* |
| Budget | `project_doc_max_bytes`, **32 KiB by default and configurable** |

⚠️ **What the budget bounds is disputed between two official pages.** The configuration reference
reads per-file — *"Maximum bytes read from `AGENTS.md` when building project instructions"* — while
the discovery page describes the combined root-to-cwd chain. Both retrieved 2026-09-02.
`check.py` deliberately enforces the **stricter chain reading**, so it is conservative rather than
wrong if the per-file reading is correct. `research/MATRIX.md` §2 carries the full record.

**`project_doc_fallback_filenames` is unmodelled by `check.py` and cannot be.** The setting can live
in `~/.codex/config.toml`, outside the repository entirely, so a repo relying on it has instruction
content the checker never sees. It covers the two default names and says so.

### A gitignored `AGENTS.override.md` is loaded and never reaches review

> *"Codex automatically copies an ignored `AGENTS.override.md` into local managed worktrees, so you
> don't need to list it in `.worktreeinclude`."* — worktrees documentation, retrieved 2026-09-02

Stated as a property rather than a convenience: an `AGENTS.override.md` in `.gitignore` **replaces
the committed `AGENTS.md` at its level, loads into every session, and follows the developer into
every Codex-managed worktree — while being invisible to anyone auditing the repository's agent
instructions, because it is not in the repository.**

Two consequences: **`check.py` scans it on disk and should**, because that measures the chain a
session actually gets rather than the chain that is committed; and **"read the repo to see what the
agent was told" is not a sound check on Codex** — `codex debug prompt-input` is.

Ordinary Git worktrees created from the command line do **not** get this copy.

**HTML comments:** Claude Code strips block-level HTML comments from `CLAUDE.md` before injecting
it. **Codex does not strip them from `AGENTS.md`.** The same `<!-- … -->` block is free on one agent
and billed on the other, every session — which is why `templates/AGENTS.md` tells you to delete its
comment block.

---

## 8. Hooks

`features.hooks` is **on by default** (`features.codex_hooks` is a deprecated alias). `documented`,
event list and blocking set re-read verbatim 2026-09-02.

**11 events:** `SessionStart` · `SessionEnd` · `UserPromptSubmit` · `PreToolUse` ·
`PermissionRequest` · `PostToolUse` · `PreCompact` · `PostCompact` · `SubagentStart` ·
`SubagentStop` · `Stop`

**7 of them can halt a turn** — `PreToolUse` denies a tool call, `PermissionRequest` approves or
denies one, and `UserPromptSubmit`, `PreCompact`, `PostCompact`, `SubagentStop` and `Stop` can
return `continue: false`.

**Handlers:** `command` and `mcp_tool` are supported; **`prompt` and `agent` are parsed but
skipped.**

**Discovery:** `~/.codex/hooks.json`, `~/.codex/config.toml` (inline `[hooks]`),
`<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml`, plus plugin-bundled hooks. **All layers
load cumulatively; none replaces another.**

**Plugin-bundled hooks are at `hooks/hooks.json` inside the plugin root — not a root-level
`hooks.json`.** *"By default, Codex looks for `hooks/hooks.json` inside the plugin root. A plugin
manifest can override that default with a `hooks` entry in `.codex-plugin/plugin.json`"* — which may
be a relative path, several paths, or inline hook objects. **Manifest hook paths resolve relative to
the plugin root and must stay inside it.** Getting this path wrong produces a plugin whose hooks
simply never load, with no error. `documented`, 2026-09-02.

> **Hooks being "enabled by default" does not mean your hooks run.** Before a non-managed command
> hook executes, Codex requires you to **review and trust the exact hook definition**, recording
> trust against its hash — so any edit re-flags it and it is skipped until re-trusted. **Installing
> or enabling a plugin does not auto-trust its bundled hooks.** `/hooks` inspects and trusts them;
> `--dangerously-bypass-hook-trust` is an invocation-scoped escape hatch for headless runs, with no
> durable config equivalent.

---

## 9. Configuration defaults

From the official configuration reference, retrieved 2026-09-02. `documented`.

| Key | Default | Meaning |
|---|---|---|
| `features.hooks` | **on** | Lifecycle hooks |
| `features.memories` | **off** | Memories is opt-in |
| `features.multi_agent` | **on** | `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent` |
| `agents.enabled` | **on** | Multi-agent tools |
| `agents.interrupt_message` | **on** | Record a model-visible message when an agent turn is interrupted |
| `features.apps` | **on** | App/connector integrations. **Traffic is *not* controlled by the sandboxed-command network proxy or its domain allowlist** |
| `features.personality` | **on** | `/personality` |
| `features.remote_plugin` | **on** | Remote plugin catalog |
| `features.fast_mode` | **on** | Model-catalog service tier selection in the TUI |
| `features.goals` | **on** | Persisted goals and automatic continuation |
| `features.shell_tool` | **on** | Default `shell` tool |
| `features.shell_snapshot` | **on** | Shell environment snapshot for faster repeat commands |
| `features.skill_mcp_dependency_install` | **on** | Prompt to install missing MCP dependencies for skills |
| `features.enable_request_compression` | **on** | zstd compression of streaming request bodies |
| `features.unified_exec` | **on except Windows** | PTY-backed unified exec tool |
| `features.network_proxy` | **off** | Experimental. **Permission-profile domain rules are not enforced while off.** Does not filter web search, apps, MCP or other hosted tools |
| `features.code_mode.enabled` | **off** | Under development |
| `features.prevent_idle_sleep` | **off** | Experimental |
| `features.rollout_budget.enabled` | **off** | Under development |
| `feedback.enabled` | **on** | `/feedback` |
| `allow_login_shell` | **on** | Login-shell semantics for shell tools |
| `memories.use_memories` | **on** | Only relevant once `features.memories` is enabled |
| `memories.generate_memories` | **on** | New threads stored as memory-generation inputs |
| `memories.disable_on_external_context` | **off** | When on, threads using MCP/web search/tool search are excluded |
| `approvals_reviewer` | `user` | `auto_review` delegates to the reviewer subagent |
| `file_opener` | `vscode` | URI scheme for opening citations |
| `model_provider` | `openai` | `openai`, `ollama`, `lmstudio` are reserved built-ins |
| `background_terminal_max_timeout` | `300000` ms | Background terminal polling window |
| `mcp_servers.<id>.startup_timeout_sec` | 10s | Per-server startup timeout |
| `mcp_servers.<id>.tool_timeout_sec` | 60s | Per-tool timeout |

**Enable at launch:** `codex --enable feature_a --enable feature_b`. **Disable:** `[features]
feature_name = false` in `~/.codex/config.toml`. Admins force features off in `requirements.toml`
with the same shape.

### Web search

Accepted values `disabled | cached | indexed | live`, default **`cached`**:

> *"cached uses an OpenAI-maintained index without external web access; indexed permits external
> access only when gated by the search index; if you use `--yolo` or another full access sandbox
> setting, it defaults to `live`."*

> ⚠️ **A full-access sandbox silently changes this default to `live`** — the one mode with
> unrestricted outbound retrieval. **The permission decision and the network-egress decision are
> coupled**, and nothing warns you.

`codex --search` is described elsewhere as selecting live search; **no `--search` flag appears in
the configuration reference** — `(unverified)`, confirm with `codex --help`.

### Permissions and sandboxing

**`sandbox_mode`:** `read-only | workspace-write | danger-full-access`. Named permission profiles
`:read-only`, `:workspace`, `:danger-full-access` via `default_permissions`; custom profiles use
`[permissions.<name>]`. Do not combine `default_permissions` with `sandbox_mode` or
`[sandbox_workspace_write]`. On Windows set the native sandbox mode to `elevated` in the `windows`
table. **Windows sandboxing is native** — restricted tokens and ACLs, no WSL or VM required.

**`approval_policy`:** `untrusted | on-request | never | { granular = { … } }`. `on-failure` is
deprecated. The **granular** form keeps some categories interactive while auto-deciding others:

```toml
approval_policy = { granular = {
  sandbox_approval    = true,
  rules               = true,
  mcp_elicitations    = true,
  request_permissions = true,
  skill_approval      = true,
} }
```

> ⚠️ **Two official pages disagree about `untrusted`.** The Help Center says
> `approval_policy = "untrusted"` was **removed** in newer clients (CLI 0.149.0, desktop and VS Code
> 26.818.31338) and that leaving it set makes Codex fail to start. The **configuration reference
> still lists `untrusted` as an accepted value**, retrieved 2026-09-02. Both are current pages.
> **Treat the Help Center as operative and remove the key** — that reading fails safe. Project-level
> `trust_level = "untrusted"` is a different setting and **remains supported**.

**Managed configuration:** `requirements.toml` — allowed approval policies, sandbox modes, web
search behaviour, MCP allowlists, feature pins, restrictive command rules. **Group-scoped policies
apply first-match, and Codex does not merge fields from later matching rules.**

---

## 10. Scheduling

**There is no native scheduler in the CLI or the IDE extension.** Scheduled Tasks are part of the
broader ChatGPT task system, surfaced in the desktop app; the local clients reach recurring work
through an external scheduler driving `codex exec`.

| Surface | Create and manage | Event triggers | Local filesystem |
|---|---|---|---|
| **ChatGPT web** | ✅ *"create them from Chat or ChatGPT Work on the web and manage their runs from **Scheduled**"* | ✅ | ❌ *"Web tasks can use uploaded context and connected tools, but they can't work directly in a folder on your computer."* No local folder or worktree is kept between runs |
| **ChatGPT desktop app** | ✅ *"Find all scheduled tasks and their runs on **Scheduled** in the ChatGPT desktop app sidebar."* | ❌ | ✅ *"scheduled tasks can work with local projects and run in the project directory or an isolated worktree"* |
| **ChatGPT mobile** | ⚠️ **Not documented.** The page states only that mobile can *run* tasks from app events | ✅ | ❌ |
| **Codex CLI / IDE** | ❌ *"Codex CLI doesn't provide the Scheduled management interface. Use ChatGPT web or the desktop app to create and manage scheduled tasks."* | ❌ | — use an external scheduler, below |
| **Codex Remote (mobile)** | **Not a scheduler.** Steers host-side work. Same device as the ChatGPT mobile row, different product | — | — |
| **API / SDK** | Scheduling belongs to the caller's application or orchestration layer. There is no generic "run this prompt daily" scheduler in the API | — | — |

**For CLI and IDE, the scheduler is external.** Drive `codex exec` from `cron`, `systemd` timers,
GitHub Actions, GitLab CI/CD or any orchestrator — it is non-interactive with `--json` JSONL
streaming and an exit code, which is what makes it schedulable.

> **The two capabilities split in opposite directions, which is the thing to remember.**
> Event triggers are **web and mobile only** — *"aren't available in the ChatGPT desktop app, Codex
> CLI, or the IDE extension."* **A local checkout is desktop only.** So an event-triggered
> web or mobile task cannot work in a local folder or worktree, and a desktop task that can does not
> support app-event triggers.
>
> **This is narrower than "cannot touch your repository", and the distinction matters.** A web task
> still reaches a repository through connected tools and uploaded context; what it lacks is a
> **local checkout kept between runs** — *"They don't keep a local folder or worktree available
> between runs."* Plan around the checkout, not around repository access in general.

**Standalone tasks versus tasks scheduled inside a chat** — `documented`, 2026-09-02:

| | Behaviour |
|---|---|
| **Standalone** | *"start a new chat for each scheduled run and report results in **Scheduled**"* |
| **Inside an existing chat** | *"return to that chat on a schedule"*, using *"the chat's existing context"* |

The second is the one worth knowing: a task scheduled from inside a chat **inherits that chat's
context on every run**, so what the conversation already contains becomes standing input to a
recurring job.

**This is a real asymmetry with Claude Code**, which has three scheduling runtimes including a
cloud one (`docs/agents/claude-code.md` §8). On Codex the equivalent of a durable cloud schedule is
CI: a `schedule:` trigger running `codex exec`. `docs/GUIDE.md` stage 7 covers which to reach for.

---

## 11. Desktop-only capabilities

`documented`, 2026-09-02. These have no CLI or IDE equivalent and are the strongest reason to run
the desktop app.

| Feature | Notes |
|---|---|
| **Local Environments** | Setup scripts, platform-specific setup, common project actions, commands that run in the integrated terminal, and initialization for new worktrees. Configuration under `.codex/` |
| **Managed Worktrees** | Codex creates isolated Git checkouts for parallel work: pick a base branch, detached HEAD, hand off to and from local. **`.worktreeinclude`** at the repo root lists ignored paths or `.gitignore`-style patterns to copy into a managed worktree; Codex copies **only** matching ignored files. Applies to desktop-managed worktrees, **not** ones you create yourself |
| **In-app Browser** | `@Browser`. Own browser state, sign-in, autofill, extensions and downloads, separate from your real Chrome. **Developer mode / full CDP** is off by default — enable under Settings → Browser; admins force it off with `browser_use_full_cdp_access = false` |
| **Computer Use** | Plugin plus OS permissions. Switch to Work or Codex, install and enable the plugin, turn on the server and skill toggles, then grant macOS Screen Recording and Accessibility. Review app access under Settings → Computer use |
| **Pets** | Profile menu → Pets, or Settings → Pets. Position persists across restarts. **CLI pets need iTerm2 3.6+, or Kitty graphics or Sixel support, and are unavailable inside tmux and Zellij.** Also available on ChatGPT **web inside Work chats** |
| **Appshots** | Attach a desktop application window to a thread. macOS only, **behind a feature flag** — the bundle ships and registers its hotkey, but the settings section appears only when the flag is on for the account |
| **Record & Replay** | Demonstrate once, get a reusable skill. macOS only; requires Computer Use; **excludes the EU, Switzerland and the UK** |
| **Codex Micro** | Limited-run hardware keypad. Pairs over USB-C or Bluetooth; needs Input Monitoring permission on macOS |
| **Visualizations** | `@Visualize`. **CLI and IDE do not render them**, though the `visualize` plugin is installable there — installable and renderable are different questions |
| **iOS Simulator / integrated terminal** | Desktop panes; Windows supports a WSL shell |

---

## 12. How to enumerate this yourself

```bash
codex debug prompt-input        # what the model actually sees, incl. every skill and its root
codex plugin list               # installed and available plugins, per marketplace
codex --help                    # CLI subcommands — including ones the docs page omits
ls $CODEX_HOME/skills/.system/  # the built-ins
codex doctor                    # startup, connectivity, performance diagnostics
```

**`codex debug prompt-input` is the one that settles arguments.** It prints a `<skills_instructions>`
block with each skill and the root it resolved from. **A `SKILL.md` on disk is not a loaded skill,
and `installed, enabled` is not an available plugin** — `codex-security` reported the latter while
contributing nothing to that list.

In the **desktop app**, type `/` and `$` and read the pickers; the app labels every skill `System`
or `Personal`.

---

## 13. Surface differences

**Officially:** "Standalone skills are available in the ChatGPT desktop app, Codex CLI, and IDE
extension." Plugin-bundled skills additionally work "in Chat and Work across ChatGPT on the web,
desktop, and mobile."

**In practice they diverge, and the CLI is not a proxy for the app:**

- The app's picker showed `Plugin Management` (from `openai-curated-remote`); the CLI's
  `prompt-input` list did **not** contain it.
- `codex debug prompt-input` on the CLI listed **16** skills from 6 roots, and `openai-curated` was
  **not among the roots**.
- Known open issue: [openai/codex#28505](https://github.com/openai/codex/issues/28505) — *"Codex app
  does not index personal skills from `~/.agents/skills` for `$` invocation."* Project-scoped
  `.agents/skills` in the app is **`(unverified)`**, and it matters here because that is where
  `install.py` writes. It was confirmed loaded on the **CLI**.
- **Plugins do not work in the IDE extension at all** (section 5).
- `/pet`, `/goal` and `/init` descriptions exist in the app menu but not in the official command
  reference.

**IDE extension: not checked at all.**

---

## 14. Known traps

1. **Bundled does not mean available**, and **installed does not mean loaded.** Three separate
   states; `codex debug prompt-input` is the only reliable test.
2. **Hooks are on by default but untrusted hooks do not run** (section 8).
3. **A full-access sandbox flips `web_search` to `live`** (section 9).
4. **A gitignored `AGENTS.override.md` is loaded instruction content that never reaches review**
   (section 7).
5. **An untrusted project silently skips every `.codex/` layer** (section 6).
6. **`features.apps` traffic bypasses the sandbox network proxy and its domain allowlist**
   (section 9).
7. **Codex usage is a shared pool.** Codex, ChatGPT Work, ChatGPT for Excel and Workspace Agents
   draw on the same allowance and credit pool. ChatGPT's own file upload, image and voice caps do
   **not** apply to Codex.
8. **Rollout variance is real.** Features ship behind maturity labels — Under development,
   Experimental, Beta, Stable, Deprecated — and availability differs across accounts, workspaces
   and app versions **on the same plan**.
9. **Regional gaps.** Sites is unavailable in the EEA, Switzerland and the UK; Record & Replay
   initially excludes the EU, Switzerland and the UK; Computer Use launched macOS-first.
10. **Model retirement has already happened once.** GPT-5.4 and GPT-5.4 mini were removed from Codex
    on ChatGPT sign-in on 2026-08-31. Audit workspace defaults, saved model settings, managed
    configuration and automations; API-key usage was unaffected.

---

## 15. Not Codex features

Worth stating, because the shared shell makes them look like Codex:

- **ChatGPT Work** — a sibling mode for longer research and deliverables. Shares Codex's usage
  allowance but is a separate experience.
- **Custom GPTs** — a ChatGPT customization system. Codex's equivalent stack is `AGENTS.md` +
  skills + plugins + MCP + hooks + configuration + subagents.
- **Work Cloud Browser** — belongs to Work, and is not the desktop in-app Browser.
- **Sites** — a ChatGPT/Work site-building workflow, plan- and region-gated, that Codex surfaces can
  edit the source of but does not own.
