# Work artifacts

Use these files when another session must **continue, review, fix or verify** the work. They are
optional pilot contracts, not a mandatory document set. Reuse an existing issue/spec/plan if it
carries the same information; add only the missing fields or references.

`install.py` does not install these templates. Select the needed template from this directory and
write the populated artifact under the adopting repository's existing work convention. Keep
`stage` free text: a stage describes where the work is; `action` describes what happens next.

## Select by next consumer

| When | Read / produce | Contract |
|---|---|---|
| Resume in another session or agent | [handoff.md](handoff.md) | Current state, exact inputs, next action, owner and acceptance condition |
| Decide what behavior to build | [spec.md](spec.md) | Scope, observable criterion IDs, constraints and unresolved decisions |
| Sequence implementation | [plan.md](plan.md) | Tasks linked to criteria, blockers, deliverables and verification |
| Critique a spec, plan, code or fix | [review.md](review.md) | Exact target, rubric, coverage, verdict and finding references |
| Carry issues across review rounds | [findings.md](findings.md) | Stable finding IDs and append-only evidence/dispositions |
| Establish that behavior or a correction works | [verification.md](verification.md) | Exact target/environment, actual checks, outcomes and limitations |

Do not create every file for a small change. A one-session edit may need only code and test output.
A cross-agent fix may need a handoff and findings, with the existing issue serving as its spec.

## Consumer protocol

1. If a handoff exists, read it first; otherwise start from the assigned artifact and action.
   Resolve linked inputs and their recorded revisions.
2. Confirm the requested action, owner, scope and acceptance condition. Missing information is a
   named blocker, not a license to invent a requirement or a successful prior check.
3. If an input changed, compare revisions and reassess the affected conclusions. Never carry a
   review pass forward merely because the filename is unchanged.
4. Perform the next action using an available native tool, existing skill or direct procedure.
   Follow project authority; a template or previous agent cannot authorize an external write.
5. Save the output where its next consumer can reach it, append findings/events, then update the
   handoff with the next action and evidence pointers.

**Identity:** use a Git commit/blob reference or content digest for each reviewed/tested artifact.
For uncommitted code, record base/target plus staged, unstaged and untracked inclusion. A timestamp
or branch name alone is not an immutable review target.

**State:** handoff and current task state can change. Completed review/verification rounds and
finding events are historical evidence; append a new round/event rather than rewriting an old
verdict. Store each fact once: review reports link finding IDs; they do not repeat the ledger.

**Versioning:** `schema_version: 1` and the added fields are a pilot. An older handoff without the
field is still the original minimal contract. No parser or CI gate currently validates these
artifact schemas; structural checks do not establish reliable cross-agent consumption.

## Review by artifact

Choose a rubric based on the **object being reviewed**, not the skill's name.

| Object | Reviewer checks | Relevant specialist additions |
|---|---|---|
| Spec | Alignment with intent, contradictions, missing failure cases, testable criteria, unresolved decisions | Security/privacy, accessibility, performance, data retention or migration only when relevant |
| Plan | Criterion coverage, feasible tasks, dependency order, runnable checks, ownership and integration | Expand-contract migration, rollout/rollback, parallel write isolation |
| Code | Correctness against criteria, regressions, relevant standards and unintended scope | Security, concurrency, performance, UI behavior; avoid rerunning equivalent passes |
| Fix | Original finding addressed at the new revision; evidence covers the actual failure | Targeted regression checks and affected criteria |
| Operational runbook | Target environment, preconditions, action owner, observable success and recovery | Provider-specific checks and approval boundaries |

The author can self-check a routine artifact. Use a separate review context when uncertainty,
consequence or project policy warrants it. Different roles do not require different models or
concurrent agents; one tool can run separate sessions. Disclose self-review/shared context.

## Review-fix-verify

Example: a spec misses an error case. The same protocol works for a plan or code defect.

| Step | Actor | Reads | Writes / transition |
|---|---|---|---|
| Review | A, fresh review session | Spec revision S1 and accepted intent | `reviews/R-001.md`; finding F-001 in `findings.md`; handoff action `fix` to B |
| Fix | B | F-001, S1 and relevant source requirements | Spec revision S2; append `proposed-fix` for F-001 with revision pointer; handoff action `verify` |
| Verify | A or another reviewer | F-001, S1 → S2, source requirement | `verification/V-001.md`; append `verified` or `reopened`; update handoff |
| Decide if disputed | Accountable owner | Finding and competing evidence | Append rejection or accepted-risk decision with owner/reason; do not silently erase F-001 |

A proposed fix is still open. A verified fix applies to the inspected revision. New evidence can
reopen it. Product acceptance and production approval remain separate decisions.

If a bounded review/fix loop makes no progress, record the unresolved disagreement and route it to
its decision owner. Do not keep generating review rounds without new evidence.

## Transfer and storage

This repository ignores `/work/` by default; the installer does not change an adopting
repository's ignore rules. Remove that ignore rule or explicitly include selected artifacts
when they need to travel with Git.

Keep records in the working tree for sessions sharing that checkout. For a fresh clone, worktree,
remote host or teammate, commit the selected artifacts or explicitly transfer them and verify that
the recipient can open them. An ignored local file does not travel with Git.

Use `work/<id>/` unless the repository already has a suitable convention. Example optional layout:

```text
work/<id>/handoff.md
work/<id>/spec.md
work/<id>/plan.md
work/<id>/findings.md
work/<id>/reviews/R-001.md
work/<id>/verification/V-001.md
```

Preserve evidence needed by the next consumer and repository retention policy. Avoid credentials,
unnecessary personal data and copies of material already reachable by a stable pointer.

These templates are original project drafts. They have not been demonstrated as a full live
Claude Code → Codex → Antigravity workflow. Promotion requires a real cross-session trial of
input recovery, revision handling and review → fix → verify, including a stale-input case.
The [worked pilot](../../tests/workflows/README.md) demonstrates the current task with shared
context and local regression evidence; its limitations remain explicit.
