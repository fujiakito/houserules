# AGENTS.md

## Commands

- `python check.py --repo <path>` runs against another repository; with no `--repo` it checks this
  one. Both are useful — this repository is expected to pass its own check.

## Conventions

- Every external claim carries a source and a retrieval date, or is tagged `(unverified)`. A claim
  that is cheaply testable locally is **tested, not cited** — documentation in this field contradicts
  itself often enough that a citation is not evidence.
- Do not repeat content that another file here holds. Cross-reference it. The inclusion test this
  project applies to `AGENTS.md` applies to these documents too.
- Skills ship with the `hr-` prefix. An unprefixed name can silently replace a bundled skill.

## Do not

- Do not add a capability that duplicates an agent built-in (`init`, `verify`, `code-review`,
  `doctor`). Read `research/PORTABILITY.md` before adding anything that looks like a framework.
- Do not cite the "repository overviews are not helpful" result as settled. It is correlational and
  no ablation isolated it — see the source-strength table in `research/PORTABILITY.md`.

## Verification

- `python check.py` must pass, and `python install.py --check` must report no drift, before a change
  is done.
