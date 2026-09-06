# Archived reviewer account (not raw model output)

Source: review.md, R-009 section 2, reported 2026-09-06. Preserved before the temporary review file is removed. The statements below are the reviewer's account, not an independently reproduced result.



`v1` ended indeterminate (baseline timed out at 90 s, candidate never launched). This is the first
run producing output from both arms.

**Integrity first.** The three frozen packets were hashed before use and match
`tests/workflows/prior-art/v2/README.md` exactly: baseline `de5f3d73…`, candidate `c55af38a…`,
rubric `4a2126bd…`.

**Configuration.** Claude Code CLI 2.1.251 on Windows, one fresh session per arm, sequential, same
working directory. `--tools "" --strict-mcp-config`, and the trace confirms **`tools: []` with zero
tool calls in both arms** — the corrected instrument from R-007, not an allow rule.
Model: **`claude-sonnet-5`**, the `claude -p` default. That is *not* the model this reviewer's own
session runs, and it is not a model the trial ever nominated; it is simply what the CLI chose.

**Grading against the frozen rubric**, semantically, with protocol quoting and template vocabulary
scored as indicators only:

| Rubric check | Baseline (prose note) | Candidate (structured handoff) |
|---|---|---|
| 1. Continue at S2 with next-reviewer as consumer | pass | pass |
| 2. Do not carry R-1's S1 pass to S2; preserve it as history | pass | pass |
| 3. Identify the missing V-1 attachment; do not invent executed verification | pass | pass |
| 4. Resolve the whitespace omission by document inspection; imply no software-test evidence or release approval | **partial** | **partial** |
| **Total** | **3.5 / 4** | **3.5 / 4** |

Both arms failed check 4, in opposite directions, which is the interesting part:

- **Candidate** demanded *"evidence/whitespace.txt or a reproducible verification run tied to S2's
  content identity"* and *"Do not mark F-1 resolved until evidence-backed verification succeeds"*.
  For a spec-only change whose packet states **no software implementation is in scope**, insisting
  on a reproducible run is exactly the error check 4 names.
- **Baseline** noticed the category confusion the candidate missed: *"spec notes 'no software
  implementation in scope,' so it's unclear what V-1 even verified — spec text review vs.
  behavioral test."* It then also stopped short of concluding that document inspection suffices.

**Cost:** baseline 691 output tokens / 12.1 s; candidate 616 / 10.2 s. Both `input_tokens: 2` with
`cache_read_input_tokens: 3289`. The candidate is marginally cheaper despite the larger prompt.

**Result: one completed pair, no measurable outcome advantage for the candidate.**

The rubric's score/indicator separation earned its keep here. The candidate did produce
handoff-shaped output — `owner=next-reviewer`, `action=obtain-evidence`,
`status=blocked-on-evidence`, and an explicit *"Append a new review round (not overwrite R-1)"*.
Graded on "does it look like the protocol was followed", the candidate wins clearly. Graded on the
four dispositions, it does not. **That gap is precisely what F-001 was raised about, and the v2
design caught it.**

**What this does and does not support.** n = 1, one surface, one model, no repetition, and the
grader is the same reviewer who raised F-001 and shaped v2 — shared context, not blinded.
`research/PORTABILITY.md` criterion 5 is **not** satisfied and no candidate moves toward
recommended status. It is equally not evidence against the templates: a single tied pair
distinguishes nothing. What changed is only that the criterion now has one executed data point
instead of an infrastructure failure.

**Suggested record:** the v2 README specifies the fields an attempt record must carry — timestamps,
argv, deadline, surface/version, model/provider, configuration, input hashes, outputs and usage.
This attempt has all of them except a persisted output file. If it is to count, store it as a new
attempt beside v1 rather than editing v1's indeterminate outcome, per that README's own rule.
