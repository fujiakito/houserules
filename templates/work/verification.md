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

## Outcome

pass | fail | blocked

List unresolved risks, skipped checks and what evidence would resolve them. Append finding
dispositions in findings.md; the fixer's claim alone is not verification.

## Next consumer

Who acts next, on which artifact revision, and what they must establish.
