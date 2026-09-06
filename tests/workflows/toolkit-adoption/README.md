# Selectable toolkit adoption acceptance

Verified 2026-09-06 on Windows, Python 3.12.14. This report separates executable installer
checks, explicit skill use in the current desktop session, and independent native-loading attempts.
No comparative improvement or cross-agent coverage is claimed.

## Implemented behavior

- `install.py --list` lists the offline catalog.
- Default installation adds a local `HOUSERULES.md` entry, hr-onboard and the existing core layer.
- `--skills` selects three optional Matt Pocock adaptations (or all/none); old selections persist.
- `--work` selects templates plus their consumer guidance under `.houserules/work/`.
- `.houserules/assets.json` tracks asset digests. Modified assets stop the full installation before
  writes, including with --force. Unmodified owned assets can upgrade; user work belongs in copies.
- Missing selected assets are detected by standalone check.py. Text checkout conversion is normalized.
- The instruction-size scan stops at nested .git directories/files rather than crossing repositories.

These are explicit experimental candidates, not recommended substitutes for native capabilities.
Their MIT notices and source revision travel with each skill; installer/runtime dependencies remain
Python standard library plus the adopting project's own tools. PyYAML was used only in a separate
local validation venv to run the skill-authoring validator; it is not an installer dependency.

## Real-repository acceptance

Target: a separate local clone at Bottle commit `2a743a302a71460bfe4c0b8b7cb99a306b0328c6`.
The source/bug provenance is recorded in the [first Bottle walkthrough](../bottle-adoption/README.md).
This second checkout is `work/bottle-toolkit-20260905` in the local houserules workspace and is ignored.
It was installed with `--agents codex --skills all --work all`.

| Check | Observed outcome |
|---|---|
| Local entry and references | All 25 local Markdown links across entry, selected templates and skills resolved |
| TDD / diagnosis procedures | Explicitly read the installed skills and TDD references in this desktop session. Added GET/HEAD conditional-response regression; two subcases failed with expected 200 versus actual 304 |
| Fix and controls | Minimal conditional guard made the regression pass. Matching-tag and date-only controls also passed |
| Core suite | 359 at baseline; 360 after adding the regression, all passing. Jinja/Mako optional suites unavailable; existing ResourceWarnings retained |
| Code review procedure | Explicitly read installed hr-code-review. Produced Standards and Spec observations separately, including untracked regression and immutable target hashes; self-review disclosed |
| Local work records | Populated verification/review/findings/handoff under target work/conditional; copied actual red/green/suite logs into its evidence directory. Installed originals unchanged |
| Reinstallation | Repeat preview exit 0. Injected a modification into one installed plan template: preview and real install both refused, preserving bytes and skill digests. Restored only the injected modification; repeat preview returned 0 |
| Checker update during development | Reconciled the known previous checker copy only after proving it differed solely by this iteration's path-boundary hardening. No forced replacement of unknown content |

This is **explicit file-based use**, not successful native catalog discovery. The author knew the
bug from the first walkthrough; this is acceptance of the installed workflow, not a blind efficacy
experiment. It establishes that the materials needed to perform and record the task are locally
available and usable without returning to the distribution's research documents.

## Independent CLI attempts and limits

Codex CLI 0.153.4, configured gpt-6-astra / medium; disposable target only, no subagents or external
writes requested. Preserve failed attempts rather than turning them into a success:

| Attempt | Outcome |
|---|---|
| Sandbox-launched CLI | UnknownIssuer prevented model transport; no task result |
| Normal host, workspace-write CLI sandbox | Model started, but Windows helper setup failed before reading the entry; task reported blocked |
| Request to remove CLI sandbox | Automatic approval review rejected the unnecessary unrestricted filesystem scope. That command was not executed |
| Clean configuration, workspace-write sandbox | Usage limit returned; no task execution |
| After usage reset, clean configuration, workspace-write sandbox | Reading HOUSERULES.md was blocked by execution policy; agent reported no files changed or tests run |

**In these Codex attempts, native discovery/loading and independent execution remain unverified.** The successful manual
walkthrough must not be substituted for them. Retest in a normal user-owned Codex task with working
local tools; start at the installed HOUSERULES.md and request the selected skills. Do not remove
sandbox controls to turn a failed acceptance test green. Raw local diagnostics and token counts
are retained under `work/toolkit-runtime*`; manually executed evidence is in
`work/toolkit-manual-evidence` and the target's work/conditional/evidence directory.

### Subsequent reviewer-reported Claude loading — 2026-09-06

Source: user-supplied review R-006, read 2026-09-06, by claude-code/opus-5. This durable summary
retains its observations because the local review.md is temporary. The reviewer reports fresh
Claude Code CLI 2.1.251 sessions on Windows after `--agents claude --skills all`, with these results:

