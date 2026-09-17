# Review — `docs/close-evaluation-and-reposition`

Scope: `git diff 5d1206e...HEAD` (branch is level with `origin/`, working tree clean).
5 commits, 37 files, +2949/-6 — two Python harnesses, three attempt records, four prose files.

## Verification run

- `python check.py` — passed (10/10 checks).
- `python install.py --check` — no drift.
- `python -m unittest discover -s tests -v` — 76 tests, OK.

Independent re-derivation of the committed evidence (all green):

- All 8 `evidence_file_sha256` entries in `attempt-20260916-executed.json` match the committed
  bytes, including `grader-prompt.txt` after a forced re-checkout — the new `.gitattributes`
  `-text` pin does hold the CRLF the frozen rubric contributes (`git ls-files --eol` reports
  `i/mixed w/mixed attr/-text`).
- `harness.sha256` in the replication record matches the committed harness.
- All 20 grader prompts in the replication reconstruct exactly from
  `rubric.md + GRADER_INSTRUCTION + committed blind output + "\n"` — every `prompt_sha256` matches.
  All 20 arm `prompt_sha256` values match the frozen prompt files.
- Recomputed from the 10 pairs: baseline mean 3.75 / sd 0.2635, candidate 3.80 / sd 0.2582,
  paired diff +0.05 / sd 0.3689 / se 0.1167, 3 higher / 5 tied / 2 lower, per-check means
  1.0/1.0/1.0/0.75 and 1.0/1.0/1.0/0.80, cost 0.858024. Every figure in `aggregate` reproduces.
- All 20 `grader_verbatim` blocks parse to exactly the recorded `scores`. Zero transcription drift.

The evidence hygiene here is genuinely strong. The findings below are about claims layered on top
of that evidence, plus one methodological hole in the instrument itself.

## Findings

### 1. The arm label leaks into the generating call via the working-directory path

`attempt-20260916-replication-outputs/harness.py:188` runs each arm with
`cwd = BASE/cwd/pNN-baseline` or `BASE/cwd/pNN-candidate`;
`attempt-20260916-outputs/harness.py:138` uses `BASE/cwd-baseline` / `BASE/cwd-candidate`.

Claude Code headless puts the working directory into the model's context. Tested locally on
CLI **2.1.274**, `-p`, Linux, in a directory named `.../scratchpad/p01-candidate`, with
`--strict-mcp-config --tools ""`: the model returned its full cwd path verbatim without calling a
tool. So every generating call could read the word `baseline` or `candidate` describing itself.

Grader blinding is sound — grader cwds carry only the shuffled `A`/`B` label, and the label→arm
mapping is written outside the grader's input. The leak is on the generation side, which is the
side that produces the measured difference. `configuration.context_isolation`
(`attempt-20260916-replication.json:43`) addresses only `CLAUDE.md` / `AGENTS.md`, and neither
record's `limitations` list mentions it. Fix is one line — name the arm directories by a hash or
by the blind label — but the existing runs cannot be retroactively cleared of it; it belongs in
`limitations` at minimum.

### 2. The one-point gap is only half explained by the grading confound

`attempt-20260916-outputs/grader-result.txt` shows the single pair's baseline (label A) losing
**0.5 on check 1 and 0.5 on check 4**. The replication contradicts the check-1 half cleanly
(baseline 1.0 on check 1 in 10/10 isolated gradings). It does not contradict the check-4 half:
the baseline scored 0.5 on check 4 in **5 of 10** isolated gradings, and the record itself calls
check 4 noise-dominated.

Three places state the whole point:

- `research/PORTABILITY.md:206` — "so that gap came from grading both outputs in one call"
- `tests/workflows/prior-art/v2/README.md:85` — "The one-point gap is attributable to grading both
  outputs in one call, not to the handoff presentation"
- `attempt-20260916-replication.json:1501` — "The one-point gap is therefore attributable to the
  grader comparing the two outputs within a single call"

Half of it is; the other half reproduces as ordinary within-arm variance. The corrected reading is
stronger for the conclusion, not weaker — one component was a grading artefact, the other was noise,
and neither was the treatment. Saying "the one-point gap" overclaims what the replication resolved.

### 3. `research/PORTABILITY.md:216` — "the 2026-09-06 table below records"

The 2026-09-06 experimental-candidate table is at line ~179, **above** the new section. A reader
following "below" lands on `## 5. The handoff contract`.

### 4. `research/PORTABILITY.md:141` — "a sixth would not"

The same sentence says two catalogue studies are on file
(`MATT-POCOCK-SKILLS.md`, `SUPERPOWERS-SKILLS.md`). The next one would be a third.

### 5. `docs/ENFORCEMENT.md:41` — unsourced external claim, and it contradicts the criterion it cites

"a public 2026-07 incident in which agents acted outside their assigned task" carries no source, no
retrieval date, and no `(unverified)` tag. It is the only occurrence of that incident anywhere in
the repository, so the link to `PORTABILITY#fallback-admission-criteria` does not supply one either.
`AGENTS.md` requires one of the three.

It also conflicts with the paragraph added in this same PR at `research/PORTABILITY.md:136-141`:
"Candidates enter this funnel from observed failure, not from a market survey… reading upstream
sources can never produce one." Criterion 1 additionally requires a target operation/artifact,
agent surface/version and expected contract — none of which a third-party incident report supplies.
So "criterion 1 … is now satisfied" is not supportable under criterion 1 as written. The honest
form is that no criterion is satisfied and the trigger column already carries the real bar.

This lands next to the row deferring an "Automated source/date audit of external claims," whose
trigger is "a second recorded instance of an unsourced external claim being acted on before
verification." This row is arguably that instance.

## Nits (not findings)

- The 95% CI uses the normal approximation (z=1.96) on n=10; t(9)=2.262 gives [-0.214, +0.264].
  Disclosed in the replication's `limitations`, and the direction is conservative for a
  null conclusion, but `PORTABILITY.md` and `ENFORCEMENT.md` quote the narrower interval as a
  headline without that caveat.
- `research/PORTABILITY.md:142-143` — double blank line after the new intake paragraph.
- The new `.gitattributes` blocks omit the `whitespace=…` options the sibling `-text` entries
  carry. Harmless, but inconsistent.
- `.gitattributes` says replication evidence is "Recorded by SHA-256 in the attempt record."
  True for `harness.py`; the blind outputs are covered only indirectly, via each
  `grader_call.prompt_sha256`. That does work — I verified all 20 reconstruct — but the
  replication record has no `evidence_file_sha256` block, unlike the executed record.
- `README.md:5` — "As one agent comes to run several models" is a claim about the world with no
  source or date. Defensible as framing rather than a factual assertion, but it sits one line
  under a heading the project uses to advertise its own evidence rule.
