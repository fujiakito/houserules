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
| A resume that would change a recorded setting: runner, model, argv, deadline, `--max-usd`, `--allow-unmetered-cells`, the harness digest or `--trials` | Cells run under two configurations in one record are not one comparison, and the record would still name only the first. Start a new `--attempt` instead |
| A resume or a second `grade --scores` on an attempt already graded | A recorded grade is not overwritten |
| `grade` when a completed cell's output no longer hashes to its `output_sha256` | The grader would score text the record does not describe |
| An `--attempt` that is not one directory name starting with `attempt-` | Keeps every attempt under the `-text` rule in `.gitattributes` |

Isolation is **not caller-settable**. `RUNNERS` fixes one profile per surface — `claude`:
`--setting-sources ""`, `--strict-mcp-config`, `--tools ""`; `codex`: `--ignore-user-config`,
`--ephemeral`, `--sandbox read-only`, `--skip-git-repo-check` — recorded verbatim in the attempt.
The codex flags are taken from the local `codex exec --help` reported in [review.md](../../review.md)
(Codex CLI 0.155.0-alpha.16.4, 2026-09-25); whether each is honoured is not verified here.

The flags alone do not keep project context out. On Claude Code CLI 2.1.282, `claude --help`
(read 2026-09-25) describes `--setting-sources` as selecting *settings* files; `CLAUDE.md`
auto-discovery is a separate behaviour, switched off only by `--bare` (which accepts API-key auth
only) or `--safe-mode`. This repository's own `CLAUDE.md` imports `AGENTS.md`, so a cell run from
the repository would load it into every arm, baseline included. Each cell therefore runs in a
**fresh, empty, system-named temporary directory** outside the repository, removed afterwards; the
record states the policy, not the path. The name matters too: the headless CLI shows the model its
working directory, which is how the 2026-09-16 prior-art runs leaked arm names. User-level context
(a user memory file, for example) is not proven excluded, and a `limitations[]` entry says so.

## Outcomes

A cell is `completed`, `failed`, `timeout` or `blocked`. An attempt records its `plan` when it is
created: every arm the case declares, times `--trials`. `--arm` only chooses which pending cells run
in one invocation. An attempt is `completed` only when every planned cell completed; anything
else, including a run of one arm, is `indeterminate`. A timeout retains whatever partial output
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
`grading{grader,blinded,rubric_sha256,graded_utc}`, `plan{arms,trials}`, and per-cell `trial`,
`output_sha256`, `cost_source`, `score_breakdown` and, when set, `workdir_left_nonempty`.
`working_directory` is the policy string `fresh-empty-system-temp-per-cell`, never a local path.

The blind packet holds the answer only. For `claude` that is the JSON `result`; for `codex` it is
the text of the last `item.completed` event whose item type is `agent_message`, per the event
definitions in `openai/codex` `codex-rs/exec/src/exec_events.rs` (branch `main`, retrieved
2026-09-25). A payload with no extractable answer is emitted raw.

## Blinding

Grading is done by a person against the frozen rubric — there is no model judge. `grade` without
`--scores` writes `blind/`: the rubric's judge span, and each completed response relabelled
`trial-<n>-response-<LABEL>.md`.

`blind_labels` ranks arms by `sha256(group_key + b"\x00" + arm)` and assigns labels in rank order.
Deterministic rather than random, so a resumed run reproduces its labels; it raises on a digest
collision rather than dropping an arm. `group_key` is `{case}|{trial}|{runner}|{model}`, and only
the group key is written to the record before grading; the mapping is recomputed by `grade`.

That hides the mapping from a reader, not from a determined grader: the record names the arms and
the key, and the function is public, so anyone holding the record can recompute the labels. The
attempt directory also holds `cell-<arm>-<trial>.out`, named by arm. **Hand a grader the `blind/`
directory alone**, not the attempt record or directory.

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
recorded SHA-256. Attempt output is hashed too (`output_sha256`, checked again at grading), so
`attempt-*/` directories carry a `-text` rule for the same reason.
`CONTRIBUTING.md` applies: append a new dated attempt; never edit a recorded one.
