---
schema_version: 1
kind: spec
id: S-001
status: draft
owner: "<author/session>"
updated: YYYY-MM-DD
---

# <Behavior to deliver>

<!-- Optional pilot template. Use an existing spec if it supplies the same information.
     Status: draft | accepted | superseded. Acceptance names a human decision owner.
     Give the next consumer a commit/blob hash or content digest; a path alone is not a revision. -->

## Intent and boundaries

Problem, affected users, desired outcome and explicit exclusions. Link existing background.

## Acceptance criteria

| ID | Observable behavior / failure case | How it can be checked |
|---|---|---|
| AC-001 | <given a situation, observable expected result> | <test, runtime observation or human criterion> |

## Decisions and constraints

Interfaces/data changes and significant alternatives. Link ADRs instead of repeating them.
Record relevant performance, security, accessibility, migration or operational requirements;
omit categories unrelated to the task.

## Open decisions

| Question | Decision owner | Blocks which criterion? |
|---|---|---|
| <unresolved decision, or None> | <owner> | <AC-ID> |

## Acceptance

Decision owner, decision/date and the exact accepted revision. Drafting or reviewing this file
does not itself accept the product requirements. Keep a content-digest acceptance record outside
the bytes it covers (for example in an issue or handoff), or reference an earlier immutable Git
revision; a file cannot contain its own full-file digest.
