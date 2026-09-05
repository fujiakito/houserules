<!--
  FINDINGS — append-only. Nothing here is ever edited or deleted.

  This is the channel that carries a reviewer's output to every later stage. A finding that
  is not written here does not survive the session that produced it, and the next agent has
  no way to know it was ever made.

  Append-only is deliberate, and it is the opposite of the rule for AGENTS.md. An instruction
  file must be pruned because every line in it bills on every session. This file is read once,
  by the next stage, and its whole value is that a path already tried is not tried again.

  Add entries at the BOTTOM. If a later stage disagrees with an earlier finding, append the
  disagreement - do not edit the original. What an earlier stage believed is part of the record.

  DELETE THIS COMMENT when you copy the template.
-->

# Findings

<!-- Optional pilot convention for new findings: use stable IDs (F-001, F-002...) and append
     lifecycle events below. Existing dated entries remain valid historical records; assign
     an ID by a new linking entry when a later session needs to act on one. -->

## F-001

**Recorded:** YYYY-MM-DD; stage; reviewer/session; severity: blocker | should-fix | note

**Target:** artifact path/URL + revision/digest, or code base/target and working-tree scope.

**Requirement:** criterion/standard ID or source location.

**Observation and evidence:** what is wrong and where it can be observed.

**Consequence:** why it matters. Keep proposed fixes separate from the observation.

### Event FE-001 — F-001 — YYYY-MM-DD — <owner/session>

**State:** proposed-fix | verified | reopened | rejected | accepted-risk

**Evidence:** changed revision + verification record, or reason and decision owner for rejection
or accepted risk. A proposed fix leaves the finding open. Verification names who checked what
on which revision; later changes can reopen it. Record no secret values.

---

<!-- Original entry forms below remain usable. Choose one finding form; do not duplicate the
     same finding in both forms or in a review report. -->

<!-- One block per finding. Keep the header line machine-parseable so a later stage can filter. -->

## [YYYY-MM-DD] [stage] [owner] [severity: blocker | should-fix | note]

**Where:** `path/to/file.py:42` — or "n/a" for a finding about the approach rather than the code

**What:** one or two lines. The observation, not the fix.

**Why it matters:** the consequence if it is left. A finding without this is a preference, and
the next stage cannot weigh it.

**Suggested action:** optional. Say if you are unsure — a reviewer guessing is more useful
labelled as a guess.

---

## [YYYY-MM-DD] [stage] [owner] [rejected-approach]

**Tried:** what was attempted

**Why it was dropped:** the reason, specifically enough that the next session does not retry it

<!-- Rejected approaches are the highest-value entries here. Without them the next agent
     re-walks them at full cost, and has no way to know they were already walked. -->
