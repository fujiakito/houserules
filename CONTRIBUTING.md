# Contributing

## Before you open a pull request

`AGENTS.md` holds the working rules — commands, evidence conventions and the verification
gate. Read it rather than this file for those; it is what a coding agent loads, and keeping
one copy is the point. This page covers only what it does not.

Three gates must pass, and CI runs all three on Python 3.9, 3.11 and 3.13:

```bash
python -m unittest discover -s tests -v && python check.py && python install.py --check
```

There is no version guard in the scripts, so a 3.10+ construct fails at import on the floor
rather than with a clear message. `from __future__ import annotations` is already in place;
keep annotations out of runtime evaluation.

Standard library only, in the scripts and in the tests. A contribution that adds a
dependency needs to argue why, because a check with an install step is a check that gets
skipped.

## Proposing a skill

A stage with no skill in it is not a gap, and a built-in on another surface does not
disqualify a fallback. Apply the admission criteria in
`research/PORTABILITY.md#fallback-admission-criteria`, and say in the pull request which
criterion the evidence meets: explicit experimental trial and recommendation/default
promotion have different bars.

Adapted material carries a `LICENSE` and a `NOTICE.md` beside `SKILL.md` recording source
URL, pinned revision, retrieval date and what changed. Add the row to `THIRD-PARTY.md`.
Skills use the `hr-` prefix.

## Proposing a document

`docs/README.md` maps every document to a reader, a resulting action and an update trigger.
A new document needs all three, plus its row. If it cannot name them, extend the canonical
document instead — the inclusion test `AGENTS.md` applies to itself applies here too, and
the documentation conformance test checks link targets and stage coverage.

## Changes that need extra care

| Change | Also required |
|---|---|
| A new agent surface | Inventory from `docs/agents/_TEMPLATE.md`, every `docs/GUIDE.md` stage and concern table, a `research/MATRIX.md` row |
| A new or changed shipped skill | Canonical `templates/skills/<name>/` source, admission status/evidence, README and relevant GUIDE choices, installation/drift tests and upstream notices/THIRD-PARTY when applicable. Installer discovery is automatic; keep `check.py`'s explicit `SHIPPED_SKILL_NAMES` set in sync when names change (an installation test checks equality). Inspect installer listing/generated-page wording for assumptions about the current set. Regenerate owned copies/manifests through the installer; never hand-edit digests. |
| A capability claim | Named surface and version for a local observation, or a source and retrieval date, or an `(unverified)` tag |
| Installer or checker behavior | A regression test in `tests/`, and a `docs/ENFORCEMENT.md` row if it changes what a pass establishes |
| Files under `tests/workflows/prior-art/` | These are frozen bytes referenced by SHA-256 records. `.gitattributes` pins their line endings. Append a new dated run; do not edit a recorded one |

Line endings are LF everywhere via `.gitattributes`. If a checkout shows the whole tree as
modified, that setting is being bypassed, not obeyed.

## Reporting a problem

A behavior report is more useful with the command, the exit code and the output. Security
issues go through `SECURITY.md` instead of a public issue.
