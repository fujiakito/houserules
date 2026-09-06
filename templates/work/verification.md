---
schema_version: 1
kind: verification
id: V-001
status: draft
owner: "<verifier/session>"
updated: YYYY-MM-DD
---

# Verify <behavior or correction>

<!-- Optional pilot template. Save completed runs separately, e.g. verification/V-001.md.
     Status: draft | complete. A test run completing is distinct from its outcome passing. -->

## Target

Artifact/code revision or content digest; reviewed source revision; relevant task, criterion,
review and finding IDs. Include working-tree scope when the target is not committed.

## Environment

Agent surface/version, runtime/tool versions, cwd, relevant fixtures and setup.
Describe secret locations only; redact secret values from commands, logs and artifacts.

## Evidence

| Criterion / finding | Command or inspection | Expected result | Actual result | Evidence |
|---|---|---|---|---|
| AC-001 / F-001 | <exact command or document comparison> | <observable condition> | pass / fail / skipped | <log, artifact or cited source location> |

For a bug fix, include the original reproduction and relevant regression checks.
For a spec/plan correction, inspect the changed clause against the source requirement; do not
substitute a software test for a document-level decision.

## Resource use (optional)

Use for costly runs or comparisons; omit for a small routine check. Record the budget before
execution, then actual use. This is a record, not an enforced spending cap.

| Field | Value |
|---|---|
| Budget / stop condition | <time, model attempts or observable allowance; agreed scope> |
| Model / effort / billing mode | <configured and observed, or unknown; subscription/API/credits> |
| Attempts / elapsed time | <include failed attempts; define wall time versus summed worker time> |
| Usage / source / scope | <raw token or credit fields and log reference; per-turn/session/account> |
| Money | <observed amount and currency, separately labelled estimate, or unknown> |
| Limit snapshots, if used | <timestamps, window/reset times, before/after, other activity unknown/known> |

Preserve the producer's field semantics: do not add cached/reasoning subcounts to totals unless
the format defines them as separate. Deduplicate cumulative snapshots. Missing counters stay
unknown. Never convert subscription percentages into tokens or money. Compare task outcomes
alongside usage; failed or blocked attempts do not disappear from the comparison.

## Outcome

pass | fail | blocked

List unresolved risks, skipped checks and what evidence would resolve them. Append finding
dispositions in findings.md; the fixer's claim alone is not verification.

## Next consumer

Who acts next, on which artifact revision, and what they must establish.
