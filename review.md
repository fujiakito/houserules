# Review of the evaluation branch and model changes

Reviewed: 2026-09-25. Reader: branch maintainer. Action: resolve the findings before using the evaluation harness to recommend a skill. Revisit this review after runner fixes, the first recorded evaluation attempt, or a change to the target model or agent surface.

Scope: fujiakito/houserules, branch claude/clever-clarke-dnni5u at 731fc7d. At the time of review, the branch was three commits ahead of and one commit behind main (1e9ee8a). This review did not run a provider-backed evaluation.

## What the branch is trying to achieve

The three commits document prior art for evaluation harnesses, add an [offline runner](tests/eval/README.md) and regression tests, and freeze the first [hr-tdd-01 case](tests/workflows/skill-eval/hr-tdd-01/README.md). Their purpose is to address [fallback admission criterion 5](research/PORTABILITY.md#fallback-admission-criteria): compare an optional skill with a baseline on representative tasks, record outcomes, cost, and failures, and only then decide whether the skill merits a recommendation.

hr-tdd-01 gives the same task to four arms: a baseline without a procedure, a candidate containing the full hr-tdd procedure, a length-matched generic procedure (control-length), and a one-line test-first instruction. The rubric emphasizes the correct failure explanation, public-interface behavior, and a minimal fix. This is a prompt-only case: it measures the effect of instruction text on a written answer. It does not test native skill discovery, iteration with tools, or actual test execution. The case was prepared and frozen on 2026-09-15 but had **not been run** at review time, so it provides no result showing that hr-tdd outperforms the other arms.

## Code review findings

### [P1] Resume can combine cells run with different settings

`cmd_run` in [runner.py](tests/eval/runner.py) checks only schema_version and input hashes when it opens an existing attempt.json. It does not compare the new model, runner, argv, timeout_seconds, budget, or intended cell plan with the recorded attempt. I reproduced this with a mocked provider: run baseline with model-A, then run candidate with model-B and --resume. The result is marked completed while the record still identifies model-A. That record cannot support an arm comparison under one fixed configuration. Resume should reject incompatible settings.

### [P1] A partial set of arms can be marked completed

`cmd_run` in [runner.py](tests/eval/runner.py) rebuilds cells from the current --arm and --trials options and uses that set to determine the status of the whole attempt. Running only baseline returned completed in a reproduction, although the case has three other arms. This conflicts with [release gate G1](tests/workflows/skill-eval/hr-tdd-01/rubric.md#release-gate--maintainer-only-not-for-the-grader). Persist the full campaign plan in the attempt record and calculate status against it.

### [P2] Grading does not verify response hashes

`run_cell` in [runner.py](tests/eval/runner.py) records output_sha256, but `cmd_grade` in [runner.py](tests/eval/runner.py) does not recheck that hash before reading an output for the blind packet or accepting scores. If a response changes after execution, the grader scores the changed text while the record retains the original hash. Grading should verify every recorded output hash.

### [P2] The Codex JSONL path does not extract the agent response

The runner invokes codex exec --json, but `parse_payload` in [runner.py](tests/eval/runner.py) extracts only usage and cost from JSONL events, leaving response unset. `cmd_grade` in [runner.py](tests/eval/runner.py) consequently writes raw JSONL to the blind packet instead of the answer alone. On 2026-09-25, codex exec --help on the local Codex CLI surface, version 0.155.0-alpha.16.4, confirmed that --json emits JSONL. This observation does not establish Desktop app or IDE behavior. Add response extraction and a Codex-specific regression test.

## Verification and limits

At the reviewed branch HEAD on Windows with Python, python check.py, python install.py --check, runner.py verify --case tests/workflows/skill-eval/hr-tdd-01, and git diff --check origin/main...HEAD passed. All 25 runner regression tests passed. The full python -m unittest discover -s tests -v run executed 101 tests with one failure and five skips. The failed test, test_follow_up_command_survives_paths_containing_spaces, was unchanged by this branch; its observed failure was a mismatch between the long and 8.3 forms of a Windows temporary path. The full suite therefore cannot be reported as passing. These findings review runner logic; no paid provider cells were executed.

## Effect of newly released models

As of 2026-09-25, the [official OpenAI GPT-6 family](https://developers.openai.com/api/docs/guides/latest-model) consists of Astra, Sol, and Luna. There is no GPT-6 Terra; Terra belongs to the GPT-5.6 family. The [OpenAI changelog](https://developers.openai.com/api/docs/changelog) records the release of GPT-6 Sol and Luna on 2026-09-22. [Anthropic's Opus 5.5 documentation](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) describes its new model behavior. These official pages were retrieved on 2026-09-25.

A newer model might already produce a strong regression test without hr-tdd, reducing the skill's marginal benefit; it might still benefit from the procedure. Both are hypotheses to test. Bind each evaluation result to the model, agent surface, CLI version, effort, task, permissions, and tools. In particular, [Anthropic documents](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) that Opus 5.5 defaults to medium effort while Opus 5 defaulted to high, so old latency and cost assumptions should not be carried over unchanged. That page was retrieved on 2026-09-25; this is an API/model documentation claim, not a measurement of the effective effort used by Claude Code CLI in this repository.

The repository's core design remains concrete: it distinguishes documented capabilities, local runtime evidence, and comparative outcomes, and uses admission criteria to constrain recommendations. The benefit of its optional skills is still unproven by this branch. Fix the two P1 findings and the grading evidence path before recording attempts on selected model/surface combinations. Raw scores across providers do not isolate the effect of a skill. New models trigger a recheck of model- and surface-specific assumptions; they do not by themselves invalidate the installer, ownership, or handoff contracts.

## Follow-up review and resolution — 2026-09-25

Reviewer: Claude Code (cloud session, Linux, Python 3.11.15). Scope: the findings above, the merge of
`main` at `1e9ee8a`, and a second pass over the runner. Resolved in `1ec1393` on top of merge
`c1296be`; the branch was renamed from `claude/clever-clarke-dnni5u` to `feat/eval-harness`, following
the `<type>/<topic>` rule `main` added to `CONTRIBUTING.md`. No provider-backed cell was executed.

### Status of the findings above

| Finding | Status | What changed |
|---|---|---|
| [P1] Resume combines settings | **Fixed** | Reproduced first with a stub `claude` on `PATH`: model-A attempt, resumed with model-B, `--max-usd 50`, `--timeout-seconds 10`; the candidate ran on model-B while the record kept model-A, 1.0 and 300. Resume now refuses on any change to runner, model, argv, deadline, `max_usd`, the unmetered allowance, the harness digest or `--trials`, naming each field |
| [P1] Partial arm set completed | **Fixed** | The record carries `plan{arms,trials}` over every case arm, set at creation. Status is judged against it; `--arm` only chooses what runs now, so a one-arm run is `indeterminate` |
| [P2] Grading skips response hashes | **Fixed** | `grade` re-hashes every completed output before writing `blind/` or accepting scores, and names the changed file. It also refuses a second grading and scores outside `0..score_max` |
| [P2] Codex answer not extracted | **Fixed** | The answer is the last `item.completed` whose item type is `agent_message`, per `openai/codex` `codex-rs/exec/src/exec_events.rs` (branch `main`, retrieved 2026-09-25). The regression test uses that event shape; it is a source reading, not a local Codex run, because no Codex CLI is installed on this surface |

Every fix has a regression test (8 new, 33 runner tests in total), and a mutation that reverts each
fix makes its test fail.

### Additional findings

**[P1] Every cell loaded this repository's own `AGENTS.md` (fixed).** Cells ran with `cwd` set to the
repository. On Claude Code CLI 2.1.282, `claude --help` (read 2026-09-25) describes
`--setting-sources` as choosing *settings* files; `CLAUDE.md` auto-discovery is separate and is
switched off only by `--bare` (API-key auth only) or `--safe-mode`. This repository's `CLAUDE.md`
imports `AGENTS.md`, so all four arms, baseline included, would have carried it: the contamination
the isolation profile exists to prevent. `main`'s prior-art runs found the related leak (the
headless CLI shows the model its working directory). Each cell now runs in a fresh, empty,
system-named temporary directory outside the repository, removed afterwards. The record states that
policy instead of an absolute local path. Not verified: whether user-level context, such as a user
memory file, is excluded; a `limitations[]` entry says so. A one-call check before the first
attempt, on the surface you will run, would settle it cheaply.

**[P2] Blinding was overstated (fixed in the harness README).** The label mapping is a public
function of the group key and arm names, both in the record, and `blind/` sat beside
`cell-<arm>-<trial>.out`. The README now says to hand a grader `blind/` alone.

**[P2] Attempt output was hashed but line-ending normalised (fixed).** `main` made captured
prior-art output `-text`; skill-eval attempt output is hashed the same way, so `attempt-*/` now has
a `-text` rule, and `--attempt` must be a single `attempt-*` name so the rule always applies.

**[P3] Minor robustness (fixed).** A leftover lock now names itself and the remedy. A leftover
`attempt.json.tmp` no longer blocks every later write.

### Still open

- **Effort is an uncontrolled variable.** The runner pins the model but not effort. The Opus 5.5
  page cited above states the default effort is `medium`, where Opus 5 ran at `high` (re-read
  2026-09-25), so an unpinned run measures whatever default each model and CLI build apply.
  Claude Code CLI 2.1.282 accepts `--effort <level>`. Pin and record it before the first attempt;
  the Codex equivalent needs a source or a local test first.
- **Codex runner is unusable at the default allowance.** Codex reports no cost, so with
  `--allow-unmetered-cells 0` the campaign stops after one completed cell. That refusal is the
  design; a Codex attempt needs an explicit allowance and a recorded reason.
- **Rubric headroom.** `main` closed the handoff evaluation with a saturated rubric. Run a small
  number of cells on the target model first. If all four arms reach the ceiling, fix the case
  before spending on trials.
- **Positioning against `main`.** `main` now states that candidates enter from observed failure,
  not from surveys, and lists an evaluation scenario with headroom as deferred. `hr-tdd-01` traces
  to the `PORTABILITY.md` sentence naming `hr-tdd` for a future trial, not to an observed failure.
  Before a PR, say in `tests/workflows/skill-eval/README.md` why it is not a survey-driven intake,
  or hold the first attempt until a failure motivates it.
- **The Windows path failure** noted above (`test_follow_up_command_survives_paths_containing_spaces`)
  is outside this branch and not reproduced on Linux.

### Verification of this follow-up

`python -m unittest discover -s tests -v`: 109 passed on Linux, Python 3.11.15. The runner tests also
passed on 3.9, 3.10 and 3.13. `python check.py` exit 0, `python install.py --check` no drift,
`runner.py verify --case tests/workflows/skill-eval/hr-tdd-01` no drift, and `git diff --check` clean.
Frozen `hr-tdd-01` packet bytes are unchanged.
