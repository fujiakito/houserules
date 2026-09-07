---
name: hr-onboard
description: >-
  Discovers what belongs in a repository's AGENTS.md by attempting real work and recording the
  friction, rather than by scanning the codebase and describing it. Use this whenever the user
  mentions AGENTS.md, CLAUDE.md, agent instructions, a context file, steering docs, onboarding a
  repo for agents, or asks what they should write down for their coding agent - and also when they
  ask why an agent keeps making the same mistake in this repo, or want to trim an instruction file
  that has grown too long. Use it even if they do not name a file, and even if they only say
  something like "set this project up for Claude" or "make Codex work properly here".
---

# Onboard a repository

## What this does not do

**It does not scan the codebase and describe it.** A scan produces a repository overview, and an
overview fails the third condition of the inclusion test below: the agent can read the directory
tree itself. Writing down what the code already says bills on every session and is not established
to help (arXiv:2602.11988). The measurements, and the limits on what they establish, are recorded
in the houserules distribution at `research/PORTABILITY.md`; do not restate them as settled.

**This holds for a documented repository.** The same paper finds context files *do* act as
effective overviews when the repo has no documentation. If this repo is thinly documented, an
overview may earn its place - judge it, do not assume.

It also does not duplicate `/init`. If the host agent has an init command, that is a fine way to get
a starting `CLAUDE.md`. This procedure produces something different: the **non-discoverable**
knowledge, found by hitting it.

## The inclusion test

Nothing enters `AGENTS.md` unless all three hold:

1. **Instruction** — tells an agent to do or not do something, not what the project is
2. **Non-standard** — a competent agent would assume otherwise
3. **Non-obvious** — cannot be read off the code, `package.json`, `Makefile` or `README`

If a candidate fails any one, discard it. **If it can become a lint rule, a test, or a CI check, do
that instead and discard the prose** — the knowledge then costs nothing per session.

---

## Step 1 — set up from clean, and record every friction point

Do not read the setup docs first. Follow them only when stuck, and record where they were wrong or
incomplete.

- Clone or copy to a fresh directory. Do not reuse an existing build, cache, `node_modules` or venv.
- Install, build, run the test suite, and start the application.
- **Record every point where the obvious thing failed**: a command that had to run from a
  subdirectory, a service that had to be up first, an environment variable with no default, a version
  constraint that is not in the lockfile.

Each recorded friction is a candidate for **Setup** or **Commands**. Anything that worked on the
first obvious attempt is not a candidate — it is discoverable, and writing it down is pure cost.

**Also record, separately:** how long the test suite takes and whether it is green from clean. Both
decide what else is possible here; a suite that is slow or red rules out later verification steps.

## Step 2 — attempt one real task and record what went wrong

Pick a change that was actually merged recently and is small. Check out its parent, and attempt it
without looking at the merged result.

Then compare against what was merged. **The difference is the highest-signal input available** — it
is the correction, and no amount of scanning produces it.

Ask of each difference: was this a project-specific convention, or general competence? Only the first
is a candidate. General competence does not belong in an instruction file.

**If the repository has review comments on merged pull requests, read a handful.** A reviewer writing
*"we don't do it that way here, use X"* is stating a house rule that exists nowhere else.

## Step 3 — interview, briefly, and only for what steps 1 and 2 cannot reveal

Attempts reveal *what* fails. They do not reveal *why* a constraint exists, and a constraint whose
reason is invisible is exactly what an agent will violate.

Ask no more than these, and skip any that steps 1–2 already answered:

- Is there a test or check that is expected to fail? Should it be left alone?
- Is there something that looks wrong but is deliberate?
- What has an agent or a new joiner got wrong here before?
- Is there anything you must not touch, and why is that not visible in the code?
- How do you know a change is actually finished here?

Keep this short. A long interview produces a long file, and length is the failure mode.

## Step 4 — write, applying the test to each line

Fill `AGENTS.md` at the repository root — **only the sections that have content.** Delete the rest, including the
comment block. Empty sections are cost with no return.

Order does not matter as much as brevity. Before writing each line, state which of the three test
conditions it satisfies. If you cannot state all three, do not write it.

**Prefer a check over a sentence.** If a rule can be enforced by CI, a lint rule or a test, write
that instead and leave the file shorter. Put it wherever this repository already runs checks — its
test suite, linter config or CI workflow — not in a new file of your own.

## Step 5 — derive the host files

- Write `CLAUDE.md` containing `@AGENTS.md` on the first line. **This is required.** Without it
  Claude Code ignores `AGENTS.md` entirely and raises no error.
- Run the skill installer if this repository ships skills, so they land in each agent's own path —
  the `SKILL.md` format is portable, the location is not.

## Step 6 — report what was found and what was rejected

State plainly:

- how many candidates were found, and how many were written
- **what was rejected and why** — this is the more useful half, and it stops the same rejected
  candidate being proposed again next time
- what became a check instead of a line
- suite runtime and whether it was green from clean

---

## Anti-patterns

| Do not write | Because |
|---|---|
| "This project is a REST API built with FastAPI" | overview; the agent can read it from the code — fails test 3 |
| "Tests live in `tests/`" | discoverable |
| "Use TypeScript" | visible in the repository |
| "Follow best practices" | not an instruction; nothing to act on |
| A section heading with no content under it | cost with no return |
| Anything discovered by reading rather than by attempting | if reading found it, the agent can read it too |
