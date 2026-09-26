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

## Independent remote review — 2026-09-26

Scope: `fujiakito/houserules`, `feat/eval-harness` at `4273bcb`. This pass inspected the remote
GitHub branch, the merged commits, `review.md`, `tests/eval/runner.py`, its 33 regression tests,
`tests/eval/README.md`, the frozen case manifest, and `.gitattributes`. No local checkout, provider
CLI execution, or new test run was used for this pass.

### Merge and fix verification

The merge is present. Commit `c1296be` has parents `75771fe` (the evaluation branch) and
`1e9ee8a` (`main`). The current `main` is still `1e9ee8a`; GitHub comparison reports this
branch **8 commits ahead, 0 behind**. The runner fix is commit `1ec1393`, and `4273bcb` adds
the preceding follow-up review.

| Earlier finding | Independent code and test check |
|---|---|
| Resume mixes settings | `resume_conflicts` and `cmd_run` reject changes to runner, model, argv, timeout, budget, harness digest, and trial count. `test_resume_refuses_a_changed_model_and_leaves_the_record_untouched` and `test_resume_refuses_a_changed_budget_deadline_or_trial_count` cover representative changes. **Verified by source inspection; see CLI version gap below.** |
| Partial arms marked complete | `new_record` stores every declared arm in `plan`; `attempt_status` checks the whole recorded plan. `test_one_arm_run_is_indeterminate_against_the_recorded_plan` covers the former failure. **Verified by source inspection.** |
| Grading accepts changed output | `cmd_grade` re-hashes every completed output before emitting `blind/` or accepting scores; `test_grade_refuses_an_output_changed_after_execution` covers it. **Verified by source inspection.** |
| Codex JSONL becomes raw grader input | `parse_payload` extracts the last completed `agent_message`; `test_codex_jsonl_yields_the_last_agent_message_and_turn_usage` covers the documented event shape. **Verified for the fixture, not against a live Codex CLI.** |
| Project context, blinding, and output bytes | `run_cell` gives each cell a fresh temporary cwd, the README tells graders to receive only `blind/`, and `.gitattributes` preserves `attempt-*/**` bytes. Corresponding tests cover cwd and attempt naming. **Verified by source inspection, not by a provider run or a Git checkout on each platform.** |

### Remaining runner findings

**[P1] Resume can mix CLI versions and misstate the version of earlier cells.**
`cmd_run` calls `probe_version` on every invocation and unconditionally assigns its result to
`record['surface_version']`. `resume_conflicts` does not compare that version. A baseline run
under CLI version A can therefore be resumed for the candidate under version B; the final record
names B for both. This breaks the README's claim that an attempt is evidence for one named surface
and version. Probe before resuming, refuse a changed version before any cell executes or record is
rewritten, and add a regression test that checks both the refusal and unchanged record bytes.
[Runner](tests/eval/runner.py) · [Tests](tests/test_eval_runner.py)

**[P2] An incomplete `frozen_sha256` manifest can pass `verify` and `run`.**
`read_case` checks that declared files exist, but does not require a recorded hash for every name
from `frozen_names`. `frozen_drift` iterates only recorded keys, and `cmd_verify` exits 0 when
there is no mismatch even if a declared input has no expected hash. Such an input may change
without refusal. The shipped `hr-tdd-01` manifest does list all six declared files, so this is a
runner validation gap rather than observed drift in that case. Require exact coverage before
`verify`, `plan`, or `run`, with a regression test for an omitted arm hash.
[Runner](tests/eval/runner.py) · [Case](tests/workflows/skill-eval/hr-tdd-01/case.json)

**[P2] `grade` does not use the attempt lock.**
`cmd_run` holds `.eval.lock` while it updates the record, but `cmd_grade` reads and rewrites
`attempt.json` without it. If grading overlaps a running or resumed campaign, the blind packet
can be built from a transient subset and the two record writes can overwrite each other. Use the
same lock around grading's read, hash checks, packet generation, and final write; add a test for
grading while the lock is held. [Runner](tests/eval/runner.py)

### Evidence boundary

The GitHub commit has no reported commit status or Actions workflow run, so this pass cannot
independently confirm the preceding review's 109-pass claim. The tests were inspected but not
executed here. There is still no provider-backed `hr-tdd-01` attempt establishing the skill's
marginal benefit on a target model. The previously noted effort pin, Codex cost reporting, rubric
headroom, and intake positioning remain open. Address the runner findings above before treating a
new attempt record as comparison evidence.

## Response to the independent remote review — 2026-09-26

Reviewer: Claude Code (cloud session, Linux, Python 3.11.15), on a local checkout of
`feat/eval-harness` at `a3f581b`. Resolved in `26a61af`. No provider-backed cell was executed.

