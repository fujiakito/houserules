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
| **tested** | run on a real installation on this machine, with the version recorded |
| **documented** | official vendor documentation, with a retrieval date. Not run |
| `(unverified)` | neither — a claim carried forward without a source |

**Only Claude Code and Codex are `tested`.** Every other agent in this file is `documented` at
best. That distinction is load-bearing: this project has twice been wrong about a vendor whose
documentation it had read correctly, because reading is not running.

**Checked: 2026-08-31. `recheck_by: 2026-11-30.`** Platform surfaces in this field change monthly —
Amazon Q Developer is being wound down — new signups blocked 2026-05-15, full end of support
2027-04-30, with AWS directing users to **Kiro**, which is in this table — Gemini CLI is being
replaced by Antigravity CLI, Cursor was acquired
and shipped a git forge, all within twelve months. **Every row below is a claim about a date, not a
permanent fact.** Re-run the local tests on each recheck; they take minutes and settle what
documentation disputes.

Status: **Claude Code and Codex are `tested`** — real installations, versions recorded, and the
only two this project should be described as supporting. **Goose, Cursor, Copilot, OpenCode,
Antigravity and Kiro are `documented`**: their rows cite official pages with retrieval dates, and
none has been run. Windsurf is backlog.

---

## 1. Instruction file — what each agent reads

