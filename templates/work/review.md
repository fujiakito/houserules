---
schema_version: 1
kind: review
id: R-001
status: draft
owner: "<reviewer/session>"
updated: YYYY-MM-DD
---

# Review <artifact or change>

<!-- Optional pilot template. Save each completed round separately, e.g. reviews/R-001.md.
     Status: draft | complete. Do not overwrite a completed round with a later verdict.
     Findings belong only in findings.md; this file indexes them and records review coverage. -->

## Target and criteria

- Artifact type: spec | plan | code | fix | operational runbook
- Target: path/URL + exact revision or content digest
- Code scope, if applicable: base revision, target revision, staged/unstaged/untracked inclusion
- Comparison sources: intent/spec/standards paths and revisions
- Focus: <questions this review must answer>
- Reviewer context: independent session | shared context | self-review
- Prior round: <path/ID or None>

## Coverage

What was actually inspected or executed; what was skipped and why.
Use the relevant rubric in README.md, not a generic demand to review everything.

## Finding references

| Finding | Ledger location | Severity |
|---|---|---|
| F-001 | ../findings.md#f-001 | blocker |

## Verdict

pass | changes-requested | blocked

Explain the evidence for the verdict and its limits. A pass applies to the target above; it
does not approve a changed revision, accept product scope, authorize release, or prove security.

## Next consumer

Fixer/decision owner, finding IDs to handle, and the acceptance condition for re-review.