| Fixture / requested skill | Reported response |
|---|---|
| Installed / hr-tdd | `# Test-first development` |
| Installed / hr-diagnosing-bugs | `# Diagnose with a feedback loop` |
| Installed / hr-code-review | `# Review on two axes` |
| Empty repository / hr-tdd | `NOT-AVAILABLE` |
| Skill only in .agents/skills / hr-agentsonly | `NOT-AVAILABLE` |

This is reviewer-reported executed evidence supporting explicit loading on that named surface;
it is not a rerun by the implementer. The reviewer also reports that print-mode self-enumeration
returned NONE in both an installed fixture and a known-loaded control, so that instrument was
discarded. Neither observation establishes implicit triggering or comparative effectiveness.

**Instrumentation limit:** R-006 records `--allowed-tools Skill` and concludes that filesystem
tools were unavailable. Local `claude --version` / `claude --help`, executed 2026-09-06, confirmed
2.1.251 and identifies `--tools` as the selector for the available built-in tool set. The recorded
allow rule alone does not establish the claimed exclusive tool set. No raw invocation trace,
complete argv/configuration or fixture hashes accompanied R-006 in this workspace. Exclusive
Skill-tool invocation is therefore `(unverified)`; retain the positive observations without
promoting the isolated-loading claim to independently checked `tested` status. A follow-up needs
the actual Skill invocation/result trace and effective tool set, with the same negative controls.
The original Codex failures above remain unchanged; no additional model run was launched here.

## Regression coverage

Installer tests cover default/optional selection, additive selections and none, offline listing,
invalid selectors, read-only preview, local references, modified/unowned asset refusal,
source upgrades of untouched assets, malformed/path-escape manifests, missing files and newline
conversion. The nested-repository test excludes both clone and worktree boundaries while proving
that a large ordinary subdirectory still fails the instruction budget.

Skill Creator quick_validate passed for all three adaptations using PyYAML 6.0.3 in a local venv.
This validates frontmatter/scaffolding only; the behavioral evidence is the walkthrough above.

Final local verification on 2026-09-06: `python check.py` passed,
`python install.py --check` reported no drift, and `git diff --check` passed.
`python -m unittest discover -s tests -v` ran 29 tests: 28 passed and one was skipped
because Windows denied symlink creation (WinError 1314).

## Implementation targets

Original acceptance targets, before the review follow-up recorded below:

SHA-256 identifies the inspected working-tree bytes, not an immutable release. Later changes need
new verification; no commit or remote push is included in this implementation request.

| File | SHA-256 |
|---|---|
| install.py | `01caa586a6d4ff84da22244d968b51f5cae88e52efb506654ac96694850544eb` |
| check.py | `871954e8ca1452366fd94a9777e832c7ba58839f0d3c6202076f1201fc065788` |
| templates/skills/hr-tdd/SKILL.md | `29dfb65709011eafb45aa840f0bd9da5c6dfe0c7bf273ccd499a603bb7576a47` |
| templates/skills/hr-diagnosing-bugs/SKILL.md | `05f879e96569989df0e9db504e2d088584a8e5f5dd53e0c0623900ffc010b17f` |
| templates/skills/hr-code-review/SKILL.md | `efbef5d654be47cebecff2ff86d0a38f3d3422e578b6e73c928c99470cac7748` |

## Review follow-up verification — 2026-09-06

The installer closing message now applies to both preview and real installation.
NOTICE files distinguish rewritten procedures from retained TDD references; LICENSE,
source revisions, Changes lists and skill bodies are unchanged. GUIDE routes the optional
skills; the [candidate comparison](../../../research/PORTABILITY.md#experimental-candidate-comparison--2026-09-06) records source-level alternatives, not efficacy.

After these changes: 29 unittest cases, 28 passed and one Windows symlink-privilege
skip; check.py passed; install.py --check reported no drift; git diff --check passed.
All three Skill Creator validators passed. The existing [.github/workflows/check.yml](../../../.github/workflows/check.yml)
already runs unittest and both gates on Ubuntu/Python 3.11. A successful Linux run of
this revision remains unobserved here; no duplicate workflow or remote run was created.

| Follow-up target | SHA-256 |
|---|---|
| install.py | `d46471fcb81a7a0bec5a0a8bfe83f8d6759c92f6dd0418b794db854d124b15fb` |
| templates/skills/hr-tdd/NOTICE.md | `0f9b440c703ca72402956b159722885cae2c58d59b08c072d2a907c9cb58c624` |
| templates/skills/hr-diagnosing-bugs/NOTICE.md | `e928015f687dbfa13b645e125668ba5cb0f7d1d05595a8dd317f02c50f740a0d` |
| templates/skills/hr-code-review/NOTICE.md | `0dea5b629101cf7de5ab9f10bc3fb7a5745a7d6f48e2f210cad6a7842e39dee5` |
