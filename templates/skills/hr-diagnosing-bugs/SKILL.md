---
name: hr-diagnosing-bugs
description: Diagnose a reported bug or performance regression using a reproducible feedback loop, falsifiable hypotheses and a verified fix.
---

# Diagnose with a feedback loop

Use the reported symptom as the acceptance condition. Read relevant project context and standards,
then establish a signal that can distinguish this bug from a healthy result before changing code.

## Establish the signal

Prefer a failing test at the real caller boundary. Otherwise use a small HTTP/CLI replay, captured
input or minimal harness. Run it and record the exact symptom. Missing dependencies are setup
failures, not proof of the reported bug. Tighten slow or noisy loops; for intermittent bugs record
the seed, trial count and failure rate instead of claiming a deterministic reproduction.

If access or evidence is insufficient, record what was attempted and the specific missing input.
Do not claim a root cause or invent a successful reproduction. Ask for the missing information
when it blocks further useful investigation.

## Isolate the cause

- Minimize inputs one change at a time while keeping the failure. Avoid cutting away the actual
  interaction that triggers it, such as multiple callers or a timing dependency.
- State plausible hypotheses and a prediction that would disprove each. Use as many as the
  uncertainty warrants; do not manufacture alternatives for an already localized failure.
- Probe one variable at a time using debugger inspection or narrowly tagged instrumentation.
  For performance, measure a baseline and compare like-for-like workloads.
- Show the causal evidence, not only the first plausible code smell. Do not expose secrets in
  requests, logs or generated records.

## Fix and verify

Turn the reproduction into a regression at the actual failure boundary before fixing it. Confirm
red, apply the minimal change, confirm green, then rerun the original scenario and relevant
regressions. If a suitable test boundary is absent, report that limitation explicitly.

Remove only instrumentation introduced for this task and only within authorized paths. Respect
repository cleanup policy; retain clearly identified debug artifacts when removal is not allowed.
Record the cause, target revision, commands/results and unresolved limitations. For cross-session
work, use existing project records or selected `.houserules/work/findings.md` and
`verification.md` templates. A proposed fix is not a verified finding disposition.

This adaptation requires no Bash harness, tracker or other skill. Human interaction is needed only
when the chosen reproduction actually depends on it. [Source and changes](NOTICE.md).
