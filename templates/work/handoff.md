<!--
  HANDOFF — state and pointer. One per unit of work.

  This is the file the next session reads FIRST to decide whether to pick this up and what
  to do. Keep it short: it is a routing decision, not a record. The record lives in
  findings.md, and the stage output lives in its own file.

  Layout:
    work/<id>/handoff.md    <- this file: where we are, what is next
    work/<id>/findings.md   <- append-only; nothing is ever edited or removed
    work/<id>/<stage>.md    <- whatever that stage produces, in whatever shape suits it

  WHY THREE FILES rather than one. A plan and a review finding are different shapes: a plan
  is forward-looking and ordered; a finding is a located observation with a severity. Forcing
  both into one template makes both worse. And findings must ACCUMULATE - a reviewer's output
  is an input to every later stage - while state must be OVERWRITTEN, because stale state
  routes the next session wrongly.

  Some ledgers should append and some should not. Findings, rejected approaches and incidents
  append. Current state does not.

  DELETE THIS COMMENT when you copy the template.
-->
---
schema_version: 1 # optional pilot extension; missing means the original minimal handoff
id:               # short, stable, also the directory name
title:            # one line
stage:            # whatever this pipeline's stages are - do not adopt someone else's set
status:           # ready | in-progress | blocked | done
owner:            # agent/model + session or task id, e.g. claude-code/sonnet-5#a1b2
                  # a review stage should not carry the same owner as the stage it reviews
updated:          # YYYY-MM-DD
action:           # draft | review | implement | fix | verify | decide; independent of stage
---

# <title>

## Read first

<!-- Link only the inputs the next action needs. Use artifact path/URL + revision or content
     digest. For a new checkout, ensure these files are committed or explicitly transferred.
     List the relevant spec/task/review/finding IDs; do not copy their contents here. -->

## Where this is

<!-- Two or three lines. What has been done, what file holds it. Not a narrative of the
     session - the next reader has none of your context and needs the shortest path to
     being useful, not the story of how you got here. -->

## Next step

<!-- Name the stage AND its acceptance condition. "Review the plan" is not actionable;
     "review plan.md against AGENTS.md and reject any rule already enforced by check.py" is.
     The next session cannot ask you what you meant. -->

## Blocked on

<!-- Only if status is blocked. Name what would unblock it and who can do that. -->

## Working state and authority

<!-- Branch/worktree and uncommitted changes that the next session must preserve. Name the
     permitted action and any still-required decision; a previous review is not authorization
     to commit, publish or deploy. Omit this section when nothing extra must be carried. -->
