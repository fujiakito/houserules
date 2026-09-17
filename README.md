# houserules

**Your repository owns its rules and its proof — whichever agent and model turn up.**
Project instructions every agent reads, executable checks with their limits written down, and task
evidence that survives a switch. As one agent comes to run several models, what your repository
states and can check is the part that stays constant. Optional skills are available and are not
the point. Everything runs locally with Python 3.9+ and the standard library.

## Install

Run these from this repository. Add `--check` to either one to preview without writing: exit 1
means changes are needed, exit 0 means no drift.

**Minimal** — project instructions, the `hr-onboard` skill, and the local checker and workflow
tool under `.houserules/`:

```bash
python install.py --repo /path/to/your-project --agents cursor
```

**Everything** — the same, plus the three optional skills and all six work templates; it also
appends the workflow routing rule to AGENTS.md and adds a CI workflow that runs the checker:

```bash
python install.py --repo /path/to/your-project --agents cursor --skills all --work all --activate-workflow --ci
```

The minimal command still installs `hr-onboard`, the default. What it leaves out is the three
*optional* skills — `hr-tdd`, `hr-diagnosing-bugs` and `hr-code-review`, **experimental
adaptations rather than a quality upgrade** — and the work templates, which are simply optional.
A later run without `--skills` or `--work` keeps whatever you selected before.

The other two flags are independent of those selections and of each other. `--activate-workflow`
appends a short routing rule to AGENTS.md, preserving its existing bytes; omit it and point your
agent at `.houserules/START.md` when it is needed. `--ci` adds a GitHub Actions gate. Neither
starts a hook or a background process.

Replace `cursor` with `claude`, `codex`, `antigravity`, `kiro`, a comma-separated selection,
or `all`. Repeat the same `--agents` selection on every later run — omitting it means `all`,
which installs for every agent.

Then verify the result:

```bash
python check.py --repo /path/to/your-project
```

Open **HOUSERULES.md in your project**. It states the first action for the state that project is
actually in, what was *not* installed and the command that adds it, which route fits which
situation, and what the workflow tool does. You do not need to return here for everyday work.

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
| CI workflow | A GitHub Actions gate that runs the installed checker | Select with --ci; it cannot gate template drift, because the installer is never copied into your project |

The three adaptations include upstream licenses and revisions. Availability is not evidence that
these outperform a built-in; [admission criteria](research/PORTABILITY.md#fallback-admission-criteria)
govern recommendation and default promotion.

Selections are additive. `--skills all` / `--work all` select the catalog; `none` adds nothing and
does not uninstall prior selections. Omitted `--skills` and `--work` retain existing choices;
skills also default to hr-onboard. Omitted `--agents` means `all`, including on updates.
Repeat your original agent selection to avoid adding paths. Previously recorded paths are retained.

## What arrives in your project

| Files | Used by / purpose |
|---|---|
| AGENTS.md and the CLAUDE.md import | Project instructions; existing content preserved, optional workflow rule appended |
| Selected agent skill directories | Agent-discoverable procedures; foreign skills preserved |
| HOUSERULES.md | Human entry linking the actual installation |
| .houserules/LICENSE | The MIT notice for the first-party files installed above; your own root LICENSE is untouched |
| .houserules/START.md | Short agent execution instructions |
| .houserules/workflow.py | Local bounded command execution and evidence freshness checks |
| .houserules/work/ | Selected template originals and their consumer protocol |
| .houserules/check.py | Instruction, skill and managed-file checks; run it from the project root, or pass `--repo` |
| .github/workflows/houserules.yml | Only with `--ci`: GitHub Actions gate running the installed checker; your other workflows are untouched |
| .houserules/skills.json and assets.json | Ownership records for drift detection; commit with the installed layer |

GUIDE and research remain distribution references. Hooks, MCP servers and plugins need separate
surface-specific installation/configuration; this installer does not enable them.
The [documentation map](docs/README.md) explains each document's reader, action and maintenance trigger.

## Update or remove

Run the same installer with `--check` before updating. Modified managed assets — the installed
checker included — stop all writes, including with `--force`; unchanged owned assets can update.
Skill conflicts require reconciliation before installation, and skill source updates must cover
all previously recorded paths. See [enforcement boundaries](docs/ENFORCEMENT.md).

Installations made before the checker moved left a `check.py` at the project root, and **upgrading
breaks it**. Its asset allowlist predates `.houserules/check.py`, so it rejects the new manifest
with `invalid managed asset: .houserules/check.py` and exits 1 — a CI job still running it fails on
its next build. Preserving the file's bytes does not preserve its behaviour.

So an upgrade stops before writing until you confirm you have dealt with it:

```bash
python install.py --repo /path/to/your-project --agents cursor --migrate-checker
```

Before passing that flag, repoint any job at `.houserules/check.py` (run from the project root, or
pass `--repo`), or delete the root file. The installer never deletes it for you — nothing recorded
who wrote it, so an old copy of ours and a script of yours are indistinguishable. A *first* install
into a project that already has its own root `check.py` is unaffected: that file is yours, nothing
of yours changes, and the run proceeds.

For example, if you originally selected `claude,codex`, preview with
`python install.py --repo /path/to/your-project --agents claude,codex --check`.
Compare conflicting copies with the current source and preserve any local changes. Once reviewed,
use the same command without `--check`, adding `--force` only if replacement is needed.
`--force` can overwrite a selected conflicting skill directory; it does not merge changes,
and it does not override a modified managed asset.

Keep filled task artifacts outside the installed originals. Preview/preflight prevents known
conflicts; it does not provide rollback for filesystem errors or concurrent edits.

There is no uninstaller. Inspect the ownership records and remove only the specific installed
files you no longer need. Preserve your own instruction content and task evidence; remove only
the houserules import/routing blocks from shared instruction files.

## License and attribution

houserules is MIT licensed — see [LICENSE](LICENSE).

`hr-tdd`, `hr-diagnosing-bugs` and `hr-code-review` are adaptations of Matt Pocock's MIT-licensed
skills. Each ships the upstream LICENSE and a NOTICE.md recording source, pinned revision,
retrieval date and the changes made, and the installer copies both into your project alongside
SKILL.md. Keep them together. [THIRD-PARTY.md](THIRD-PARTY.md) summarises every upstream source.

The first-party files the installer writes — check.py, workflow.py, START.md, the work templates
and hr-onboard — arrive with this project's MIT notice at `.houserules/LICENSE`. Your own root
LICENSE is never read or written.

Changes go through [CONTRIBUTING](CONTRIBUTING.md); the three gates and the evidence conventions
are in [AGENTS.md](AGENTS.md). Suspected vulnerabilities go through [SECURITY](SECURITY.md), which
also lists the designed behaviors that are not vulnerabilities — the installer writes where you
point it, and an installed skill is model-directed text from whatever source you took it from.

## What has been verified

Claude Code and Codex have named local runtime observations in their [inventories](docs/agents/README.md);
those observations do not certify every feature. Antigravity is documentation-based. Cursor and
Kiro have dated capability maps and [local installer acceptance](tests/workflows/cursor-kiro/README.md),
but native skill loading remains untested. Copilot, Goose and OpenCode are matrix-only.

External claims have sources and dates, or an unverified label. Runtime evidence names its surface
and version. [MATRIX](research/MATRIX.md) tracks recheck dates; [workflow reports](tests/workflows/README.md)
preserve what actually ran. No measured model-quality or cost-saving claim is made.
