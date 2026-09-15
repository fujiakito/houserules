# hr-tdd-01 rubric

Frozen before any output was read. Grade semantically. Naming a procedure, quoting it, reusing its
headings or announcing which method is being followed earns nothing: those are process indicators,
and a process indicator is not the outcome. Score only what the response actually produced.

Everything outside the judge markers below is for the maintainer, not the grader. The release gate
at the foot of this file names the arms, and sending it to a blind grader would leak the vocabulary
the blinding exists to hide.

<!-- judge:begin -->
Score the response from 0 to 100 by adding the five weighted checks below. Judge only what is
written; nothing was executed, and no response had tools.

| # | Check | Weight |
|---|---|---:|
| 1 | The stated failure is correct: run against the code as given, the new test fails because the over-cap spend is recorded rather than refused. Not an import error, not a fixture or environment error, not a syntax error. A response that predicts the wrong failure, or is vague about which line fails, scores low here | 35 |
| 2 | The new test reaches the behaviour through the public interface. It observes the refusal **and** that the balance is unchanged afterwards, using the documented methods. Reading or asserting on a private attribute, or on an internal call, scores low | 25 |
| 3 | The code change is the smallest one that satisfies the stated requirement. Extra configuration, new abstractions, unrequested logging, or a broader redesign score low. A change that fixes the requirement but silently alters the existing documented return value also scores low | 20 |
| 4 | The response is honest about what it did not do. It does not claim to have run anything, and it names what it could not establish | 10 |
| 5 | Length is proportionate to the four items requested. Restating the task, narrating an approach before answering, or repeating the same point in two forms scores low | 10 |

Deduct across every check for anything factually wrong about the code as given.

Record an unavailable or truncated response as indeterminate. Do not score it, and do not retry to
improve a score.
<!-- judge:end -->

## Release gate — maintainer only, not for the grader

The attempt supports a promotion claim only when all four hold:

- **G1** Every planned cell completed. A timeout or a blocked cell makes the attempt
  indeterminate, and no comparison is reported.
- **G2** `candidate` beats `baseline` **and** beats `control-length`. Losing to `control-length`
  means the effect is instruction weight, not this procedure.
- **G3** `candidate` beats `one-line`. A tie is the finding "one line suffices", not "promote the
  skill".
- **G4** Grading was structurally blinded and the grader is disclosed. A non-blinded grade is
  recorded but cannot support promotion.

Passing the gate is evidence for
[criterion 5](../../../../research/PORTABILITY.md#fallback-admission-criteria) on the recorded
surface and version only. It is not promotion, and it does not establish that the skill was
natively discovered or loaded.
