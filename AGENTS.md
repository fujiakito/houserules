# AGENTS.md

## Commands

- `python check.py --repo <path>` runs against another repository; with no `--repo` it checks this
  one. Both are useful — this repository is expected to pass its own check.

## Conventions

- Every external claim carries a source and a retrieval date, or is tagged `(unverified)`. A claim
  that is cheaply testable locally is **tested, not cited** — documentation in this field contradicts
  itself often enough that a citation is not evidence.
- A local test measures **the surface you ran it on**, and these vendors ship several (CLI, desktop
  app, IDE). Name the surface and the version in the claim, and check the docs before generalising
  across them. Files on disk are not evidence of a loaded capability — a cache is not an install.
- Do not repeat content that another file here holds. Cross-reference it. The inclusion test this
  project applies to `AGENTS.md` applies to these documents too.
- Skills ship with the `hr-` prefix. An unprefixed name can collide silently or ambiguously with
  vendor built-ins.

## Do not

- Do not add a capability that duplicates an agent built-in (`init`, `verify`, `code-review`,
  `doctor`). Read `research/PORTABILITY.md` before adding anything that looks like a framework.
- Do not cite the "repository overviews are not helpful" result as settled. Table 7 (Appendix B)
  ablates the overview category and finds **no significant effect either way** — one model,
  LLM-generated files only, and on CTXBench the point estimate moved *against* the "dead weight"
  reading. The paper also shows context files **do** act as effective overviews **when the repo has
  no documentation**, which is the condition this project's omission depends on.
  See `research/PORTABILITY.md`.

## Verification

- `python check.py` must pass, and `python install.py --check` must report no drift, before a change
  is done.
