# hr-tdd-01: does the hr-tdd procedure change what gets produced?

Prepared 2026-09-15. **Not run.** No attempt record exists yet, and no claim is made about
`hr-tdd`.

The question is narrow: given one small task with an obvious over-build trap and an obvious
wrong-failure trap, does supplying the `hr-tdd` procedure change the produced red test, the stated
failure and the implementation — relative to no procedure, to a length-matched generic procedure,
and to a one-line instruction?

This serves [criterion 5](../../../../research/PORTABILITY.md#fallback-admission-criteria), which
`PORTABILITY.md` records as open. `hr-tdd` is the target because that file already names it:
*"Start a future trial with hr-tdd as a bounded test-design experiment."* The arm design comes from
[prior art](../../../../research/PRIOR-ART-EVAL-HARNESSES.md); the runner is
[`tests/eval/runner.py`](../../../eval/README.md).

## The instrument

Prompt-only, no tool use, reusing the configuration the
[v2 packets](../../prior-art/v2/README.md) used. The task shows a module and its existing test file
inline and asks for four things as text: the new test, what it does when run against the code as
given and why, the change that makes it pass, and anything the responder could not establish.
Nothing is executed by the responder, so the graded object is the reasoning, not a test run.

The task has two traps a procedure could plausibly help with. The requirement says a rejected
spend must leave the ledger *exactly as it was*, so a test that only asserts the refusal misses
half the requirement; and `spend()` has a documented return value that a careless fix silently
changes.

## Arms

Four arms, **byte-identical except one block**. Each treated arm is its treatment, then `\n---\n\n`,
then `task.md` verbatim. `arm-baseline.md` is `task.md` and nothing else — which is why its digest
below equals `task.md`'s, and that equality is the control, not a coincidence.

| Arm | Treatment | Bytes |
|---|---|---:|
| `baseline` | none | 1,470 |
| `candidate` | `templates/skills/hr-tdd/SKILL.md` body verbatim, with its `tests.md` and `mocking.md` inlined because the arm has no tools to follow their links | 7,142 |
| `control-length` | A generic slice-and-report procedure with the test-first content removed, matched to the candidate treatment's length (5,469 vs 5,666 bytes, ratio 0.965) | 6,945 |
| `one-line` | *"Write the failing test first, then the minimal implementation."* | 1,539 |

`control-length` separates "this procedure works" from "more instructions work". `one-line`
separates it from "one sentence would have done". Upstream ponytail ran both controls and the
second one materially changed its conclusion.

## Frozen inputs

SHA-256 covers exact file bytes, including line endings. `.gitattributes` pins these paths with
`-text` so checkout normalisation cannot invalidate the table.

| Input | SHA-256 |
|---|---|
| arm-baseline.md | `cfd03f6b88e38ef4c11c7b138c3f6d338d8b30c7ee9ce23467a34cbc173988b7` |
| arm-candidate.md | `6caf1f2b5aa7182d8a9b4aa093c874bd8928e425145429268547c8d089c7c441` |
| arm-control-length.md | `810d20223138213e17b4d58e9e5d1f1282af26ec5e11da3d99f589a11012477b` |
| arm-one-line.md | `ba8b782c2f34cef43b397222e86ba690be9648513fcbfe08df559aacf6a56400` |
| rubric.md | `5263d08157dac0f5df32c556b3a7a245309ff767fa6cd0bb73471f3a34430bdd` |
| task.md | `cfd03f6b88e38ef4c11c7b138c3f6d338d8b30c7ee9ce23467a34cbc173988b7` |

`case.json` carries the same table as `frozen_sha256`. The runner refuses to execute when any entry
drifts, and `tests/test_eval_runner.py` recomputes them on every test run, so an edited packet
fails the gate rather than silently changing what a recorded attempt measured.

## Scoring

[`rubric.md`](rubric.md), frozen before any output was read, weighted **against** the candidate: a
correct account of the failure carries 35 and public-interface behaviour 25, while concision — the
thing extra instructions most easily buy — carries 10. Process indicators score nothing.

Grading is done by a person against the judge span, with `runner.py grade` relabelling responses
first. The release gate (G1–G4) is stated at the foot of the rubric, outside the judge markers,
because it names the arms.

## Execution requirements

Inherited from [prior-art/v2](../../prior-art/v2/README.md) and enforced by the runner: a 300-second
per-arm deadline as a chosen budget, not a proven sufficient one; partial output retained on
timeout and recorded as indeterminate; an explicit model pin; the fixed isolation profile; a
required spend ceiling; unknown usage recorded as `null`, never `0`. Do not raise the deadline to
obtain a score — the runner refuses it.

```bash
python tests/eval/runner.py verify --case tests/workflows/skill-eval/hr-tdd-01
python tests/eval/runner.py plan   --case tests/workflows/skill-eval/hr-tdd-01 \
       --runner claude --model <pinned-id> --trials 3
python tests/eval/runner.py run    --case tests/workflows/skill-eval/hr-tdd-01 \
       --runner claude --model <pinned-id> --trials 3 --max-usd 4.00
```

Three trials over four arms is twelve cells on one surface with one model. That is enough to record
a result and not enough to support a small difference: read a per-case gap below roughly half a
rubric band as noise, and expect the honest outcome to be "no measurable advantage" or
indeterminate. Criterion 5 asks for evidence, not for a win.

## Limitations, before any attempt exists

- The candidate arm supplies the skill body as prompt text. It measures the instruction text, not
  skill discovery or native invocation; files on disk are not evidence of a loaded capability.
- One surface, one model. `codex` was unavailable where this case was prepared, so a first
  attempt will be single-surface evidence and must be labelled as such.
- Prompt-only. A procedure whose value lies in iterating against a real test runner is not being
  given its best conditions here; a tool-using case is separate work.
- The grader is a project participant. Structural blinding hides labels; it is not independence.
