# houserules

**Give your coding agent project rules, optional skills and a repeatable way to verify work.**
Keep the same task evidence when switching agents. Everything runs locally with Python 3.9+
and the standard library.

## Install

From this repository, preview the files for your project:

```bash
python install.py --repo /path/to/your-project --agents cursor --work handoff,verification --activate-workflow --check
```

Replace `cursor` with `claude`, `codex`, `antigravity`, `kiro`, a comma-separated selection,
or `all`. Preview writes nothing: exit 1 means changes are needed; exit 0 means no drift.
Apply the same selection by removing `--check`:

```bash
python install.py --repo /path/to/your-project --agents cursor --work handoff,verification --activate-workflow
python check.py --repo /path/to/your-project
```

Open **HOUSERULES.md in your project**. It links your installed skills, templates and workflow
instructions. You do not need to return here for everyday work.

`--activate-workflow` appends a short routing rule to AGENTS.md while preserving its existing bytes.
Omit it to leave existing instructions untouched and explicitly point your agent to
`.houserules/START.md` when needed. Activation is an instruction, not a background hook.

If `python` is unavailable, use `py` on Windows, `python3` where available, or your interpreter's full path.
Omitting `--repo` targets the current directory.

## Use it on a task

Give your agent a concrete request, for example:

> Fix the failing parser test. Follow .houserules/START.md, use the installed hr-diagnosing-bugs
> skill if selected, and leave a verified result or a clear handoff.

For repeated checks, the installed workflow tool records command attempts, logs and file hashes.
It limits run count and elapsed command time, refuses an unchanged repeated passing command,
and detects stale evidence before reuse. [Run a bounded check](docs/USAGE.md#run-a-bounded-check)
shows the commands and their limits. The agent still chooses relevant tests and judges the outcome.

For choosing native tools or integrations, use the [stage guide](docs/GUIDE.md).
It maps **five agents across 12 stages and three cross-cutting concerns**, with surface limits.

## Choose what to add

```bash
python install.py --list
python install.py --repo /path/to/your-project --agents codex --skills hr-tdd,hr-diagnosing-bugs --work handoff,verification --check
```

| Choice | Purpose | Default |
|---|---|---|
| hr-onboard | Capture project rules from friction during real work | Installed |
| hr-tdd | A meaningful red-green slice | Experimental, opt-in; [provenance](templates/skills/hr-tdd/NOTICE.md) |
| hr-diagnosing-bugs | Reproduce, diagnose and verify a fix | Experimental, opt-in; [provenance](templates/skills/hr-diagnosing-bugs/NOTICE.md) |
| hr-code-review | Review a pinned change against standards and intent | Experimental, opt-in; [provenance](templates/skills/hr-code-review/NOTICE.md) |
| Work templates | Handoff, spec, plan, review, findings, verification | Select with --work; copy only useful artifacts |

The three adaptations include upstream licenses and revisions. Availability is not evidence that
these outperform a built-in; [admission criteria](research/PORTABILITY.md#fallback-admission-criteria)
govern recommendation and default promotion.

Selections are additive. `--skills all` / `--work all` select the catalog; `none` adds nothing and
does not uninstall prior selections. Omitted options retain existing choices; skills also default
to hr-onboard. Agent paths previously selected are retained.

## What arrives in your project

| Files | Used by / purpose |
|---|---|
| AGENTS.md and the CLAUDE.md import | Project instructions; existing content preserved, optional workflow rule appended |
| Selected agent skill directories | Agent-discoverable procedures; foreign skills preserved |
| HOUSERULES.md | Human entry linking the actual installation |
| .houserules/START.md | Short agent execution instructions |
| .houserules/workflow.py | Local bounded command execution and evidence freshness checks |
| .houserules/work/ | Selected template originals and their consumer protocol |
| check.py | Instruction, skill and managed-file checks |
| .houserules/skills.json and assets.json | Ownership records for drift detection; commit with the installed layer |

GUIDE and research remain distribution references. Hooks, MCP servers and plugins need separate
surface-specific installation/configuration; this installer does not enable them.
The [documentation map](docs/README.md) explains each document's reader, action and maintenance trigger.

## Update or remove

Run the same installer with `--check` before updating. Modified managed work assets stop all
writes, including with `--force`; unchanged owned assets can update. Root check.py differences
and skill conflicts require reconciliation before installation. Skill source updates must cover
all previously recorded paths. See [enforcement boundaries](docs/ENFORCEMENT.md).

Keep filled task artifacts outside the installed originals. Preview/preflight prevents known
conflicts; it does not provide rollback for filesystem errors or concurrent edits.

There is no uninstaller. Inspect the ownership records and remove only the specific installed
files you no longer need. Preserve your own instruction content and task evidence; remove only
the houserules import/routing blocks from shared instruction files.

## What has been verified

Claude Code and Codex have named local runtime observations in their [inventories](docs/agents/README.md);
those observations do not certify every feature. Antigravity is documentation-based. Cursor and
Kiro have dated capability maps and [local installer acceptance](tests/workflows/cursor-kiro/README.md),
but native skill loading remains untested. Copilot, Goose and OpenCode are matrix-only.

External claims have sources and dates, or an unverified label. Runtime evidence names its surface
and version. [MATRIX](research/MATRIX.md) tracks recheck dates; [workflow reports](tests/workflows/README.md)
preserve what actually ran. No measured model-quality or cost-saving claim is made.
