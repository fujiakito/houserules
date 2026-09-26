# Model-aware evaluation pilot

Prepared 2026-09-26. Reader: evaluation maintainer. Action: review the offline plans and close
the execution prerequisites before authorizing a provider run. Revisit after an observed task
failure, CLI/model change, or completed pilot. **Not run. Provider execution is not authorized.**

This plan implements a user-requested comparison, not a recommendation of an optional skill.
The machine-readable [pilot.json](pilot.json) is an offline planning fixture; it is not an
execution scheduler and does not authorize billing. No provider is installed or invoked by CI.

## Decision and intake

The immediate question is whether the existing frozen hr-tdd-01 instrument has headroom on
GPT-6 Sol, GPT-6 Luna and Claude Opus 5.5. It is a synthetic instrument check requested by the
maintainer, not evidence of an observed adopter failure. It therefore does not satisfy
[fallback admission criterion 1](../../research/PORTABILITY.md#fallback-admission-criteria).
The case remains experimental; the survey did not earn it a recommendation.

Use one trial of all four existing arms per model: 12 planned cells across three separate
attempts, not one mixed-model attempt. Start at explicit medium effort as a declared pilot
choice, not an optimized setting or an assertion of equal compute. CLI versions and effective
effort must be checked on the eventual execution surface. Preserve all original packet bytes.

These commands only print plans and make no provider calls:

```bash
python tests/eval/runner.py verify --case tests/workflows/skill-eval/hr-tdd-01
python tests/eval/runner.py plan --case tests/workflows/skill-eval/hr-tdd-01 --runner codex --model gpt-6-sol --effort medium --trials 1
python tests/eval/runner.py plan --case tests/workflows/skill-eval/hr-tdd-01 --runner codex --model gpt-6-luna --effort medium --trials 1
python tests/eval/runner.py plan --case tests/workflows/skill-eval/hr-tdd-01 --runner claude --model claude-opus-5-5 --effort medium --trials 1
```

The regression suite checks that every profile plans four cells, matches frozen hashes,
passes effort to the runner, creates no attempt directory and never spawns a provider.

## Before paid execution

1. Approve the provider/account and total budget separately. This change leaves max_usd null
   and execution_authorized false. Do not put credentials in a record, command line or artifact.
2. Pin the CLI build and capture its version. Confirm model access and effort support; do not
   silently fall back to another model, default effort or a different authentication route.
3. Verify effective isolation on that surface. Fresh cwd and flags are only requested controls.
   The [2026-09-26 canary smoke test](README.md#isolation-smoke-test--claude-code-cli-21283-2026-09-26)
   covers Claude Code CLI 2.1.283 in a cloud session: user and project `CLAUDE.md` excluded,
   no tools, effort accepted. Repeat it on any other surface or build. Codex is untested; its
   read-only sandbox is not equivalent to disabling every tool, so confirm no tools ran in this
   prompt-only case.
4. For Codex, explicitly approve an unmetered allowance and record its reason. Raw tokens can
   be retained, but they are not an observed billed total. If a hard spend bound is required,
   do not run until the provider/account offers a suitable enforced limit.
5. Keep the frozen 300-second deadline. One model's timeout is an indeterminate result, not a
   reason to raise its deadline or replace its output. A running cell may exceed the remaining
   reported-cost threshold. Resume only executes never-attempted cells.
6. Give the human grader only blind/. Record grader identity and scoring before revealing arms.
   A project participant is not an independent grader.

A CLI version probe or mock test is not a model execution check. Any paid isolation smoke check
also needs approval and must be counted in the agreed provider budget.

## Headroom decision, fixed before outputs

Apply the existing rubric and retain per-check scores in a separate dated grading note, alongside
the numeric scores ingested by grade. The runner's numeric ingestion does not collect per-check
breakdowns automatically.

- If any cell fails, times out, or is unavailable, retain it and label that model's pilot
  indeterminate. Do not selectively retry it to obtain a complete comparison.
- If every arm scores at least 95/100, mark that model/case near-ceiling and do not buy more
  trials to seek a small difference. This is a declared pilot heuristic, not a statistical test.
- Otherwise inspect which substantive checks discriminate and whether the case reflects a
  failure observed in real work. A one-trial gap supports instrument revision or a replication
  plan only; it cannot support promotion, equivalence, or a cost-saving claim.
- A tie with one-line is evidence that the longer treatment has not earned its overhead here.
  A tie at the ceiling says the instrument cannot distinguish the treatments.
- Do not pool scores across models or treat equal effort labels as equal compute. Compare arms
  within each model/configuration first. Any later replication must predeclare trial count,
  execution order/counterbalancing, thresholds and treatment bytes.

The current runner uses fixed arm order per trial. This is disclosed in each record; a confirmatory
replication needs an order-control design before execution. Do not edit the existing frozen case
after looking at its results; create a separately versioned case if the instrument changes.

## Model-specific guidance without duplicating whole skills

Keep three concerns separate:

| Concern | Shared or variable | Evidence needed |
|---|---|---|
| Task contract: requirements, authority, public interfaces, acceptance tests | Shared across all arms and models | Identical facts and acceptance criteria |
| Procedure: concise outcome guidance, detailed steps, examples, recovery hints | Experimental treatment | Within-model comparative outcomes and overhead |
| Runner configuration: model, effort, tools, CLI, permissions | Pinned within an attempt | Recorded settings and surface-specific runtime observation |

Astra, Fable and Opus 5.5 are not one interchangeable "frontier" behavior class. Likewise,
"older model needs a comprehensive prompt" is a hypothesis, not an admission rule. Task novelty,
surface system prompts and tool access may matter more than release age. An Opus 4.6 comparison
requires an explicit supported model ID and surface/access check; it is not in this initial pilot.

For a later failure-driven case, compare the same task under bare, concise-contract,
detailed-procedure and length-control treatments. Add a vendor-informed treatment only when a
specific behavior motivates it, freeze its bytes before execution, and evaluate on held-out
tasks as well as the motivating failure. Model-specific guidance must not change authority,
requirements or the quality bar, and must not be injected into baseline as common setup.

Use one canonical skill contract and small optional guidance files if data earns them. Record
the exact model/surface/effort/task scope, sources, prompt hash and recheck trigger. Avoid a
router that guesses a model from prose or substitutes models. Unknown configurations use the
shared contract and explicitly selected guidance; no extra instructions are selected merely
because a model is old. No new skill or model router is installed by this change.

Official guidance informs these hypotheses, but is not evidence for houserules' performance.
Sources retrieved 2026-09-26:

- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra):
  unnecessary procedural scaffolding can constrain Astra, and guidance useful to Sol or Luna
  may not suit it. Prefer selective loading and reevaluate existing instructions.
- [Anthropic: Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5):
  calibrate effort and address observed model-specific behaviors.
  [Model changes](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)
  document medium default effort versus high on Opus 5.
- [Anthropic: Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1):
  targeted guidance covers completion, tool batching, edits and other behavior differences.
  This source concerns Fable 5.1, not every Fable version.

## Next tool-using case: entry contract

Do not claim the prompt-only result proves actual red-green behavior. Prepare a new tool-using
case only after a real failure is captured with its source revision, expected behavior, command,
actual outcome, model, surface and configuration. Possible motivating classes are a regression
test that misses half a requirement, an implementation that changes a public return value, or
reuse of stale verification evidence. These are candidate classes, not newly observed incidents.

The new case must use a disposable fixture repository at one pinned revision per cell, equivalent
tools and permissions, a bounded execution budget, frozen treatment files and independent
acceptance checks kept out of the generating prompt. Preserve the diff, command trace, red failure
reason, final tests, elapsed time, raw usage and unknown-cost markers. Grade final behavior,
regression sensitivity, interface preservation, unnecessary edits and honesty of verification.

Run deterministic acceptance checks against deliberately correct and incorrect fixture solutions
before using them to score models. Keep native skill loading as a separate treatment from pasted
skill text. The current empty-directory, prompt-only runner does not implement this tool-using
protocol; weakening its isolation flags would not implement it.

## Remote workflow and completion evidence

Changes can be authored through GitHub's contents/Git-data APIs without a local checkout.
A draft PR triggers the existing GitHub Actions workflow on hosted runners for Python 3.9,
3.11 and 3.13. It runs the regression suite (including offline pilot plans), check.py and
install.py --check. CI has no provider installation, provider credentials or paid evaluation step.

Record the PR and exact CI run/head after observing completion. Passing those jobs establishes
runner/installer/checker behavior under their fixtures; it does not establish model compatibility,
honored isolation, native skill discovery or a skill-quality improvement. A red CI job is still
an unresolved check, even when an earlier maintainer run was green.