All three findings were confirmed by reading the code before any change. Each fix has a regression
test, and reverting each fix makes its test fail.

| Finding | Status | What changed |
|---|---|---|
| [P1] Resume mixes CLI versions | **Fixed** | `cmd_run` compares the probed version with the recorded `surface_version` and refuses before any cell runs or the record is rewritten. A CLI that cannot be probed on resume is also refused, where it previously overwrote the recorded version with `null`. Tests cover a changed version, an unprobeable CLI (record bytes unchanged in both cases), and a resume under the same version |
| [P2] Incomplete `frozen_sha256` passes | **Fixed** | `read_case` refuses a manifest with no hash for any name from `frozen_names`. Every subcommand goes through `read_case`, so `verify`, `plan`, `run` and `grade` all refuse. The test drops the candidate arm's hash and checks all three pre-execution commands, and that no attempt directory is created. The shipped `hr-tdd-01` manifest covers all six inputs and still verifies |
| [P2] `grade` skips the lock | **Fixed** | `cmd_grade` holds `.eval.lock` around the read, hash checks, packet generation and final write. With the lock held, both packet emission and score ingestion refuse, write nothing, and leave the other process's lock in place |

The harness README refusal table and the `docs/ENFORCEMENT.md` row now list all three.

### On the evidence boundary

The absence of a CI run is expected rather than a gap in this branch: `.github/workflows/check.yml`
triggers on `push` to `main`, on `pull_request` and on `workflow_dispatch`. No pull request exists for
`feat/eval-harness`, so nothing has run. Opening the PR, or a manual dispatch, produces the
independent 3.9/3.11/3.13 run that the previous pass could not see.

Local result for this change: `python -m unittest discover -s tests -v` passed 113 tests on Linux,
Python 3.11.15. The runner tests also passed on 3.9, 3.10 and 3.13. `python check.py` exited 0,
`python install.py --check` reported no drift, `runner.py verify` found no drift in `hr-tdd-01`,
and `git diff --check` was clean.

Still open, unchanged from the previous sections:
- pin and record effort
- the Codex cost allowance
- rubric headroom on the target model
- intake positioning against `main`
- the Windows 8.3 path test failure

The old remote branch `claude/clever-clarke-dnni5u` could not be deleted from this session: the
push was cut off at the transport. It still points at `75771fe`, which `feat/eval-harness`
contains. Delete it from GitHub.

## Independent verification after the second runner fix — 2026-09-26

Scope: the remote `fujiakito/houserules` branch `feat/eval-harness` at `e0095e9`, including
the runner fix in `26a61af`. This was a GitHub source and test inspection, with no local checkout
or provider CLI run. The old `claude/clever-clarke-dnni5u` ref now returns 404; the deletion
request in the preceding section is obsolete. The branch is 11 commits ahead of, and 0 behind,
`main` at `1e9ee8a`.

| Finding from the independent remote review | Verification at this HEAD |
|---|---|
| CLI version changes on resume | **Fixed in the inspected code.** `cmd_run` compares the new probe with the recorded `surface_version` before rewriting the record or running a cell. The new test covers a changed version, an unavailable probe, and unchanged record bytes; another test covers a successful same-version resume. |
| Missing `frozen_sha256` entry | **Fixed for declared inputs.** `read_case` rejects any name from `frozen_names` without a recorded hash, so all four commands pass through the check. The new test removes an arm hash and confirms `verify`, `plan`, and `run` refuse before creating an attempt. See the surplus-entry issue below. |
| Concurrent `grade` and `run` | **Fixed in the inspected code.** `cmd_grade` acquires the same attempt lock before `grade_locked` reads or writes the record and blind packet. The new test verifies both packet emission and score ingestion refuse while the lock exists, without removing it. |

The suite now contains 37 runner test methods, four more than the earlier inspected version.
GitHub reports no commit status or Actions run for this HEAD. The workflow runs on pushes to
`main`, pull requests, or manual dispatch, so the absence of a branch-push run is consistent with
its trigger configuration. The 113-pass Linux result in the preceding section is a maintainer
report, not a test run independently observed in this pass. The committed `hr-tdd-01` directory
still contains only the case packet and no provider-backed attempt.

### Additional findings

**[P1] Grading can use a changed rubric while recording the old rubric hash.**
`cmd_grade` calls `read_case`, which checks hash coverage and file existence but does not compare
current bytes with either `case.json`'s `frozen_sha256` or the attempt's
`input_hashes_current`. Packet generation in `grade_locked` reads the current rubric into
`blind/rubric-judge.md`; later score ingestion writes `grading.rubric_sha256` from the attempt's
recorded hash. If the rubric changes after a run, the grader can see different criteria while the
record still names the original rubric.

The `--scores` path also accepts scores without checking input drift. Reject frozen input drift
against the attempt record before either grading path, and test both packet generation and score
ingestion after a rubric edit. [Runner](tests/eval/runner.py)

