---
name: hr-tdd
description: Build or fix behavior test-first with a red-green loop. Use for explicit TDD requests, regression fixes, or integration-test work.
---

# Test-first development

Start from the requested behavior, the project's existing tests and relevant CONTEXT.md/ADRs
when present. Identify the public interface and expected observable result. Reuse a seam already
established by the task or tests; ask only if choosing a different interface changes the scope.

## One vertical slice at a time

1. Choose one observable behavior and a known expected result from the requirement or a worked
   example. Avoid expectations computed by repeating the implementation.
2. Write one test through that public interface. Run it and confirm it fails for the intended
   missing behavior, not an import, environment or fixture error. Capture the command and failure.
3. Implement only enough to satisfy that behavior. Run the same test and observe it pass.
   If the completed slice needs refactoring, preserve its observable behavior and rerun the
   covering tests after the change. Refactoring is optional and stays within the agreed scope.
4. Repeat for the next relevant behavior. Do not write a batch of speculative tests before the
   first implementation. Keep unrelated refactoring out of the loop.
5. Run relevant regression checks. Propose broader refactoring separately; do not turn a small
   fix into an architecture redesign.

Read [tests.md](tests.md) for boundary-focused examples and [mocking.md](mocking.md) when choosing
what to isolate. Internal-call expectations and implementation-shaped assertions are poor evidence.
If no meaningful automated test is possible, record the constraint and actual alternative check;
do not label an unexecuted scenario red/green.

## Result

Report the behavior, the observed red and green checks, remaining gaps and exact changed target.
When work crosses sessions, use the project's existing record or the installed
`.houserules/work/verification.md` template if selected. Create only the record the next consumer
needs. No external tracker, other skill or subagent is required.

Source and adaptation details: [NOTICE.md](NOTICE.md).
