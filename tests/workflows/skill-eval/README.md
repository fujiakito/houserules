# Skill evaluation cases

Dated comparison records produced by [`tests/eval/runner.py`](../../eval/README.md). Each case
answers one narrow question about one shipped `hr-` skill, on a named surface and version.

These exist to serve
[criterion 5](../../../research/PORTABILITY.md#fallback-admission-criteria) — comparative evidence
— which `PORTABILITY.md` records as open. Until a case records a passing gate, that criterion stays
open and no skill is promoted.

| Case | Skill | Question | State |
|---|---|---|---|
| [hr-tdd-01](hr-tdd-01/README.md) | `hr-tdd` | Does the procedure change the produced red test, the stated failure and the implementation, against no procedure, a length-matched generic procedure and a one-line instruction? | Prepared 2026-09-15, **not run** |

## Rules

Each case freezes its inputs. `case.json` carries `frozen_sha256` for every packet and the rubric;
the runner refuses to execute on drift, and `tests/test_eval_runner.py` recomputes the table on
every test run. `.gitattributes` pins each frozen path with `-text`.

Arms are byte-identical except one treatment block, and a test asserts it: every arm file ends with
the exact bytes of that case's `task.md`. This is the control that
[R-003 / F-001](../prior-art/v2/README.md) was raised about, mechanically enforced rather than
reviewed.

Attempt directories are generated output, not frozen. Per `CONTRIBUTING.md`, **append a new dated
attempt; never edit a recorded one.** A later attempt supersedes an earlier one for the revisions it
names; the earlier one stays as historical evidence of what was tried.

A recorded attempt is evidence about the surface and version it names. It is not promotion, not
semantic acceptance, and not evidence that a skill was natively discovered or loaded — the
candidate arm supplies the skill body as prompt text. [ENFORCEMENT](../../../docs/ENFORCEMENT.md)
holds the full limits row.
