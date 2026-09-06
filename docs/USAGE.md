# Usage and cost

Operational guidance, reviewed 2026-09-06. This project does not enforce provider spending limits,
choose a model automatically, or measure savings from its instructions.

## Start with the right measurement

| Measure | What to keep | What it cannot establish |
|---|---|---|
| Subscription allowance | Dated before/after snapshots, window and reset time, concurrent activity | An isolated task cost or a dollar amount |
| Run tokens | Raw producer fields, model, effort, session/turn identity, retries | Billed credits without the applicable rate and accounting semantics |
| Billed credits / money | Provider record, billing mode, currency and date | A universal rate for another plan/model |
| Elapsed time | Start/end and whether parallel workers overlap | Token use or quality |
| Outcome | Passed criteria, failures and blocked attempts | Savings without a comparable baseline |

OpenAI's [pricing guidance](https://learn.chatgpt.com/docs/pricing), retrieved 2026-09-06,
states that task context, model, reasoning, tools and caching affect allowance. It distinguishes
token/credit rates from subscription limits and points to the usage dashboard or CLI `/status`.
Keep those units separate; do not estimate a task's price from a five-hour percentage change.
Consult the current rate card for your actual billing mode rather than freezing prices here.

## Run a bounded check

The installer includes `.houserules/workflow.py` and the short agent entry `.houserules/START.md`.
Use `--activate-workflow` during [installation](../README.md#install) to append the AGENTS.md trigger,
or ask the agent to follow START explicitly. No hook or provider integration is required.

From the adopting project's root, substitute the files and test command relevant to your task:

```bash
python .houserules/workflow.py start parser-fix --task "Reject malformed input" --target src/parser.py --target tests/test_parser.py --max-runs 3 --max-seconds 300
python .houserules/workflow.py run parser-fix -- python -m unittest discover -s tests -v
python .houserules/workflow.py status parser-fix
```

The start command creates `work/parser-fix/workflow.json`; runs retain separate logs there.
Routine output is a short status and latest-log pointer; full command history stays in the file.
The defaults are three attempts and 300 total seconds of command execution. Set task-appropriate
limits at creation. Failed, blocked and timed-out attempts count. The runner refuses a repeated
passing command when the selected inputs and its log are unchanged.

Use status before resuming or reusing a result. A change to selected files or the retained log
makes that result stale. A command that changes its own selected inputs also needs a subsequent
stable check. Include test files and relevant configuration as targets; missing future files are
allowed at creation but cannot establish a verified pass until they exist.

| Exit | Meaning |
|---|---|
| 0 | Task created, or latest command passed with unchanged selected targets and log |
| 1 | No current passing evidence: not run, failed, blocked, timed out or stale |
| 2 | Invalid request/state, exhausted budget, duplicate pass or another execution refusal |

Inspect the log and acceptance criterion; a zero exit does not prove the task was solved.
`result` describes the latest command outcome (or detected staleness); `verified` says whether
its evidence is currently reusable. A successful command with a missing target can report
`result: "pass"` and `verified: false`; use `verified` and the exit code, not the word "pass" alone.
Only the **latest command** is the current result. Use a project check that covers the necessary
gates together when acceptance needs multiple checks; prior attempts remain in the record.

## What the controls cover

- Bounds apply only to commands invoked through workflow.py. They do not cap surrounding chat,
  token use, API charges or other processes. A timeout stops the direct child, not necessarily
  detached descendants; use short-lived verification commands.
- Freshness covers exact selected files and log bytes, not the entire repository, dependencies,
  network state or environment. Choose targets deliberately; this is not tamper-proof attestation.
  The entire work/ record area is excluded from targets, including other tasks' logs and records.
  Keep inputs to verify outside that area; its mutable records remain evidence pointers.
- Commands run as exact arguments without a shell, with normal user permissions. This is not a
  security sandbox. Keep credentials out of arguments and logs.
- After an interrupted run or lock, inspect the recorded state and process before recovery.
  The tool does not silently retry or replace existing task records. Do not evade a budget by
  creating another task ID; agree on a new scope/budget when needed.
- Raw Codex `turn.completed` usage is retained when a command emits it. Other commands normally
  have unknown token/cost data. No token total or bill is inferred.

The optional [verification resource record](../templates/work/verification.md#resource-use-optional)
holds model, billing and outcome context that command logs cannot supply. It travels with
`--work verification`. Human guidance stays here; the installed START carries the short procedure.

## Apply the budget to agent work

For this project, apply them as follows:

- Keep the user's selected model until they choose otherwise. Compare another available model
  on the same bounded task before claiming equal quality at lower usage. Model benchmarking is pending.
- Use the accepted scope and existing evidence to avoid repeating research or review without a new question.
- Resolve startup, tool access and authentication problems before launching a full repository task.
- Retain both the outcome and raw usage for an experiment. A timeout or blocked task can still
  have consumed resources; a missing usage event supplies no zero-cost claim.
- Finish with the required gates and a short handoff. There is no need for an extra model review
  solely because the prior review passed.

## What our existing runs show

Read from the original Codex CLI 0.153.4 JSONL and metadata on 2026-09-06; configured
gpt-6-astra / medium. The [acceptance report](../tests/workflows/toolkit-adoption/README.md#independent-cli-attempts-and-limits)
records the blockers. Each row below has one `turn.completed` event, not a sum of snapshots.

| Local attempt | Elapsed seconds | input_tokens | cached_input_tokens | output_tokens | Task outcome |
|---|---:|---:|---:|---:|---|
| work/toolkit-runtime-normal | 77.73 | 152441 | 134784 | 1089 | Windows helper blocked the task |
| work/toolkit-runtime-20260906 | 23.64 | 60876 | 46080 | 289 | Tool policy blocked the task |

These are selected failed attempts, not the whole session's usage. Raw files remain ignored/local.
Cached counts are displayed as reported, not added again. Dollars and subscription allowance
attributable to these attempts are unknown. There is no measured before/after saving yet.
The actionable next measurement is completed task outcome plus resource use under the bounded
retry procedure, not another replay of an unchanged infrastructure failure.
