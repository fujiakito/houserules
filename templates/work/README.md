# Work artifacts

The channel between sessions and between agents. Context does not survive a session boundary
and certainly not an agent boundary, so when one session plans, another reviews the plan, a
third implements in a different agent and a fourth commits, **these files are the only thing
that reaches the next step**.

```
work/<id>/handoff.md    state and pointer — overwritten, kept short
work/<id>/findings.md   append-only — reviews, rejected approaches, incidents
work/<id>/<stage>.md    whatever that stage produces, in whatever shape suits it
```

## Why not one template for every stage

A plan is forward-looking and ordered. A review finding is a located observation with a
severity. A task list is a checklist. Forcing them into one template makes each of them
worse, so this ships a **contract**, not a document set.

## Why no fixed stage names

`requirements.md` → `design.md` → `tasks.md` is one methodology's set. Adoption of every such
methodology measured at essentially zero across 2,424 repositories, and methodology migration
happened zero times in 91 repositories selected to be the most likely to show it.

**Name the stages your pipeline actually has.** The `stage` field in `handoff.md` is free text
for that reason. If your pipeline is plan → review-plan → implement → review-code → commit,
those are your stage names and your file names.

## What decides whether a file belongs here at all

> A template that only gets read is overhead. A template the next session must **parse and act
> on** is a contract.

If no other session or agent will read it, it is a note to yourself — keep it out of the
repository, or accept that it is costing review attention for nothing.

## Committing these

Gitignore `work/` unless the trail is wanted in history. The files must exist **in the
repository working tree** — that is the only place every agent looks — but they do not have to
be committed to serve their purpose.

One reason to commit them anyway: `findings.md` entries about rejected approaches keep their
value long after the work is done, and that is exactly the kind of knowledge that is expensive
to rediscover.
