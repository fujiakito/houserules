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
