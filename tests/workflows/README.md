# Worked contract pilot: skill coexistence

**Distribution note:** R-002 is a local review record excluded from this repository's published
files. Its identifiers below are provenance labels, not file links. Unavailable links were removed
before commit; recorded criteria, checks, hashes and dispositions are unchanged.

**Latest evidence:** [Round 3](#round-3--source-upgrade-and-conflict-remedies) records the later upgrade fixes; prior rounds retain their original revisions.

**Revision notice:** Round 1 below describes a superseded code revision; see [Round 2](#round-2--preflight-and-ownership-verification) for later evidence.

**Recorded 2026-09-05.** A compact, retrospective record of the actual change in this repository,
using the [work artifact protocol](../../templates/work/README.md). It combines small records in
one file rather than creating every template. This is dated evidence, not a second live policy.

**Execution context:** one Codex desktop conversation, shared author/reviewer context; desktop
build version unavailable in the app context. All executable evidence below is native Windows
PowerShell with Python 3.12.14 and Git 2.51.0.windows.1. This tests local scripts, not skill loading
in Codex, Claude Code or Antigravity. No fresh-context or cross-agent trial was performed.

## Spec → review → revise → scope decision

The user requested portable contracts with optional fallbacks and explicitly authorized proceeding.
This task addresses the observed foreign-skill sync failure; it does not add an SDLC skill suite.

| Record | Input | Action and output |
|---|---|---|
| S-001, original requirement | Prior adoption fixture: a user skill only in `.claude/skills` caused four missing-copy failures | Preserve user skills and check only content this project manages |
| R-001, self-review | S-001 and installer options | F-001: a name prefix alone cannot establish ownership; selected agents, legacy installs and conflicts need explicit behavior |
| S-002, revised contract | F-001 and existing installer behavior | Criteria below; explicit names/paths/digest record, additive selections and an unknown legacy state |
| Scope decision | User's instruction to proceed in this conversation | Implementation is authorized within that scope. This record does not invent a separate product acceptance or release approval |

S-001 and S-002 above reconstruct the reasoning; they are not preserved, independently reviewed
spec snapshots. That limits this pilot to illustrating the protocol, not proving input recovery.

| Criterion | Observable result | Executable evidence in `tests/test_installation.py` |
|---|---|---|
| AC-001 | Foreign skill bytes stay unchanged and are not copied to other agent paths | `test_foreign_skill_is_preserved_and_not_replicated`, `test_prefix_does_not_claim_ownership` |
| AC-002 | Selected installs pass; later selections add managed paths | `test_selected_agents_and_additive_install` |
| AC-003 | Missing recorded roots, extra support files and identically modified copies fail sync | `test_absent_recorded_root_fails`, `test_extra_support_file_is_drift`, `test_same_change_to_every_copy_is_still_drift` |
| AC-004 | A same-name conflict is neither overwritten nor enrolled | `test_same_name_conflict_is_never_owned_or_overwritten`, symlink integration test below |
| AC-005 | Preview writes nothing; invalid metadata blocks installation before writes | `test_preview_is_read_only_and_idempotent_after_install`, `test_invalid_manifest_blocks_before_writes` |
| AC-006 | Missing ownership metadata reports unknown; a successful installer run establishes it | `test_legacy_ownership_is_unknown_until_installer_runs` |
| AC-007 | Different bytes cannot be hidden by equal file size and mtime | `test_matching_size_and_mtime_do_not_hide_different_bytes` |
| AC-008 | UTF-8 text checkout conversion preserves the baseline; binary changes remain significant | `test_text_checkout_line_endings_do_not_invalidate_baseline`, `test_binary_line_endings_remain_significant` |

## Build → review → fix → verify

Base: Git commit `35034a86ec54dd8012865e65ab354401be7d4cf9`. Reviewed scope: working-tree changes
to `check.py`, `install.py` and the new, untracked-at-review regression file. Both tracked changes
and the untracked tests were inspected; a committed-only diff would omit the tests.

| Finding | Evidence and correction | Disposition |
|---|---|---|
| F-001 | Directory union treated foreign skills as managed. Explicit `.houserules/skills.json` records source digests and selected paths; unknown ownership stays unknown. | Verified for AC-001–006 on the tested filesystem surface |
| F-002 | `filecmp.dircmp` could use shallow equality; installer and checker did not share the same content comparison. Both now use the same byte-based tree digest. | Verified by AC-007 regression |
| F-003 | The installer excluded existing symlinks from its no-force conflict guard. The guard now also protects differing or broken symlinks. | Proposed fix; source reviewed, real symlink integration verification blocked by Windows privilege |
| F-004 | An adopting repository may convert text to CRLF on checkout. Digests now normalize line endings for UTF-8 text while preserving binary bytes. | Verified by AC-008 regressions; simulated text conversion on Windows, not a second OS run |

F-003 remains unverified on a real symlink. The test is retained and will execute on a filesystem
where symlink creation is permitted. A skipped test must not close that finding as verified.

### Revision check

The first 11-test pass inspected an earlier installer. Its SHA-256 was
`f7fb60c4c078673f7f19c9702c5e09c052b20feba36804ce8114aaca526d9537`.
The symlink correction changed those bytes. That old pass was not reused: the suite was rerun
with the added integration case, then again after F-004. These are the final file digests for this record:

| Target | SHA-256 |
|---|---|
| `check.py` | `512fd037a625065549b19e5755b8594fd25a5666b21ab051e94be00453e16842` |
| `install.py` | `bd3a7f9a962cf07c00985fd0f38c4d90d29bb374aab75e67d5cc313da193cf3c` |
| `tests/test_installation.py` | `dbaec849b89e1e7262ee3a330ab47baf38f44c5d8ac088b0c622162cfc3a08b3` |

This demonstrates revision invalidation during a shared-context task. It does not test whether
a fresh agent detects a stale artifact unaided. Later code changes need new evidence; do not
silently update the hashes to carry this verdict forward.

### Verification V-001

From the repository root, using the bundled Python interpreter where `python` is not on PATH:

```text
python -m unittest discover -s tests -v
python check.py
python install.py --check
git diff --check
```

The regression run discovered 14 tests: 13 passed, 1 skipped (`test_different_symlink_is_preserved`,
Windows error 1314: symlink creation privilege unavailable). No `--force` was used. Test fixtures
are retained in OS temporary directories; the suite performs no recursive cleanup.
`check.py` passed, `install.py --check` reported no drift, and `git diff --check` passed.

## Next consumer

For future fallback admission, run the [consumer protocol](../../templates/work/README.md#consumer-protocol)
in a fresh session on each claimed surface, using an actual project artifact and a deliberately
stale revision. Record whether it recovers the inputs, routes review/fix/verification correctly,
and preserves an unresolved finding. Also run the symlink integration test where supported.
These are explicit validation limits, not prerequisites for using the optional draft templates.


---

## Round 2 — preflight and ownership verification

**Recorded 2026-09-05; Verification V-002.** This round supersedes V-001 for the file revisions
below. V-001's hashes, test count and conclusions remain unchanged as historical evidence.
Input: independent local review R-002 and its round-2 follow-ups (not shipped).
Execution: original Codex desktop authoring context, native Windows PowerShell, Python 3.12.14;
app build version unavailable. This is author verification, not a fresh independent review.

### Additional acceptance criteria

These extend AC-001–008 for the stricter preflight design. AC-006 is narrowed by AC-011:
unknown ownership fails when a shipped-name path exists, while unrelated skills still warn.

| Criterion | Observable behavior | Regression in `tests/test_installation.py` |
|---|---|---|
| AC-009 | A conflict in a mixed agent selection stops the entire install before writes | `test_mixed_agent_conflict_stops_before_any_write` |
| AC-010 | A root checker conflict also prevents skill and scaffold writes | `test_root_file_conflict_stops_before_skill_writes` |
| AC-011 | A shipped-name path with no ownership record fails the actual checker without claiming or changing user content | `test_missing_manifest_with_shipped_name_fails_without_claiming_ownership` |
| AC-012 | The standalone shipped-name catalogue stays aligned with installer sources | `test_standalone_shipped_name_catalog_matches_sources` |
| AC-013 | Conflict preview and installation report the same refusal, except for their mode banner, and neither advertises writes that cannot run | Output comparison added to `test_mixed_agent_conflict_stops_before_any_write` |

### Finding dispositions at this revision

| Finding namespace / ID | Current disposition |
|---|---|
| Pilot F-002, shallow comparison | Still verified: the equal-size/mtime regression passes at the revisions below. |
| Pilot F-003, symlink preservation | Still proposed fix, not verified on a real symlink: Windows error 1314 skips the test. Preflight covers symlink conflicts in source, but CI configuration alone is not execution evidence. |
| R-002 F-002, unrecorded partial writes | Verified by AC-009 and AC-010. Known conflicts refuse the entire selection before writes; no rollback claim for I/O errors or concurrent edits. |
| R-002 F-003, missing ownership record | Verified by AC-011 and AC-012. Names identify ambiguity, not ownership; unrelated user skills remain outside managed sync. |
| R-002 F-011, misleading preview | Verified by AC-013. The new comparison failed before the fix; both modes now share the same preflight. |

### Verification V-002

Scope: current working-tree script changes and the untracked regression suite, including
preflight and preview behavior. No commit or hosted CI run was made. Commands were run from
`C:/Projects/houserules` with the bundled Python interpreter.

| Command | Actual result |
|---|---|
| `python -m unittest discover -s tests -k mixed_agent -v`, before the preview fix | Failed on the preview/install output comparison, reproducing F-011. |
| `python -m unittest discover -s tests -v`, after the fix | 18 tests: 17 passed, 1 skipped for Windows symlink privilege error 1314; exit 0. |
| `python check.py` | Passed; five managed copies match the installed source; exit 0. |
| `python install.py --check` | No drift, no writes; exit 0. |
| `git diff --check` | Passed. |

| Target | SHA-256 |
|---|---|
| `check.py` | `61e3955899d2baae962dd6ae1d1e2b5cb703b658dc58b8e63abd709f224e11ba` |
| `install.py` | `e21f057fe9fd541d15212d3167d346ce61ef3e64929f0184ab76ff8848cb4475` |
| `tests/test_installation.py` | `060ab2c61a37938142c91c5f8be8d073f38255820fac501658c17187a730eb32` |

### Next consumer for round 2

Independent reviewer: verify this round's digests and AC-009–013 at the next review. Keep the
pilot's F-003 open until an observed Linux run executes and passes the real symlink test.
Linux CI remains configured but unobserved in this task. No agent skill loading or fresh-context
artifact recovery was tested by this round.


---

## Round 3 — source upgrade and conflict remedies

**Recorded 2026-09-05; Verification V-003.** Current evidence for the revisions below; earlier
rounds remain historical. Inputs: local review R-002 F-012–014 (not shipped).
Author verification in the original Codex desktop context, native Windows PowerShell, Python
3.12.14; app build version unavailable. No independent-verifier claim.

| Criterion | Expected behavior | Evidence |
|---|---|---|
| AC-014 | A root checker conflict gives a root-file remedy; changing agents is explicitly insufficient. Preview and install agree. | Enhanced `test_root_file_conflict_stops_before_skill_writes` |
| AC-015 | A changed skill source cannot advance the shared digest while omitting a recorded path; refusal preserves the target and old valid baseline, even with `--force`. | `test_source_upgrade_requires_all_recorded_paths`, preview and actual refusal branches |
| AC-016 | After explicit reconciliation of the old fixture file, selecting all recorded paths plus the new path completes the upgrade and passes the installed checker. | Same upgrade test: v1 Codex → v2 partial Claude refused → Codex+Claude upgrade → installed `check.py --repo` exit 0 |
| AC-017 | Verify-stage guidance uses Claude's project skill path and distinguishes the cross-agent installer pattern. | GUIDE text inspected against the canonical Claude inventory; link targets checked. No runtime invocation claimed. |

**Dispositions:** R-002 F-012 is corrected and locally verified; F-013 is fixed by refusing partial
source upgrades before writes rather than changing the manifest schema or automatically replacing
old copies; F-014 is corrected in the guide. Root checker version tracking remains a future design
option. Pilot F-003 (real symlink preservation) remains proposed and unverified on this machine.

**Verification V-003:** from `C:/Projects/houserules` using bundled Python:

| Check | Actual result |
|---|---|
| New upgrade and root-remedy assertions before fixes | Both failed, reproducing the missing upgrade refusal and inapplicable root remedy. |
| `python -m unittest discover -s tests -v` after fixes | 19 tests: 18 passed, 1 skipped for Windows symlink privilege error 1314; exit 0. |
| `python check.py` | Passed; exit 0. |
| `python install.py --check` | No drift or writes; exit 0. |
| `git diff --check` | Passed. |

The upgrade fixture uses its own source copy; it does not change this repository's shipped skill.
`--force` is exercised only in rejected partial upgrades and a read-only preview. The successful
full upgrade follows an explicit write to one known fixture file; no recursive deletion or
forced directory replacement was performed.

| Target | SHA-256 |
|---|---|
| `check.py` | `61e3955899d2baae962dd6ae1d1e2b5cb703b658dc58b8e63abd709f224e11ba` |
| `install.py` | `301047038ee95842367dcdb8e544b4e5c9f72f2b003f07e7628d5d93b1245425` |
| `tests/test_installation.py` | `f357c51df5d4000b4de44116fc305a7bbfeeff888718e5142630ae48c7cdfa89` |
| `docs/GUIDE.md` | `32a1b14082146c95d1d63d12787f739d59c711a5b69f483b08eed92620c08967` |
| `README.md` | `0932481c69f38b8a5b5cafa628294cccbe5d88b95541e5a4236b7c44a37235a0` |

**Next consumer:** independently recheck AC-014–017. A successful upgrade requires the complete
recorded path selection and resolved conflicts; automatic migration of a differing root checker
is not implemented. No Linux CI run or fresh-agent skill loading was observed in this round.


## Prior-art follow-up

See the [paired artifact-consumption smoke trial](prior-art/README.md) for its frozen
packets, outcome rubric, execution status and limitations. This is separate from the historical
author-only pilot above; neither upgrades untested vendor surfaces.


## Public-repository adoption walkthrough

[Bottle adoption](bottle-adoption/README.md) records a real clone/install/bug-fix walkthrough,
installer preservation, manual workflow gaps and its shared-context evidence limits.


## Selectable toolkit acceptance

[Toolkit adoption](toolkit-adoption/README.md) covers the implemented local entry, optional Matt
skills and work templates, preservation tests, and the explicit native-loading limitation.
