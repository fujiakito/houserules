# Evaluation harness

`runner.py` executes a frozen baseline-vs-candidate comparison and records revision-bound evidence.
It exists to serve criterion 5 of the
[fallback admission criteria](../../research/PORTABILITY.md#fallback-admission-criteria), which is
recorded there as open: this project ships four `hr-` skills with no comparative evidence.

The requirements it implements were written before it existed, in
[prior-art/v2](../workflows/prior-art/v2/README.md) § *Next execution requirements*. The arm design
and the refusal conditions come from [prior art](../../research/PRIOR-ART-EVAL-HARNESSES.md).

**This directory is distribution-only.** It is never copied into an adopting project, carries no
entry in `check.ASSET_PATHS`, and has no `__init__.py`, so `python -m unittest discover -s tests`
does not descend into it. Its regression tests live in [`../test_eval_runner.py`](../test_eval_runner.py).

## What a run establishes, and what it does not

Bounded attempts, deadlines and spend are **usage control, not a sandbox** — the same distinction
`SECURITY.md` draws for `workflow.py run`. The runner does not restrict what the provider CLI may
do, and it cannot prove that CLI honoured the isolation flags it was passed.

A recorded attempt is evidence about the named surface and version only. It is not promotion, not
semantic acceptance, and not a claim that a skill was natively discovered or loaded: the candidate
arm supplies the skill body as prompt text, so it measures the instruction text. Every attempt
record carries these as `limitations[]` entries rather than leaving them to a reader.

## Commands

```bash
python tests/eval/runner.py verify --case tests/workflows/skill-eval/<case>
python tests/eval/runner.py plan   --case tests/workflows/skill-eval/<case> \
       --runner claude --model <pinned-id> --trials 3
python tests/eval/runner.py run    --case tests/workflows/skill-eval/<case> \
       --runner claude --model <pinned-id> --trials 3 --max-usd 4.00
python tests/eval/runner.py grade  --case tests/workflows/skill-eval/<case> \
       --attempt attempt-<date>-claude                 # emits blind/
python tests/eval/runner.py grade  --case tests/workflows/skill-eval/<case> \
       --attempt attempt-<date>-claude --scores scores.json --grader <name> --blinded
```

`verify` and `plan` need no provider CLI and make no network call. `run` spawns one.

## What it refuses, and why

| Refusal | Reason |
|---|---|
| A frozen input whose bytes no longer match `case.json`'s `frozen_sha256`, naming the file | An arm that differs from another in more than the declared variable yields a number that looks like a result and is not one. This is the failure behind this repository's R-003/F-001 finding and behind upstream ponytail's contaminated baseline |
| A runner with no `--model` | Isolation drops the operator's saved model, so without a pin the comparison silently runs whatever the operator or the CLI release defaults to, and per-token cost varies with it |
| No `--max-usd` | Refusal is pre-execution; nothing is created |
| More unmetered completed cells than `--allow-unmetered-cells` (default 0) | An unreportable cost is unknown, and unknown is not free. A matching `limitations[]` entry is appended automatically |
| `--timeout-seconds` above the deadline `case.json` records | Raising a deadline until the score improves is not a control |
| An existing `attempt.json` without `--resume` | Existing work is never replaced — `workflow.py`'s posture |
| A resume whose inputs changed since the recorded attempt | Same reason as the first row |

Isolation is **not caller-settable**. `RUNNERS` fixes one profile per surface — `claude`:
`--setting-sources ""`, `--strict-mcp-config`, `--tools ""`; `codex`: `--ignore-user-config`,
`--ephemeral`, `--sandbox read-only`, `--skip-git-repo-check` — recorded verbatim in the attempt.
This repository installs an always-on `AGENTS.md` workflow block; without those flags it reaches
the baseline arm and the comparison measures the skill against itself.

## Outcomes

A cell is `completed`, `failed`, `timeout` or `blocked`. An attempt is `completed` only when every
planned cell completed; anything else is `indeterminate`. A timeout retains whatever partial output
the process produced and is recorded as indeterminate, **not** as a diagnosed defect.

Unknown values are `null`. Never `0` — a zero cost reads as free, and an absent cost is not free.

## Reading a record next to the older ones

`schema_version: 2` extends the reviewer-reported record at
[`prior-art/v2/attempt-20260906-reported.json`](../workflows/prior-art/v2/attempt-20260906-reported.json).
The `_reported` suffixes there (`status_reported`, `elapsed_seconds_reported`, `usage_reported`,
`score_reported`) are a **provenance marker** meaning a reviewer supplied the value. Fields this
harness measures itself drop the suffix (`status`, `elapsed_seconds`, `usage`, `score`). Both
spellings may appear in one corpus; that is the point, and it is what lets v1, v2 and harness
records be read side by side under one schema.

Added by this schema: `case`, `case_dir`, `harness{path,sha256}`, `isolation{profile,flags}`,
`budget{max_usd,spent_usd,cost_source,allow_unmetered_cells}`,
`blinding{method,group_key_template,judge_marker,revealed}`,
`grading{grader,blinded,rubric_sha256,graded_utc}`, and per-cell `trial`, `output_sha256`,
`cost_source`, `score_breakdown`.

## Blinding

Grading is done by a person against the frozen rubric — there is no model judge. `grade` without
`--scores` writes `blind/`: the rubric's judge span, and each completed response relabelled
`trial-<n>-response-<LABEL>.md`.

`blind_labels` ranks arms by `sha256(group_key + b"\x00" + arm)` and assigns labels in rank order.
Deterministic rather than random, so a resumed run reproduces its labels; it raises on a digest
collision rather than dropping an arm. `group_key` is `{case}|{trial}|{runner}|{model}`, and **only
the group key is written to the record before grading** — the mapping is recomputed by `grade`, so
a grader can hold the packet and the record without holding the answer.

The rubric's gradable checks sit between `<!-- judge:begin -->` and `<!-- judge:end -->`; only that
span reaches the blind packet. Gate wording names the arms, so sending a whole rubric would leak
the vocabulary the blinding exists to hide. A rubric with no markers is emitted whole and recorded
as `judge_marker: false` — the frozen `prior-art/` rubrics are not retrofitted.

Structural blinding is not independence. `grading.blinded` records only that labels were hidden; a
`limitations[]` entry records that the grader is a project participant.

## Case layout

```
tests/workflows/skill-eval/<case>/
  README.md              # the dated record: hash table, arms, gate, outcome
  case.json              # manifest, including frozen_sha256 for every input
  task.md                # frozen
  arm-<name>.md          # frozen; task.md verbatim plus exactly one treatment block
  rubric.md              # frozen; judge markers around the gradable checks
  attempt-<date>-<runner>/
    attempt.json  cell-<arm>-<trial>.out  cell-<arm>-<trial>.err  blind/
```

Frozen inputs need a `-text` line in `.gitattributes`, or checkout normalisation invalidates their
recorded SHA-256. Attempt files are generated, not frozen, and stay under the global `eol=lf`.
`CONTRIBUTING.md` applies: append a new dated attempt; never edit a recorded one.