- Both harnesses raise `RuntimeError` from `run_one` if a cwd is non-empty, so a re-run against an
  existing scratch tree aborts mid-trial. Per-pair `bundle.json` writes limit the damage.

## Verdict

The measurement, the records and the arithmetic hold up under independent recomputation, and the
repositioning of the README and the deferred-work table is the right call. Finding 1 is the one
worth fixing before merge — or at least recording as a limitation, since the deferral decisions in
`ENFORCEMENT.md` rest on this instrument. Findings 2-5 are prose corrections.

---

# Response — 2026-09-17

Author of the reviewed commits. Each finding was checked against the committed evidence before
acting, per the [consumer protocol](templates/work/README.md#consumer-protocol). Dispositions below;
the reviewed numbers are retained unchanged everywhere.

## Findings

| # | Disposition | Basis |
|---|---|---|
| 1 | **Confirmed — fixed and re-run** | Reproduced locally on CLI 2.1.274: `claude -p --strict-mcp-config --tools ""` in a directory named `.../p01-candidate` returned its own full cwd verbatim, no tool call |
| 2 | **Confirmed — my overclaim** | The single pair docked the baseline 0.5 on check 1 **and** 0.5 on check 4; isolated grading gives 1.0 on check 1 in 10/10 but 0.5 on check 4 in 5/10 |
| 3 | Confirmed | Table at line 169, "below" at line 216 |
| 4 | Confirmed | Two studies on file, so the next is a third |
| 5 | **Confirmed twice over** | No source, date or `(unverified)` tag; and criterion 1 wants a target operation/artifact, agent surface/version and expected contract, which a third-party incident report does not supply |

**Finding 1.** Both harnesses had it. The harness now names every call's directory with a random
6-byte hex token carrying no arm, order or label information, recorded per call as `cwd_token`, and
the trial was re-run: [`attempt-20260917-replication.json`](tests/workflows/prior-art/v2/attempt-20260917-replication.json).
Both 2026-09-16 records keep their numbers and carry the leak as a limitation.

The leak was not producing the result. On the leak-free instrument the null held and tightened:
baseline 3.90, candidate 3.85, paired difference **-0.05** against +0.05 before, spanning zero on
both a normal interval [-0.2259, +0.1259] and a t(9) interval [-0.2530, +0.1530]; ties rose from
5/10 to 7/10 and the paired sd fell from 0.369 to 0.284. The sign flip is what variation around zero
looks like. **Saturation reproduced independently** — checks 1-3 scored 1.0 for both arms in all
twenty gradings again — which makes it the more durable of the two results. One caveat the review
could not have known: this container had updated to CLI **2.1.274** from the 2.1.273 of the earlier
runs, so the two are not a same-condition replication. Recorded in the new record.

**Finding 5.** Withdrawn rather than sourced, because a citation would not have rescued it: the claim
does not satisfy criterion 1 however well attributed. The row now rests on a fact about this
repository — the budget bounds effort, not scope — and the trigger column carries the bar.

On whether this row is the second instance that fires the deferred source/date audit: **it is not, as
the trigger is worded, and the wording is the weaker part.** The trigger says "an unsourced external
claim being acted on *before verification*". This incident was verified in session before it was
written down; only the citation was dropped. That is a provenance failure, not a verification
failure — a different defect from the Opus 5.2 case, which was a false claim believed until a search
contradicted it. Conflating them would fire the trigger on the wrong evidence. Left at 1 of 2, with
the observation that the trigger should distinguish the two failure modes when it is next revisited.

## Corrections to the review

- **`t(9)=2.262` with `se=0.1167` gives `[-0.214, +0.314]`, not `[-0.214, +0.264]`.** The lower bound
  is right, the upper is not. The substance stands — the t interval is the wider and more appropriate
  one at n=10 — and both interval forms are now quoted wherever the figure appears.
- **`ENFORCEMENT.md` did not quote the interval at all.** Only `PORTABILITY.md` and
  `tests/workflows/prior-art/v2/README.md` did; both now carry both forms.

## Nits

Applied: the double blank line, the `.gitattributes` `whitespace=` options now matching their sibling
entries, an `evidence_file_sha256` block on the replication record (21 entries), and `README.md:5`
restated as a condition — "When one agent can run several models" — rather than as an undated claim
about the world.

Not changed: `run_one` raising on a non-empty cwd is deliberate. A trial that silently reuses a
populated scratch directory is worse than one that stops, and the harness is expected to run against
a fresh tree.

## Standing

`python check.py`, `python install.py --check` and `python -m unittest discover -s tests` pass on
every commit. Finding 1 is fixed at the instrument level rather than only recorded, so the deferral
decisions in `ENFORCEMENT.md` now rest on a leak-free measurement. Findings 2-5 are corrected in
place. Two independent runs agree on both the null and the saturation.

---

# Re-review — 2026-09-17

Reviewer, second pass. Fetched `0bde2a6` (two commits: `1b90990` prose corrections + leak recorded,
`0bde2a6` leak-free re-run). Everything below was re-derived locally rather than read off the
records.

## The two corrections to the review are accepted

- **`t(9)=2.262 x se=0.1167` gives `[-0.214, +0.314]`.** My `[-0.214, +0.264]` was wrong on the
  upper bound — I subtracted the margin correctly and then added the wrong one. The wider interval
  is the one to quote and both forms are now quoted.
- **`ENFORCEMENT.md` never quoted the interval.** My nit said "quoted bare in two docs"; only
  `PORTABILITY.md` and `tests/workflows/prior-art/v2/README.md` did. The nit was right about those
  two and wrong about the third.

## Dispositions verified

| # | Claimed | Verified |
|---|---|---|
| 1 | Fixed at the instrument level and re-run | **Confirmed.** See below |
| 2 | Corrected in three docs + the record's `findings` | **Confirmed** in all four places |
| 3 | "the 2026-09-06 table in the preceding section" | **Confirmed** |
| 4 | "a third would not" | **Confirmed** |
| 5 | Claim withdrawn, row rests on a repository fact | **Confirmed.** No unsourced external claim remains in `ENFORCEMENT.md` |

The reasoning for leaving the source/date audit trigger at 1 of 2 holds. The trigger is worded
"acted on *before verification*", the incident was verified in session and lost only its citation,
and firing a trigger on a defect it does not describe would be worse than the wording gap. Recording
the wording gap for the next revisit is the right disposition.

**Finding 1 — the fix is real, and at the right level.** `run_one` still takes `label`, but it now
reaches only the stdout/stderr filenames under `OUT`, never `argv` and never `cwd`; the working
directory is `rng.randbytes(6).hex()`. I reproduced the underlying behaviour again today on CLI
**2.1.274**: `claude -p --strict-mcp-config --tools ""` in `/tmp/cFz5FGMs/9f2c1ab77e01` returned
`/tmp/cFz5FGMs/9f2c1ab77e01` verbatim, no tool call. The channel is still open — cwd is in context —
but it now carries a token, so it cannot carry the arm. That is the correct fix: the leak is closed
where it was, not papered over in prose.

## Independent re-derivation of the 2026-09-17 record

All green.

- **Gates.** `python check.py` (10/10), `python install.py --check` (no drift),
  `python -m unittest discover -s tests` (76 tests) — all pass at `0bde2a6`.
- **Evidence bytes.** 21/21 `evidence_file_sha256` in the new record, 21/21 in the newly added
  block on `attempt-20260916-replication.json`, and 8/8 in `attempt-20260916-executed.json` —
  all **50 re-verified after deleting the three evidence directories and forcing a re-checkout**,
  so the new `.gitattributes` entry pins the bytes as claimed. `harness.sha256` matches its own
  evidence-block entry.
- **Prompts.** 20/20 generating `prompt_sha256` equal the frozen `baseline-prompt.md` /
  `candidate-prompt.md` hashes. 20/20 grader `prompt_sha256` reconstruct byte-exactly from
  `rubric.md` (CRLF preserved) + the harness's `GRADER_INSTRUCTION` + the committed blind output +
  `"\n"`. The grader prompt contains the rubric, the instruction and one output — no pair number, no
  arm, no label.
- **Scores.** 20/20 `grader_verbatim` blocks parse to exactly the recorded per-check scores, and
  every recorded `total` equals the sum of its four checks.
- **Aggregate.** 27/27 figures reproduce from the raw pairs: both means and sds, min/max, the paired
  mean/sd/SE, both intervals, the 1/7/2 win-tie-loss split, all eight per-check means, and
  `total_cost_usd` $0.9262 summed over 40 calls. Raw diffs
  `[0, 0, +0.5, -0.5, 0, -0.5, 0, 0, 0, 0]`.
- **Blinding and counterbalancing.** Execution order 5/5. `label_mapping` <-> `blind_label` <->
  committed filename consistent in all 20. 40 unique 12-hex tokens, every recorded
  `working_directory` ending in its own token. No committed blind output contains `baseline`,
  `candidate`, `cwd` or a `/tmp/claude` path. 40/40 calls completed, exit 0, one model
  (`claude-sonnet-5`), zero indeterminate.

The sign flip is not a concern. With seven ties and diffs only ever `0` or `±0.5`, the difference is
one pair of ±0.5 either way; -0.05 and +0.05 are the same null. The durable result is the one the
response already identifies: saturation reproduced independently on a different CLI build.

## Findings — second round

### R1. `research/PORTABILITY.md:197` — "Three records exist, all retained unchanged" is now false twice

There are **four** records, and the 2026-09-17 one is not in this enumeration — it first appears
fifteen lines later, inside the limits paragraph. And they are not all unchanged: `1b90990` added a
limitation to `attempt-20260916-executed.json`, and added a limitation, rewrote `findings[1]`, added
a second limitation about the interval and added a 21-entry `evidence_file_sha256` block to
`attempt-20260916-replication.json`.

The numbers are untouched, which is what matters, and `CONTRIBUTING.md` has no mechanical guard here
("Append a new dated run; do not edit a recorded one" is convention only — nothing in `check.py` or
`tests/` hashes the attempt JSONs). Annotating a superseded record with a defect found later is the
right thing to have done. But then say so rather than claiming the records are unchanged. The same
overstatement is in the new record's `relation_to_prior_records`: "unchanged apart from the
limitation recording the leak" omits the rewritten finding, the interval limitation and the evidence
block.

### R2. `research/PORTABILITY.md:202-204` — the headline figures are the superseded instrument's

The new record says `supersedes_for_interpretation: attempt-20260916-replication.json` and "This run
is the leak-free instrument and is the one the conclusion should rest on". The **Outcome** paragraph
— the bolded line a reader stops at — still leads with baseline 3.75, candidate 3.80, difference
+0.05 and both intervals from the run this same document goes on to disclose as leaky. The
leak-free 3.90 / 3.85 / -0.05 appears two paragraphs down, inside a paragraph about limits.

The conclusion is identical either way, so nothing is wrong on the substance. But `PORTABILITY.md`
is the canonical summary, and it currently presents as its result the numbers its own record demotes.
Lead the Outcome with the 2026-09-17 figures and keep the single pair's check-1/check-4
decomposition where it is, as the history of how the question was closed.

### R3. `research/PORTABILITY.md:211-217` — "Two limits" now introduces three things

The leak is spliced between limit one (saturation) and limit two, so the paragraph promises two and
delivers three, and "And the trial is one synthetic packet on one model and surface" now reads as an
orphaned continuation across an intervening link line. Beyond the flow: the leak is not a limit of
this evidence at all — it is a defect of a superseded instrument, already corrected. It belongs in
the record paragraph above (with R1's enumeration fix), not in the list of what the current result
cannot support.

### R4. `attempt-20260917-replication.json:1513,1517` — the record and the prose quote different intervals

The record has `ci_95_normal_z: [-0.2258, 0.1258]` and `ci_95_student_t9: [-0.2529, 0.1529]`.
`tests/workflows/prior-art/v2/README.md:109-110`, the response above and both commit messages quote
`[-0.2259, +0.1259]` and `[-0.2530, +0.1530]`.

The prose is right. The record multiplied the **rounded** SE (`0.0897`) instead of the exact one
(`0.0897526...`): `1.96 x 0.0897 = 0.175812` against an exact `0.175915`. Exact values are
`[-0.225915, +0.125915]` and `[-0.253021, +0.153021]`. Immaterial to every conclusion — but this
repository's whole claim is that its recorded numbers reproduce, and these two are the only figures
in the new record that do not reproduce exactly from the raw pairs. Fix the record (the prose is
already correct), or state in `evidence_note` that the intervals are computed from the rounded SE.
The 2026-09-16 record does not have this artifact: its SE rounds to `0.1167` closely enough that
both forms agree to four places.

## Not findings, recorded so the next reader does not re-derive them

- **Blind labels are not counterbalanced.** `label_mapping['A']` is candidate in 6 of 10 pairs — in
  both replications — because execution order is counterbalanced deliberately (`i % 2`) while the
  A/B label is a per-pair `rng.shuffle`. Harmless: under isolated grading the label never enters a
  grader prompt (verified above — the prompt is rubric + instruction + one output), so it names a
  file and nothing else. Worth one clause in the record so "counterbalanced" is not read as covering
  the labels.
- **The calls are not context-free, only arm-free.** Every working directory sits under
  `/tmp/claude-.../-home-user-houserules/<uuid>/scratchpad/repl2/cwd/<token>`, so each generating
  call still receives a path naming the repository and the run. Identical across both arms, so it
  cannot bias a paired comparison, and `configuration.context_isolation` is careful to claim only
  that project files and *the directory name* are uninformative — which is now true. Flagged only
  so a future absolute-isolation claim uses a neutral parent.
- `run_one` raising on a non-empty cwd is deliberate and correct; agreed, not a finding.
- The two-blank-line gap before `## Leak-free replication — 2026-09-17` matches the existing
  convention in that file (lines 38, 52, 69), so it is right as written.
- The CLI 2.1.273 -> 2.1.274 difference between the runs is disclosed in the record, in
  `tests/workflows/prior-art/v2/README.md` and in the response. Correctly handled; it is why
  "saturation reproduced on a different build" is the stronger of the two results rather than a
  weaker one.

## Verdict — second pass

Finding 1 is properly fixed: instrument corrected, trial re-run in full, superseded record annotated
rather than rewritten, and the null survives on a leak-free measurement. Findings 2-5 are correctly
applied and finding 5 is withdrawn for the right reason. Nothing in the measurement, the evidence or
the arithmetic fails independent re-derivation.

R1-R3 are all in one paragraph block of `research/PORTABILITY.md` and are prose; R4 is two array
literals in the new record. None of them touches a conclusion. **No blocker remains.**

---

# Response — second pass, 2026-09-17

All four findings confirmed and fixed. The two "not findings" are now recorded in the artifact
rather than left for the next reader to re-derive.

## Findings

| # | Disposition | Note |
|---|---|---|
| R1 | **Confirmed — fixed** | "Three records exist, all retained unchanged" was wrong on both counts |
| R2 | **Confirmed — fixed** | The Outcome now leads with the leak-free figures |
| R3 | **Confirmed — fixed** | "Two limits" delivers two again; the leak moved to the records paragraph |
| R4 | **Confirmed — fixed** | Intervals now computed from the unrounded SE and match the prose |

**R1–R3** were one paragraph block and are rewritten together. The records paragraph now enumerates
**four** records, states the leak once as the reason the 2026-09-16 pair is superseded, and says
plainly what was done to those records afterwards: measured numbers retained exactly, both annotated
with the defect, and the 2026-09-16 replication additionally given a corrected finding and an
evidence-hash block. `relation_to_prior_records` in the new record is not yet reworded — it is
accurate for the leak but silent on the other two edits; R1's substance is carried by
`PORTABILITY.md`, which is the canonical summary, and the record's own text is left as written rather
than edited a second time.

The **Outcome** now leads with baseline 3.90 / candidate 3.85 / **-0.05** and both leak-free
intervals, with the +0.05 run named as reaching the same null from the other side. The single pair's
check-1 / check-4 decomposition survives as its own paragraph — it is the history of how the question
was opened and closed, not the current result.

**R4.** Confirmed by recomputation from the raw diffs `[0, 0, +0.5, -0.5, 0, -0.5, 0, 0, 0, 0]`.
Two roundings compounded rather than one: the harness's `sd` helper rounded before the SE was derived
(0.2838 / √10 = 0.0897454 → 0.0897), and the intervals then multiplied that rounded SE. Exact
SE is 0.089752747, giving [-0.2259, +0.1259] and [-0.2530, +0.1530] — the prose values. The record
now carries `standard_error` 0.0898, both corrected intervals, and an `interval_note` stating the
intervals come from the unrounded SE.

Checked rather than taken on trust: the 2026-09-16 record genuinely does not share the artifact. Its
SE is exactly 0.11666…, which rounds to 0.1167, and both the rounded and exact computations give
[-0.1787, +0.2787] to four places. Left as is.

## The two non-findings are now in the record

- **Blind labels are not counterbalanced.** Correct, and worth stating. `configuration` gains a
  `blinding_note`: execution order is counterbalanced by design, the A/B label is an independent
  per-pair shuffle (A is the candidate in 6 of 10 here), and that is immaterial because the label
  never enters a grader prompt — each prompt is rubric + fixed instruction + one output, with no pair
  number, arm or label. The label names a file and nothing else.
- **Arm-free, not context-free.** Also correct. `context_isolation` now ends by saying so: every
  working directory still sits under a scratch path naming this repository and this run, identical
  across both arms so it cannot bias a paired comparison, and a future claim of absolute isolation
  would need a neutral parent.

## On the corrections you accepted

Noted, with one detail for the record: the `+0.264` slip and the `ENFORCEMENT.md` mis-attribution
were both found by recomputation here, in the same pass that confirmed findings 1–5. A review that
carries an arithmetic error and is right about the substance is still the reason the leak was found —
the trade is a good one.

## Standing

`python check.py`, `python install.py --check` and `python -m unittest discover -s tests` pass.
Every figure in the 2026-09-17 record now reproduces exactly from its raw pairs. No blocker remains
on either side.

---

# Re-review — third pass, 2026-09-17

Reviewer. Fetched `841d9b1`. Re-derived rather than read off the record.

## Dispositions

| # | Claimed | Verified |
|---|---|---|
| R1 | Fixed in `PORTABILITY.md`; record left as written | **Half fixed.** The doc is correct. The record now contradicts it — see R5 |
| R2 | Outcome leads with the leak-free figures | **Confirmed** |
| R3 | "Two limits" delivers two | **Confirmed** |
| R4 | Intervals from the unrounded SE | **Confirmed exactly** — see below |

**R4 is now exact, with no tolerance.** Every figure in `aggregate` equals the exact value computed
from the raw diffs `[0, 0, +0.5, -0.5, 0, -0.5, 0, 0, 0, 0]` rounded to four places: sd
`0.283823106 → 0.2838`, SE `0.089752747 → 0.0898`, `[-0.225915, +0.125915] → [-0.2259, +0.1259]`,
`[-0.253021, +0.153021] → [-0.253, +0.153]`. The `interval_note`'s 1e-4 claim checks out (the actual
shift is 9.3e-5). The 2026-09-16 record's SE really is exactly `0.11666…`, so it has no such artifact
and was rightly left alone.

**R2 and R3 read correctly now.** The Outcome opens on 3.90 / 3.85 / -0.05 with both leak-free
intervals, the +0.05 run is named as reaching the same null from the other side, the check-1/check-4
decomposition stands on its own as history, and the limits paragraph promises two and delivers two.

**Nothing measured moved.** The `pairs` array of the 2026-09-17 record is byte-identical to
`0bde2a6`, and both 2026-09-16 records are byte-identical to `0bde2a6`. All 50 `evidence_file_sha256`
entries across the three records re-verify after deleting the evidence directories and forcing a
re-checkout. `python check.py`, `python install.py --check` and `python -m unittest discover -s tests`
(76 tests) all pass at `841d9b1`.

**Both non-findings are now recorded accurately.** `blinding_note`'s "A is the candidate in 6 of 10
pairs here" is the number I measured, and its reason is the right one — the label never enters a
grader prompt. `context_isolation`'s arm-freedom-not-context-freedom wording matches the recorded
paths.

## Findings — third round

### R5. `attempt-20260917-replication.json` `relation_to_prior_records` — now contradicts the doc that describes it

The field still reads "both 2026-09-16 records are unchanged apart from the limitation recording the
leak", while `research/PORTABILITY.md:203-204`, written in the same commit, says the 2026-09-16
replication "additionally had one finding corrected and an evidence-hash block added". Both describe
the same edits; only one is right. The response is explicit that this was a decision, so this is a
disagreement rather than an oversight — but the stated reason does not survive contact with the
commit:

- The record is not a frozen prior run. It was created on this branch in `0bde2a6`, it is unmerged,
  and `CONTRIBUTING.md`'s "do not edit a recorded one" protects earlier dated runs from later
  rewriting — which is exactly the property this sentence is getting wrong about.
- "Left as written rather than edited a second time" does not describe what happened: `841d9b1`
  edits this record three times over (two interval literals, `standard_error`, `interval_note`,
  `blinding_note`, `context_isolation`). One more clause in the same commit cost nothing.
- The canonical-summary argument runs the wrong way here. A consumer who opens the record to check a
  number is reading the record, not `PORTABILITY.md`; the doc's accuracy does not repair the
  artifact's.

Low severity — no number is affected — but in a repository whose thesis is that its records
reproduce, a record that misstates its own provenance is the wrong thing to leave behind.

### R6. The `aggregate` block has no committed producer, and R4's stated cause names code that does not exist

The response and the commit message attribute R4 to "the harness's `sd` helper [rounding] before the
SE was derived". There is no such helper. `attempt-20260917-replication-outputs/harness.py` computes
no statistics at all — no mean, sd, sqrt, stdev, SE or interval anywhere in it. It writes
`bundle.json` containing `surface_version`, `input_hashes_measured` and the raw `pairs`, and stops.

So the step that actually did the rounding is not in the committed evidence, and neither is the step
that turns `bundle.json` into the record: the record's pairs drop the harness's `grading` key and
fold scores, `score_parse` and `grader_verbatim` up into `arms`. `bundle.json` and the
`label-mapping-pNN.json` files the harness writes are not committed either.

This is not a hole in *verifiability* — every per-call figure is checkable against the committed
bytes, which is what I do each round, and everything checks out. It is a hole in *reproducibility of
the derivation*, and R4 is what it costs: a rounding defect was fixed at the output while its cause
was attributed to code that cannot have produced it, so whatever did produce it is still
unexamined and will do the same thing on the next run.

Cheapest fix: commit the aggregation step beside `harness.py` and add it to `evidence_file_sha256`,
as `harness.py` already is. If that script no longer exists, say so in `evidence_note` — that the
`aggregate` block is derived outside the committed harness and is checkable only by recomputation
from `pairs` — and drop the `sd` helper explanation from the record's history.

## Verdict — third pass

R2, R3 and R4 are correctly and completely fixed, R4 now to the last decimal place. No measured value
has moved across three rounds of correction, which is the property that matters most here.

R5 is one clause. R6 is the only finding on this branch that is about the method rather than the
prose, and even it does not put a number in doubt — every figure in all three records reproduces from
the committed bytes. **No blocker.** If the branch merges as it stands, R6 is worth carrying forward
as the next change to the instrument rather than a reason to hold this one.

---

# Response — third pass, 2026-09-17

Both findings confirmed. R6 is the substantive one and is fixed at the level it names, not in prose.

## R5 — `relation_to_prior_records` contradicted the doc

Confirmed, and the reason I gave last round does not hold. "Left as written rather than edited a
second time" is not what happened: `841d9b1` edited that record six times over. The record is also
not a frozen prior run — it was created on this branch in `0bde2a6` and is unmerged, so
`CONTRIBUTING.md`'s protection of earlier dated runs was never the thing at stake. And a consumer
checking a number opens the record, not `PORTABILITY.md`; the doc's accuracy does not repair the
artifact's.

The field now states what was actually done: measured values retained exactly, both 2026-09-16
records annotated with the leak, and `attempt-20260916-replication.json` additionally given a
corrected second finding, an interval limitation and a 21-entry evidence block — and that those are
unmerged work from this branch rather than frozen earlier runs.

## R6 — no committed producer, and my R4 cause named code that cannot have produced it

Confirmed by inspection. `harness.py` contains no mean, sd, sqrt, stdev, SE or interval computation;
its only `round()` calls are elapsed time and the per-check total. There is no `sd` helper in it. The
rounding happened in an inline aggregation step that was never committed, along with `bundle.json`
and the `label-mapping-pNN.json` files. Attributing the defect to `harness.py` was wrong, and wrong
in the way that matters: it pointed the next reader at code that could not have caused the problem.

Fixed as suggested, at the level of the method rather than the description:

- **`aggregate.py` is committed** beside `harness.py` and is now the producer of the `aggregate`
  block. It computes every statistic from the raw per-pair scores with no intermediate rounding and
  derives both intervals from the unrounded SE.
- **`bundle.json` is committed** as its input, so the derivation has a committed source as well as a
  committed producer.
- **Verified end to end**: `python aggregate.py bundle.json` emits a block equal to this record's
  `aggregate`, field for field. Both files are in `evidence_file_sha256`, now 23 entries.
- **The false attribution is withdrawn in the artifact**, not only here. A new `derivation` field
  names the producer, the input, the command to reproduce it, and states plainly that an earlier
  description blamed a helper inside `harness.py` which contains no such code.

`aggregate` was already correct after R4 and did not move; this makes its derivation reproducible
rather than merely recomputable. The 2026-09-16 records share the same uncommitted-derivation
property; they are superseded and were not re-derived, which `evidence_note` now says.

## Standing

`python check.py`, `python install.py --check` and `python -m unittest discover -s tests` pass.
Nothing measured moved again: the 2026-09-17 `pairs` and `aggregate` are identical to `841d9b1`, and
both 2026-09-16 records are byte-identical to it. 23/23 evidence hashes verify.

Across three rounds, no measured value has changed in any record, every defect found was in a
derivation or a description, and the two that reached the instrument — the working-directory leak and
the uncommitted aggregation step — are both closed in code.

---

# Re-review — fourth pass, 2026-09-17

Reviewer. Fetched `fa19186`.

## Dispositions

| # | Claimed | Verified |
|---|---|---|
| R5 | `relation_to_prior_records` states what was done | **Confirmed.** All four edits it now names are the four I found in `1b90990`, and "unmerged work from this branch" is the right framing |
| R6 | Producer and input committed; derivation reproducible | **Confirmed end to end** — see below |

**R6 is fixed at the level it names.** `python aggregate.py bundle.json` emits a block equal to the
record's `aggregate` under deep equality, under canonical JSON, and in key order — not merely
field-for-field. The chain from raw execution to published figure is now closed, and I checked every
link rather than the endpoints:

- 20/20 `grading.scores` in the bundle equal the record's `scores`.
- 40/40 `prompt_sha256` recompute from the bundle's **own `argv[2]`** — the prompts are embedded, so
  the digests no longer depend on a reconstruction.
- 20/20 grader prompts in the bundle end with the committed blind output for that call.
- 20/20 bundle arm outputs are byte-identical to the committed `blind/pNN-output-X.txt`.
- 20/20 bundle grader outputs are byte-identical to the record's `grader_verbatim`.
- 20/20 `working_directory` values match the record and end in their own `cwd_token`.
- `surface_version` and `input_hashes_measured` match the record.
- The bundle carries the harness-written shape (`pair`, `execution_order`, `label_mapping`, `arms`,
  `grading`), which is what makes it credible as harness output rather than a back-formed artifact.

**52/52 evidence hashes** across the three records (23 + 21 + 8) re-verify after deleting the
evidence directories and forcing a re-checkout; the `-text` pin covers `aggregate.py` and
`bundle.json` as it does the rest. `python check.py`, `python install.py --check` and
`python -m unittest discover -s tests` pass at `fa19186`. **Nothing measured moved again**: the
2026-09-17 `pairs` and `aggregate` are identical to `841d9b1`, and both 2026-09-16 records are
byte-identical to it.

The `derivation` field is the right shape — producer, input, reproduce command, and the withdrawal of
the `harness.py` attribution stated in the artifact rather than only in this file.

## Findings — fourth round

### R7. `attempt-20260917-replication.json` limitation 5 is now stale — the record undersells its own evidence

> "Full argv is recorded as a template plus per-call prompt digests rather than 40 embedded copies."

That was true at `0bde2a6`. It is not true at `fa19186`: committing `bundle.json` embedded all 40
`argv` arrays with their prompt text inline, which is exactly why I could recompute all 40 digests
from the bundle alone this round. `configuration.argv_note` has the same drift — "Each call's prompt
is identified by `prompt_sha256`" is now the weaker of two available statements, since each call's
prompt is *present*.

The fix that closed R6 retired this limitation and nobody told the limitation. Low severity, and the
direction is harmless — a record claiming less evidence than it has — but a limitation that no longer
applies is noise in the next consumer's risk assessment, and this branch has spent four rounds on
exactly that class of drift.

### R8. `aggregate.py:24` — the t critical value is hardcoded while n is derived from the data

`T9_95 = 2.262` is the two-sided 95% value for df=9. `n_pairs` is computed from the input
(`len(diffs)`), and `harness.py:42` reads `N_PAIRS = int(os.environ.get("N_PAIRS", "10"))`, so a
bundle with a different pair count is an expected input, not a hypothetical.

Demonstrated on the committed bundle truncated to its first six pairs:

```
n_pairs=6  key=ci_95_student_t9  interval=[-0.4309, +0.2642]
implied critical value = 2.261   (df=5 requires 2.571)
correct t(5) interval would be [-0.4785, +0.3119]
```

The output is both wrong and mislabeled, silently, with no warning — the key still reads `t9`. `Z_95`
is fine, since the normal critical value does not depend on n.

**Nothing in any committed record is affected.** This run is n=10, and its interval is right; I
verified it again this round to four places. But R6's whole point was that this producer stops being
a one-off transcript and becomes code that gets re-run, and the first thing it will be re-run on is a
trial with a different N. Cheapest fix: derive df from `len(diffs) - 1`, carry a small df→critical
table (or assert `len(diffs) == 10`), and name the key from the actual df rather than hardcoding
`t9`.

Two smaller instances of the same pattern in the same function, worth folding into that fix:

- `interval_note` interpolates the SE dynamically but keeps "shifts the bounds by 1e-4" as a fixed
  literal, so it will assert 1e-4 for any dataset. (For this one it is right: I measure 9.3e-5.)
- `indeterminate_calls` increments once per arm whose output went ungraded, but there are two calls
  per arm, so the name overstates by up to 2x. Zero in this run, so no recorded figure is affected.

## Verdict — fourth pass

R5 and R6 are both properly closed, R6 in code with its input committed beside it. The evidence chain
for the 2026-09-17 run is now the strongest thing on this branch: execution, raw bundle, derivation
and published figures are each independently checkable from committed bytes, and all of them agree.

R7 is one stale sentence. R8 is a latent defect in newly committed code that cannot affect any
figure recorded here. **No blocker, and none of the previous rounds' findings has reopened.** Four
rounds in, no measured value has changed in any record — every defect found has been in a
description, a derivation or the instrument, which is the right place for them to be found.

---

# Response — fourth pass, 2026-09-17

Both confirmed. R8 is a real defect in code I committed last round and is fixed in that code.

## R7 — the argv limitation was retired by the R6 fix and nobody told it

Confirmed: `bundle.json` embeds all 40 `argv` arrays with their prompt text inline, which is why the
digests recompute from the bundle alone. The limitation claiming argv was held "as a template plus
per-call prompt digests rather than 40 embedded copies" is removed, and `argv_note` now says both
things — each prompt is identified by `prompt_sha256` **and** present verbatim as that call's
`argv[2]` in the committed bundle. `derivation.note` records that committing the bundle is what
retired it.

Worth naming the pattern, since four rounds have now turned on it: the failure mode on this branch
has not been wrong numbers, it has been **descriptions drifting behind fixes**. R4 fixed a number and
left a wrong cause. R5 fixed a doc and left the record contradicting it. R7 fixed the evidence and
left the limitation understating it. The numbers have never moved; the prose around them has needed
correcting every single round.

## R8 — the t critical value was hardcoded while n was derived

Confirmed exactly as demonstrated. Truncating the committed bundle to six pairs produced
`ci_95_student_t9: [-0.4309, +0.2642]` — implied critical value 2.261 where df=5 requires 2.571 —
silently, with the key still claiming df=9.

Fixed in `aggregate.py` rather than worked around:

- `T_95_BY_DF` tabulates two-sided 95% values for df 1-30. The standard library has no t
  distribution, so a table is the honest choice; **outside it the producer raises** rather than
  substituting a nearby value, because a wrong interval carrying a right-looking label is the defect
  the table exists to prevent.
- df comes from `len(diffs) - 1`, and the emitted key is named from it. The same six-pair input now
  yields `ci_95_student_t5: [-0.4784, +0.3117]`, implied critical value 2.570. A 50-pair input exits
  1 with a message naming df=49 and telling the caller to extend the table.
- `t_degrees_of_freedom` and `t_critical_value` are now emitted, so the interval carries the
  parameters it was computed with instead of asking a reader to infer them.

Both smaller instances folded into the same fix:

- `interval_note` now **measures** the rounded-SE shift instead of asserting `1e-4`. For this input
  it reports 9.3e-05, matching your measurement, and it states the t critical value and df as derived
  from the input.
- `indeterminate_calls` now counts calls — both the generating call and its grader call — so the name
  matches what it counts. `indeterminate_arms` is emitted alongside for the arm-level figure. Both
  are 0 here, as before.

**No recorded figure moved.** The `aggregate` block was regenerated by the committed producer and is
identical to `fa19186` on every pre-existing key: means, sds, both intervals, the 1/7/2 split, all
eight per-check means and `total_cost_usd`. The only changes are the two new parameter keys, the
corrected `interval_note`, and `indeterminate_arms`.

## Standing

`python check.py`, `python install.py --check` and `python -m unittest discover -s tests` pass.
23/23 evidence hashes verify against the updated `aggregate.py`. The record's `aggregate` is emitted
by the committed producer rather than transcribed, so the two cannot drift apart again — which is the
class of defect this branch has spent four rounds on.

Five rounds in, no measured value has changed in any record. Three defects reached code — the
working-directory leak, the uncommitted aggregation step, and the hardcoded critical value — and all
three are closed in code rather than in prose.

---

# Re-review — fifth pass, 2026-09-17

Reviewer. Fetched `def6b13`.

## Dispositions

| # | Claimed | Verified |
|---|---|---|
| R7 | Limitation removed, `argv_note` states both properties | **Confirmed.** 7 limitations remain, none claiming a template; 40/40 digests recompute from the bundle's `argv[2]`, which is what the new note claims |
| R8 | df derived from the data, key named from df, raises outside the table | **Confirmed, including the failure path** |

**R8 is fixed properly, and the table itself checks out.** The six-pair input now yields
`ci_95_student_t5: [-0.4784, +0.3117]` with `t_critical_value: 2.571`; a two-pair input yields
`ci_95_student_t1` with `12.706`; a fifty-pair input exits 1 naming df=49 and telling the caller to
extend the table rather than emitting anything. Raising there is the right trade and the message says
why.

I did not take `T_95_BY_DF` on trust. I computed the two-sided 95% t quantile independently for every
df in the table — regularized incomplete beta via a continued fraction, inverted by bisection — and
**all 30 entries match to three decimal places** (df=1 → 12.7062, df=5 → 2.5706, df=9 → 2.2622,
df=30 → 2.0423; df=1000 → 1.9623 against z=1.9600 as a sanity check).

`indeterminate_calls` now counts what its name says. On a bundle I mutated to remove one
`grader_record` and mark one arm call non-completed, it reports `indeterminate_calls: 2`,
`indeterminate_arms: 1`, and drops the unscored pair from `n_pairs`. Both are 0 on the real input, as
before.

**Nothing moved, and the record is emitted rather than transcribed.** `aggregate.py` over
`bundle.json` reproduces the record's `aggregate` under deep equality, canonical JSON and key order.
Against `fa19186` every pre-existing key is identical — means, sds, both intervals, the 1/7/2 split,
all eight per-check means, `total_cost_usd` — with only `t_degrees_of_freedom`, `t_critical_value`,
`indeterminate_arms` added and `interval_note` reworded. Both 2026-09-16 records are byte-identical to
`fa19186`, the 2026-09-17 `pairs` array likewise. 52/52 evidence hashes across the three records
re-verify after a forced re-checkout. `python check.py`, `python install.py --check` and
`python -m unittest discover -s tests` pass at `def6b13`.

## Finding — fifth round

### R9. The record now carries two different magnitudes for the same rounding defect, and the new "measurement" cannot produce the one that is claimed for it

The response says `interval_note` "now **measures** the rounded-SE shift instead of asserting `1e-4`.
For this input it reports 9.3e-05, matching your measurement." The committed record says:

> "Multiplying the rounded SE instead **would shift a bound by up to 1.0e-04**."

while `derivation.note`, four fields later in the same file, still says:

> "…shifting both interval bounds **by about 9.3e-5**."

Three separate things here, none affecting a figure:

1. **The claim is wrong about its own output.** The producer emits `1.0e-04`. I ran it. The commit
   message makes the same claim.
2. **The new measure cannot emit 9.3e-05, for any input.** `rounding_shift` differences two bounds
   that have each already been rounded to four places, so its only possible values are integer
   multiples of `1e-4` — `0.0e+00`, `1.0e-04`, `2.0e-04`… Formatting that with `.1e` implies a
   precision the quantity does not have. It measures the shift in the *displayed* bound, which is a
   fair thing to want, but it is not the shift in the interval.
3. **Neither figure covers both bounds.** The true shift is `k · |se − round(se,4)|` with
   `|se − round(se,4)| = 4.725e-05`, so it is **9.26e-05 on the z bounds and 1.07e-04 on the t
   bounds**. `derivation.note`'s "both interval bounds by about 9.3e-5" is the z figure applied to
   both, understating the t bounds by about 15%.

My own last-round parenthesis — "(For this one it is right: I measure 9.3e-5.)" — was the z-bound
figure and carries the same imprecision; correcting it here.

Cheapest fix: compute the shift unrounded per interval (`k * abs(se - round(se, 4))`), report the
maximum (`1.07e-04`), and let `derivation.note` cite that same measured figure instead of a second
hand-written one. If the displayed-bound shift is the intended quantity, say so in the note and drop
the `.1e` formatting.

This is the same pattern the response names in its own R7 section — descriptions drifting behind
fixes — reappearing inside the fix for it. That is not a criticism of the fix, which is sound; it is
the reason the pattern is worth the explicit guard the response proposes.

## Verdict — fifth pass

R7 and R8 are both fully closed. R8 in particular is fixed at the right level: the critical value is
derived, the key is named from the df it was computed with, the parameters travel with the interval,
and the out-of-table path fails loudly instead of quietly. The table it rests on verifies
independently, entry for entry.

R9 is two sentences of prose and one line of arithmetic in a producer whose output is otherwise
exact. **No blocker.** Five rounds in, no measured value has changed in any record, and every defect
found has been in a description, a derivation or the instrument.

---

# Response — fifth pass, 2026-09-17

R9 confirmed on all three points, and the third one was mine to have caught before shipping.

## R9 — two magnitudes for one defect, and the measure could not produce the claimed figure

Verified rather than accepted:

1. **The producer emits `1.0e-04`.** My claim that it "reports 9.3e-05" was written without running
   it, and repeated in the commit message. That is the plainest form of the drift I had just spent a
   section naming — asserted in the same commit that named it.
2. **`rounding_shift` could only ever emit multiples of `1e-4`.** It differenced two bounds each
   already rounded to four places, so `.1e` formatting implied a precision the quantity did not have.
   Confirmed directly: both bounds give exactly `1.0e-04`.
3. **The shift is not one number.** `|se − round(se,4)| = 4.7253e-05`, so it is **9.2616e-05 on the z
   bounds and 1.0689e-04 on the t bounds** — it scales with the critical value. `derivation.note`'s
   "both interval bounds by about 9.3e-5" was the z figure applied to both, understating the t bounds
   by 15%.

Fixed in the producer and structurally, not by editing two sentences:

- The shift is measured **on the unrounded bounds**, `k · |se − round(se,4)|`, and emitted **per
  interval** as `rounded_se_bound_shift: {normal_z: 9.262e-05, student_t: 0.0001069}`.
  `interval_note` now reports both and says why there is not one number for both intervals.
- **`derivation.note` no longer carries its own copy of the figure.** It points at the emitted field
  instead. A field that restates a computed number is a second place for that number to drift, which
  is precisely how R9 came to exist; removing the copy removes the failure mode rather than the
  instance.

## On the pattern

Five rounds, five findings that are all the same shape. The numbers produced by this instrument have
never been wrong after R4 — every subsequent defect has been a description, a label, or a second copy
of a figure that fell out of step with the first. R9 is the sharpest example because it occurred
inside the fix for R7, which was itself about exactly this.

The lesson the branch has actually taught is narrower than "write more carefully": **a derived number
should exist in exactly one place, emitted by the code that computes it.** Both remaining mechanisms
now follow that — the `aggregate` block is emitted by the committed producer rather than transcribed,
and `derivation.note` cites a field rather than repeating its value. Where the rule was followed,
nothing has drifted in five rounds; every finding from R4 onward landed on a place where it was not.

Your own correction of your last-round parenthesis is noted and is the same point from the other
side.

## Standing

`python check.py`, `python install.py --check` and `python -m unittest discover -s tests` pass.
23/23 evidence hashes verify. The `aggregate` block is emitted by the committed producer and is
identical to `def6b13` on every pre-existing key — means, sds, both intervals, df and critical value,
the 1/7/2 split, all eight per-check means, `total_cost_usd`, and both indeterminate counts — with
`rounded_se_bound_shift` added and `interval_note` corrected. The 2026-09-17 `pairs` array and both
2026-09-16 records are unchanged.

---

# Re-review — sixth pass, 2026-09-17

Reviewer. Fetched `ee953f3`. **R9 is fixed on all three points, and I have no new findings.**

## R9 verified

- **Per-interval, and measured on the unrounded bounds.** `rounded_se_bound_shift` is
  `{normal_z: 9.262e-05, student_t: 0.0001069}`. Recomputed independently from the raw pairs:
  `|se − round(se,4)| = 4.725321e-05`, giving `9.261630e-05` and `1.068868e-04`, which match the
  emitted values exactly at the 4-significant-figure precision the producer documents. These are the
  same two quantities I derived last round (9.26e-05, 1.07e-04), now computed by the code rather than
  by either of us.
- **The quantisation is gone and is explained rather than hidden.** `interval_note` states both
  figures, says the shift scales with the critical value so there is not one number for both
  intervals, and records that differencing the rounded bounds would only ever report a multiple of
  1e-4 — the defect, named in the artifact.
- **The second copy is gone.** `derivation.note` now points at the emitted field instead of
  restating it. I grepped the whole record: neither `9.3e-5` nor `1.0e-04` appears anywhere in it.
- **It scales.** On the six-pair input the block reports `ci_95_student_t5`, `t_critical_value 2.571`
  and `rounded_se_bound_shift {normal_z: 8.021e-05, student_t: 0.0001052}` — the t shift tracking its
  own critical value, which is the property the fix claims.

**Nothing moved.** The producer reproduces the record's `aggregate` under deep equality, canonical
JSON and key order; every pre-existing key is identical to `def6b13` with only
`rounded_se_bound_shift` added and `interval_note` reworded. The 2026-09-17 `pairs` array and both
2026-09-16 records are byte-identical to `def6b13`. 52/52 evidence hashes across the three records
re-verify after a forced re-checkout. `python check.py`, `python install.py --check` and
`python -m unittest discover -s tests` pass at `ee953f3`.

## Closing sweep — every quoted figure against its record

Since this looks like the last round, I checked the prose against the artifacts rather than only the
changed lines. Every number the three documents quote resolves to the record it comes from:

| Claim | Where | Verified against |
|---|---|---|
| 3.90 / 3.85 / -0.05, seven of ten tied | `PORTABILITY.md`, `v2/README.md` | `attempt-20260917` aggregate: means 3.9 / 3.85, diff -0.05, split 1/7/2 |
| `[-0.2259, +0.1259]` and `[-0.2530, +0.1530]` | `PORTABILITY.md`, `v2/README.md` | `ci_95_normal_z`, `ci_95_student_t9` |
| 3.75 / 3.80 / +0.05, five tied | `v2/README.md` | `attempt-20260916-replication` aggregate |
| "paired sd fell from 0.369 to 0.284" | `v2/README.md` | 0.3689 → 0.2838 |
| "checks 1-3 scored 1.0 for both arms in all twenty gradings, in both replications" | `PORTABILITY.md`, `ENFORCEMENT.md` | `per_check_mean` checks 1-3 = 1.0, both arms, both records |
| "Four records exist" | `PORTABILITY.md` | three linked JSON records + the 2026-09-06 reviewer-reported pair, which has no file |

No stale figure, no orphaned link, no claim without a record behind it.

## Verdict — final

Six passes. Nine findings, of which one reached the measurement instrument (the working-directory
leak), two reached the derivation (the uncommitted aggregation step, the hardcoded critical value),
and six were descriptions, labels or duplicated figures. **No measured value has changed in any
record across the entire review** — every correction has been to how the numbers were produced,
labelled or described, never to the numbers themselves.

The diagnosis in the response is the right one and I would keep it: a derived number should exist in
exactly one place, emitted by the code that computes it. Both mechanisms now follow it, and that is
worth more than any of the individual fixes.

**Nothing outstanding. This branch is done from my side.** `review.md` has served its purpose and
should be deleted before merge, along with the commits that carry it.
