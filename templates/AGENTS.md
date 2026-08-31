<!--
  AGENTS.md — read by Codex, Cursor, Copilot, Kiro, Antigravity, OpenCode and others.
  Claude Code does NOT read this file. It reads CLAUDE.md, which must contain @AGENTS.md
  on its first line. Without that import Claude Code ignores this file and raises no error.

  ── THE INCLUSION TEST ──────────────────────────────────────────────────────────
  Every line here is loaded on every session, for every agent, for everyone on the
  team, and is billed whether or not it helps.

  ESTABLISHED (arXiv:2602.11988, ETH Zurich / LogicStar.ai, 4 models, 438 tasks):
  context files do not generally improve task success rates, and cost over 20% more
  inference unconditionally. Instructions in them are well followed.

ISOLATED BUT NULL (same paper, Table 7, Appendix B): ablating the overview category
  moved accuracy 68.12%->62.32% (p=0.15) on CTXBench and 54.36%->54.20% (p=0.73) on
  SWE-bench. Not significant either way. One model, LLM-generated files only - and a
  null result is not proof overviews are useless.

  THE CONDITION THAT MATTERS: the same paper finds context files DO act as effective
  overviews when the repository has NO documentation. Omitting one is advice for a
  DOCUMENTED repo. If yours is not, an overview may well earn its place.

  Note that overviews are the default: 8 of 12 developer-written files in that study
  carried a codebase overview, and 95-100% of LLM-generated ones did. Omitting one
  here is deliberate. It is omitted because it fails test 3 below - an agent can read
  the directory tree - not because overviews are proven useless.

  So an entry earns its place only if all three hold:

    1. INSTRUCTION   it tells an agent to do or not do something — not what the project is
    2. NON-STANDARD  a competent agent would assume otherwise
    3. NON-OBVIOUS   it cannot be read off the code, package.json, Makefile or README

  If a line fails any of them, delete it. If it can become a lint rule, a test or a CI
  check, do that instead and delete it — the knowledge then costs nothing per session.

  Budget: 32 KiB (Codex project_doc_max_bytes). A configurable DEFAULT, not a hard
  ceiling - and two official pages disagree on whether it bounds each file or the whole
  root-to-cwd AGENTS.md chain. check.py enforces the stricter chain reading. Aim far under
  either way: every byte bills on every session.

  DELETE THIS COMMENT BLOCK once the file is filled. Not just for tidiness: Claude Code
  STRIPS block-level HTML comments before injecting CLAUDE.md, but Codex does NOT strip
  them from AGENTS.md. Left in place, this block is free on one agent and billed on the
  other, every session. See research/MATRIX.md section 2.
-->

# AGENTS.md

## Commands

<!-- Exact invocations that are NOT discoverable from package.json, Makefile or README.
     If `npm test` just works, do not write it down. Write the one that surprised you. -->

<!-- e.g. Run tests from the package directory, not the root — the root script exits 0
     without running anything. -->

## Setup

<!-- What a clean environment actually needs, recorded from an attempt rather than guessed.
     Run the onboard procedure to discover these; do not fill this in from memory. -->

<!-- e.g. Start the local queue with `docker compose up -d redis` before integration tests,
     or they hang with no output. -->

## Conventions

<!-- Only where this project differs from what an agent would assume, AND the reason is not
     visible in the code. "We use TypeScript" is visible. "We do not use the ORM's relation
     loading because it N+1s under our access pattern" is not. -->

## Do not

<!-- Constraints whose reason is invisible. This section is usually the highest-value one
     because it is the least recoverable from reading the code. -->

<!-- e.g. Do not fix `test_legacy_import` — it is expected to fail until the 2.0 migration
     lands. Chasing it burns a session. -->

## Verification

<!-- How to confirm work is actually done here. Agents skip verification unless told to,
     and the check they invent is usually weaker than yours. -->

<!-- e.g. A change is done when `make check` passes AND the app starts — the test suite
     does not exercise the startup path. -->
