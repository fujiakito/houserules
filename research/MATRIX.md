# Extension mechanism matrix

What each agent lets you extend, in what format, at what path. This is the raw material; the
portability verdict derived from it lives in `PORTABILITY.md`.

**Evidence rule for this file:** every row carries a source and a retrieval date, or is tagged
`(unverified)`. Anything testable locally is **tested, not cited** — sources in this field contradict
each other often enough that a citation is not evidence.

**Checked: 2026-08-31. `recheck_by: 2026-11-30.`** Platform surfaces in this field change monthly —
Amazon Q Developer was retired, Gemini CLI is being replaced by Antigravity CLI, Cursor was acquired
and shipped a git forge, all within twelve months. **Every row below is a claim about a date, not a
permanent fact.** Re-run the local tests on each recheck; they take minutes and settle what
documentation disputes.

Status: **Tier 1** (Claude Code, Codex) and the open-source floor (Goose) established by
documentation plus local tests. **Tier 2/3** (Cursor, Antigravity, Copilot, Kiro) surveyed from
documentation only — treat as `(unverified)` until tested. Windsurf is backlog.

---

## 1. Instruction file — what each agent reads

| Agent | Reads | Path / discovery | Notes |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md` only | project root and up the tree; `~/.claude/CLAUDE.md` personal | **Does not read `AGENTS.md` natively** — tested 2026-08-29, v2.1.251. `@AGENTS.md` import from `CLAUDE.md` works. With both files present and no import, `AGENTS.md` is ignored **and nothing says so** |
| **Codex** | `AGENTS.md` | every directory level from repo root to cwd; `~/.codex/AGENTS.md` global | Files **concatenate**, they do not override — a subdirectory adds to the root. `AGENTS.override.md` replaces its `AGENTS.md` at that level. Hard limit `project_doc_max_bytes` = **32 KiB** |
| **Goose** | `.goosehints`, plus skills | project directories | No documented `AGENTS.md` read in the skills docs, despite Goose being an AAIF founding project alongside `AGENTS.md` — **(unverified, needs a local test)** |
| **Cursor** | **`AGENTS.md`** | project root **and any subdirectory, no configuration** | Also `.cursor/rules/*.mdc`. **No global `~/.cursor/AGENTS.md`** — cross-project instructions go to User Rules or Team Rules instead `(unverified)` |
| **Copilot** | **`AGENTS.md`** | repo root, plus nested per-subtree | Also reads `.github/copilot-instructions.md`, `.github/instructions/**`, **and `CLAUDE.md` and `GEMINI.md`** — the most permissive reader found `(unverified)` |
| **Kiro** | **`AGENTS.md`** | loads as steering context from anywhere in the workspace tree | Plus `.kiro/steering/` `(unverified)` |
| **Antigravity** | **`AGENTS.md`** | — | Plus `GEMINI.md` `(unverified)` |

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
| **Claude Code** | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/` | `.claude/commands/*.md` still works (merged into skills) |
| **Codex** | **`.agents/skills/`** — searched from cwd up to repo root | **`~/.agents/skills/`** | `/etc/codex/skills` admin, plus bundled |
| **Goose** | **`.agents/skills/`** | **`~/.agents/skills/`** | `~/.agents/plugins/<name>/`; legacy `.goose/skills/` still read but **deprecated in favour of `.agents/skills/`** |
| **Antigravity** | — | **`~/.agents/skills`** (2.0 global default) | `(unverified)` |
| **Cursor** | `.cursor/skills/` (committed) | `~/.cursor/skills/` | `(unverified)` |
| **Kiro** | `.kiro/skills/` | project or global | `(unverified)` |
| **OpenCode** | `.opencode/skills/` | `~/.config/opencode/skills/` | `(unverified)`; noted because it is another `AGENTS.md` reader |

> **Correction to an earlier draft of this file.** It claimed `.agents/skills/` was converging as
> the neutral standard. Tier 2/3 does not support that. **Three** agents use it (Codex, Goose,
> Antigravity); **four** use a vendor path (Claude Code, Cursor, Kiro, OpenCode). It is the largest
> single group, not a standard.
>
> **The accurate statement: there is no portable skills location.** The `SKILL.md` *format* is
> universal; the *path* is not, and no majority exists.
>
> **Tested 2026-08-31:** a skill in `.agents/skills/` was invisible to Claude Code v2.1.251 while a
> skill in `.claude/skills/` in the same directory was found. Both had valid frontmatter.
>
> The ecosystem's own answer to this is **installers** — third-party skill collections ship a CLI
> that copies the same `SKILL.md` into each vendor's path. That is the working pattern, and it
> confirms the fragmentation rather than solving it.

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
| **Codex** | `.codex/agents/*.toml` — `name`, `description`, `developer_instructions`, `model`, `sandbox_mode` (`read-only` / `suggest` / `auto-edit` / `full-access`). Built-in types: `default`, `worker`, `explorer`. Global caps in `config.toml`: `max_threads`, `max_depth`, `job_max_runtime_seconds` |
| **Goose** | subrecipes |

Not portable. Every vendor has its own format.

## 5. Hooks and lifecycle

| Agent | Mechanism |
|---|---|
| **Claude Code** | `.claude/settings.json`. Events include `UserPromptSubmit`, `PreToolUse` (can block), `PostToolUse`, `SessionEnd`, `Setup` (fires on `--init-only` / `--init` / `--maintenance`, intended for CI or scripts). Also **prompt-based hooks** (`type: "prompt"` — decision made by a model, Haiku by default) and agent-based hooks |
| **Codex** | plugins "sometimes" bundle hooks — **(unverified)**, no documented standalone hook schema found |
| **Goose** | **(unverified)** |

**Not portable at all.** Different schemas, different event names, different files. Anything that must
survive an agent switch cannot be a hook.

## 6. Bundles

| Agent | Unit |
|---|---|
| **Claude Code** | plugins — package skills, agents, commands, hooks, MCP |
| **Codex** | plugins — `plugin.json` with `components` (skills, mcp_servers, agents) and `install_policy` (`INSTALLED_BY_DEFAULT` / `AVAILABLE` / `NOT_AVAILABLE`). `codex marketplace add <repo>` from v0.120.0 |
| **Goose** | recipes — YAML packaging a goal, required extensions, structured inputs, execution steps. Plus subrecipes |

Not portable.

## 7. Configuration precedence — Codex documents it, others less so

Codex, highest to lowest: CLI flags and `--config` → profile (`--profile`) → project
`.codex/config.toml` root-to-cwd → user `~/.codex/config.toml` → system `/etc/codex/config.toml` →
built-in defaults. `AGENTS.md` is the exception: concatenated, not overridden.

**Security boundary worth copying:** untrusted projects skip *all* project-scoped `.codex/` layers
and fall back to user, system and built-in settings only.

## 8. Claude Code bundled skills — measured, not cited

Obtained 2026-08-31 by asking a Claude Code v2.1.251 session to enumerate its own skills:

```
code-review  security-review  simplify  init  run  verify(*)  loop  schedule
claude-api   update-config    keybindings-help  fewer-permission-prompts
design  dataviz  artifact-design  artifact-diagramming  artifact-capabilities
workflow-authoring
```

(*) `/verify`, `/doctor`, `/debug`, `/batch`, `/deep-research`, `/run-skill-generator` appear in the
published commands reference but did not all appear in this session's enumeration — availability
varies by feature flags and settings. Treat the published reference as the superset.

---

## Open items

| | |
|---|---|
| Goose and `AGENTS.md` | docs do not mention it; needs a local test |
| Codex and Goose hook schemas | no standalone hook mechanism found; may not exist |
| Tier 2/3 | Cursor, Antigravity, Copilot, Kiro |
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

**Codex** ships roughly 70 commands including `goal`, `review`, `doctor` and `exec` — the same rule
applies, and the overlap with Claude Code's names (`review`, `doctor`) is itself a reason to prefix.