| Agent | Reads | Path / discovery | Notes |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md` only | `./CLAUDE.md` **or `./.claude/CLAUDE.md`**; up the tree; `~/.claude/CLAUDE.md` personal; managed-policy path or the `claudeMd` settings key | **`tested`** — v2.1.251, 2026-08-29. **Does not read `AGENTS.md` natively.** `@AGENTS.md` import from `CLAUDE.md` works. With both files present and no import, `AGENTS.md` is ignored **and nothing says so** |
| **Codex** | `AGENTS.md` | every directory level from repo root to cwd; `~/.codex/AGENTS.md` global | Files **concatenate**, they do not override — a subdirectory adds to the root. `AGENTS.override.md` replaces its `AGENTS.md` at that level. `project_doc_max_bytes` = **32 KiB by default — configurable, not a hard ceiling**. What it bounds is disputed between two official pages; see section 2. **Mixed grade:** that Codex reads `AGENTS.md` is **`tested`** (0.151.0-alpha.7.2, 2026-08-31); the precedence and byte-budget rules are `documented`, retrieved 2026-09-01 |
| **Goose** | **`AGENTS.md`**, then `.goosehints` | project directories; `~/.config/goose/` global | Default is `["AGENTS.md", ".goosehints"]`, overridable with the `CONTEXT_FILE_NAMES` env var. All found files are combined. `documented`, retrieved 2026-08-31 |
| **Cursor** | **`AGENTS.md`** | project root **and any subdirectory, no configuration** | Also `.cursor/rules/*.mdc`, and the Cursor CLI reads `CLAUDE.md` too. **No global `~/.cursor/AGENTS.md`** — cross-project instructions go to User Rules or Team Rules. `documented`, retrieved 2026-09-01 |
| **Copilot** | **`AGENTS.md`** | repo root, plus nested per-subtree | Also reads `.github/copilot-instructions.md`, `.github/instructions/**`, **and `CLAUDE.md` and `GEMINI.md`**. Note the precedence: `.github/copilot-instructions.md` **outranks** `AGENTS.md`. `documented`, retrieved 2026-09-01 |
| **Kiro** | **`AGENTS.md`** | loads as steering context from anywhere in the workspace tree | Plus `.kiro/steering/`. `documented`, retrieved 2026-08-31 — **not re-checked on 2026-09-01** |
| **Antigravity** | **`AGENTS.md`** | — | Plus `GEMINI.md`. `documented`, retrieved 2026-08-31; the `GEMINI.md` half is **`(unverified)`** — carried forward without a source |
| **OpenCode** | **`AGENTS.md`** | project | Listed in section 2 as an `AGENTS.md` reader but omitted from this table until 2026-09-01. `documented`, retrieved 2026-09-01 |

> **Finding — the cleanest result in this survey.** Every agent surveyed reads `AGENTS.md`
> **except Claude Code.** Codex authored it; Cursor, Copilot, Kiro and Antigravity all read it;
> Copilot goes further and reads `CLAUDE.md` and `GEMINI.md` as well.
>
> The `@AGENTS.md` import line in `CLAUDE.md` is therefore not an optional adapter but a
> **correctness requirement** — and it is the only one-line change that makes a repository legible
> to every agent in this table.

## 2. Skills — the same standard, three different paths

All three implement the [Agent Skills](https://agentskills.io) open standard: a directory containing
`SKILL.md` with YAML frontmatter (`name`, `description`) and markdown body. **The format is portable.
The location is not.**

| Agent | Project path | User path | Other |
|---|---|---|---|
| **Claude Code** | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/` | `.claude/commands/*.md` still works (merged into skills). **`tested`** — v2.1.251, 2026-08-31 |
| **Copilot** | **`.agents/skills`**, `.claude/skills`, `.github/skills` | `~/.copilot/skills`, **`~/.agents/skills`** | `documented`, retrieved 2026-09-01 |
| **Codex** | **`.agents/skills/`** — searched from cwd up to repo root | **`~/.agents/skills/`** | `/etc/codex/skills` admin, plus plugin `skills/` and the vendored catalogue. **Invoked with `$<name>`, not `/`**. **`tested`** — 0.151.0-alpha.7.2, 2026-08-31 |
| **Goose** | **`.agents/skills/`** | **`~/.agents/skills/`** | `~/.agents/plugins/<name>/`; legacy `.goose/skills/` still read but **deprecated in favour of `.agents/skills/`**. `documented`, retrieved 2026-09-01 |
| **Antigravity** | **`<project-root>/.agents/skills/`** | **`~/.agents/skills`** (2.0 global default) | Google's Antigravity Skills codelab documents the project path. `documented`, retrieved 2026-09-01 |
| **Cursor** | **`.agents/skills/`** and `.cursor/skills/` | **`~/.agents/skills/`**, `~/.cursor/skills/` | Also loads `.claude/skills/` and `.codex/skills/` for compatibility. Not copied to Cloud Agents — use project skills there. `documented`, retrieved 2026-09-01 |
| **Kiro** | `.kiro/skills/` | project or global | Default agent loads `.kiro/skills/` and `~/.kiro/skills/`; a custom agent needs a `skill://` resource entry. `documented`, retrieved 2026-09-01 |
| **OpenCode** | `.opencode/skills/`, `.claude/skills/`, **`.agents/skills/`** | `~/.config/opencode/skills/`, `~/.claude/skills/`, **`~/.agents/skills/`** | Walks up to the git worktree, loading each match along the way. `documented`, retrieved 2026-09-01 |

> **`.agents/skills/` has become the majority path — reversing what this section said before.**
> Per official documentation retrieved 2026-09-01, it is read by **Codex, Goose, Antigravity,
> Cursor, Copilot and OpenCode**; only **Claude Code** and **Kiro** do not.
>
> **That aggregate is `documented`, not `tested`.** Six of the eight rows behind it have never been
> run here — only Codex and Claude Code have. Read it as "six of eight vendors document support",
> which is a weaker and more accurate claim than "six of eight verified".
>
> **The minimal covering set is three directories, not five:**
>
> | Directory | Covers |
> |---|---|
> | `.agents/skills/` | Codex, Goose, Antigravity, Cursor, Copilot, OpenCode |
> | `.claude/skills/` | Claude Code (also read by Cursor, Copilot, OpenCode) |
> | `.kiro/skills/` | Kiro |
>
> `.cursor/skills/` and `.opencode/skills/` are **redundant** — both agents read `.agents/skills/`.
> `install.py` still writes all five; see the open item below.
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

**The `description` field is a trigger, not a title.** Codex's documentation is explicit: it
determines whether the model selects the skill for a task. Write it as *use when…*, not as a label.

## 3. MCP — the one mechanism that is portable and executable

| Agent | Configuration |
|---|---|
| **Claude Code** | `.mcp.json` / settings; `/mcp` command manages servers and OAuth |
| **Codex** | `config.toml` — `[mcp_servers.<name>]` with `command`, `args`, `env`, `enabled_tools`. Project `.codex/config.toml` or user `~/.codex/config.toml` |
| **Goose** | extensions; documented as connecting to 3,000+ tools via MCP |

> MCP is the **only** extension mechanism that is both cross-vendor and carries executable
> capability. `AGENTS.md` is cross-vendor but is only text; skills carry capability but are
> path-bound; hooks are neither.

## 4. Subagents

| Agent | Format and path |
|---|---|
| **Claude Code** | `.claude/agents/` |
| **Codex** | `.codex/agents/*.toml` — `name`, `description`, `developer_instructions`, `model`, `sandbox_mode` (`read-only`, `workspace-write`, `danger-full-access`). Built-in types: `default`, `worker`, `explorer`. Concurrency cap in `config.toml`: `agents.max_concurrent_threads_per_session`, legacy alias `agents.max_threads`. Retrieved 2026-09-01 |
| **Goose** | subrecipes |

Not portable. Every vendor has its own format.

## 5. Hooks and lifecycle

| Agent | Mechanism |
|---|---|
| **Claude Code** | `.claude/settings.json`. **33 documented events**, including `SessionStart`/`SessionEnd`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`/`StopFailure`, `SubagentStart`/`Stop`, `PreCompact`/`PostCompact`, `FileChanged`, `InstructionsLoaded`, `Setup`. **Around 10 can block**, not just `PreToolUse`. **5 handler types**: `command`, `http`, `mcp_tool`, `prompt` (decided by a model), `agent` |
| **Codex** | **`<repo>/.codex/hooks.json` and `~/.codex/hooks.json`**, plus plugin-bundled `hooks.json`. All layers load cumulatively; none replaces another. `/hooks` manages them. **11 events**: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreToolUse` (**can block**), `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `Stop`. Handlers `command` and `mcp_tool`; `prompt` and `agent` are parsed but skipped. Official docs retrieved 2026-09-01 |
| **Goose** | **(unverified)** |

**Codex has hooks, and the schema shape is close to Claude Code's.** *(Revised — see the revision
log.)* Read from `figma/hooks.json` in the `openai-curated` marketplace, 2026-08-31:

```json
{ "hooks": { "PostToolUse": [ { "matcher": "Write|Edit",
    "hooks": [ { "type": "command", "command": "./scripts/post_write_parity_check.sh" } ] } ] } }
```

`replayio/hooks.json` adds a `Stop` event of the same shape, matching on `Bash`.

**The event names, the `matcher` key, the nested `hooks` array and `type: "command"` all match
Claude Code.** Note what these two samples do and do not show: between them they exercise **2 of
Codex's 11 documented events** and **1 of its 2 supported handler types**. They were enough to
establish that the schema shape matches; they say nothing about the breadth of either set. The
documented comparison — 11 events against 33, roughly ten names shared — is below. So do the matcher values, because they are tool names and the two agents name their
tools alike. What differs is *where the file lives* — `<repo>/.codex/hooks.json` for Codex versus
`.claude/settings.json` for Claude Code — and the size of the event set: **11 for Codex against 33
for Claude Code**, with roughly ten names shared, including a blocking `PreToolUse` on both.

The two files above were read from plugins because that is where this survey first looked. **Codex
also supports repository- and user-level hooks**, which is the layer that actually matters for a
portable gate: `<repo>/.codex/hooks.json` is committed to the repository the same way
`.claude/settings.json` is.

**Revised verdict: more portable than this document previously claimed, and still not portable
enough to depend on.** The shape survives a copy between these two vendors; the location does not,
Goose is untested, and nothing guarantees the event sets stay aligned across releases. The rule in
`PORTABILITY.md` is unchanged and is what matters: **write the gate as a CI check, mirror it as a
hook for fast local feedback, and let the check win when they disagree.** What changes is only the
cost of the mirror — between these two agents it is closer to one file than to two implementations.

## 6. Bundles

| Agent | Unit |
|---|---|
| **Claude Code** | plugins — package skills, agents, commands, hooks, MCP |
| **Codex** | plugins — required `.codex-plugin/plugin.json`, plus optional `skills/`, `commands/`, `agents/`, `hooks.json`, `.mcp.json`, `.app.json`, `assets/`. `codex plugin add\|list\|remove`, `codex plugin marketplace …`. **Measured 2026-08-31** — full list in `docs/agents/codex.md` |
| **Goose** | recipes — YAML packaging a goal, required extensions, structured inputs, execution steps. Plus subrecipes |

Not portable.

## 7. Configuration precedence — Codex documents it, others less so

Codex, highest to lowest: CLI flags and `--config` → profile (`--profile`) → project
`.codex/config.toml` root-to-cwd → user `~/.codex/config.toml` → system `/etc/codex/config.toml` →
built-in defaults. `AGENTS.md` is the exception: concatenated, not overridden.

**Security boundary worth copying:** untrusted projects skip *all* project-scoped `.codex/` layers
and fall back to user, system and built-in settings only.

## 8. Capability inventories — moved

Per-agent inventories now live in **`docs/agents/`**, one file each:

- [`docs/agents/claude-code.md`](../docs/agents/claude-code.md)
- [`docs/agents/codex.md`](../docs/agents/codex.md)

**Why they left this file.** They are reference data about *one* agent, and this file is a
*comparison across* agents. Mixing them pushed it past 400 lines and made both jobs harder. The
directory also fixes the scaling problem: **adding an agent adds a file, and never widens a table.**

Both inventories are lower bounds, and each was caught missing an entire tier before being moved —
Codex's `.system/` built-ins, and Claude Code's `anthropic-skills:` plugin namespace. That is the
standing argument for the prefix rule in section 9 over any maintained blocklist: **`check.py`
cannot be complete, and a prefix does not need it to be.**

Two results from those files that this comparison depends on:

- **Both vendors ship the same two tiers**, under different names. Codex labels skills `System` or
  `Personal`; Claude Code distinguishes bare-named bundled skills from `plugin:skill` ones. Only
  five skills genuinely ship with Codex.
- **Surfaces differ within a vendor.** A CLI check does not describe the desktop app. `codex debug
  prompt-input` is authoritative for a Codex CLI session and nothing else.

---

## Open items

| | |
|---|---|
| ~~Goose and `AGENTS.md`~~ | **resolved 2026-08-31** — Goose defaults to `["AGENTS.md", ".goosehints"]`. Section 1 |
| ~~Codex hook schema~~ | **resolved 2026-09-01** — `<repo>/.codex/hooks.json`, `~/.codex/hooks.json` and plugin-bundled files, all loading cumulatively. Section 5 |
| Goose hook schema | still **(unverified)** |
| ~~Codex hook event set~~ | **resolved 2026-09-01** — 11 documented events **including a blocking `PreToolUse`**, which is the one that matters for a gate. Not yet exercised locally |
| Codex skill precedence | when a plugin skill, a vendored catalogue skill and a project `.agents/skills/` skill share a name, which wins is untested. Section 9 assumes "both appear"; that is documented for duplicates but the three-way case is **(unverified)** |
| **install.py writes 5 skill directories; 3 would cover every surveyed agent** | `.cursor/skills/` and `.opencode/skills/` are redundant as of 2026-09-01. Reducing them changes what lands in adopters' repositories and leaves orphans in existing installs, so it is a decision, not a cleanup. Section 2 |
| Claim-level sourcing | This file carries a document-level "checked" date. Volatile rows should each carry their own official link and retrieval date; several now do, most do not |
| Tier 2/3 | Antigravity, Kiro — Cursor and Copilot now have sourced skill-path rows |
| Windsurf | backlog |


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

**The pattern worth noticing:** most of these were an enumeration mistaken for an inventory, or a
local artefact mistaken for a loaded capability. The overview-ablation entry is a third kind, and
the worst: **a summarised fetch was treated as a full read, and a specific citation was invented on
top of it.** Two separate summaries of that paper reported "no Table 7" and "no p-values"; the PDF
has both. Where a claim rests on a document's fine detail, extract the document. Both are why section 9's rule is a **prefix**
rather than a blocklist, and why `docs/agents/` states its measurement surface on every claim.
