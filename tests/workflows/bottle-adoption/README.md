# Bottle adoption walkthrough

Date: 2026-09-05. **Executed local adoption and bug-fix walkthrough, not a paired efficacy eval.**
Houserules revision: `af8e465`. Surface: this Codex desktop task, shared author context;
app build unavailable. Runtime: Windows, Python 3.12.14 in a fresh venv.
No new model session or native skill-discovery probe was run. The operator read and followed
`hr-onboard`; copied files alone are not proof that a new agent would load it.

## Target and task

Public source: [bottlepy/bottle](https://github.com/bottlepy/bottle), retrieved 2026-09-05.
Cloned with depth 40; inspected revision `62d7e07` then checked out the parent of a small recent fix:
[`2a743a302a71460bfe4c0b8b7cb99a306b0328c6`](https://github.com/bottlepy/bottle/tree/2a743a302a71460bfe4c0b8b7cb99a306b0328c6).
Task: reproduce and correct conditional static-file responses when both If-None-Match and
If-Modified-Since are supplied. The merged patch
[`b73bd1db5b7a915cf6a78656955c4059f58195ae`](https://github.com/bottlepy/bottle/commit/b73bd1db5b7a915cf6a78656955c4059f58195ae)
was viewed only after saving the independent fix and its passing regression.
These source links share the retrieval date above. No issue, PR, commit or push was made upstream.

The checkout is local and ignored under `work/adoption-bottle-20260905`; logs are under
`work/adoption-bottle-evidence`. The upstream README appeared during repo selection, so this is
not a fully blind setup exercise. Existing upstream AGENTS.md was read before work and retained.

## Observed execution

| Step | Actual result |
|---|---|
| Clone | Sandbox Git failed TLS setup; normal Git clone succeeded with escalation, without disabling certificate checks |
| Fresh venv, package build/install | Bottle 0.14.dev0 wheel built and installed. First pip attempt hit cache-directory permission error; --no-cache-dir succeeded |
| Initial unittest invocation | A first call used the wrong cwd (operator error). From target root, discovery without -t . caused relative-import errors; package-aware discovery resolved those |
| Baseline suite | 359 tests ran, 6 failures caused by CRLF template fixtures. Restoring test/views/*.tpl from exact Git blob bytes made all 359 pass in 0.371 s (0.69 s process time) |
| Install houserules | install.py --repo work/adoption-bottle-20260905 --agents codex succeeded; existing AGENTS.md hash unchanged |
| Installed checker and repeat preview | Target check.py passed; repeating install.py with --check exited 0, no drift |
| New regression before fix | GET and HEAD subcases expected 200 but observed 304; regression failed |
| Independent fix | Guard date processing when the entity-tag header is present; regression passed and 360 tests passed |
| Upstream comparison | Same conditional-precedence intent; upstream also covered matching-tag/old-date behavior. Added that direction for GET/HEAD; 361 tests passed in 0.379 s (0.72 s process time) |
| Application smoke test | Started Bottle via stdlib WSGI server on 127.0.0.1 with an ephemeral port; GET /health returned 200 and adoption-ok; server closed |
| Handoff / verification | Manually populated target work/cache-condition using this repo's contract; neither was installed or automatically discovered |

Jinja2 and Mako tests were omitted by upstream when dependencies were unavailable; this is core
suite coverage, not every optional integration. Existing ResourceWarnings remained. Tests imported
the checkout source, not the installed wheel. The test checkout has uncommitted source/test changes,
local venv and installed files; template byte restoration also appears in Git status under this
machine's conversion settings. No bulk cleanup was performed.

The independent fix checks header-key presence; upstream uses header-value truthiness. Behavior
for an empty header was not settled by this exercise. Do not claim exact semantic equivalence.
Final local bottle.py SHA-256: `741d2482aa5e992b2a3244ceede391e8ae1db0430e3e1baa755525a9420036fe`.
The independently saved patch predates the upstream comparison and complementary test.

## What the adopting project actually received

- Existing AGENTS.md preserved byte-for-byte.
- .agents/skills/hr-onboard/SKILL.md, check.py, CLAUDE.md import and ownership manifest installed.
- No local GUIDE, work templates, Matt Pocock or other optional skills were installed.
- No hooks or MCP configuration were added. A green checker did not reveal these absent workflows.
- The operator returned to houserules to use the work contract and manually create the handoff.

That establishes installer preservation and repeatability on this repository. It does **not**
establish that houserules caused the bug fix to succeed: there was no without-houserules control,
and reproduction, code editing, testing and upstream comparison used the operator's general tools.

## Onboarding candidates and rejected instructions

Five friction candidates were considered; **zero new AGENTS.md instructions were written**:

| Candidate | Disposition |
|---|---|
| Git TLS backend failure | Local sandbox/environment issue; not a Bottle house rule |
| pip cache permissions | Local environment issue; invocation workaround, not a recurring project instruction |
| unittest package context | Discoverable in relative imports and existing test setup; no duplicated instruction |
| Template line endings | Real checkout-sensitive failure, already detected by tests. Prefer a separately reviewed Git attribute fix over prose; no unrelated upstream policy change made here |
| Missing installed workflow material | A houserules product gap, not a rule Bottle's AGENTS.md should carry |

Wrong cwd was operator error and was not promoted into a sixth candidate. No maintainer interview
or unsolicited review-comment interaction occurred. No new lint/CI rule was necessary for the
conditional bug: executable regression tests were added in the isolated checkout.

## Product implications and next implementation slice

The distribution layer works, but the workflow remains manual. Prioritize these concrete gaps:

1. Install a short adopter-facing entry point that shows what was installed, what is optional,
   and how to start a task without returning to this repository.
2. Offer selective installation of local work templates plus their consumer guidance. Keep full
   research inventories out of default session context; do not require every artifact per task.
3. Offer explicit optional skill selection with provenance and dependencies. Installation smoke
   checks and experimental status should enable trial use; comparative evidence governs stronger
   recommendations, not whether any optional capability can be tried.

Acceptance for that slice: in a fresh adopting checkout, a user can locate the selected guidance,
create a handoff/verification artifact and use a selected procedure using only installed material.
Repeat installation must preserve their edits. Native loading must be tested on the claimed surface.
The current walkthrough demonstrates the gap; it does not implement or validate that future slice.

## Local evidence digests

Raw logs remain in the ignored local evidence directory; these hashes identify this machine's
records, not downloadable artifacts. The commands above permit a separate reproduction, whose
counts can change with Python, optional dependencies and source revision.

| Log | SHA-256 |
|---|---|
| baseline-lf.log | `fd0a44f0a50e8b793522d5725bc35d9d7b14854bd4fd3896a9a033a4dbb2ee97` |
| baseline.log | `080368ffce8e9c5b292c222733b144887019cb2758ff77a1c396d3427413a82c` |
| install-package.log | `04d29be473b958b6c8f91987d96eb0297833f5aac3dc7ce3c1cfb3b376a2e83b` |
| installed-check.log | `2267a0ba9168b4d8b6f8af377e4afd25cfbeea27ee018878ffe6cb1957d095f2` |
| regression-after.log | `23d535201e913e1daf6b3ae60c5f53965978e84a8ab246cebba008b567d2c893` |
| regression-before.log | `ddef5a75d6572c48c0dba6efb52d84fe7c82a764ea221333c2ff45384651e4e6` |
| suite-after.log | `95350496e430c18841e9ec541982ae59df354a7965f0ee8128ef6f9d8539c9a6` |
| suite-final.log | `4399edc95b817d47406a5b3babce761308f89bb6de9e3cb71da37f0c992cfdeb` |

## Additional checker boundary finding

After the walkthrough, running houserules' own check.py counted the ignored nested clone's
AGENTS.md as part of the parent instruction chain (3,513 B total). The target is a separate Git
repository with its own .git directory. The check still passed, but the printed chain shows that
nested-repository boundaries are not excluded by this scan. Record this as a checker-scope issue
for a focused regression/fix; it is separate from whether any native agent loaded those files.
The ignored checkout is retained, so subsequent local checks will continue to expose it.

Houserules completion checks: check.py passed; install.py --check reported no drift.
