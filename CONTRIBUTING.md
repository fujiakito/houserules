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

## Commit conventions

Use [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
(retrieved 2026-09-07) for commits and PR titles:

```text
type(scope): short description
```

- Use `feat` for new behavior, `fix` for bug fixes, `docs` for documentation,
  `test` for tests, `refactor` for restructuring, `ci` for CI, or `chore` for maintenance.
- Scope is optional. Write a short imperative description: `fix(installer): preserve user files`.
- Keep each commit focused on one coherent change. Use the body for the reason and validation.
- For breaking changes, add `!` before `:` and a `BREAKING CHANGE:` footer explaining migration.
- Name branches `<type>/<topic>`, reusing the types above, lowercase and kebab-case:
  `fix/preserve-user-files`, `docs/close-evaluation`. Lead the topic with an issue number
  when one exists: `fix/123-preserve-user-files`. Open a PR against `main` and use squash
  merge with a compliant PR title; retain any breaking-change footer in the final commit message.
- An agent session often opens on a generated placeholder branch such as
  `claude/amazing-carson-mxs5dr`. Set the name when the session starts, or rename before opening
  the PR. The branch name is the first summary a reviewer reads; a generated one says nothing.
- Amend or rewrite published commits only when authorized; use `--force-with-lease` when pushing
  an authorized rewrite.

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
| A changed installed asset (`templates/START.md`, `templates/work/*`, `templates/ci/*`, root `check.py`) | Its entry in `check.ASSET_PATHS`, a re-run of the installer against this repository so the digests in `.houserules/assets.json` advance, and any document naming the file. Adopters reconcile a modified copy by hand, so a rename is a migration, not an edit. |
| A new or changed shipped skill | Canonical `templates/skills/<name>/` source, admission status/evidence, README and relevant GUIDE choices, installation/drift tests and upstream notices/THIRD-PARTY when applicable. Installer discovery is automatic; keep `check.py`'s explicit `SHIPPED_SKILL_NAMES` set in sync when names change (an installation test checks equality). Inspect installer listing/generated-page wording for assumptions about the current set. Regenerate owned copies/manifests through the installer; never hand-edit digests. |
| A capability claim | Named surface and version for a local observation, or a source and retrieval date, or an `(unverified)` tag |
| Installer or checker behavior | A regression test in `tests/`, and a `docs/ENFORCEMENT.md` row if it changes what a pass establishes |
| Files under `tests/workflows/prior-art/` | Three kinds of content live here and the rule differs. **Captured observations** — the evidence files (captured outputs, harness, aggregation input) and, in an attempt record, the per-call results in `pairs` with their scores, argv, timestamps and usage, plus `input_hashes_measured` — are frozen bytes referenced by SHA-256 records; `.gitattributes` pins their line endings. Never edit them: append a new dated run instead. **Derived values and producer provenance** — `aggregate`, `evidence_file_sha256`, `derivation` — may be corrected when the derivation itself was wrong (a miscomputed statistic, a producer that changed), never to alter what was observed; the correction entry carries the previous value. **Interpretation** — `findings`, `conclusion`, `limitations` and the various notes — may be amended when a later review shows it wrong, since a record asserting something known false serves its next consumer worse than one carrying a correction. Any amendment appends an entry to the record's `corrections.amendments` array giving the date, the commit, why, and the fields changed grouped by those three kinds. Field paths are arrays of literal key segments, never dotted strings — a key may contain a dot, so a dotted path cannot be parsed back. Every changed derived or provenance field is listed in `derived_field_history` with its previous value, or marked `added` when the commit introduced it; a lookup that cannot resolve a path is an error, not an omission. `recorded_date` keeps naming the execution, not the edit |

Line endings are LF everywhere via `.gitattributes`. If a checkout shows the whole tree as
modified, that setting is being bypassed, not obeyed.

## Reporting a problem

A behavior report is more useful with the command, the exit code and the output. Security
issues go through `SECURITY.md` instead of a public issue.