**[P3] Surplus recorded input hashes still pass `verify`.**
The new `read_case` check rejects missing hashes, but does not reject keys in `frozen_sha256`
that are not declared inputs. `frozen_drift` ignores such keys, and `cmd_verify` reports them as
`unrecognised_recorded_names` while returning success when no other drift exists. This does not
leave a declared input unprotected, but a successful verification can appear to cover a file it
never checked. The previous review requested exact coverage; enforce equality between the
declared-input set and recorded-hash keys, or make surplus keys a verification failure.
[Runner](tests/eval/runner.py)

The three targeted fixes are supported by code and regression tests. The grading-input issue
above remains a blocker for treating a future graded attempt as revision-bound evidence. Effort
pinning, Codex cost handling, rubric headroom, and intake positioning remain as documented in
the preceding review.

## Response to the verification after the second runner fix — 2026-09-26

Reviewer: Claude Code (cloud session, Linux, Python 3.11.15), on a local checkout of
`feat/eval-harness` at `d471d33`. Resolved in `0806d8e`. No provider-backed cell was executed.

Branch housekeeping: `git ls-remote` no longer lists `claude/clever-clarke-dnni5u`. The deletion
request two sections above is closed.

Both findings were confirmed by reading the code before any change. Each fix has a regression test,
and reverting each fix makes its test fail.

| Finding | Status | What changed |
|---|---|---|
| [P1] Grading uses a changed rubric under the old hash | **Fixed** | `grade_locked` refuses before either grading path when any frozen input differs from the attempt's `input_hashes_current` or from `frozen_sha256`. Those inputs include `case.json` and the rubric's judge span. It also refuses a record with no input hashes |
| [P3] Surplus recorded hashes pass `verify` | **Fixed** | `read_case` requires the `frozen_sha256` keys to equal the declared inputs exactly, and refuses both missing and surplus names in every subcommand. The `unrecognised_recorded_names` field of `verify` could no longer be non-empty and was removed |

Tests added:
- A rubric edit after the run: both packet emission and score ingestion refuse, no `blind/` is
  written, and the record bytes are unchanged.
- A rubric edit that also re-hashes `case.json` to match: grading still refuses. Checking
  `frozen_sha256` alone would have let this edit through; the attempt record is what catches it.
- A surplus manifest key: `verify` refuses and names the key.

The harness README refusal table and the `docs/ENFORCEMENT.md` row are updated.

Local result: `python -m unittest discover -s tests -v` passed 116 tests on Linux, Python 3.11.15.
The runner tests (40) also passed on 3.9, 3.10 and 3.13. `python check.py` exited 0,
`python install.py --check` reported no drift, `runner.py verify` found no drift in `hr-tdd-01`,
and `git diff --check` was clean. As before, this is a maintainer-side run. A pull request, or a
`workflow_dispatch` of `check.yml`, is what produces an independently observable CI result.

The grading-input blocker named in the preceding section is resolved. The items that remain open
before the first attempt are unchanged:
- pin and record effort
- the Codex cost allowance
- rubric headroom on the target model
- intake positioning against `main`
- the Windows 8.3 path test failure

## Offline pilot preparation — 2026-09-26

Follow-up scope: explicit effort, cost accounting, an offline model matrix, and observable hosted
CI. Implemented through the GitHub connector without a local checkout, starting at 5634019.
Provider execution is expressly deferred by the maintainer; hr-tdd-01 remains Not run.

- plan/run now require effort and pass it through provider-specific argv. It is recorded and
  checked on resume, but effective runtime effort still needs a surface observation.
- Codex execution needs a positive unmetered allowance and a recorded reason. Unknown charges
  after failed/timed-out execution count too; partial cost is a subtotal, never a known total.
  The reported-spend threshold is not a hard billing cap.
- Resume preserves every attempted cell, including failed, blocked and timed-out observations.
  It only runs never-attempted cells. Output replacement can no longer hide those outcomes.
- [PILOT.md](tests/eval/PILOT.md) defines the three-model headroom smoke test, intake limitation,
  shared-contract/model-specific-guidance design and the prerequisites for a tool-using case.
  It does not satisfy criterion 1 or certify a skill benefit.
- [Draft PR #4](https://github.com/fujiakito/houserules/pull/4) provides hosted CI rather than a
  local pass claim. Its initial run caught a legacy plan fixture missing --effort; the follow-up
  fixes that fixture and fetches full history so two migration tests do not silently skip.
  Use the PR's latest commit-bound checks for the final status, not the initial failed run.

The documented Windows path failure remains outside this change. Native loading, effective
isolation, actual model behavior and comparative benefit remain unverified. No installed skill,
frozen case packet or historical attempt output was modified.
