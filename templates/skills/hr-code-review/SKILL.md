---
name: hr-code-review
description: Review a specified code change against project standards and intended behavior, including explicitly scoped uncommitted or untracked changes.
---

# Review on two axes

Keep **Standards** and **Spec** findings separate: a change can satisfy one and fail the other.
Review by inspection and relevant checks; do not edit the implementation unless asked to fix it.

## Pin the target

Resolve the requested base and target. For committed branch work use its merge-base comparison;
for working-tree work record staged, unstaged and untracked inclusion explicitly and inspect
untracked contents too. A branch name alone is not immutable evidence. Record commit/blob IDs
or content digests. Ask for scope only when it cannot be established from the request/context.
Report an empty diff or invalid reference before inventing review findings.

## Gather criteria

Use the user's supplied intent, issue or local spec. Follow an existing configured tracker only
when needed and available; do not require a tracker account or setup skill. If intent is missing,
state that the Spec axis is limited or blocked while completing useful Standards inspection.
Read applicable repository instructions and coding standards; do not invent a universal standard.

## Standards

Identify concrete violations with a file/location and the relevant documented rule. Possible code
smells (unclear naming, duplicated logic, feature envy, scattered changes, speculative abstraction)
are judgment calls, not automatic defects. Explain their actual consequence in this change and
respect documented project tradeoffs. Skip style issues already handled by existing tooling.

## Spec

Check missing or partial requirements, behavior outside scope, and implementations that appear
present but produce the wrong result. Tie findings to observable examples and criterion references.
Inspect regression coverage at the behavior boundary. Missing execution evidence is a limitation,
not proof that a test would fail or that it passed.

## Report

Report Standards and Spec separately, each with severity, target location, evidence and a useful
next action. Say no findings where appropriate. Disclose self-review/shared context; sequential
review is supported, and independent sessions may be used when available and warranted. No
parallel agents are required. Do not equate different owner names with independence.

Use the project's severity scale; when using the selected `.houserules/work/findings.md` template,
follow its vocabulary. If neither provides a scale, define the labels in the report by consequence.

For durable work, use the existing project record or selected `.houserules/work/review.md` and
`findings.md` templates. Append a new round for a changed target; do not carry forward the old
pass without reassessment. A review does not authorize commit, publishing or release.

[Source and adaptation details](NOTICE.md).
