# Google Antigravity

**Evidence status:** capability claims remain `documented`, not `tested`. A read-only presence audit
on Windows found Antigravity 2.0 v2.11.0 and Antigravity IDE v2.5.5 installed on 2026-09-04, but
neither application was run or capability-tested. `agy` was not on `PATH`, and the CLI/SDK were not
locally enumerated. Installation presence is not evidence that a capability loaded.

**Documented versions:** Antigravity 2.0 v2.12.2, Antigravity CLI v1.1.25, Antigravity SDK
v0.1.16, and Antigravity for IDEs v2.5.5. These are the versions shown by the official
[documentation home](https://antigravity.google/docs/home), retrieved 2026-09-04; they are not
local measurements.

**Sources:** only `antigravity.google`, `ai.google.dev`, Google Developers Codelabs, and linked
Google-owned product documentation, all retrieved 2026-09-04. The main entry point is the official
[Google Antigravity documentation](https://antigravity.google/docs/home).

> Lower bound — see [README](README.md). Absence means "not recorded", not "not there". A
> documentation inventory is not support: install a real release and repeat section 15 before
> changing this file's grade to `tested`.

## Evidence grades used in this file

| Grade | Means |
|---|---|
| **`documented`** | Present in current official Google documentation, with retrieval date |
| ⚠️ **disputed** | Two current or still-published official pages disagree |
| `(unverified)` | No official source or local execution supports the claim |

Nothing below is `tested`.

## 1. Surfaces

The official home page describes four core products on one shared agent harness. Delivery channels
and enterprise deployment modes sit beside those products; they are not five more equivalent
clients. `documented`, 2026-09-04.

| Surface | Documented version | Role | Important boundary |
|---|---:|---|---|
| **Antigravity 2.0** | 2.12.2 | Standalone desktop command center; Projects, local/worktree conversations, parallel subagents, artifacts, scheduled sidecars | The docs also call its command surface "Desktop and Web"; the exact web delivery boundary was not locally checked |
| **Antigravity CLI** | 1.1.25 | `agy` TUI plus headless/print mode | Own settings and global customization roots under `~/.gemini/antigravity-cli/` |
| **Antigravity SDK** | 0.1.16 | Python framework for custom agents | Programmatic policies, tools, hooks, structured output, and subagents; not the coding-agent UI |
| **Antigravity for IDEs** | 2.5.5 | IDE family: a standalone Antigravity IDE plus extensions for VS Code, Visual Studio, JetBrains, Zed, and Xcode | Standalone IDE and extensions are separate deliveries; do not infer one delivery's capability or enterprise support from another |

Adjacent official delivery and deployment modes:

| Mode | Role | Boundary |
|---|---|---|
| **Remote Control** | Browser dashboard that drives an Antigravity 2.0 session, or a separately installed headless daemon | A control channel over the host session, not an independent skills/MCP/browser runtime |
| **Gemini API Antigravity agent** | Managed preview agent `antigravity-preview-05-2026` through the Interactions API and Google AI Studio | Google-hosted Linux sandbox and API billing; distinct from the local Python Antigravity SDK |
| **Gemini Enterprise** | Google Cloud deployment, identity, governance, residency, and billing mode | Supports 2.0, CLI, and IDE Extensions; standalone Antigravity IDE is not supported |

Official sources: [Choose Your Surface](https://antigravity.google/docs/home),
[Download](https://antigravity.google/download),
[Remote Control](https://antigravity.google/docs/remote-control),
[Gemini API Antigravity agent](https://ai.google.dev/gemini-api/docs/antigravity-agent), and
[Enterprise](https://antigravity.google/docs/enterprise), retrieved 2026-09-04.

## 2. Commands

### Cross-surface agent commands

The public command page says these operate consistently across Antigravity 2.0 Desktop/Web and
Antigravity CLI. `documented`, 2026-09-04.

| Command | Does what | Gate |
|---|---|---|
| `/boost` | Three-tier multi-agent reasoning, test execution, and independent verification | Paid plans |
| `/teamwork-preview` | Long-horizon collaborative agent teams | Paid plans; preview |
| `/goal` | Continue autonomous execution until the objective is achieved | All plans |
| `/plan` | Inspect the repository and produce a reviewable Implementation Plan artifact | All plans |
| `/grill-me` | Interview the user about architecture and edge cases before editing | All plans |
| `/learn` | Distil session corrections into a Rule or Skill | All plans; output path is disputed, section 17 |
| `/schedule` | Create a one-time or recurring Scheduled Task | All plans |
| `/browser` | Spawn the built-in sandboxed Chrome browser subagent | All plans |
| `/btw` | Run a side question in a background thread | All plans |

Official source: [Slash commands overview](https://antigravity.google/docs/slash-commands),
retrieved 2026-09-04.

### CLI TUI commands

The CLI adds management commands around the shared workflows. The official reference lists:

`/add-dir`, `/agents`, `/artifact`, `/btw`, `/clear` (`/new`), `/config` (`/settings`), `/context`,
`/copy`, `/credits`, `/diff`, `/exit` (`/quit`), `/fast`, `/feedback`, `/fork` (`/branch`), `/help`,
`/hooks`, `/keybindings`, `/logout`, `/mcp`, `/model`, `/open`, `/permissions`, `/planning`,
`/rename`, `/resume` (`/switch`, `/conversation`), `/rewind` (`/undo`), `/skills`, `/statusline`,
`/tasks`, `/teamwork-preview` (`/teamwork`), `/title`, `/usage` (`/quota`), and `/voice`
(`/record`). `documented`, 2026-09-04.

`/boost` and `/codesearch` have dedicated command pages and appear in the current docs navigation.
The reference is a lower bound rather than proof that no other command exists.

Official source: [CLI reference](https://antigravity.google/docs/cli/reference), retrieved
2026-09-04.

### CLI process commands

| Command | Does what |
|---|---|
| `agy` | Launch the interactive TUI in the current project |
| `agy -p <prompt>` | Run one headless prompt and exit; aliases `--print`, `--prompt` |
| `agy -p ... --output-format json` | Return machine-readable result and usage |
| `agy -p ... --output-format stream-json` | Emit NDJSON `init`, `step_update`, and final `result` events |
| `agy -p ... --json-schema <schema>` | Constrain and return structured output |
| `agy plugin list\|install\|enable\|disable\|uninstall` | Manage CLI plugins |

Headless mode uses cached credentials, writes the response to stdout and diagnostics to stderr,
and exits instead of hanging when authentication is absent in a non-interactive environment.
`documented`, [Headless mode](https://antigravity.google/docs/cli/headless), retrieved 2026-09-04.

## 3. Built-in agents and skills

### Built-in subagents

| Agent | Does what |
|---|---|
| `research` | Codebase research, file navigation, and structural exploration |
| `browser` | Sandboxed browser navigation and UI verification; invoked through `/browser` |
| `self` | Clone of the calling agent's system instructions and toolset |

`documented`, [Subagents](https://antigravity.google/docs/subagents), retrieved 2026-09-04.

### Built-in skills

The changelog confirms this lower bound; it is not an exhaustive inventory:

| Surface | Confirmed built-in skill |
|---|---|
| Antigravity 2.0 | **Antigravity Guide** |
| CLI | `antigravity_guide`, `migrate-workflows` |

The "Build with Google" integrations are optional bundles and belong in section 6, not in this
built-in set. Source: [Changelog](https://antigravity.google/changelog), retrieved 2026-09-04.

## 4. Tools

For the local products, the Hooks documentation publishes hook matcher names and argument schemas.
That is still a documentation list rather than the tool array from a running session.
`documented`, [Hooks](https://antigravity.google/docs/hooks), retrieved 2026-09-04.

| Category | Documented tools |
|---|---|
| Files | `view_file`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `list_dir`, `find_by_name` |
| Search/web | `grep_search`, `search_web`, `read_url_content` |
| System | `run_command`, `manage_task`, `schedule`, `list_permissions`, `ask_permission` |
| Agents | `invoke_subagent`, `define_subagent`, `send_message`, `manage_subagents` |
| Interaction/media | `ask_question`, `generate_image` |

The browser subagent additionally navigates pages, inspects DOM, captures screenshots, and verifies
layouts. `/browser` is a public shared command on both 2.0 Desktop/Web and CLI; the absence of a
separate entry in a shorter CLI feature table is not evidence that CLI lacks it.

The Python SDK has its own exact `BuiltinTools` contract:

| Category | SDK identifiers |
|---|---|
| Files | `list_directory`, `search_directory`, `find_file`, `view_file`, `create_file`, `edit_file` |
| System/interaction | `run_command`, `ask_question`, `finish` |
| Agents/media | `start_subagent`, `generate_image` |
| Web | `search_web`, `read_url_content` |

`search_web` and `read_url_content` are enabled by default. `CapabilitiesConfig` filters tools;
`LocalAgentConfig` adds custom Python functions and `skills_paths`. The SDK also documents
streaming, image/PDF input, Pydantic structured output, policies with human approval, dynamic or
static subagents, lifecycle hooks, scheduled `every(...)` triggers, cost auditing, and persisted
sessions. The current SDK pages do not document audio/video input; do not generalise broader
product media support to the SDK. Sources: [SDK Tools & Skills](https://antigravity.google/docs/sdk/tools),
[Structured Output](https://antigravity.google/docs/sdk/structured-output/),
[Policies](https://antigravity.google/docs/sdk/policies/), and
[Lifecycle](https://antigravity.google/docs/sdk/lifecycle/), retrieved 2026-09-04.

The Gemini API Antigravity agent exposes a different tool contract: `code_execution`,
`google_search`, and `url_context` by default, plus custom functions and remote MCP servers. It has
no standalone filesystem tool; files belong to the managed `environment`. The local-product, SDK,
and managed-API tool lists must not be merged.

## 5. Projects, product UI, artifacts, and verification

Antigravity 2.0 Projects can span multiple folders, isolate settings and permission grants, and
start conversations against local folders or new Git worktrees. A conversation outside a Project
runs in its own local scratch folder. The 2.0 UI also includes an integrated terminal, live voice
transcription in prompts and artifact comments, and a Git-native VCS panel for staged/unstaged,
branch, and agent-edit diffs plus stage, discard, commit, and push actions. `documented`,
[Feature overview](https://antigravity.google/docs/features), retrieved 2026-09-04.

Artifacts are structured review deliverables: Implementation Plans, code diffs, architecture
diagrams, images, screenshots, walkthroughs, and browser recordings. Antigravity 2.0 provides a
visual review pane; the CLI provides a keyboard-driven Artifact Review Panel and status notices.

The important distinction is that an artifact reports and supports review; it is not proof by
itself. `/boost` explicitly documents running tests and independent verification, while `/browser`
can inspect UI and capture evidence. Project-specific deterministic checks remain the binding
verification layer.

Official sources: [Artifacts](https://antigravity.google/docs/artifacts) and
[Slash commands](https://antigravity.google/docs/slash-commands), retrieved 2026-09-04.

## 6. Installable — official

Antigravity 2.0 offers optional Google-built bundles under
`Settings > Customizations > Build with Google Plugins`. They are not part of a fresh agent merely
because the docs list them. `documented`, [Build with Google](https://antigravity.google/docs/build-with-google),
retrieved 2026-09-04.

| Bundle | Contains / purpose |
|---|---|
| Modern Web Guidance | Expert-vetted web-development skills |
| Firebase | Skills for Firestore, Authentication, App Hosting, Cloud Functions, and resource actions |
| Google Antigravity SDK | SDK architecture, setup, policies, hooks, subagents, and observability skill |
| Android CLI | Android tools and skills for build, test, deploy, and migration |
| Science | Curated scientific skills |
| Chrome DevTools | Chrome DevTools and Puppeteer skills |
| Dart and Flutter | Skills plus Dart MCP server |
| Data Agent Kit Starter Pack | Data-engineering skills and Google Cloud data MCP tools |
| Google Maps Platform | Skills covering Maps Platform APIs and SDKs |

The docs do not expose a single machine-readable catalogue of every component inside these bundles.

The **MCP Store** is a separate installable catalogue, not part of those nine plugin bundles. Its
current official list has 46 integrations: Databases & Storage (14), Developer Tools & CI/CD (13),
Frontend & Design (6), and Analytics, AI & Cloud (13). A listed server is not connected until the
user adds it: 2.0 uses `Settings > Customizations > Installed MCP Servers > Add MCP`; IDE uses
`... > MCP Servers > Install` in the agent side panel. Chrome DevTools is the exception to that
store-install boundary: the Features page documents native Chrome DevTools MCP integration in the
browser subagent. A read-only inspection of installed 2.0 v2.11.0 found the packaged
`resources/app.asar.unpacked/node_modules/chrome-devtools-mcp` directory; that corroborates shipping,
not activation. Official sources: [MCP](https://antigravity.google/docs/mcp) and
[Feature overview](https://antigravity.google/docs/features), retrieved 2026-09-04; local package
inspected 2026-09-04.

## 7. Extension points

These rows are not a promise of cross-surface parity. The Notes column names the surface where a
path is documented or locally observed.

| Mechanism | Project/workspace | Global/user | Notes |
|---|---|---|---|
| Context files | `AGENTS.md`, `GEMINI.md` | `~/.gemini/GEMINI.md` | CLI website says workspace root; installed 2.0 v2.11.0 built-in docs say per-directory walk-up — disputed, section 8 |
| Rules | `.agents/rules/*.md` | `~/.gemini/GEMINI.md` for global rules | Manual, Always On, Model Decision, or Glob activation; `.agent/rules` legacy fallback |
| Skills — 2.0/general docs | `.agents/skills/<name>/SKILL.md` | `~/.gemini/config/skills/<name>/SKILL.md` | Progressive disclosure; `.agent/skills` legacy fallback |
| Skills — IDE | `.agents/skills/<name>/SKILL.md` | `~/.gemini/antigravity/skills/<name>/SKILL.md` | Official IDE path; installed IDE state uses `.antigravity-ide`, but Skill loading from either root was not tested |
| Skills — CLI | `.agents/skills/*.md` | `~/.gemini/antigravity-cli/skills/*.md` | CLI docs describe flat Markdown skills that become slash commands |
| Workflows | `.agents/workflows/*.md` | user customization path | IDE docs and installed IDE 2.5.5 manifest; deprecated in favour of Skills by 2026-11-01 |
| MCP | `.agents/mcp_config.json` | `~/.gemini/config/mcp_config.json` | 2.0/general docs; project loading was not observed in IDE 2.5.5 and remains untested; `stdio` and remote `serverUrl` |
| Custom agents | `.agents/agents/<name>.md` or `<name>/agent.md` | `~/.gemini/config/agents/` | CLI-documented; do not infer IDE parity; Markdown plus YAML frontmatter |
| Hooks | `.agents/hooks.json` | `~/.gemini/config/hooks.json` | Command handlers at five lifecycle events |
| Plugins | `.agents/plugins/<name>/` (also documented with `_agents/plugins/`) | `~/.gemini/config/plugins/<name>/`; CLI stages installed bundles under `~/.gemini/antigravity-cli/plugins/<name>/` | Product plugins bundle skills, rules, MCP, and hooks; CLI plugins may also bundle agents |
| Sidecars | No project sidecar path documented | `~/.gemini/config/sidecars/<name>/`; plugins may provide `sidecars/<name>/` | Disabled until enabled in `~/.gemini/config/config.json`; managed background process, not a hook |
| SDK | Python configuration | Python application | Custom tools, policies, hooks, subagents, MCP, structured output |

Sources: [Rules](https://antigravity.google/docs/rules-workflows/),
[2.0 Skills](https://antigravity.google/docs/skills),
[IDE Skills](https://antigravity.google/docs/ide/skills),
[CLI Skills](https://antigravity.google/docs/cli/plugins/), [MCP](https://antigravity.google/docs/mcp),
[Subagents](https://antigravity.google/docs/subagents), [Hooks](https://antigravity.google/docs/hooks),
and [Plugins](https://antigravity.google/docs/plugins), retrieved 2026-09-04.

## 8. Instruction and rule loading

Instruction discovery is ⚠️ **disputed**. The CLI best-practices page says workspace-root
`GEMINI.md`/`AGENTS.md`; the documentation shipped in installed Antigravity 2.0 v2.11.0 at
`~/.gemini/antigravity/builtin/skills/agy-customizations/docs/rules.md` says files may occur in any
directory and are loaded by walking from the current working directory to the repository root.
Neither contract was exercised. The global `~/.gemini/GEMINI.md` path is documented by both the
CLI migration and Rules material. Sources: [Best Practices](https://antigravity.google/docs/cli/best-practices/)
and [Gemini CLI migration](https://antigravity.google/docs/gcli-migration), retrieved 2026-09-04;
installed 2.0 v2.11.0 built-in documentation inspected 2026-09-04.

Rules add a richer activation layer under `.agents/rules`:

- **Manual** — activated with an `@` mention.
- **Always On** — included for the workspace.
- **Model Decision** — matched by a natural-language description.
- **Glob** — activated for matching file paths.

Rule files are documented as limited to 12,000 characters each and may `@`-reference other files.
The docs do not establish that this limit also binds directory-based `AGENTS.md`/`GEMINI.md`, so
`check.py` records but does not enforce it against the instruction chain. Current docs default to
`.agents/rules` and retain `.agent/rules` for backward compatibility.

What the docs do **not** establish is precedence when `AGENTS.md`, `GEMINI.md`, an Always On Rule,
and a plugin Rule conflict. That remains `(unverified)` until run.

## 9. Skills

Current product docs use the Agent Skills folder format with `SKILL.md`. `description` is required;
`name` is optional and defaults to the folder name. At conversation start the agent sees names and
descriptions, then reads the full body only when relevant. `documented`, 2026-09-04.

The shared workspace directory name is `.agents/skills`, but file layout and global paths differ:

- Antigravity 2.0/general Skills docs: `.agents/skills/<name>/SKILL.md` and
  `~/.gemini/config/skills/<name>/SKILL.md`.
- Current IDE Skills page: `.agents/skills/<name>/SKILL.md` and
  `~/.gemini/antigravity/skills/<name>/SKILL.md`. Installed IDE 2.5.5 stores product state under
  `~/.gemini/antigravity-ide/`; that naming difference is a test prompt, not proof that the
  documented customization path is wrong.
- CLI: flat Markdown files under `.agents/skills/` and
  `~/.gemini/antigravity-cli/skills/`; registered Skills become slash commands.
- SDK: explicit `LocalAgentConfig.skills_paths`; a path may name one Skill directory or a parent
  containing several Skill directories.

Official codelabs published during the path migration still mention `.agent/skills` or
`~/.agents/skills`. Current product docs explicitly default to `.agents/skills` and keep
`.agent/skills` only as a legacy fallback. The project path used by this repository is current for
2.0/IDE, but the CLI page's flat-file contract is not evidence that it loads the same nested
`SKILL.md` layout. A single global path or file layout is not portable across all Antigravity
surfaces.

## 10. Subagents and agent teams

The parent invokes `invoke_subagent`; each child gets an isolated context and may use `inherit`,
`branch` (Git worktree), or `share` workspace storage. Multiple children can run concurrently.

Custom agents are Markdown with YAML frontmatter. Documented fields include `name`, `description`,
`tools`, `mainAgent`, `subagent`, `model` (`inherit`, `flash`, `pro`),
`commandExecutionPolicy` (`off`, `auto`, `eager`, `sandbox`), `mcpServers`, `skills`, and `plugins`.
The CLI `/agents` panel switches primary agents, forks an active conversation when switching,
shows child status, exposes approvals, and can terminate children.

Known official issue: an unknown or misspelled tool name in `tools` may hang a custom subagent;
schema validation was documented as pending. Source: [Subagents](https://antigravity.google/docs/subagents),
retrieved 2026-09-04.

`/boost` and `/teamwork-preview` are higher-level orchestrators, not synonyms for one ordinary
subagent. Both are plan-gated; `/teamwork-preview` is also explicitly preview.

## 11. Hooks

Hooks live in `.agents/hooks.json` or `~/.gemini/config/hooks.json`; plugins may bundle their own
`hooks.json`. The schema groups named hooks around events and matcher-selected tools. Only
`type: "command"` handlers are currently documented.

| Event | Timing / control |
|---|---|
| `PreToolUse` | Before a tool; may allow, deny, or modify tool input |
| `PostToolUse` | After a tool; may attach context or diagnostics |
| `PreInvocation` | Before an agent invocation |
| `PostInvocation` | After an agent invocation |
| `Stop` | When the agent is about to stop |

Handlers receive JSON on stdin and return JSON on stdout. The official page documents command
timeouts and event-specific output contracts. This is a vendor-local accelerator: a hook only
binds if the surface loads it, the command runs, and the result is honored. Keep non-negotiable
gates in CI.

Official source: [Hooks](https://antigravity.google/docs/hooks), retrieved 2026-09-04.

## 12. Permissions and sandbox

Permissions use `action(target)` resources in **Deny**, **Ask**, and **Allow** lists, with strict
precedence `Deny > Ask > Allow`. Documented actions are `read_file`, `write_file`, `read_url`,
`execute_url`, `command`, `unsandboxed`, and `mcp`. Workspace reads and writes are auto-allowed by
default; unconfigured commands, MCP, browser actuation, web access, and outside-workspace files ask.

The Terminal Sandbox is opt-in/preview and disabled by default. It derives filesystem and network
mounts from permission grants. ⚠️ **The current official pages disagree about Windows:** CLI
Features names `AppContainer`, while both dedicated Sandbox pages list only Linux namespaces and
macOS `sandbox-exec`. Record Windows as `disputed`, not present or absent, until the installed
Windows CLI is exercised.

CLI settings live at `~/.gemini/antigravity-cli/settings.json`; `/permissions` and `/config` edit
them interactively. CLI permission modes include `request-review` (default),
`proceed-in-sandbox`, `strict`, and `always-proceed`. The sandbox flag is documented as
`--sandbox`, though the sandbox page's example uses `antigravity --sandbox` while installation and
the rest of the CLI docs use `agy`; see section 17.

Sources: [Permissions](https://antigravity.google/docs/permissions),
[CLI permissions](https://antigravity.google/docs/cli/permissions),
[Sandbox](https://antigravity.google/docs/sandbox), and
[CLI sandbox](https://antigravity.google/docs/cli/sandbox), retrieved 2026-09-04.

## 13. Scheduling, models, and plans

- `/schedule` creates one-time or recurring Scheduled Tasks; Antigravity 2.0 describes these as
  cron sidecars. A recurring agent prompt is orchestration, not an observability backend.
- Sidecars are global or plugin-provided `sidecar.json` processes, disabled until explicitly
  enabled. The only documented `builtin` value is `schedule`; `agentapi` is the helper used to
  create conversations. This is more general than the `/schedule` UI command.
- Model selection is plan-dependent and sticky within the current user turn. The live list is
  volatile; use `/model` and `/usage` rather than copying a static list into project instructions.
- ⚠️ Model availability is disputed even within the current official docs: Plans says AI Ultra
  includes third-party models, while Models marks Claude Sonnet/Opus and GPT-OSS available on every
  individual tier. Do not encode one table as policy without checking the active account.
- `/boost` and `/teamwork-preview` require paid plans. Other public shared commands are documented
  for all plans.
- Custom subagent/model availability is plan-gated; the official Subagents page owns the current
  plan table.

Sources: [Sidecars](https://antigravity.google/docs/sidecars),
[Models](https://antigravity.google/docs/models), and [Plans](https://antigravity.google/docs/plans),
retrieved 2026-09-04.

## 14. Remote Control, managed API, and Enterprise

### Remote Control

Remote Control is off until enabled under Antigravity 2.0 Settings. Its browser dashboard can view
conversations, start tasks, review plans, and inspect artifacts on the selected host. Mobile users
may install the web app to the home screen for push notifications; the official page does not call
this a native mobile application.

A separate headless daemon is available on Linux, macOS, and Windows. Windows service install and
uninstall require an Administrator Command Prompt. Daemon identity uses a separate one-time sign-in
and `cliRemoteControlHostname` in `~/.gemini/config/config.json` (or the Windows equivalent).
Capabilities visible through Remote Control belong to the controlled host; do not mark MCP,
Skills, Browser, Git, or Artifacts as independently implemented by the dashboard.

Source: [Remote Control](https://antigravity.google/docs/remote-control), retrieved 2026-09-04.

### Gemini API Antigravity agent

`antigravity-preview-05-2026` is a general-purpose managed agent on the Gemini API, not the Python
Antigravity SDK. An Interaction can provision a Google-hosted Linux sandbox with persistent files,
code execution, Search/URL tools, custom functions, remote MCP, synchronous hooks, multi-turn
continuation, automatic context compaction, streaming, cancellation, scheduled triggers, and a
best-effort `max_total_tokens` budget. It is preview and available to free- and paid-tier API
projects under API pricing.

Customization is inline or mounted into the environment: `system_instruction` is additive with
`.agents/AGENTS.md`; Skills under `.agents/skills/<name>/SKILL.md` are auto-discovered; managed
agent sources may be Git, GCS, or inline. This is not parity with the local SDK. The managed agent
explicitly does **not** support structured output, `file_search`, `computer_use`, or `google_maps`;
remote MCP requires Streamable HTTP rather than SSE; function calling is stateful-only; and only
text/image input is supported. `background=True` requires `store=True`.

Sources: [Gemini API Antigravity agent](https://ai.google.dev/gemini-api/docs/antigravity-agent)
and [Building managed agents](https://ai.google.dev/gemini-api/docs/custom-agents), retrieved
2026-09-04.

### Gemini Enterprise

Enterprise is a deployment and governance mode, not another local agent binary. It supports
Antigravity 2.0, CLI, and IDE Extensions; standalone Antigravity IDE is excluded. Documented
controls include Google Cloud identity/licensing, BYOID/WIF, VPC Service Controls, request/response
logging, and `global`, `us`, and `eu` endpoints. ADC authentication is CLI-only, and image
generation is available only on the `global` endpoint.

Source: [Enterprise](https://antigravity.google/docs/enterprise), retrieved 2026-09-04.

## 15. How to enumerate this yourself

Do this on a real installation before upgrading the evidence grade:

1. Record the surface, OS, account plan, and exact version. The official docs currently show four
   independently versioned products.
2. In CLI, run `agy`, open `/help`, `/skills`, `/agents`, `/hooks`, `/mcp`, `/permissions`,
   `/config`, `/model`, and `/usage`; compare each live panel with this file.
3. Run `agy -p "Return OK" --output-format stream-json` and record the `init.tools` array,
   permission mode, version output, and exit code.
4. In a disposable repository, test root and nested loading separately for `AGENTS.md`, `GEMINI.md`,
   `.agents/rules`, `.agents/skills`, `.agents/agents`, `.agents/hooks.json`, and
   `.agents/mcp_config.json`. Test conflicts, not just presence.
5. Exercise one deny rule and one blocking `PreToolUse` hook. A file on disk is not evidence that
   the active surface loaded or enforced it.
6. Repeat the discovery checks in Antigravity 2.0, standalone Antigravity IDE, and one IDE
   extension; one delivery does not describe the others.
7. If Remote Control is enabled, confirm which actions are dashboard-native and which are merely
   forwarded to the host. Test the Gemini API agent separately with an explicit API budget.

A read-only presence/file inspection was performed on installed 2.0 v2.11.0 and IDE v2.5.5; none
of the loading or execution steps above was performed.

## 16. Surface differences

| Area | Difference |
|---|---|
| Skills | 2.0/general docs use `~/.gemini/config/skills`; IDE uses `~/.gemini/antigravity/skills`; CLI uses `~/.gemini/antigravity-cli/skills` and documents flat `.md` files rather than nested `SKILL.md` folders |
| Context discovery | CLI website says workspace root; installed 2.0 v2.11.0 built-in docs say per-directory walk-up — disputed until run |
| Plugin staging | CLI documents `~/.gemini/antigravity-cli/plugins/<name>`; 2.0 manages Google bundles through Settings |
| Artifacts | 2.0 has a visual pane; CLI has a keyboard review panel; IDE has editor-integrated review |
| Settings | 2.0 has global/project hierarchy; CLI uses its own `settings.json`; SDK uses Python configuration |
| IDE delivery | Standalone IDE and five editor extensions share a family/version but are separate clients; Enterprise supports extensions, not standalone IDE |
| Remote Control | Browser dashboard or headless daemon controls a host session; it does not own a second capability stack |
| Managed API | `antigravity-preview-05-2026` runs in a Google-hosted Linux sandbox and has its own tools, hooks, persistence, budgets, and billing |
| Multimodal input | SDK documents image/PDF; managed API documents text/image only and explicitly rejects audio/video/document input |
| Enterprise | Deployment/governance mode across 2.0, CLI, and IDE Extensions; not a fifth core product |
| Sandbox | CLI Features documents Windows `AppContainer`; the dedicated Sandbox pages omit Windows — disputed |
| Automation | 2.0 exposes Scheduled Tasks/sidecars; headless CLI is the CI/programmatic surface |
| Models | Plans and Models disagree about which individual tiers receive third-party models |
| Workflows | IDE docs retain Workflows during migration; current guidance deprecates them for Skills by 2026-11-01 |

## 17. Known traps and official disputes

1. **Documentation is not execution.** This entire inventory remains `documented`; current version
   labels in a website navigation bar are not installed-version evidence.
2. **`/learn` path conflict.** The shared slash-command page says `.antigravity/rules.md`; the
   current Rules page says `.agents/rules` and documents `.agent/rules` only as backward
   compatibility. Use `.agents/rules`; verify `/learn` before depending on its output location.
3. **Skill paths and layouts differ by surface.** Do not rewrite all global skills to one path or
   infer CLI loading from the 2.0/IDE `SKILL.md` contract. Only the `.agents/skills` directory name
   is shared by the current pages. IDE's documented `~/.gemini/antigravity/skills` path still needs
   a loading test because installed IDE state otherwise lives under `.antigravity-ide`.
4. **CLI executable name conflict.** Installation and examples use `agy`; the CLI sandbox page
   shows `antigravity --sandbox`. Treat `agy --sandbox` as a reasonable inference, not a verified
   command, until `agy --help` confirms it.
5. **Windows sandbox conflict.** CLI Features says `AppContainer`; the dedicated Sandbox pages omit
   Windows. Neither official statement resolves the installed behavior.
6. **Custom-agent typos can hang.** The official Subagents page warns that invalid tool names may
   hang the child process.
7. **Workflows are transitional.** They are scheduled for deprecation in favour of Skills by
   2026-11-01; do not build a new portable contract on `.agents/workflows`.
8. **`always-proceed` is not a sandbox.** Permission policy and OS isolation are independent; the
   sandbox is disabled by default.
9. **Plans and Models conflict.** The live pages disagree about third-party-model plan access; use
   the active selector and `/usage` rather than freezing either table here.
10. **Remote Control inherits.** Seeing a host feature in the dashboard does not make it a separate
    Remote Control implementation or configuration surface.
11. **Context discovery conflicts.** The CLI website says workspace root, while installed 2.0
    v2.11.0 built-in docs say per-directory walk-up. Test root plus nested files before relying on
    either precedence model.

## 18. Not Antigravity features

- Google `agents-cli` is a separate tool for building and deploying ADK/Gemini Enterprise agents.
  Official codelabs explicitly describe it as a tool *for* coding agents, not a replacement for
  Antigravity.
- Agent Skills installed by `npx skills`, Firebase, Android, or other Google bundles are
  installables. Their presence in Google documentation does not make them built-ins.
- The official IDE-extension catalogue lists VS Code, Visual Studio, JetBrains, Zed, and Xcode; it
  documents no Antigravity Chrome extension. Chrome is a browser automation/debugging target, and
  the native Chrome DevTools MCP integration is not a browser extension. Sources:
  [IDE Extensions](https://antigravity.google/docs/ide/extensions/) and
  [Browser](https://antigravity.google/docs/ide/browser), retrieved 2026-09-04.
- A plugin directory or cached skill is not evidence that a running Antigravity surface loaded it.
