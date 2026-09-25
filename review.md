# Review of the evaluation branch and model changes

Reviewed: 2026-09-25. Reader: branch maintainer. Action: resolve the findings before using the evaluation harness to recommend a skill. Revisit this review after runner fixes, the first recorded evaluation attempt, or a change to the target model or agent surface.

Scope: fujiakito/houserules, branch claude/clever-clarke-dnni5u at 731fc7d. At the time of review, the branch was three commits ahead of and one commit behind main (1e9ee8a). This review did not run a provider-backed evaluation.

## What the branch is trying to achieve

The three commits document prior art for evaluation harnesses, add an [offline runner](tests/eval/README.md) and regression tests, and freeze the first [hr-tdd-01 case](tests/workflows/skill-eval/hr-tdd-01/README.md). Their purpose is to address [fallback admission criterion 5](research/PORTABILITY.md#fallback-admission-criteria): compare an optional skill with a baseline on representative tasks, record outcomes, cost, and failures, and only then decide whether the skill merits a recommendation.

hr-tdd-01 gives the same task to four arms: a baseline without a procedure, a candidate containing the full hr-tdd procedure, a length-matched generic procedure (control-length), and a one-line test-first instruction. The rubric emphasizes the correct failure explanation, public-interface behavior, and a minimal fix. This is a prompt-only case: it measures the effect of instruction text on a written answer. It does not test native skill discovery, iteration with tools, or actual test execution. The case was prepared and frozen on 2026-09-15 but had **not been run** at review time, so it provides no result showing that hr-tdd outperforms the other arms.

## Code review findings

### [P1] Resume can combine cells run with different settings

[cmd_run](tests/eval/runner.py#L364) checks only schema_version and input hashes when it opens an existing attempt.json. It does not compare the new model, runner, argv, timeout_seconds, budget, or intended cell plan with the recorded attempt. I reproduced this with a mocked provider: run baseline with model-A, then run candidate with model-B and --resume. The result is marked completed while the record still identifies model-A. That record cannot support an arm comparison under one fixed configuration. Resume should reject incompatible settings.

### [P1] A partial set of arms can be marked completed

[cmd_run](tests/eval/runner.py#L366) rebuilds cells from the current --arm and --trials options and uses that set to determine the status of the whole attempt. Running only baseline returned completed in a reproduction, although the case has three other arms. This conflicts with [release gate G1](tests/workflows/skill-eval/hr-tdd-01/rubric.md#release-gate--maintainer-only-not-for-the-grader). Persist the full campaign plan in the attempt record and calculate status against it.

### [P2] Grading does not verify response hashes

[run_cell](tests/eval/runner.py#L490) records output_sha256, but [cmd_grade](tests/eval/runner.py#L498) does not recheck that hash before reading an output for the blind packet or accepting scores. If a response changes after execution, the grader scores the changed text while the record retains the original hash. Grading should verify every recorded output hash.

### [P2] The Codex JSONL path does not extract the agent response

The runner invokes codex exec --json, but [parse_payload](tests/eval/runner.py#L201) extracts only usage and cost from JSONL events, leaving response unset. [cmd_grade](tests/eval/runner.py#L519) consequently writes raw JSONL to the blind packet instead of the answer alone. On 2026-09-25, codex exec --help on the local Codex CLI surface, version 0.155.0-alpha.16.4, confirmed that --json emits JSONL. This observation does not establish Desktop app or IDE behavior. Add response extraction and a Codex-specific regression test.

## Verification and limits

At the reviewed branch HEAD on Windows with Python, python check.py, python install.py --check, runner.py verify --case tests/workflows/skill-eval/hr-tdd-01, and git diff --check origin/main...HEAD passed. All 25 runner regression tests passed. The full python -m unittest discover -s tests -v run executed 101 tests with one failure and five skips. The failed test, test_follow_up_command_survives_paths_containing_spaces, was unchanged by this branch; its observed failure was a mismatch between the long and 8.3 forms of a Windows temporary path. The full suite therefore cannot be reported as passing. These findings review runner logic; no paid provider cells were executed.

## Effect of newly released models

As of 2026-09-25, the [official OpenAI GPT-6 family](https://developers.openai.com/api/docs/guides/latest-model) consists of Astra, Sol, and Luna. There is no GPT-6 Terra; Terra belongs to the GPT-5.6 family. The [OpenAI changelog](https://developers.openai.com/api/docs/changelog) records the release of GPT-6 Sol and Luna on 2026-09-22. [Anthropic's Opus 5.5 documentation](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) describes its new model behavior. These official pages were retrieved on 2026-09-25.

A newer model might already produce a strong regression test without hr-tdd, reducing the skill's marginal benefit; it might still benefit from the procedure. Both are hypotheses to test. Bind each evaluation result to the model, agent surface, CLI version, effort, task, permissions, and tools. In particular, [Anthropic documents](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) that Opus 5.5 defaults to medium effort while Opus 5 defaulted to high, so old latency and cost assumptions should not be carried over unchanged. That page was retrieved on 2026-09-25; this is an API/model documentation claim, not a measurement of the effective effort used by Claude Code CLI in this repository.

The repository's core design remains concrete: it distinguishes documented capabilities, local runtime evidence, and comparative outcomes, and uses admission criteria to constrain recommendations. The benefit of its optional skills is still unproven by this branch. Fix the two P1 findings and the grading evidence path before recording attempts on selected model/surface combinations. Raw scores across providers do not isolate the effect of a skill. New models trigger a recheck of model- and surface-specific assumptions; they do not by themselves invalidate the installer, ownership, or handoff contracts.
