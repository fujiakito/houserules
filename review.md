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
