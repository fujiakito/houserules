# Paired artifact-consumption smoke trial

Date: 2026-09-05. **Execution incomplete; no comparative result.**
This is a bounded first attempt under the user's remaining-usage constraint, not a runner or benchmark.

## Protocol and scope

[Baseline packet](baseline-prompt.md), [candidate packet](candidate-prompt.md), and
[outcome rubric](rubric.md) were saved before launch. The synthetic packet bundles resume,
stale-review, missing-evidence and finding-resolution checks into one scenario. Both arms have
the same task facts. The candidate adds a populated handoff and the existing consumer protocol.
Task facts are matched; generic protocol guidance was supplied only to the candidate.

Planned execution: one new ephemeral CLI session per arm, sequential baseline then candidate,
same working directory and default configuration, read-only sandbox. Prompt supplied on stdin:
`codex exec --ephemeral --sandbox read-only --color never -`.
The packets prohibit tools and writes. They model explicitly transferred documents; they do not
test automatic file discovery, real task execution, or cross-agent portability. Project/user
configuration was not isolated. Any successful future run must record the actual model and
context exposure before treating it as a controlled comparison. Repetition and a real repository
artifact remain necessary before promotion decisions.

## Observed execution

- Surface: Windows, sandbox-launched Codex CLI **0.153.4**, version measured locally.
- Working directory: `C:/Projects/houserules`.
- Baseline: process did not finish within **90.03 seconds**; terminated by the subprocess timeout.
- Candidate: **not launched**, following the stop-on-infrastructure-failure rule.
- Outcome: **indeterminate**; zero completed pairs, no score and no evidence of candidate benefit.
- Model/provider and token/cost totals: unavailable; no zero-cost inference. The timeout does not
  establish whether the cause was startup, transport, configuration or model execution.
- Partial process streams were not retained on timeout. [Run metadata](run-metadata.json) records
  the observed duration and baseline prompt hash; it cannot diagnose the underlying cause.
- No retry or larger campaign was started. No `--work` validator or fallback skill is justified
  by this attempt. The comparative-evaluation step remains open.

## Reproducible inputs

Hashes are SHA-256 of the exact saved UTF-8 file bytes, including their line endings.

| Input | SHA-256 |
|---|---|
| baseline-prompt.md | `73fd5cbfd0195f04ae351c917de648af24318b535e1a3d26d4d83ce8f1a856db` |
| candidate-prompt.md | `c55af38a425d6c35863c5382495f8422a051505c3516cc7bd1fdee8c7b4ae12c` |
| rubric.md | `7dfb1baf1df4d524c4d7727bb5c16390e881f8fb5988f5de526b1cc31991fbe0` |

These v1 packets are historical and superseded for future attempts by the [v2 input set](v2/README.md).
Preserve output and diagnostics even on timeout and record model/configuration and usage. Keep this attempt in the
history and record a new attempt separately; do not replace its indeterminate outcome with a score.
A shared-context author grader is not an independent or blinded reviewer.

## Local repository verification

Python 3.12.14 on Windows, 2026-09-05: `check.py` passed; `install.py --check` reported no drift;
unit tests: 18 passed, 1 skipped because Windows could not create a symlink (error 1314).
Those checks validate the existing repository layer, not this live evaluation's outcome.
