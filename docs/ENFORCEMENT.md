# Enforcement map

This maps current checks, not proposed gates. Source: local `check.py`, `install.py` and
work contracts inspected 2026-09-06. Mechanical success is limited to the predicate checked.

| Rule / contract | Current enforcement | Limit / remaining judgment |
|---|---|---|
| Claude instruction import | `check.py`: import marker present in either supported project file | Substring check only; does not parse imports or prove runtime loading |
| Instruction budget and empty sections | `check.py`: applicable instruction-chain size and empty headings | Independent nested Git repositories are excluded; inclusion value and semantic quality need review |
| Skill name coexistence | `check.py`: known reserved-name checks, with failures/warnings and generated-name exceptions | Not universal collision detection or enforcement of every `hr-` prefix |
| Skill trigger metadata | `check.py`: description-field pattern near the start of SKILL.md | Not a complete YAML/schema validator or a trigger-quality eval |
| Managed copies and ownership | `check.py`: manifest/digests; `install.py --check`: installation drift; installer preflight | Files on disk do not establish loaded capability; preflight is not transactional rollback |
| Documented command inventory | `check.py`: one-way inventory-to-reserved-name comparison | Does not establish exhaustive or current vendor coverage |
| Selected work assets and the installed checker | `check.py`: assets manifest/digests; installer preflight preserves modifications even with --force | Does not validate populated work records; untouched managed assets may update |
| Adopter CI gate | Opt-in `--ci` workflow runs the installed checker on push and pull request | Runs the checker only: `install.py --check` needs the distribution, which is never copied into an adopting project. Whether the job is a required check stays the adopter's branch-protection decision |
| Installed-script placement | Installer writes both executables to `.houserules/`; a root `check.py` is never written, moved or deleted, and an upgrade past one stops until `--migrate-checker` | Provenance of that root file was never recorded, so nothing here can distinguish an old owned copy from a user script; removal stays manual. The flag records an acknowledgement, and does not verify that CI was repointed |
| Workflow activation | Installer explicitly appends an idempotent AGENTS.md block with --activate-workflow | Routes an agent to START; does not prove it followed instructions or enable a hook |
| Command attempt/time budgets | Installed workflow.py counts attempts and bounds total direct-command elapsed time | **Bounds effort, not scope.** A run/second budget constrains how much work is attempted, not what it may reach: one in-budget command can still act outside the assigned task. Covers only commands invoked through it; not chat/token/provider spend, detached processes, or any blast-radius limit |
| Repeated passing check | workflow.py refuses the same latest argv at unchanged selected targets/log | Does not deduplicate arbitrary commands or failed attempts; budget bounds retries |
| Recorded check freshness | workflow.py status compares selected target and log hashes, including before/after command inputs | Latest command only, exact files only; no environment attestation or semantic acceptance |
| Five-agent GUIDE coverage | Documentation conformance test checks every stage/concern table against inventory files | Checks mapping presence, not vendor truth or runtime capability |
| External claims and evidence grades | Human/agent review under [evidence rules](../AGENTS.md) | No automated source/date or runtime-evidence audit |
| Work-artifact targets and finding resolution | [Consumer protocol](../templates/work/README.md#consumer-protocol) and review | No prose-artifact parser; workflow freshness covers separately selected files only |
| Review independence and authority | [Review protocol](../templates/work/README.md#review-by-artifact) and accountable owner | Identity labels do not authenticate sessions; evidence grade is separate |
| Optional fallback admission | [Admission criteria](../research/PORTABILITY.md#fallback-admission-criteria) | Explicit experimental trial is allowed; comparative fresh-session evidence required for recommendation/default promotion |
| Comparative evaluation records | `tests/eval/runner.py`: refuses a drifted frozen input by name, an unpinned model/effort, an absent reported-spend threshold, unacknowledged unmetered execution, a deadline raised above the one the case records, a manifest whose hashes do not cover exactly the declared inputs, a resume under changed settings or a changed CLI version, and grading an output whose hash changed, an input that drifted since the run, or while a run holds the attempt lock; pins isolation flags per surface and runs each cell in a fresh empty directory outside the repository; judges attempt status against the recorded full-arm plan; preserves failed/timeout observations on resume; records per-cell status, usage, partial cost and blinded scores. `tests/test_eval_runner.py` covers hashing, blinding determinism, refusals, timeout handling, resume and the working directory | Produces records usable in assessing criterion 5 on the named surface/version; a recorded execution alone does not satisfy that criterion. Effort is requested, not runtime-attested. Unknown executed-cell cost keeps total spend null; max_usd is an inter-cell threshold, not a hard billing cap. Not promotion, not semantic acceptance, not a sandbox. Isolation flags are recorded as passed, not verified per run; a canary smoke test observed user and project `CLAUDE.md` excluded on Claude Code CLI 2.1.283 in a cloud session only, not on other surfaces, builds or Codex. The candidate arm supplies skill text as a prompt, so it does not establish native discovery or loading. Grading is human judgment against a frozen rubric; structural blinding is not independence |

In this repository run `python check.py` and `python install.py --check` before completing a change. In an adopting repository the same checker is `.houserules/check.py`, run from the project root or with an explicit `--repo`.
Script/test changes additionally require `python -m unittest discover -s tests -v`.
Neither command validates work-artifact semantics, authorizes release, or proves an agent loaded a skill.

## Known platform verification limit

Recorded 2026-09-26 from the
[branch review](https://github.com/fujiakito/houserules/blob/d69a5821d168f631ec498125b46c1da5d52375ec/review.md#verification-and-limits).
The reviewer reported a Windows failure in
`test_follow_up_command_survives_paths_containing_spaces`: a string comparison differed between
the long and 8.3 forms of a temporary path. This was not reproduced on Linux and remains open.
The current hosted matrix runs on Linux, so a green run does not resolve this finding or establish
Windows compatibility. Before making that claim, reproduce the test on Windows, record the Python
and OS versions, and distinguish equivalent path spellings from an actual command-quoting failure.

## Deferred checks and their triggers

Recorded 2026-09-17. These are known gaps in the map above that are **deliberately not built yet**.
Each names the condition that would justify building it, so the decision is revisited on evidence
rather than on impulse or on a calendar. A gap with no fired trigger is not a backlog item.

| Deferred | Why not now | Trigger to revisit |
|---|---|---|
| Age reporting for dated snapshots | Every check here is structural; none is time-aware. [PORTABILITY](../research/PORTABILITY.md) revisits snapshots on demand, not on a schedule, and that remains the cheaper default while vendor churn stays slower than the revisit rate | Any retrieval date older than ~90 days, **or** one revisit finding a substantive conflict (not merely an addition) between an inventory and the live surface |
| Automated source/date audit of external claims | The evidence rule in [AGENTS.md](../AGENTS.md) is the only one with no mechanical backing. A naive linter over prose would be noisy, and the admission bar this project applies to new capability applies to its own checks | A second recorded instance of an unsourced external claim being acted on before verification |
| Scope / blast-radius budgets | The budget row above bounds effort, not scope, so nothing here limits what an in-budget command can reach — a real gap in this map. No admission criterion is satisfied by that observation alone: criterion 1 in [PORTABILITY](../research/PORTABILITY.md#fallback-admission-criteria) wants a target operation/artifact, agent surface/version and expected contract observed failing, and criterion 5 wants comparative evidence. The trigger column carries the real bar | A recorded adopter requirement, **or** an observed in-scope-budget run that acted outside its assigned task in a repository using this layer |
| An evaluation scenario with headroom | The v2 rubric is saturated: checks 1-3 scored 1.0 for both arms across all twenty gradings in both runs, the [2026-09-16 replication](../tests/workflows/prior-art/v2/attempt-20260916-replication.json) and the leak-free [2026-09-17 replication](../tests/workflows/prior-art/v2/attempt-20260917-replication.json), so it cannot resolve a small effect in either direction. No pending decision currently depends on that measurement | A handoff or artifact-consumption failure observed in real work, creating a decision that needs the instrument |
