# Extension mechanism matrix

What each agent lets you extend, in what format, at what path. This is the raw material; the
portability verdict derived from it lives in `PORTABILITY.md`.

**Evidence rule for this file:** every row carries a source and a retrieval date, or is tagged
`(unverified)`. Anything testable locally is **tested, not cited** — sources in this field contradict
each other often enough that a citation is not evidence. Section 2 below documents a case where two
official pages disagree with each other.

**Evidence grades.** Three, and they are not interchangeable:

| Grade | Means |
|---|---|
| **tested** | run on a real installation on this machine, with the surface and version recorded |
| **documented** | official vendor documentation, with a retrieval date. Not run |
| `(unverified)` | neither — a claim carried forward without a source |

**Only Claude Code and Codex are `tested`.** Every other agent in this file is `documented` at
best. That distinction is load-bearing: this project has twice been wrong about a vendor whose
documentation it had read correctly, because reading is not running.

**Checked baseline: 2026-08-31. `recheck_by: 2026-11-30.`** Claude Code and Codex rows were re-read
2026-09-02 against seventeen official pages; that pass was documentation-only and changed no
evidence grade, because reading is not running. Follow-up documentation and local verification
through **2026-09-04** did change the evidence set: Codex `--search` became `documented`,
project-scoped `.agents/skills` became `tested` in the Desktop app and a sandbox-launched CLI child,
repository `hr-onboard` became `tested` for both agents, and `tested` now requires a named surface
and version. A 2026-09-04 official-documentation pass added a full Antigravity inventory spanning
2.0 v2.12.2, CLI v1.1.25, SDK v0.1.16 and IDE v2.5.5; it remains `documented`, not `tested`. See the
revision log and the canonical inventories in `docs/agents/`. Platform surfaces in this field change monthly —
Amazon Q Developer is being wound down — new signups blocked 2026-05-15, full end of support
2027-04-30, with AWS directing users to **Kiro**, which is in this table — Gemini CLI is being
replaced by Antigravity CLI, Cursor was acquired
and shipped a git forge, all within twelve months. **Every row below is a claim about a date, not a
permanent fact.** A 2026-09-05 documentation recheck also confirms Goose moved to the
Agentic AI Foundation (AAIF); use the current [official documentation host](https://goose-docs.ai/docs/guides/context-engineering/using-skills/)
for future rechecks. This changes neither its skill path nor its `documented` grade. Re-run the local tests on each recheck; they take minutes and settle what
documentation disputes.

Status: **Claude Code and Codex are `tested`** — real installations, surfaces and versions recorded
(with any historical environment gap explicit), and the
only two this project should be described as supporting. **Goose, Cursor, Copilot, OpenCode,
Antigravity, Kiro and Devin are `documented`**: their rows cite official pages with retrieval
dates, and native capability loading has not been run for those rows. **Devin, added 2026-09-14,
is the weakest-sourced of them** — its pages were unreachable from the authoring session and every
row came through a documentation index; see the open items and the
[Devin inventory](../docs/agents/devin.md). Cursor and Kiro now have
[dated inventories](../docs/agents/README.md) and local launcher/installer checks (2026-09-06);
these do not promote their capabilities to tested. Zed has supplemental documented skill-path coverage below. The Windsurf documentation URL
redirected to Devin Desktop Cascade documentation on 2026-09-05; the supplemental row records
that source observation, not a verified product identity. Remaining mechanisms and runtime
behavior are backlog. That Windsurf row is **superseded as of 2026-09-14**: the product was renamed
and the row is now a full Devin inventory, corrected — see section 2 and the revision log.

**2026-09-06 supplemental observation:** a reviewer reports successful explicit invocation of the
three optional toolkit skills in Claude Code CLI 2.1.251, with empty-repository and `.agents`-only
negative controls. The [acceptance record](../tests/workflows/toolkit-adoption/README.md#subsequent-reviewer-reported-claude-loading--2026-09-06)
preserves the results and the unresolved tool-isolation evidence. This is reviewer-reported
execution, not an independently checked expansion of the `tested` claims below; implicit triggering,
comparative effectiveness and loading of these candidates on other surfaces remain unverified.

---

## 1. Instruction file — what each agent reads

| Agent | Reads | Path / discovery | Notes |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md` only | `./CLAUDE.md` **or `./.claude/CLAUDE.md`**; up the tree; `~/.claude/CLAUDE.md` personal; managed-policy path or the `claudeMd` settings key | **`tested`** — Claude Code CLI/Desktop session v2.1.251, 2026-08-29. **Does not read `AGENTS.md` natively.** `@AGENTS.md` import from `CLAUDE.md` works. With both files present and no import, `AGENTS.md` is ignored **and nothing says so** |
| **Codex** | `AGENTS.md` | every directory level from repo root to cwd; `~/.codex/AGENTS.md` global | Files **concatenate**, they do not override — a subdirectory adds to the root. `AGENTS.override.md` replaces its `AGENTS.md` at that level. `project_doc_max_bytes` = **32 KiB by default — configurable, not a hard ceiling**. What it bounds is disputed between two official pages; see section 2. **Mixed grade:** reading `AGENTS.md` was `tested` on the CLI 0.151.0-alpha.7.2 baseline (process environment not recorded), 2026-08-31, and reconfirmed in the Desktop Codex-mode task and its sandbox-launched CLI 0.153.0 child, 2026-09-04; the precedence and byte-budget rules are `documented`, retrieved 2026-09-01 |
| **Goose** | **`AGENTS.md`**, then `.goosehints` | project directories; `~/.config/goose/` global | Default is `["AGENTS.md", ".goosehints"]`, overridable with the `CONTEXT_FILE_NAMES` env var. All found files are combined. `documented`, retrieved 2026-08-31 |
| **Cursor** | **`AGENTS.md`** | project root **and any subdirectory, no configuration** | Also `.cursor/rules/*.mdc`, and the Cursor CLI reads `CLAUDE.md` too. **No global `~/.cursor/AGENTS.md`** — cross-project instructions go to User Rules or Team Rules. `documented`, retrieved 2026-09-01 |
| **Copilot** | **`AGENTS.md`** | repo root, plus nested per-subtree | Also reads `.github/copilot-instructions.md`, `.github/instructions/**`, **and `CLAUDE.md` and `GEMINI.md`**. Note the precedence: `.github/copilot-instructions.md` **outranks** `AGENTS.md`. `documented`, retrieved 2026-09-01 |
| **Kiro** | **`AGENTS.md`** | workspace root/subdirectories, plus global steering location | Custom-agent inheritance is disputed; see [Kiro inventory](../docs/agents/kiro.md#5-extension-points). [Steering](https://kiro.dev/docs/steering/), `documented`, retrieved 2026-09-06 |
| **Antigravity** | **`AGENTS.md`** and `GEMINI.md` | ⚠️ **disputed:** CLI website says workspace root; installed 2.0 v2.11.0 built-in docs say walk from cwd to repository root; `~/.gemini/GEMINI.md` global | Neither discovery contract was exercised. `.agents/rules/*.md` adds Manual, Always On, Model Decision and Glob activation; `.agent/rules` is a legacy fallback. [Best Practices](https://antigravity.google/docs/cli/best-practices/), [Migration](https://antigravity.google/docs/gcli-migration), and [Rules](https://antigravity.google/docs/rules-workflows/), retrieved 2026-09-04; installed built-in `agy-customizations/docs/rules.md` inspected 2026-09-04. Precedence remains `(unverified)` |
| **OpenCode** | **`AGENTS.md`** | project | Listed in section 2 as an `AGENTS.md` reader but omitted from this table until 2026-09-01. `documented`, retrieved 2026-09-01 |
| **Devin** (formerly Windsurf) | **`AGENTS.md`** | project root, read automatically; nested `AGENTS.md` scopes instructions to a subtree | Also `.devin/rules/` — **preferred, and it takes precedence over `.windsurf/rules/`** — plus legacy `.windsurfrules` and imported `.cursor/rules`. Discovery walks workspace subdirectories up to the **git root**; root rules load at session start while subdirectory rules load **lazily** on first access. Rule frontmatter triggers: `always_on`, `manual`, `model_decision`, `agent`, `glob`. `documented`, retrieved 2026-09-14; see the [Devin inventory](../docs/agents/devin.md#5-extension-points) for the retrieval-channel limit |

> **Finding — the cleanest result in this survey.** Every agent surveyed reads `AGENTS.md`
> **except Claude Code.** Codex authored it; Cursor, Copilot, Kiro and Antigravity all read it;
> Copilot goes further and reads `CLAUDE.md` and `GEMINI.md` as well.
>
> The `@AGENTS.md` import line in `CLAUDE.md` is therefore not an optional adapter but a
> **correctness requirement** — and it is the only one-line change that makes a repository legible
> to every agent in this table.

## 2. Skills — the same standard, three different paths

Most surveyed skill-capable agents implement the [Agent Skills](https://agentskills.io) open
standard: a directory containing `SKILL.md` with YAML frontmatter and markdown body. Antigravity
2.0 and IDE document that layout, while Antigravity CLI currently documents flat `.md` skills in
the same `.agents/skills/` directory. **The format is broadly portable, but not uniform across even
one vendor's surfaces; the location is not portable either.**

| Agent | Project path | User path | Other |
|---|---|---|---|
| **Claude Code** | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/` | `.claude/commands/*.md` still works (merged into skills). **`tested`** — Claude Code CLI/Desktop session v2.1.251, 2026-08-31 |
| **Copilot** | **`.agents/skills`**, `.claude/skills`, `.github/skills` | `~/.copilot/skills`, **`~/.agents/skills`** | `documented`, retrieved 2026-09-01 |
| **Codex** | **`.agents/skills/`** — searched from cwd up to repo root | **`~/.agents/skills/`** | `/etc/codex/skills` admin, plus plugin `skills/` and the vendored catalogue. **Invoked with `$<name>`, not `/`**. Project path `tested`: CLI 0.151.0-alpha.7.2 baseline (process environment not recorded), 2026-08-31; reconfirmed in the Desktop Codex-mode task and its sandbox-launched CLI 0.153.0 child, 2026-09-04. Other locations `documented`, [official Build skills](https://learn.chatgpt.com/docs/build-skills), retrieved 2026-09-04 |
| **Goose** | **`.agents/skills/`** | **`~/.agents/skills/`** | `~/.agents/plugins/<name>/`; legacy `.goose/skills/` still discovered; `.agents/skills/` is recommended. `documented`, [official skills](https://goose-docs.ai/docs/guides/context-engineering/using-skills/), retrieved 2026-09-05 |
| **Antigravity** | **2.0/IDE:** `<project-root>/.agents/skills/<name>/SKILL.md`; **CLI:** `.agents/skills/*.md` | **2.0/general:** `~/.gemini/config/skills/`; **IDE:** `~/.gemini/antigravity/skills/`; **CLI:** `~/.gemini/antigravity-cli/skills/` | `.agent/skills` remains a 2.0/IDE legacy fallback. The shared directory name hides different file-layout and global-path contracts. **`documented`**, [2.0 Skills](https://antigravity.google/docs/skills), [IDE Skills](https://antigravity.google/docs/ide/skills), and [CLI Plugins & Skills](https://antigravity.google/docs/cli/plugins/), retrieved 2026-09-04 |
| **Cursor** | **`.agents/skills/`** and `.cursor/skills/` | **`~/.agents/skills/`**, `~/.cursor/skills/` | Also loads `.claude/skills/` and `.codex/skills/` for compatibility. Nested project skill directories are discovered and scoped to their subdirectory. Optional Cloud sync covers ~/.cursor/skills only; other local roots are not automatically copied. See [Cursor inventory](../docs/agents/cursor.md#7-surface-differences) and [skills source](https://cursor.com/docs/skills). `documented`, retrieved 2026-09-06; nested discovery rechecked, not runtime-tested |
| **Kiro** | `.kiro/skills/` | project or global | Workspace/global skills are documented; custom-agent default inheritance differs between official pages. Explicit `skill://` resources are supported, not established as universally required. See [Kiro inventory](../docs/agents/kiro.md#5-extension-points). `documented` / disputed, retrieved 2026-09-06 |
| **OpenCode** | `.opencode/skills/`, `.claude/skills/`, **`.agents/skills/`** | `~/.config/opencode/skills/`, `~/.claude/skills/`, **`~/.agents/skills/`** | Walks up to the git worktree, loading each match along the way. `documented`, retrieved 2026-09-01 |
| **Devin** (formerly Windsurf) | **`.agents/skills/`**, `.devin/skills/`, `.windsurf/skills/` | **`~/.agents/skills/`**, `~/.config/devin/skills/`, `~/.codeium/<channel>/skills/` | Nested `<name>/SKILL.md` in all six. `<channel>` is a **variable** — `windsurf`, `windsurf-next` or `windsurf-insiders` — not the literal directory `windsurf`; on Windows the global root is `%APPDATA%\devin\skills\`. Frontmatter extends well past the portable core (`model`, `subagent`, `allowed-tools`, `permissions`, `triggers`). `devin skills paths` prints what a running build actually uses. `documented`, [CLI Skills](https://docs.devin.ai/cli/extensibility/skills), retrieved 2026-09-14. Same-name precedence across the three project roots is **`(unverified)`** |

### Supplemental skill-path coverage (2026-09-05)

These are official-documentation observations, not additional tested agents or installer targets.

| Surface | Project / user paths | Evidence and limit |
|---|---|---|
| Zed Agent | `.agents/skills/`; `~/.agents/skills/` | `documented`, [Skills](https://zed.dev/docs/ai/skills), retrieved 2026-09-05. Named directories with SKILL.md; project loading requires a trusted worktree. Does not establish external-agent behavior inside Zed |
| ~~Windsurf / current Devin Desktop Cascade docs~~ | ~~`.windsurf/skills/`; `~/.codeium/windsurf/skills/`~~ | **Superseded 2026-09-14 — promoted to the main table above as Devin, and corrected.** The 2026-09-05 row was wrong in three ways, all of them the same mistake: it read one page and generalised. It named the **Desktop/Cascade** surface when the current source is the **CLI** extensibility section, it missed `.devin/skills/` and `~/.config/devin/skills/` entirely, and it recorded `~/.codeium/windsurf/skills/` as a literal path when `<channel>` is a variable. See the [Devin inventory](../docs/agents/devin.md#0-product-identity--read-this-before-the-paths) |

> **Why that row was wrong is more useful than the correction.** It was written from the page a
> redirect happened to land on. The vendor had renamed the product, moved the authoritative
> extensibility documentation to a different surface's section, and added a native directory —
> and a single-page read reproduced none of that. This is the same failure this file warns about
> at the top: **reading is not running, and reading one page is not reading the documentation.**

> **`.agents/skills/` has become the majority path — reversing what this section said before.**
> Per official documentation retrieved through 2026-09-14, it is read by **Codex, Goose,
> Antigravity 2.0/IDE, Cursor, Copilot, OpenCode and Devin**; only **Claude Code** and **Kiro**
> do not. Devin is the newest row and reads it alongside two vendor-native project roots.
>
> **That is a vendor-level path count, not end-to-end surface coverage.** Seven of the nine rows
> have never been run here — only Codex and Claude Code have. Antigravity CLI documents the same
> directory name but a flat `.md` layout, which this repository's nested `SKILL.md` installer does
> not synthesize.
>
> **For the documented nested `SKILL.md` surfaces, the minimal covering set is still three
> directories, and a ninth agent did not add a fourth:**
>
> | Directory | Covers |
> |---|---|
> | `.agents/skills/` | Codex, Goose, Antigravity 2.0/IDE, Cursor, Copilot, OpenCode, Devin |
> | `.claude/skills/` | Claude Code (also read by Cursor, Copilot, OpenCode) |
> | `.kiro/skills/` | Kiro |
>
> `.cursor/skills/` and `.opencode/skills/` are **redundant** — both agents read `.agents/skills/`.
> `install.py` still writes all five. Antigravity CLI coverage is a separate open test below.
>
> **Devin was admitted as documentation only, with no installer target, and this table is the
> reason.** Its native project root is `.devin/skills/` and it also reads the legacy
> `.windsurf/skills/`, but it reads `.agents/skills/` as well — so the existing installation
> already reaches it, and adding either directory would have widened what lands in adopters'
> repositories to buy nothing. That is the same redundancy argument already standing against
> `.cursor/` and `.opencode/`; it would be incoherent to act on it in one direction only.
> Reaching a path is not loading a skill: nothing Devin-related has been run.
>
> ### A ninth consumer, and not a coding agent
>
> **Anthropic Managed Agents reads `.claude/skills/` too** — the same directory, with no installer,
> no configuration and no entry in the agent's `skills` array. When a session mounts a repository
> through the `github_repository` resource, the repo's root `.claude/skills` is scanned at session
> start and every skill found becomes available. `documented`, retrieved 2026-09-02.
>
> It is stricter than any coding agent's discovery, and the constraints are worth knowing because
> `install.py` already satisfies them:
>
> | Rule | Effect |
> |---|---|
> | Exactly `.claude/skills/<name>/SKILL.md`, **one level deep at the repo root** | A bare `SKILL.md`, anything deeper, or a `skills/` outside `.claude` is not discovered |
> | Scanned **once, at session start** | Mid-session commits are not picked up |
> | Requires the toolset's **`read`** tool | An agent with `read` disabled loads no repository skills |
> | **Cloud sandboxes only** | Self-hosted sandboxes do not support GitHub repository resources |
>
> This matters to the portability argument in `PORTABILITY.md`: the layer reaches a surface that is
> not a coding agent at all, which is the strongest available evidence that **a checked-in
> `SKILL.md` is the durable artifact** and the vendor path is the accident.
>
> ⚠️ **It also widens the trust boundary, and Anthropic says so directly:** repository skills are
> agent instructions, loaded **without a review step**, and session tools such as `bash` and
> `web_fetch` give them real reach. Anyone who can commit to the repository — including through a
> merged external pull request — can add one. Review `.claude/skills` before mounting a repository
> that accepts outside contributions.
>
> **This is the second reversal of this row**, which is the point: an earlier draft called
> `.agents/skills/` the emerging standard, a later one called that wrong, and the vendors have now
> moved to make the first reading correct. *(See the revision log.)*
>
> **Tested 2026-08-31:** a skill in `.agents/skills/` was invisible to Claude Code v2.1.251 while a
> skill in `.claude/skills/` in the same directory was found. Both had valid frontmatter.
>
> The ecosystem's own answer to this is **installers** — third-party skill collections ship a CLI
> that copies the same `SKILL.md` into each vendor's path. That is the working pattern, and it
> confirms the fragmentation rather than solving it.

### An asymmetry worth designing around: HTML comments

**Claude Code strips block-level HTML comments from `CLAUDE.md` before injecting it.** Codex does
**not** strip them from `AGENTS.md`. Comments inside code blocks survive in both; opening the file
with the Read tool shows them either way.

So the same `<!-- ... -->` block is **free on Claude Code and billed on Codex, every session**. This
repository's `templates/AGENTS.md` carries a ~3.5 KB instructional comment block, which is why it
tells you to delete it once the file is filled — a cost that only exists on one of the two agents.

Source: Claude Code memory documentation, retrieved 2026-08-31; Codex has no equivalent statement
and the file is concatenated as-is.

### Two official pages disagree on `project_doc_max_bytes`

The `AGENTS.md` discovery page says the limit applies to the **combined size of all concatenated
files** and that Codex "stops adding files" once reached. The configuration reference describes it
as "Maximum bytes read from `AGENTS.md`", reading as **per file**. Both retrieved 2026-09-01.

`check.py` measures the **chain total**, the stricter of the two readings. If the per-file reading
is the correct one, the check is conservative rather than wrong. **This is exactly the case the
evidence rule at the top of this file exists for**, and it is unresolved by documentation alone.

Also unmodelled: **`project_doc_fallback_filenames`** — "additional filenames to try when
`AGENTS.md` is missing". A repository whose Codex config names other files has instruction content
the checker cannot see, because the setting can live in `~/.codex/config.toml`, outside the
repository entirely. `check.py` covers the two default names only and says so.

### A gitignored `AGENTS.override.md` is loaded instruction content that never reaches review

Codex's worktree documentation, retrieved 2026-09-02:

> "Codex automatically copies an ignored `AGENTS.override.md` into local managed worktrees, so you
> don't need to list it in `.worktreeinclude`."

Stated as a property rather than a convenience: an `AGENTS.override.md` that is in `.gitignore`
**replaces the committed `AGENTS.md` at its level, is loaded into every session, and follows the
developer into every Codex-managed worktree — while being invisible to anyone auditing the
repository's agent instructions, because it is not in the repository.**

Two consequences for this project:

- **`check.py` sees it and should.** It scans `AGENTS.override.md` on disk, so it measures the chain
  a session actually gets rather than the chain that is committed. That is the correct behaviour and
  is now deliberate rather than incidental.
- **"Read the repo to see what the agent was told" is not sound on Codex.** The equivalent of
  Claude Code's `/context` is `codex debug prompt-input`, which renders what the model actually
  receives. Reading files is not the same check.

Ordinary Git worktrees created from the command line do **not** get this copy; the behaviour is
specific to worktrees the desktop app manages. `documented`, retrieved 2026-09-02 —
`docs/agents/codex.md` section 7.

**The `description` field is a trigger, not a title.** Codex's documentation is explicit: it
determines whether the model selects the skill for a task. Write it as *use when…*, not as a label.

## 3. MCP — the one mechanism that is portable and executable

| Agent | Configuration |
|---|---|
| **Claude Code** | `.mcp.json` / settings; `/mcp` command manages servers and OAuth |
| **Codex** | `config.toml` — `[mcp_servers.<name>]` with `command`, `args`, `env`, `enabled_tools`. Project `.codex/config.toml` or user `~/.codex/config.toml` |
| **Antigravity** | `.agents/mcp_config.json` workspace; `~/.gemini/config/mcp_config.json` global; `/mcp` manager in CLI. Supports `stdio` `command` or remote `serverUrl`, plus auth and tool-disable fields. **`documented`**, [official MCP docs](https://antigravity.google/docs/mcp), retrieved 2026-09-04 |
| **Goose** | extensions; documented as connecting to 3,000+ tools via MCP |
| **Devin** | `.devin/mcp_config.local.json` project config, documented as gitignored because it carries tokens; plugins may also declare servers through a root `.mcp.json` or an inline manifest. `devin mcp list` includes plugin-contributed servers. A server's published **prompts** surface as `/mcp__<server>__<prompt>` slash commands. **`documented`**, [MCP overview](https://docs.devin.ai/cli/extensibility/mcp/overview), retrieved 2026-09-14 |

> MCP is the **only** extension mechanism that is both cross-vendor and carries executable
> capability. `AGENTS.md` is cross-vendor but is only text; skills carry capability but are
> path-bound; hooks are neither.

## 4. Subagents

| Agent | Format and path |
|---|---|
| **Claude Code** | `.claude/agents/` |
| **Codex** | `.codex/agents/*.toml` — `name`, `description`, `developer_instructions`, `model`, `sandbox_mode` (`read-only`, `workspace-write`, `danger-full-access`). Built-in types: `default`, `worker`, `explorer`. Concurrency cap in `config.toml`: `agents.max_concurrent_threads_per_session`, legacy alias `agents.max_threads`. Retrieved 2026-09-01 |
| **Antigravity** | `.agents/agents/<name>.md` or `<name>/agent.md`; global `~/.gemini/config/agents/`; plugin `agents/`. YAML frontmatter scopes tools, primary/subagent role, model, shell policy, MCP, skills and plugins. Built-ins: `research`, `browser`, `self`. **`documented`**, [Subagents](https://antigravity.google/docs/subagents), retrieved 2026-09-04 |
| **Goose** | subrecipes |
| **Devin** | `agents/<name>/AGENT.md` **inside a plugin**, surfaced as `<plugin>:<agent>` profiles; a skill may also set `subagent: true` in its frontmatter. No project-scoped subagent directory outside a plugin was documented in this pass. **`documented`**, [CLI changelog](https://docs.devin.ai/cli/changelog/stable), retrieved 2026-09-14 |

Not portable. Every vendor has its own format.

## 5. Hooks and lifecycle

| Agent | Mechanism |
|---|---|
| **Claude Code** | `.claude/settings.json`. Supports `command`, `http`, `mcp_tool`, `prompt` and `agent` handlers. The event list, decision contracts, blocking mechanisms and fail-open behavior are owned by the [Claude Code inventory](../docs/agents/claude-code.md#7-hooks), rechecked 2026-09-03. |
| **Codex** | **`<repo>/.codex/hooks.json` and `~/.codex/hooks.json`**, inline `[hooks]` in either `config.toml`, and plugin-bundled hooks. All layers load cumulatively; none replaces another. `/hooks` manages them. `command` and `mcp_tool` handlers run; `prompt` and `agent` are parsed but skipped. The event list, decision contracts, blocking mechanisms and trust behavior are owned by the [Codex inventory](../docs/agents/codex.md#8-hooks), rechecked 2026-09-03. |
| **Antigravity** | **`.agents/hooks.json` and `~/.gemini/config/hooks.json`**, plus plugin-bundled hooks; command handlers on `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, and `Stop`. JSON stdin/stdout contracts include pre-tool allow/deny/modify decisions. **`documented`**, [official Hooks docs](https://antigravity.google/docs/hooks), retrieved 2026-09-04; not exercised locally. |
| **Goose** | **(unverified)** |
| **Devin** | **`.devin/hooks.v1.json`** plus a user-level config, discovered from the working directory up to the repository root — **and hooks already present in `.claude/` directories are picked up automatically.** Events: `PreToolUse`, `PostToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `PostCompaction`, `SessionStart`, `SessionEnd`. Handlers read event data on stdin and block by non-zero exit or by returning `{"decision": "block", "reason": …}`. Plugin-bundled `hooks.json` loads alongside project hooks. **`documented`**, [Hooks overview](https://docs.devin.ai/cli/extensibility/hooks/overview), retrieved 2026-09-14; not exercised. |

> **The one row that partially answers this section's own complaint.** Every revision of this
> section has concluded that the inner schema is shared but *the file location is not*. Devin is
> the first surveyed agent documented to read **another vendor's** hook directory — `.claude/` —
> rather than only its own. If that holds when run, a `.claude/` hook is portable across at least
> two agents without an adapter, which no other pair here manages.
>
> It does not change the verdict, for the reason the verdict has always rested on: a hook still
> **binds only the agent that reads it**, and a Devin-shaped `PermissionRequest` or
> `PostCompaction` event has no equivalent elsewhere. It is also `documented` and unexercised, and
> the claim is sourced from the CLI's pages only — Desktop, Cloud and the JetBrains product are
> not established to do the same. Verify it before relying on it; the procedure is step 5 of the
> [Devin inventory's enumeration section](../docs/agents/devin.md#6-how-to-enumerate-this-yourself).

**No hook system is a hard guarantee.** Use hooks as vendor-local guardrails and fast feedback;
put the binding, agent-independent gate in CI. Exact failure contracts stay in the canonical
inventories so this comparison does not drift from them.

**Codex has hooks, and the schema shape is close to Claude Code's.** *(Revised — see the revision
log.)* Read from `figma/hooks.json` in the `openai-curated` marketplace, 2026-08-31:

```json
{ "hooks": { "PostToolUse": [ { "matcher": "Write|Edit",
    "hooks": [ { "type": "command", "command": "./scripts/post_write_parity_check.sh" } ] } ] } }
```

`replayio/hooks.json` adds a `Stop` event of the same shape, matching on `Bash`.

**The event names, the `matcher` key, the nested `hooks` array and `type: "command"` all match
Claude Code.** The samples establish that the schema shape matches; they do not establish the
breadth of either event or handler set. The canonical inventories own that comparison. Matcher
values can also transfer where two agents use the same tool name. Antigravity now documents the
same event/matcher/nested-command core, with an additional named-hook wrapper. What differs immediately is
*where the file lives* — `<repo>/.codex/hooks.json` for Codex versus `.claude/settings.json` for
Claude Code versus `.agents/hooks.json` for Antigravity — while the inventories document the
current event and decision differences.

The two files above were read from plugins because that is where this survey first looked. **Codex
also supports repository- and user-level hooks**, which is the layer that actually matters for a
portable gate: `<repo>/.codex/hooks.json` is committed to the repository the same way
`.claude/settings.json` is.

**Revised verdict: more portable than this document previously claimed, and still not portable
enough to depend on.** A common inner shape exists across three vendors; the wrapper, location,
tool names and decision contracts do not. Antigravity is documentation-only, Goose is untested,
and nothing guarantees the event sets stay aligned across releases. The rule in
`PORTABILITY.md` is unchanged and is what matters: **write the gate as a CI check, mirror it as a
hook for fast local feedback, and let the check win when they disagree.** What changes is only the
cost of the mirror — it is closer to adapting one schema than inventing three implementations.

## 6. Bundles

| Agent | Unit |
|---|---|
| **Claude Code** | plugins — package skills, agents, commands, hooks, MCP |
| **Codex** | plugins — required `.codex-plugin/plugin.json`, plus optional `skills/`, `commands/`, `agents/`, `hooks.json`, `.mcp.json`, `.app.json`, `assets/`. `codex plugin add\|list\|remove`, `codex plugin marketplace …`. **Measured 2026-08-31** — full list in `docs/agents/codex.md` |
| **Antigravity** | plugins — `plugin.json` plus optional `skills/`, `rules/`, `mcp_config.json`, `hooks.json`; CLI plugins may also package `agents/`. CLI stages them under `~/.gemini/antigravity-cli/plugins/<name>/`. **`documented`**, [Plugins](https://antigravity.google/docs/plugins) and [CLI Plugins](https://antigravity.google/docs/cli/plugins/), retrieved 2026-09-04 |
| **Goose** | recipes — YAML packaging a goal, required extensions, structured inputs, execution steps. Plus subrecipes |
| **Devin** | plugins — installed from a GitHub `owner/repo`, a git URL or a local path with `devin plugins install`, behind an interactive trust prompt (`-y` skips it). One bundle can contribute **skills, rules, hooks, MCP servers and subagents**: its `AGENTS.md`/`AGENT.md`/`.windsurfrules` load as always-on rules, `hooks.json` loads alongside project hooks, `.mcp.json` or an inline manifest runs servers for the session, and `agents/<name>/AGENT.md` becomes a `<plugin>:<agent>` profile. `devin plugins list\|info\|update\|remove\|prune`; team marketplaces and governance configs are organization features. **`documented`**, [CLI changelog](https://docs.devin.ai/cli/changelog/stable) and [plugin ecosystem](https://docs.devin.ai/product-guides/plugin-ecosystem), retrieved 2026-09-14 |

Not portable. **Devin's bundle is the widest single confirmation in this table** — one trust
prompt can admit always-on instructions, a blocking hook, an external tool server and a subagent
together. That is a larger grant than the repository-committed `SKILL.md` this file already warns
about under Managed Agents, and it is worth stating plainly wherever plugin installation is
suggested.

## 7. Configuration precedence — Codex documents it, others less so

Codex, highest to lowest: CLI flags and `--config` → profile (`--profile`) → project
`.codex/config.toml` root-to-cwd → user `~/.codex/config.toml` → system `/etc/codex/config.toml` →
built-in defaults. `AGENTS.md` is the exception: concatenated, not overridden.

**Security boundary worth copying:** untrusted projects skip *all* project-scoped `.codex/` layers
and fall back to user, system and built-in settings only.

Antigravity documents global versus project settings in 2.0 and a separate CLI profile at
`~/.gemini/antigravity-cli/settings.json`; permission conflicts resolve `Deny > Ask > Allow`.
The complete precedence across `AGENTS.md`, `GEMINI.md`, Rules, Plugins, project settings and CLI
flags is not documented and remains `(unverified)`. See the canonical
[Antigravity inventory](../docs/agents/antigravity.md), retrieved 2026-09-04.

Devin documents precedence for **rules only**: `.devin/rules/` takes precedence over
`.windsurf/rules/`, with legacy `.windsurfrules` and imported `.cursor/rules` also read, and
discovery walking up to the git root. What is *not* documented is the corresponding rule for
**skills**, where three project roots (`.agents/`, `.devin/`, `.windsurf/`) can hold the same
name — that is `(unverified)` and is exactly the case `devin skills show <name>` would settle.
Devin also shares Codex's trust boundary in shape: a workspace must be trusted before local agents
activate. Retrieved 2026-09-14; see the [Devin inventory](../docs/agents/devin.md#5-extension-points).

## 8. Capability inventories — moved

Per-agent inventories now live in **`docs/agents/`**, one file each:

- [`docs/agents/claude-code.md`](../docs/agents/claude-code.md)
- [`docs/agents/codex.md`](../docs/agents/codex.md)
- [`docs/agents/antigravity.md`](../docs/agents/antigravity.md) — official-documentation inventory;
  no local installation test

**Why they left this file.** They are reference data about *one* agent, and this file is a
*comparison across* agents. Mixing them pushed it past 400 lines and made both jobs harder. The
directory also fixes the scaling problem: **adding an agent adds a file, and never widens a table.**

All inventories are lower bounds. The two locally tested files were each caught missing an entire tier —
Codex's `.system/` built-ins, and Claude Code's `anthropic-skills:` plugin namespace. That is the
standing argument for the prefix rule in section 9 over any maintained blocklist: **`check.py`
cannot be complete, and a prefix does not need it to be.**

Three results from those files that this comparison depends on:

- **The two tested vendors ship the same two tiers**, under different names. Codex labels skills `System` or
  `Personal`; Claude Code distinguishes bare-named bundled skills from `plugin:skill` ones. Only
  five skills genuinely ship with Codex.
- **Surfaces differ within a vendor.** A CLI check does not describe the desktop app. `codex debug
  prompt-input` is authoritative for a Codex CLI session and nothing else.
- **Antigravity is four independently versioned core products.** The IDE family separately ships
  a standalone IDE and editor extensions; Remote Control is a host control channel, the Gemini API
  agent is a managed runtime, and Enterprise is a deployment mode. The project/workspace
  `.agents/skills` directory name is shared by 2.0/IDE and CLI, but the documented file layouts,
  global paths, settings, artifacts and plugin management differ by surface.

---

## Open items

| | |
|---|---|
| ~~Goose and `AGENTS.md`~~ | **resolved 2026-08-31** — Goose defaults to `["AGENTS.md", ".goosehints"]`. Section 1 |
| ~~Codex hook schema~~ | **resolved 2026-09-01** — `<repo>/.codex/hooks.json`, `~/.codex/hooks.json` and plugin-bundled files, all loading cumulatively. Section 5 |
| Goose hook schema | still **(unverified)** |
| ~~Codex hook event set~~ | **resolved 2026-09-01** — the documented event set includes a blocking `PreToolUse`, which is the one that matters for a gate. See the canonical [Codex inventory](../docs/agents/codex.md#8-hooks). Not yet exercised locally |
| Codex skill precedence | when a plugin skill, a vendored catalogue skill and a project `.agents/skills/` skill share a name, which wins is untested. Section 9 assumes "both appear"; that is documented for duplicates but the three-way case is **(unverified)** |
| **install.py writes 5 nested-Skill directories; 3 cover the documented nested surfaces** | `.cursor/skills/` and `.opencode/skills/` are redundant as of 2026-09-01. Reducing them changes what lands in adopters' repositories and leaves orphans in existing installs, so it is a decision, not a cleanup. Section 2 |
| Antigravity CLI Skill installation | CLI docs describe flat `.agents/skills/*.md`; this installer writes `.agents/skills/<name>/SKILL.md` for 2.0/IDE, Codex and Goose. Do not synthesize a flat duplicate until an installed `agy` test settles loading and duplicate-name behaviour |
| Antigravity Rule limit | Website docs state 12,000 characters per Rule, but do not establish that the bound applies to directory-based `AGENTS.md`/`GEMINI.md`. `check.py` records the distinction and does not change its Codex instruction-chain threshold pending a named-surface test |
| Antigravity `GEMINI.md` check coverage | `check.py` intentionally measures the Codex `AGENTS.override.md`/`AGENTS.md` chain and does not count `GEMINI.md`. Test Antigravity precedence and size behavior when both context files exist, then decide whether a separate informational divergence/budget check is justified; do not add `GEMINI.md` to the Codex chain |
| Antigravity IDE global Skill root | Official IDE docs say `~/.gemini/antigravity/skills`; installed IDE 2.5.5 state uses `~/.gemini/antigravity-ide`. This is a test prompt, not a contradiction, until Skill loading is exercised |
| Claim-level sourcing | This file carries a document-level "checked" date. Volatile rows should each carry their own official link and retrieval date; several now do, most do not |
| Antigravity local verification | Windows presence audit found 2.0 v2.11.0 and IDE v2.5.5 installed; neither was run or capability-enumerated. CLI/SDK were not locally enumerated and `agy` was absent from `PATH`. Test the exact checklist in `docs/agents/antigravity.md` section 15 before calling any capability `tested`; treat Remote Control and the managed API separately |
| Tier 2/3 | Cursor/Kiro native invocation remains pending after launcher/installer checks; Copilot, Goose and OpenCode still need canonical inventories |
| Zed | Skill paths documented in section 2, 2026-09-05; other mechanisms and runtime loading remain backlog |
| **Devin retrieval channel** | Every Devin row was retrieved through a documentation index because `docs.devin.ai` and `docs.windsurf.com` were unreachable from the authoring session's network egress policy. An index can lag the live page. **Re-read the cited paths directly on the next pass**, starting from the vendor's own machine-readable index at `https://docs.devin.ai/llms.txt`, and upgrade or correct the rows rather than carrying them forward on this channel |
| **Devin surface split** | Nearly every Devin extension row is sourced from `/cli/...` pages. Whether Devin Desktop, Devin Cloud and Windsurf JetBrains honour the same discovery order, precedence and frontmatter is **unknown**. This is the same generalisation that produced the superseded Windsurf row; do not repeat it |
| **Devin `.claude/` hook pickup** | Documented: Devin CLI automatically picks up hooks already present in `.claude/` directories — the first surveyed case of an agent reading another vendor's hook location. If true when run, it is the only hook portability in this file that needs no adapter. Unexercised, and CLI-sourced only |
| **Devin skill precedence and built-ins** | Three project skill roots (`.agents/`, `.devin/`, `.windsurf/`) can hold the same name and no page states which wins; `devin skills show <name>` would settle it. The shipped-skill set is also unenumerated, so built-in skills are **unknown, not absent**. Duplicate-name failure mode — silent replacement, both listed, or neither — is `(unverified)`, which is why no `RESERVED_DEVIN` set was added |


---

## 9. Naming — skill names collide with built-ins, and the failure is silent

**Claude Code:** a project skill whose directory name matches a bundled skill **replaces it**. From
the documentation: a `code-review` skill in `.claude/skills/` replaces the bundled `/code-review`,
and typing the bundled alias `/review` never reaches your skill. **No warning is raised.** You lose
the vendor's implementation — usually the better one — and may not notice.

**Codex:** different semantics. Duplicate names produce **both** entries in the selector, unmerged.

Two vendors, two behaviours, neither of them an error. Checked 2026-08-31.

### Rule: namespace every skill this project ships

Prefix project skills so they can never shadow a built-in and are visible as local in any selector.
The prefix is the project's own short name; the point is that it exists, not which one it is.

```
✗  review/          shadows Claude Code's bundled /code-review, silently
✗  verify/          shadows /verify
✓  hr-review/       cannot collide; reads as local in every selector
```

### Reserved — do not use as a skill directory name

Measured from a Claude Code v2.1.251 session plus the published commands reference, 2026-08-31.
Treat as a **lower bound**: it grows with each release, which is another reason for the prefix rule
rather than a maintained blocklist.

**Bundled skills:** `code-review` (alias `review`), `security-review`, `simplify`, `init`, `run`,
`verify`, `run-skill-generator`, `doctor` (alias `checkup`), `debug`, `batch`, `loop`
(alias `proactive`), `schedule`, `deep-research`, `claude-api`, `update-config`,
`keybindings-help`, `fewer-permission-prompts`, `workflow-authoring`, `design`, `dataviz`,
`artifact-design`, `artifact-diagramming`, `artifact-capabilities`

**Built-in commands:** `plan`, `memory`, `clear` (`reset`, `new`), `resume`, `branch`, `fork`,
`context`, `compact`, `model`, `effort`, `advisor`, `tasks`, `background` (`bg`), `subtask`,
`permissions` (`allowed-tools`), `mcp`, `config` (`settings`), `usage`, `cost`, `status`, `copy`,
`export`, `rewind`, `diff`, `feedback`, `bug`, `help`

### Codex reserved names — measured 2026-08-31

Same rule, different failure. Codex does not replace a bundled skill: a duplicate name puts **both**
entries in the selector, unmerged. Nothing is lost, so it is a warning rather than a failure — but
`$pdf` matching two different skills is a coin flip over which one runs, and `.agents/skills/` is
read by Codex, Goose and Antigravity, so a name chosen for one lands in all three.

Enumerated from `docs/agents/codex.md` — built-in, plugin and curated skills, the vendored
`openai/skills` catalogue, and the documented slash commands. `check.py` carries this as
`RESERVED_CODEX`, separate from `RESERVED_CLAUDE` because the two failures differ.

**Plugin skills:** `documents`, `pdf`, `presentations`, `spreadsheets`, `excel-live-control`,
`template-creator`, `visualize`, `control-chrome`, `control-in-app-browser`, `plugin-management`,
`computer-use`, `latex`, `browser`, `chrome`

**codex-security:** `security-scan`, `deep-security-scan`, `security-diff-scan`, `threat-model`,
`finding-discovery`, `attack-path-analysis`, `validation`, `triage-finding`, `fix-finding`,
`track-findings`

**Vendored catalogue:** `define-goal`, `migrate-to-codex`, `hatch-pet`, `yeet`, `screenshot`,
`speech`, `transcribe`, `playwright`, `playwright-interactive`, `cli-creator`, `openai-docs`,
`jupyter-notebook`, `figma`, `figma-use`, `linear`, `sentry`, `aspnet-core`, `chatgpt-apps`,
`winui-app`, `gh-fix-ci`, `gh-address-comments`, `skill-installer`, `security-best-practices`,
`security-ownership-map`, `security-threat-model`, `vercel-deploy`, `netlify-deploy`,
`render-deploy`, `cloudflare-deploy`

**Slash commands:** `ide`, `keymap`, `vim`, `agent`, `subagents`, `apps`, `plugins`, `hooks`,
`rename`, `archive`, `delete`, `title`, `stop`, `approvals`, `undo`

**The overlap is the point.** `review`, `doctor`, `pdf`, `plan`, `resume`, `fork`, `clear`, `copy`,
`help`, `permissions`, `mcp` and `status` collide in *both* agents, with different consequences in
each. One prefix prevents both, which is why the rule is "prefix", not "consult two blocklists".

### Antigravity reserved names — documented 2026-09-04

Antigravity CLI turns registered skills into slash commands, while the product also owns public
slash commands. The official docs do not state how a same-named skill and built-in command resolve;
the consequence is therefore `(unverified)`, not assumed to match Claude Code or Codex.

`check.py` keeps two official lower-bound sets. Public commands and aliases include `add-dir`,
`agents`, `artifact`, `boost`, `browser`,
`btw`, `clear`, `codesearch`, `config`, `context`, `copy`, `credits`, `diff`, `exit`, `fast`,
`feedback`, `fork`, `goal`, `grill-me`, `help`, `hooks`, `keybindings`, `learn`, `logout`, `mcp`,
`model`, `open`, `permissions`, `planning`, `rename`, `resume`, `rewind`, `schedule`, `skills`,
`statusline`, `tasks`, `teamwork-preview`, `title`, `usage`, `voice`, and their documented aliases.
Confirmed built-in Skill names are tracked separately: `antigravity_guide` and
`migrate-workflows`.
Source: [official shared commands](https://antigravity.google/docs/slash-commands) and
[CLI reference](https://antigravity.google/docs/cli/reference), and
[Changelog](https://antigravity.google/changelog), retrieved 2026-09-04.

### Devin reserved names — documented 2026-09-14

Same mechanism again, and the same unanswered question. A Devin skill whose frontmatter declares
`triggers: [user]` becomes a slash command, sharing one namespace with the built-ins
`/help`, `/shortcuts`, `/config`, `/context`, `/compact`, `/usage`, `/session-stats` (alias
`/stats`), `/copy`, `/feedback`, `/bug`, `/update`, `/upgrade`, `/login`, `/logout`,
`/login-status` (advertised to ACP hosts as `/status`), `/org`, `/mouse` and `/handoff`, plus MCP
prompts under `/mcp__<server>__<prompt>`. Source:
[commands reference](https://docs.devin.ai/cli/reference/commands), retrieved 2026-09-14.

**No reserved set was added to `check.py` for Devin**, matching how Cursor and Kiro were admitted.
Two reasons, and the second is the load-bearing one. The offline sets exist to catch *this
repository's own inventories* drifting out of sync, and the drift check reads only the Claude Code
and Antigravity files. More importantly, **Devin's collision behaviour is `(unverified)`**: no
retrieved page says whether a same-named skill replaces the built-in silently as Claude Code does,
lists both as Codex does, or something else. A blocklist enforcing an unknown failure mode would
assert more than the evidence supports.

**The overlap is now four-way, and only one of the four has a known failure mode.** A prefix avoids
Claude replacement, Codex ambiguity, and Antigravity's and Devin's untested resolution behaviour
without depending on any blocklist being complete — which remains the whole argument for the
prefix rule over a maintained list.

---

## Revision log

Kept out of the sections above so a reader wanting the current fact does not have to parse
revision history. Each entry is a claim this file once made and no longer does.

| Date | Was | Now |
|---|---|---|
| 2026-08-31 | "`.agents/skills/` is converging as the neutral standard" | No majority exists — 3 agents vs 4. Tier 2/3 evidence did not support the original claim |
| 2026-08-31 | "Codex has no hook mechanism; not portable at all, different schemas and event names" | Codex has `hooks.json` inside plugins, and the schema shape matches Claude Code's. **Both original statements were wrong** — the mechanism was one directory below where the survey looked |
| 2026-08-31 | "Codex ships roughly 70 commands" | Withdrawn as uncited; the circulating figure conflates CLI flags with slash commands |
| 2026-08-31 | "`/goal` is not in the official reference — (unverified)" | `/goal` and `/init` are real. The fetched reference names them without descriptions, and treating that as absence was an error in the opposite direction |
| 2026-08-31 | Capability inventories lived in sections 8 and 8b | Moved to `docs/agents/`, one file per agent. Each had been caught missing an entire tier — Codex's `.system/` built-ins, Claude Code's `anthropic-skills:` namespace |
| 2026-08-31 | "Codex `codex-security` skills are available as `$security-scan`" | A gated add-on requiring Codex Security access. **The files were read from the plugin cache and assumed loaded — cache is not load** |
| 2026-08-31 | "Goose: no documented `AGENTS.md` read (unverified)" | Goose defaults to `["AGENTS.md", ".goosehints"]`, overridable via `CONTEXT_FILE_NAMES` |
| 2026-08-31 | "Amazon Q Developer was retired" | Being wound down, not retired: signups blocked 2026-05-15, end of support 2027-04-30, users directed to Kiro |
| 2026-08-31 | Claude Code hooks described as ~5 events, one of which can block | **33** documented events, ~10 can block, 5 handler types |
| 2026-09-01 | "Codex hooks live inside plugins; 2 events observed" | Codex documents **repository- and user-level** hooks at `<repo>/.codex/hooks.json` and `~/.codex/hooks.json`, with **11 events including a blocking `PreToolUse`**. The mechanism is far closer to Claude Code's than section 5 claimed — **third revision of this row, each time in the same direction** |
| 2026-09-01 | "`.agents/skills/` is not converging; 3 agents use it, 4 use vendor paths" | **Reversed by the vendors.** Cursor, Copilot and OpenCode now all read `.agents/skills/`, making it 6 of 8. The minimal covering set is 3 directories, not 5 |
| 2026-09-01 | "`codex mcp-server` runs Codex as an MCP server — the most portability-relevant thing either vendor ships" | **Deprecated**: "Use the Codex app server instead." The claim is withdrawn |
| 2026-09-01 | "`codex apply` applies the agent's latest diff" | Applies the latest diff from a Codex **cloud** task, by task ID — not a local-session diff |
| 2026-09-01 | Subagent caps given as `max_threads`; sandbox values as read-only/suggest/auto-edit/full-access | `agents.max_concurrent_threads_per_session` (legacy alias `agents.max_threads`); documented sandbox values are `read-only`, `workspace-write` and `danger-full-access`; `max_depth` and `job_max_runtime_seconds` are not in the configuration reference and are now marked `(unverified)` |
| 2026-09-01 | `check.py` summed **every** `AGENTS.md` in the repo | A chain is one file per directory along a single root-to-cwd path. 18 sibling packages were failing a budget no session ever sees. **Introduced while fixing the opposite bug** |
| 2026-09-01 | `check.py` counted HTML-comment bodies as section content | The shipped scaffold, every section empty, passed as "none empty" |
| 2026-09-01 | `check.py` scanned only `AGENTS.md` | Codex checks **`AGENTS.override.md` then `AGENTS.md` in each directory along the path**. A chain of four overrides totalling 35 KB was reported as "7 B, ok" |
| 2026-09-01 | `install.py --check` exited 0 unless there was a CONFLICT | Any pending change now exits non-zero. A repository missing a whole skill directory printed "would create" and passed both gates, contradicting the README |
| 2026-09-01 | Antigravity skills row had no project path and was `(unverified)` | Google's Antigravity Skills codelab documents `<project-root>/.agents/skills/`, which is what the 6-of-8 aggregate rested on |
| 2026-09-01 | Hooks corrected in `docs/agents/codex.md` only | Section 5, the open items and `PORTABILITY.md` still carried the plugin-only, two-event model for a full round. **A correction applied to one file is not applied** |
| 2026-09-01 | "6 of 8 verified" | **`documented`, not `tested`.** Six of the eight rows have never been run here. Evidence grades are now defined at the top of this file |
| 2026-09-01 | 32 KiB called a "hard limit" in three files after being corrected in one | Configurable default. What it bounds is disputed between two official pages; this project enforces the stricter combined-chain reading **as a deliberate choice**, and now says so |
| 2026-09-01 | "Tier 2/3 — treat as `(unverified)` until tested" survived alongside the new grades | Contradicted the grade definitions in the same file. Those agents are `documented`: sourced and dated, never run |
| 2026-09-01 | "Hard limit: 32 KiB. Codex truncates beyond it" in `templates/AGENTS.md` | Corrected everywhere else first. **The sweep searched `research/`, `docs/` and `check.py` and never included `templates/`** — the one directory whose contents ship into adopters' repositories |
| 2026-09-01 | "all 16 rows carry a grade and a date" | **False, and produced by a bad measurement.** The count matched `| **` and swept up the evidence-grade legend's own rows. The two agent tables held 15 rows, six carried no grade, and OpenCode was missing from the instruction table entirely |
| 2026-08-31 | "no ablation isolated the overview result; the paper's one ablation (Figure 5) strips documentation files" | **Wrong, and more specifically wrong than the vaguer claim it replaced.** Table 7 (Appendix B) ablates the overview category directly: p = 0.15 / p = 0.73, null either way. Figure 5 is a tool-use chart, not an ablation. The overview paragraph is §4.3, not §4.2. Corrected in `PORTABILITY.md`, `AGENTS.md`, `templates/AGENTS.md` and the six `SKILL.md` copies |
| 2026-09-02 | Section 5: Claude Code hooks "**around 10** can block" | **11**, now named. The hedge survived from the 2026-08-31 correction because nobody counted the list |
| 2026-09-02 | `check.py`'s `RESERVED_CLAUDE` was assembled from a **session enumeration** | Rebuilt from the published commands reference. **A session cannot tell a bundled skill from one the user installed**, so it was the wrong evidence for a reserved-name set — the same class of error as reading the Codex plugin cache and calling it loaded. `/sandbox`, `/design`, `/security-review`, `/simplify`, `/workflows`, `/worktree` and ~40 built-in command names were missing, every one of them a plausible project skill name |
| 2026-09-02 | `docs/agents/claude-code.md` described `/verify` and `/run` as settled | **Two official pages disagree** about both, including where `/verify` writes its recorded recipe. Recorded as ⚠️ `disputed` in three files rather than resolved by picking one. This is the second such case in this project, after `project_doc_max_bytes` in section 2 |
| 2026-09-02 | Section 2 listed **eight** consumers of a checked-in `SKILL.md`, all of them coding agents | **Nine.** Anthropic **Managed Agents** scans a mounted repository's root `.claude/skills/` at session start — no installer, no configuration, no `skills`-array entry. The survey's frame was "coding agents" when the actual boundary is "anything that mounts the repo", and the miss came from never looking outside `code.claude.com` |
| 2026-09-02 | The `ide` MCP server was attributed to VS Code alone | **JetBrains runs the same server**, with a smaller model-visible tool surface. Both are hidden from `/mcp`, which matters for anyone allowlisting MCP tools with a `PreToolUse` hook. **Claims about a vendor were sourced to that vendor's general pages rather than its own** — the JetBrains page had never been cited |
| 2026-09-02 | Section 5: Codex hooks — only `PreToolUse` marked **can block** | **7 of the 11 can halt a turn.** `PermissionRequest` approves or denies outright; `UserPromptSubmit`, `PreCompact`, `PostCompact`, `SubagentStop` and `Stop` can return `continue: false`. **This is the fourth revision of the Codex hooks row and the fourth in the same direction** — every one has found the mechanism more capable than the previous draft assumed. The correction came from checking a research file *against* this one, not from re-reading the vendor page |
| 2026-09-02 | Section 1 treated the `AGENTS.md` chain as fully visible in the repository | **A gitignored `AGENTS.override.md` is loaded, overrides the committed file at its level, and is auto-copied into every Codex-managed worktree** — instruction content that never reaches code review. "Read the repo to see what the agent was told" is not a sound check on Codex; `codex debug prompt-input` is |
| 2026-09-02 | `docs/agents/codex.md` filed `hatch-pet` under curated skills | **Bundled.** The Pets page: creating a custom pet *"installs the bundled `hatch-pet` skill"*. A minor row, but it came from the same error as the big ones — **a name seen in the curated catalogue was assumed to be only there** |
| 2026-09-03 | Section 5 repeated Claude Code's blocking set as **11**, one day after the canonical inventory changed | The duplicated event lists and counts were removed. Section 5 now links to the two canonical hook inventories; the Claude inventory records 15 exit-status-blocking events plus `PermissionRequest`'s structured decision and the fail-open contracts. |
| 2026-09-04 | `tested` meant only "run on this machine, with the version recorded"; the file-level status stopped at the 2026-09-02 documentation-only pass | `tested` now requires the **surface and version**, every local Claude Code/Codex row carries that stamp or an explicit historical gap, and the status separates the 2026-08-31 baseline, 2026-09-02 documentation pass, and evidence changes verified through 2026-09-04 |
| 2026-09-04 | The Codex instruction and skills rows carried a flat `tested` stamp from CLI 0.151.0-alpha.7.2, with no process-environment qualifier; the skills stamp read as covering every location | The baseline process environment is explicitly **not recorded**. Reading `AGENTS.md` and the repository `.agents/skills/` path were reconfirmed in the Desktop Codex-mode task and its sandbox-launched CLI 0.153.0 child; non-project skill locations are separately `documented` rather than inheriting the project path's `tested` grade |
| 2026-09-04 | Antigravity was one thin matrix row: `AGENTS.md` had no path, `GEMINI.md` was unverified, global skills were incorrectly flattened to `~/.agents/skills`, and MCP/subagents/hooks/plugins/configuration were absent | Added the official-documentation inventory for 2.0 v2.12.2, CLI v1.1.25, SDK v0.1.16 and IDE v2.5.5; sourced `AGENTS.md`/`GEMINI.md`, split global paths by surface, and added MCP, agents, hooks, plugins, permissions and documented conflicts. Evidence remains `documented`, not `tested` |
| 2026-09-04 | The first Antigravity inventory treated the IDE family as extensions only, omitted Remote Control, the Gemini API managed agent and Enterprise, and resolved Windows sandbox documentation by choosing the dedicated page | Split standalone IDE from extensions, classified Remote Control/API/Enterprise as adjacent delivery or deployment modes, added their boundaries, and recorded the Windows sandbox and third-party-model plan tables as official disputes instead of selecting one page |
| 2026-09-04 | Antigravity 2.0 and IDE were flattened to one global Skill path; CLI's `.agents/skills/` directory was treated as proof of the nested `SKILL.md` layout; SDK tools and managed-API limits were only summarized | Split all three Skill path/layout contracts, added confirmed built-in Skills and exact SDK `BuiltinTools`, and recorded the managed API's explicit unsupported tools and structured-output limitation |
| 2026-09-04 | The Antigravity inventory said no application was installed; instruction discovery was flattened to workspace root; installer output implied nested `SKILL.md` covered CLI; commands and built-in Skills shared one drift set | Recorded installed-but-unrun 2.0/IDE presence, marked root-versus-walk-up discovery disputed, exposed the CLI installer gap, split command/Skill drift checks, and moved unresolved Rule/path questions into named test items |
| 2026-09-05 | The portable-layer rule excluded skills whenever any agent had a similar built-in | Narrowed the exclusion to unevaluated replicas; optional fallbacks may address a demonstrated gap on a particular surface. This is a user-authorized scope decision, not a vendor evidence-grade change. Prior rule and rationale are preserved in [PORTABILITY.md section 3](PORTABILITY.md#3-the-rule). |

| 2026-09-14 | Windsurf was one supplemental skill-path row: two project paths, `~/.codeium/windsurf/skills/` as a literal directory, sourced from a Cascade page the redirected Windsurf URL happened to land on | **Promoted to a full inventory as [Devin](../docs/agents/devin.md), and corrected in three places.** The vendor renamed the product (Windsurf → Devin Desktop, with Cloud/CLI/Review under one brand), the authoritative extensibility documentation sits under the **CLI** section rather than Desktop/Cascade, `.devin/skills/` and `~/.config/devin/skills/` were missing entirely, and `<channel>` is a variable, not the literal `windsurf`. Added instruction-file, skills, MCP, subagent, hook, bundle, precedence and reserved-name rows. Evidence is `documented`, not `tested`, and **weaker than every other file here**: the vendor's documentation host was unreachable from the authoring session, so all of it came through a documentation index rather than the pages themselves |
| 2026-09-14 | "Six of the eight rows have never been run"; `.agents/skills/` read by 6 of 8 | Nine agents, seven of them never run here; `.agents/skills/` is read by 7 of 9. **The minimal covering set stayed three directories** — Devin reads `.agents/skills/` alongside its own `.devin/skills/`, so no installer target was added for it, on the same redundancy argument already standing against `.cursor/` and `.opencode/` |

**The pattern worth noticing:** most of these were an enumeration mistaken for an inventory, or a
local artefact mistaken for a loaded capability. The overview-ablation entry is a third kind, and
the worst: **a summarised fetch was treated as a full read, and a specific citation was invented on
top of it.** Two separate summaries of that paper reported "no Table 7" and "no p-values"; the PDF
has both. Where a claim rests on a document's fine detail, extract the document. Both are why section 9's rule is a **prefix**
rather than a blocklist, and why `docs/agents/` states its measurement surface on every claim.
