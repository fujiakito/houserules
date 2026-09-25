# V2 controlled packet comparison

Prepared 2026-09-05 in response to review R-003 / F-001. **Not run.**
The [v1 attempt](../README.md) and its hashes remain unchanged as evidence of that attempt.
Use this input set for a future trial, not the superseded v1 packets.

Both [baseline](baseline-prompt.md) and [candidate](candidate-prompt.md) contain the exact same
consumer-protocol bytes and task facts. Only the session-note/handoff presentation varies.
The [rubric](rubric.md) evaluates dispositions; protocol repetition is not a scored outcome.
This resolves the unequal-instruction control problem without changing historical inputs.
A win would concern this combined handoff presentation only, not broad portability or skill admission.

## Frozen inputs

SHA-256 covers exact file bytes, including line endings.

| Input | SHA-256 |
|---|---|
| baseline-prompt.md | `de5f3d7354351f8d4857ae297eb5cff0e99409d04e50efcbd875eee236cdbab5` |
| candidate-prompt.md | `c55af38a425d6c35863c5382495f8422a051505c3516cc7bd1fdee8c7b4ae12c` |
| rubric.md | `4a2126bdd5d96ff469c1c3a39b2530c820fa3ca4c7846efb66a7bac9436cba67` |

## Next execution requirements

No retry was performed in this revision. For a future attempt:
use a 300-second per-arm process deadline as a chosen budget, not a proven sufficient timeout.
Retain partial stdout/stderr on timeout and record outcome as indeterminate, not a diagnosed
infrastructure defect. Preserve the v1 metadata unchanged. Store a new attempt record with:
UTC start/end timestamps, exact argv, timeout_seconds, surface/version, actual model/provider
(or explicitly unavailable), configuration/permissions, working directory and input hashes,
exit/timeout status, elapsed time, output/diagnostic paths and available token/cost totals.
Do not expose credentials. Missing usage is unknown, not zero. Keep progress reporting separate
from the process deadline, and do not increase the deadline repeatedly to obtain a desired score.

A completed synthetic pair is only a smoke test. Real task artifacts, actual consumption and
fresh-session evidence remain required before a promotion claim.


## Archived reviewer-reported attempt — 2026-09-06

R-009 reports one completed Claude Code CLI pair after this packet was prepared: both arms scored
3.5/4 under the reviewer's grading. See the [attempt record](attempt-20260906-reported.json) and
[archived reviewer account](attempt-20260906-reviewer-excerpt.md). The original "Not run" statement
above describes preparation, not this later reported event; v1 and the frozen packets remain unchanged.

This is an incomplete archival record, not recovered primary execution evidence. Full outputs,
traces, argv, timestamps and the deadline were unavailable in the supplied account and repository
work files; unknown fields are null. Current input hashes match the frozen set. No model rerun or
independent regrading was performed. Reported token counts do not establish a billing advantage.
The pair remains reviewer-reported and does not satisfy fallback promotion criteria.


## Executed pair with primary evidence — 2026-09-16

One completed pair was executed on Claude Code CLI **2.1.273** headless (`-p`) on Linux, each arm a
separate process with an empty non-repository working directory so no project context file loaded.
The [attempt record](attempt-20260916-executed.json) holds argv, UTC timestamps, the 300-second
deadline, surface/version, model, configuration, measured input hashes, exit status, usage and cost.
Complete arm and grader outputs are in [attempt-20260916-outputs/](attempt-20260916-outputs/),
alongside the harness that produced them.

Blind grading by a third separate process scored **baseline 3/4** and **candidate 4/4**; neither arm
was indeterminate and the measured input hashes match the frozen set. This is one synthetic pair with
no repetition, graded by the same vendor and model family as the arms. It is a smoke test, not a
promotion claim: the record's limitations list applies, and real task artifacts, actual consumption
and independent regrading remain required. The 2026-09-06 reviewer-reported attempt, the v1 record
and the frozen packet bytes are unchanged.


## Replication with isolated grading — 2026-09-16

Ten pairs of the same frozen packet were executed on the same surface (CLI **2.1.273**, headless,
`claude-sonnet-5`), with arm order counterbalanced and **each output graded in its own grader
process** seeing only the rubric and that one output. The
[replication record](attempt-20260916-replication.json) holds every call's timestamps, deadline,
working directory, exit status, usage, cost and verbatim grader prose; the graded outputs and the
harness are in [attempt-20260916-replication-outputs/](attempt-20260916-replication-outputs/).

**No advantage demonstrated.** Baseline mean 3.75, candidate mean 3.80; paired difference +0.05
spanning zero on both a normal (z) and a t(9) interval — [-0.179, +0.279] and [-0.214, +0.314]. Five pairs tied, three
favoured the candidate, two favoured the baseline; no call was indeterminate.

The single pair's one-point gap recorded above **was not reproduced consistently**. That run docked
the baseline 0.5 on check 1 and 0.5 on check 4. Across ten isolated gradings the baseline scored 1.0
on check 1 in all ten, and 0.5 on check 4 in 5 of 10. These observations are consistent with
grading-procedure differences and within-arm variation. Because the replication also used newly
generated outputs, it does not isolate those causes or exclude a presentation effect; the original
gap cannot be reliably attributed to the handoff presentation.

**The rubric is saturated.** Checks 1-3 scored 1.0 for both arms in all twenty gradings. Only
check 4 varies, and it varies within each arm. On this scenario and model the instrument has
effectively one discriminating check, and that check is noise-dominated, so this smoke test cannot
detect a small effect in either direction. A scenario with headroom is required before any
comparison here can support a promotion decision. The 2026-09-06 reviewer-reported attempt, the
2026-09-16 executed pair, the v1 record and the frozen packet bytes are unchanged.


## Leak-free replication — 2026-09-17

Review found a generation-side defect in both 2026-09-16 harnesses: each arm ran in a directory named
after its own arm, and the headless CLI places the working directory in the model's context. Verified
on CLI 2.1.274 — a `-p` call with no tools returns its own cwd verbatim — so every generating call
could read a word naming its arm. Grader blinding was never affected.

The harness now names every call's directory with an opaque random token and the trial was re-run.
The [2026-09-17 record](attempt-20260917-replication.json) carries the correction, the per-call
tokens and the full evidence; the 2026-09-16 numbers stand as recorded, with the leak noted.

**No advantage demonstrated after correcting the harness.** Baseline mean 3.90, candidate 3.85, paired difference
**-0.05**, spanning zero on both a normal interval [-0.2259, +0.1259] and a t(9) interval
[-0.2530, +0.1530]. Seven pairs tied, two favoured the baseline, one the candidate. The difference
changed sign and the paired sd fell from 0.369 to 0.284. These are descriptive comparisons, not
evidence that the leak had no effect: random variation and the changed CLI build prevent isolating
its contribution. **Saturation reproduced in the leak-free run**: checks 1-3 again scored 1.0 for both arms
in all twenty gradings. The two runs share the frozen scenario, the rubric, the model family and
the grader family, so this is a second execution on a corrected harness and a different CLI build,
not an independent replication. Note the CLI build differs (2.1.273 then, 2.1.274 now), so this is not a
same-condition replication.
