# Devin — formerly Windsurf

**Evidence status:** `documented, not tested`. No Devin surface was installed, launched or
enumerated for this file.
**Measured:** `not run`. `devin`, `windsurf` and `codeium` were absent from `PATH` and no
`~/.codeium`, `~/.devin` or `~/.config/devin` directory existed on the Linux container used on
2026-09-14. Absence on one machine establishes nothing about the product.
**Surfaces:** Devin Cloud, Devin Desktop, Devin CLI and Devin Review are the four the vendor
names; Windsurf JetBrains survives as a separate local-agent product name. None was checked.
**Docs:** `https://docs.devin.ai`, retrieved **2026-09-14**.

> **Retrieval channel, and it is weaker than the other files here.** `docs.devin.ai` and
> `docs.windsurf.com` are blocked by this session's network egress policy, so no page was read
> directly. Every claim below comes from the Context7 index of `docs.devin.ai` and carries the
> upstream page path the index reported. **An index is a mirror and can lag the live page.**
> Re-read the cited paths directly before relying on a row, and prefer
> [`https://docs.devin.ai/llms.txt`](https://docs.devin.ai/llms.txt) — the vendor publishes a
> machine-readable page index — as the enumeration entry point.

> Lower bound — see [README](README.md). Absence means "not recorded", not "not there".

## 0. Product identity — read this before the paths

This is the one inventory in this directory whose **subject was renamed while the project was
tracking it**, so the name in your editor, the name in the docs and the name in the paths on
disk disagree with each other by design.

| Claim | Evidence |
|---|---|
| Windsurf is now **Devin Desktop**; the vendor unified Devin Cloud, Devin Desktop, Devin CLI and Devin Review under the Devin brand, with Desktop as the primary command center | [Devin Desktop FAQ](https://docs.devin.ai/desktop/devin-desktop-faq), retrieved 2026-09-14 |
| Legacy `.windsurfrules` files **remain supported**; `.devin/rules/` is preferred and takes precedence over `.windsurf/rules/` | [Devin Desktop FAQ](https://docs.devin.ai/desktop/devin-desktop-faq), retrieved 2026-09-14 |
| `.windsurf/skills/` remains a documented project skill location alongside `.devin/skills/` | [CLI Skills](https://docs.devin.ai/cli/extensibility/skills), retrieved 2026-09-14 |
| "Windsurf" still names a shipping product: an org ACU limit covers "Devin Desktop, **Windsurf JetBrains**, and Devin CLI" together as local agents | [Org ACU limits](https://docs.devin.ai/admin/billing/org-acu-limits), retrieved 2026-09-14 |
| "Cascade" still appears in current documentation paths (`/desktop/cascade/...`) and as a model-policy group name covering Devin CLI and Devin Local | [Memories](https://docs.devin.ai/desktop/cascade/memories), [Model provisioning](https://docs.devin.ai/federal/model-provisioning), retrieved 2026-09-14 |

**What is deliberately not claimed here.** Secondary reporting states a rename date, that Cascade
was replaced by "Devin Local" and that legacy Cascade was retired on a specific date. Those are
blog and aggregator sources, not vendor documentation, so under this project's
[evidence rules](../../AGENTS.md) they are `(unverified)` and are **not** recorded as facts above.
The vendor's own pages still carry `cascade` path segments and still use the word as a policy
group, which is a reason to date any such claim rather than repeat it. `Devin Local` is documented
as the agent identity the Devin CLI presents over ACP, which is a narrower statement than a
retirement; see section 7.

> **Consequence for this repository.** `research/MATRIX.md` recorded a Windsurf row on 2026-09-05
> that cited a Cascade Skills page and listed two project paths. That row is superseded by
> section 5 below: it named the wrong surface (the current source is the **CLI** extensibility
> section), missed `.devin/skills/` and `~/.config/devin/skills/`, and treated `<channel>` as the
> literal string `windsurf`. Corrected there, dated here.

## 1. Commands

Devin CLI slash commands, from the [commands reference](https://docs.devin.ai/cli/reference/commands),
retrieved 2026-09-14. All are built-in unless noted. This is the documented list, not an
enumeration of a running build.

| Command | Does what |
|---|---|
| `/help` | Show available slash commands |
| `/shortcuts` | Browse and rebind keyboard shortcuts; exposes each action's `context.action` identifier |
| `/config` | Open the interactive config editor |
| `/context` | Show context window usage |
| `/compact` | Force conversation compaction |
| `/usage` | Show estimated credit/ACU usage for the session, including earlier openings of a resumed session |
| `/session-stats` | Session statistics (alias `/stats`) |
| `/copy` | Copy the last response to the clipboard |
| `/feedback` | Rate the last response (`up`/`down`) |
| `/bug` | Report a bug to the Devin CLI developers |
| `/update` | Check for and install updates (`--force` reinstalls on the latest version) |
| `/upgrade` | Upgrade the subscription plan |
| `/login`, `/logout`, `/login-status` | Authentication; `/login-status` is advertised to ACP hosts as `/status` |
| `/org` | Select the Devin organization |
| `/mouse` | Toggle mouse event capture |
| `/handoff` | Package conversation context and the current git branch into a **cloud** Devin session ([handoff](https://docs.devin.ai/work-with-devin/devin-handoff)) |

Shell entry points, same reference:

| Entry | Does what |
|---|---|
| `devin -- <task>` | Start a session with a task |
| `devin -p "<task>"` | Print the response and exit |
| `devin -c` / `devin -r <id>` | Resume the last / a specific session |
| `devin --model <name>` | Select the model for the session |
| `devin --permission-mode accept-edits` | Run under a named permission mode |
| `devin --sandbox` | Run the session sandboxed |
| `devin --export [path]` | Export the conversation |
| `devin acp` | Serve the agent over ACP; this is the form an ACP host launches as **Devin Local** |
| `devin skills list\|show\|paths` | Enumerate skills, inspect one, print skill directory locations |
| `devin plugins install\|list\|info\|update\|remove\|prune` | Manage plugin bundles |
| `devin rules list`, `devin mcp list` | List active rules and MCP servers, including plugin-contributed ones |

**A skill can become a slash command.** A skill whose frontmatter declares `triggers: [user]` is
invoked as a slash command, and an MCP server's published prompts appear as
`/mcp__<server>__<prompt>`. Both share the namespace with the built-ins above, which is why
this project's `hr-` prefix rule applies here as it does everywhere else; see section 7.

## 2. Built-in skills

**Not recorded.** No vendor page enumerating skills that ship with Devin was retrieved, and the
`devin skills list` output that would settle it was not run. Under this directory's rules that
makes built-in skills **unknown, not absent** — do not read the empty table as evidence that
Devin ships none.

What *is* documented is that the skills mechanism carries both user-invoked commands and
agent-triggered context blobs ([commands reference](https://docs.devin.ai/cli/reference/commands)),
so any built-in set would occupy the same namespace as installed and project skills.

## 3. Tools

Named in the [permissions reference](https://docs.devin.ai/cli/reference/permissions), retrieved
2026-09-14, as the values a permission rule may allow or deny: `read`, `edit`, `grep`, `glob`,
`exec`. The same identifiers appear as `allowed-tools` values in skill frontmatter (section 5).

This is a permission-surface list, obtained from configuration documentation rather than from a
model-visible schema dump. Treat it as a lower bound: it names the tools the permission system
arbitrates, not necessarily every tool the model can call. Permission rules support
`allow` / `deny` / `ask` and path-scoped forms such as `Read(src/**)` and `Write(**)`.

## 4. Installable — official

| Name | Does what | How to install | Gated? |
|---|---|---|---|
| Plugins | Bundle **skills, rules, hooks, MCP servers and subagents** in one installable unit | `devin plugins install <source>` — a GitHub `owner/repo`, a git URL or a local path; an interactive trust prompt lists the contents before confirmation (`-y` skips it) | Team marketplaces and governance configs are organization features |
| MCP servers | External tool servers; their published prompts also become slash commands | Declared in MCP configuration (section 5) | Each server has its own setup, credentials and network access |

Plugin bundles are the widest extension unit documented here, and the vendor states their reach
explicitly ([CLI changelog](https://docs.devin.ai/cli/changelog/stable), retrieved 2026-09-14): a
plugin's `AGENTS.md`, `AGENT.md` or `.windsurfrules` load as **always-on rules**, its `hooks.json`
loads alongside project hooks, MCP servers declared through a root `.mcp.json` or an inline
manifest run for the session, and `agents/<name>/AGENT.md` files surface as `<plugin>:<agent>`
subagent profiles. `devin plugins info` and the install trust prompt list all of them first.

> **Read that list against this project's trust argument.** Installing one plugin can add
> always-on instructions, a blocking hook, an MCP server and a subagent in a single confirmed
> step. `research/MATRIX.md` makes the same point about repository-committed skills; here the
> unit is larger and the confirmation is a single prompt.

## 5. Extension points

All rows `documented`, retrieved 2026-09-14, via the Context7 index caveat at the top.

| Mechanism | Documented location / boundary | Source |
|---|---|---|
| Instructions | `AGENTS.md` at the project root, read automatically; nested `AGENTS.md` in subdirectories scope instructions to that subtree | [CLI rules](https://docs.devin.ai/cli/extensibility/rules), [AGENTS.md](https://docs.devin.ai/desktop/cascade/agents-md) |
| Rules, native | `.devin/rules/` — preferred, and takes precedence over `.windsurf/rules/` | [Devin Desktop FAQ](https://docs.devin.ai/desktop/devin-desktop-faq) |
| Rules, legacy and foreign | `.windsurf/rules/*.md`, `.windsurf/global_rules.md`, legacy `.windsurfrules`, plus imported `.cursor/rules` | [CLI rules](https://docs.devin.ai/cli/extensibility/rules), [Devin Desktop FAQ](https://docs.devin.ai/desktop/devin-desktop-faq) |
| Rules discovery | Workspace and sub-directories, searching up to the **git root**; multiple open folders are deduplicated. Root rules load at session start; subdirectory rules load **lazily**, when the agent touches files there | [Memories](https://docs.devin.ai/desktop/cascade/memories), [CLI rules](https://docs.devin.ai/cli/extensibility/rules) |
| Rule activation | Frontmatter trigger values `always_on`, `manual`, `model_decision`, `agent`, `glob` | [CLI rules](https://docs.devin.ai/cli/extensibility/rules) |
| Skills | Six documented roots — see the table below | [CLI Skills](https://docs.devin.ai/cli/extensibility/skills) |
| MCP | `.devin/mcp_config.local.json` for project servers, documented as gitignored because it carries tokens; plugins may declare servers via a root `.mcp.json` or an inline manifest | [MCP overview](https://docs.devin.ai/cli/extensibility/mcp/overview) |
| Hooks | `.devin/hooks.v1.json` plus user-level config; **hooks already present in `.claude/` directories are picked up automatically**; discovered from the working directory up to the repository root | [Hooks overview](https://docs.devin.ai/cli/extensibility/hooks/overview) |
| Subagents | `agents/<name>/AGENT.md` inside a plugin, surfaced as `<plugin>:<agent>`; a skill may also declare `subagent: true` | [CLI changelog](https://docs.devin.ai/cli/changelog/stable), [creating skills](https://docs.devin.ai/cli/extensibility/skills/creating-skills) |

### Skill roots — six, and three of them are project-scoped

| Location | Scope | Committed |
|---|---|---|
| `.agents/skills/<name>/SKILL.md` | project | yes |
| `.devin/skills/<name>/SKILL.md` | project | yes |
| `.windsurf/skills/<name>/SKILL.md` | project | yes |
| `~/.agents/skills/<name>/SKILL.md` | global | no |
| `~/.config/devin/skills/<name>/SKILL.md` | global | no |
| `~/.codeium/<channel>/skills/<name>/SKILL.md` | global | no |

`<channel>` is a **variable**, documented as `windsurf`, `windsurf-next` or `windsurf-insiders`
depending on the CLI channel — not the literal directory `windsurf`. On Windows the global root is
`%APPDATA%\devin\skills\<name>\SKILL.md` rather than `~/.config/devin/skills/`.

**houserules already writes one of these roots.** `.agents/skills/` is installed for the existing
`codex`/`goose`/`antigravity` selection, so a Devin adopter is covered by the current installer
with **no new directory**, and this project deliberately did not add a `.devin/skills/` or
`.windsurf/skills/` target — the reasoning, and the redundancy analysis it follows, are in
[`MATRIX.md` section 2](../../research/MATRIX.md#2-skills--the-same-standard-three-different-paths).
Coverage by path is not evidence of loading; nothing here was run.

### Skill frontmatter is wider than the portable core

```yaml
name, description, argument-hint, model, subagent,
allowed-tools, permissions: {allow, deny, ask}, triggers: [user|model]
```

From [creating skills](https://docs.devin.ai/cli/extensibility/skills/creating-skills), retrieved
2026-09-14. `name` and `description` are the portable subset this project's checker looks for; the
rest — model pinning, subagent dispatch, per-skill tool permissions — are **vendor-local fields**.
A `SKILL.md` written for Devin's full frontmatter is not portable content, even though the file
layout is identical. A skill written to the portable core travels in the other direction.

### Hook events

`PreToolUse`, `PostToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `PostCompaction`,
`SessionStart`, `SessionEnd` ([hooks overview](https://docs.devin.ai/cli/extensibility/hooks/overview),
retrieved 2026-09-14). A handler receives event data on stdin and blocks either by exiting
non-zero or by returning `{"decision": "block", "reason": "..."}` — the same event → matcher →
command shape Claude Code, Codex and Antigravity use, with `PermissionRequest` and
`PostCompaction` as events not present in all of them. See
[`MATRIX.md` section 5](../../research/MATRIX.md#5-hooks-and-lifecycle) for the cross-agent
comparison and for why a shared schema still does not make a hook a portable guarantee.

## 6. How to enumerate this yourself

Nothing below was run. This is the procedure that would move rows from `documented` to `tested`,
and until it is run with a named surface and version, this file stays `documented`.

1. **Identify the surface and version first.** Devin Desktop reports its own version; the bundled
   CLI is separate, and on Windows the vendor documents Desktop writing a shim so that updating
   Desktop updates the `devin` command. Record both, plus the CLI channel (`windsurf`,
   `windsurf-next`, `windsurf-insiders`) — the channel changes the global skill path.
2. **Skills:** `devin skills paths` prints the directory locations the running build actually
   uses; `devin skills list [--trigger user|model]` enumerates what it discovered; `devin skills
   show <name>` confirms which copy won. This is the one command that settles the six-root table
   above against a real build, including same-name precedence across `.agents/`, `.devin/` and
   `.windsurf/`, which is `(unverified)` here.
3. **Rules:** `devin rules list` against a fixture carrying `AGENTS.md`, `.devin/rules/`,
   `.windsurf/rules/` and `.windsurfrules` at once, to observe the documented precedence rather
   than assume it. Add a subdirectory rule and confirm it stays unloaded until a file there is
   touched.
4. **MCP and plugins:** `devin mcp list` and `devin plugins list` / `devin plugins info <name>`.
5. **Hooks:** place a `PreToolUse` handler returning `{"decision":"block"}` and confirm the
   action is actually refused; then repeat with the handler in `.claude/` only, which is the
   documented cross-vendor pickup and the claim most worth checking.
6. **Negative controls throughout:** an empty repository and a fixture with only a foreign path,
   as used in the [Cursor/Kiro acceptance record](../../tests/workflows/cursor-kiro/README.md).
   A self-reported list is not loading evidence.

## 7. Surface differences

| Surface | Native capability route | Extension route / boundary |
|---|---|---|
| Devin Desktop | Editor plus the **Agent Command Center** — a Kanban board over local *and* cloud agents, grouped by status; `Ctrl/Cmd+G` switches Agent and Editor mode, and `devin.agentWindow.location` can split it into its own window ([Agent Command Center](https://docs.devin.ai/desktop/agent-command-center), [changelog](https://docs.devin.ai/desktop/changelog)) | `.devin/` preferred over `.windsurf/`; a workspace must be **trusted** before local agents activate |
| Devin CLI | Interactive and `-p` headless sessions; `--sandbox` and `--permission-mode`; `/handoff` promotes work to a cloud session | The extensibility surface documented above — rules, skills, MCP, hooks, plugins — is written from the CLI's pages |
| Devin Local (ACP) | The CLI launched as `devin acp` and registered by an ACP host under the id `devin-cli`, name **Devin Local** ([ACP](https://docs.devin.ai/desktop/acp)) | Whatever the ACP host exposes; `/login-status` is re-advertised as `/status` to hosts |
| Devin Cloud | Sessions created from a handoff or directly | Plugins are documented as spanning cloud sessions, the CLI and Desktop |
| Windsurf JetBrains | Not documented in this pass beyond its existence | Counted with Desktop and CLI under one org **local-agent** ACU budget |

**The surface split is the trap here.** Nearly every extension path above is documented on
`/cli/...` pages. Devin Desktop, Devin Cloud and Windsurf JetBrains are **not** established to
honour the same precedence, discovery order or frontmatter by the sources retrieved for this
file. This project has been wrong before about a vendor whose documentation it read correctly, so
treat "Devin CLI documents X" as exactly that until section 6 is run per surface.

**Known unknowns, carried to `MATRIX.md` open items:** built-in skill set; same-name precedence
across the three project roots; whether `.claude/` hook pickup also applies outside the CLI;
whether Devin's duplicate-skill behaviour replaces silently like Claude Code or lists both like
Codex — the failure mode that decides how dangerous an unprefixed name is.
