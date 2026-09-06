# Continue, review or verify work

Agent-facing protocol. Read only the record needed for the assigned action. Reuse the project's
existing issue, spec or tracker when it carries the required information; do not create every file.
Copy selected templates into work/<id>/ or the existing project convention. Leave installed originals intact.

## Select by next consumer

| Action | Record | Required information |
|---|---|---|
| Resume | [handoff.md](handoff.md) | Current state, exact inputs, next owner/action and acceptance condition |
| Specify | [spec.md](spec.md) | Scope, criteria, constraints and unresolved decisions |
| Plan | [plan.md](plan.md) | Tasks linked to criteria, dependencies and verification |
| Review | [review.md](review.md) | Artifact/revision, rubric, coverage, findings and verdict |
| Fix findings | [findings.md](findings.md) | Stable IDs and append-only dispositions/evidence |
| Verify | [verification.md](verification.md) | Actual commands/results, target/environment and limitations |

## Consumer protocol

1. Read the handoff if present; otherwise use the assigned artifact/action. Check referenced revisions.
2. Confirm the outcome, scope, owner and authority. Missing facts are named gaps, never invented passes.
3. For work/<id>/workflow.json, run `python .houserules/workflow.py status <id>` before reusing evidence.
   For other records, compare their input and evidence revisions directly. Reassess changed conclusions.
4. Use an available native capability, selected skill or direct procedure. A record grants no new authority.
5. Run the relevant check; preserve actual results and unresolved findings. A successful command is not
   automatically a satisfied task criterion.
6. Save output where the next consumer can reach it. Update the handoff; append completed review,
   verification and finding events rather than rewriting history.

## Bound the work and record usage

The short execution entry at .houserules/START.md owns the budget/retry method. Use its installed
workflow tool for bounded command checks; it records actual elapsed time, attempts and logs.
Keep unavailable tokens/cost unknown. Do not start a new task id to bypass a budget or repeat a
blocked model experiment without a changed precondition. Continue unaffected authorized work.

## Review by artifact

| Object | Check |
|---|---|
| Spec | Intent alignment, contradictions, failure cases and testable criteria |
| Plan | Criterion coverage, dependencies, feasible checks and migration order |
| Code | Correctness, regressions, relevant standards and unintended scope |
| Fix | Original reproduction plus evidence at the corrected revision |
| Runbook | Target environment, preconditions, accountable owner, success and recovery |

Use specialist security/performance/UI review only when relevant. A routine self-review is allowed;
disclose shared context. Equivalent full reviews need new uncertainty or evidence to justify repetition.

## Transfer and storage

Current task state may change; completed evidence is historical. Use commit/blob references or file
digests for targets, including staged/unstaged/untracked scope. Branch names and timestamps alone
are not immutable identities. Workflow hashes cover only explicitly selected files, not the whole repo.

Before moving to a fresh clone, worktree or host, commit or transfer needed work records and logs.
An ignored local work directory does not travel with Git. Preserve user edits and secrets: record
secret locations, never values. Work records remain optional and schema_version: 1 remains a pilot;
workflow.json has its own executable checks and does not validate these Markdown schemas.
