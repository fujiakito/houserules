# Security

## What this project is

Local Python scripts and text files. No service, no telemetry, no background updates, no
dependencies beyond the standard library. Nothing here runs unless you invoke it. Report
vulnerabilities against that scope.

**Nothing that installs into your project makes a network call.** The one exception is not
installed: `tests/eval/runner.py`, the distribution-only evaluation harness, spawns a provider
CLI which does reach the network. It is never copied into an adopting repository and runs only
when you invoke it; its `verify` and `plan` subcommands spawn nothing.

## Reporting

Open a private security advisory on this repository (Security → Advisories → Report a
vulnerability). Do not open a public issue for an unreported vulnerability.

This is a small project with no staffed rotation and no response-time commitment. Expect
acknowledgement to be best-effort. If a report needs a fix, the fix and its disclosure land
in the same commit; there is no embargo process to coordinate with.

## In scope

| Surface | Concern |
|---|---|
| `install.py` | Writing outside the target repository; following a symlink out of it; overwriting a file it does not own or has not recorded; preflight passing where a write then damages user content |
| `check.py` (installed as `.houserules/check.py`) | Reading outside the target repository; `--fix` repairing something it does not own |
| `.houserules/workflow.py` | Shell injection through recorded argv; escaping the `cwd`; writing state or logs outside `work/`; a stale-evidence check reporting `verified` for evidence that has changed |
| Ownership manifests | `skills.json` / `assets.json` content causing a write to an arbitrary path |
| `tests/eval/runner.py` (distribution-only) | Escaping the case directory; writing outside the attempt directory; recording credentials or environment into an attempt record; an isolation profile or a frozen-input check failing open, so an operator's own configuration reaches the baseline arm |

Path containment is guarded in `install.py` (`workflow_activation`, and `plan_assets` via
`asset_path`), `check.py` (`asset_path`), `workflow.py` (`safe_path`) and
`tests/eval/runner.py` (`safe_path`). Named rather than
numbered, because line numbers go stale silently. Commands run through `subprocess.run(argv, shell=False, cwd=repo,
timeout=...)`. A way around any of those is a bug — report it.

## Out of scope: designed behavior, not vulnerabilities

**The installer writes into a repository you name.** `--repo` is your instruction. `--force`
overwrites an existing same-named skill, and `--link` creates symlinks into this
distribution, so the target then tracks your working copy. Preview with `--check` first.

**`workflow.py run` executes the command you give it.** Bounding attempts and elapsed time
is a usage control, not a sandbox. It does not restrict what the command may do.

**`tests/eval/runner.py run` spawns the provider CLI you name.** Bounding cells, deadlines and
spend is the same usage control, not a sandbox. It passes isolation flags and records them, but
it cannot prove the CLI honoured them; treat a recorded profile as a declaration, not a guarantee.
A spend ceiling is required because an unreportable cost is unknown, and unknown is not free.

**Skills and instruction files are model-directed text.** `AGENTS.md`, `SKILL.md` and work
artifacts are read by an agent as instructions. Installing a skill from a source you do not
trust is closer to running its code than to reading its documentation, and a work artifact
written by one agent is untrusted input to the next. `check.py` checks structure, name
collisions and file digests — it does not read for intent and cannot detect a hostile
instruction. Review skill content before installing it, and read `docs/ENFORCEMENT.md` for
what a passing check does and does not establish.

**Agent behavior is not enforced.** Nothing here constrains what a model does with an
instruction. See the limits column in `docs/ENFORCEMENT.md`.
