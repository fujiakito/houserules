# Cursor / Kiro installation acceptance

Executed 2026-09-06 on Windows with Python 3.12.14. Scope: launcher identity, local installer
behavior and delivery of budget guidance. **No native agent task or model-backed evaluation ran.**

## Surface identification

| Observation | Result | Establishes |
|---|---|---|
| cursor --version | IDE 3.19.13, dd066f332fcea7382764400fde902f61920648d0, x64 | Installed IDE launcher |
| cursor --help | Editor launcher options and an agent subcommand entry | Advertised launcher interface, not authentication or skill loading |
| cursor agent --version | Same IDE version/build | Inconclusive for a separate agent CLI version |
| kiro --version | IDE 1.0.437, 5349479558af37fecbfcdb58c199ee59d86d4dd3, x64 | Installed IDE launcher |
| kiro chat --help | IDE chat modes and window options | IDE launch interface, not headless task execution |
| PowerShell Get-Command | cursor.cmd, kiro.cmd found; agent and kiro-cli absent from PATH | Current PATH only; not proof of absence elsewhere |

The resolved .cmd launchers were inspected: both dispatch to their editor executable and
resources/app/out/cli.js. No user account configuration was read or changed. The current tool
surface cannot inspect/control native IDE UI; no model task was launched through an unobserved UI.
Official capability claims and source dates live in the [Cursor](../../../docs/agents/cursor.md)
and [Kiro](../../../docs/agents/kiro.md) inventories.

## Executed installation checks

Two fresh synthetic fixtures, each with a .git directory marker, an existing AGENTS.md, a user
configuration sentinel and a foreign hr-personal skill. These are not public-repository clones.
For each, run the distributor's install.py with `--agents cursor` or `--agents kiro`,
`--skills all --work handoff,verification`.

| Check | Cursor | Kiro |
|---|---|---|
| Preview missing installation, no writes | exit 1 | exit 1 |
| Install selected files | exit 0 | exit 0 |
| Distributor check.py --repo target | exit 0 | exit 0 |
| Repeat preview, no drift | exit 0 | exit 0 |
| Installed standalone check.py --repo target | exit 0 | exit 0 |
| Original instructions/configuration/foreign skill bytes | unchanged | unchanged |
| Installed consumer budget guidance and optional resource record | present | present |
| Modify verification template, then install | refused, exit 1; entire file snapshot unchanged | refused, exit 1; entire file snapshot unchanged |
| Restore only the injected modification, preview again | exit 0 | exit 0 |

Local evidence: `work/surface-acceptance-20260906-0kg217f7/results.json` plus each agent's evidence
directory. The local harness is `work/surface-check-20260906.py`; all are ignored and retained.
An earlier harness attempt at `work/surface-acceptance-20260906-h8ul9y7p` stopped because Windows
child stdout used a different encoding from the harness decoder. Setting PYTHONIOENCODING=utf-8
for child processes resolved that harness failure. It was not a native-agent or installer failure.

## Remaining native acceptance protocol

This is future work, not a completed checklist. Use a fresh, bounded session for each named surface.

1. Record the actual runtime version, effective agent/profile and available tools. In the IDE,
   inspect its discovered-skill UI and preserve names plus paths. On Kiro, distinguish Default
   from custom agents and record effective resource inheritance.
2. In a disposable fixture, install one hr- skill and inspect its native invocation/load trace.
   For a diagnostic probe, use a unique temporary name/body marker absent from the prompt;
   knowing a familiar heading is not sufficient evidence of how it was obtained.
3. Use fresh empty and non-discovered-path controls, retaining the same prompt structure and
   permissions. Verify the effective tool set if the experiment requires excluding direct file
   reads; an allow rule alone does not establish tool exclusion.
4. Record the actual loaded path/body and negative results. Test same-name alternate roots
   separately, especially Cursor's compatibility roots; do not infer precedence from file order.
5. Only after loading works, run one bounded task and inspect its result against existing tests.
   Explicit invocation, implicit triggering, task quality and cost are separate outcomes.

Stop a blocked experiment according to the installed budget guidance. Keep the two agents'
capability grade documented until their named runtime passes; installer acceptance does not
promote a platform. No permission relaxation, credential changes or paid-capacity enablement is
needed to retain a blocked result honestly.

## Completion checks and targets

At base commit `f68db60` with the documentation/template follow-up uncommitted:

- `python check.py`: passed.
- `python install.py --check`: no drift; the distribution's default installation remains hr-onboard.
- `python -m unittest discover -s tests -v`: 29 cases, 28 passed and one Windows symlink-privilege
  skip (WinError 1314). No claim of Linux execution.
- `git diff --check`: passed.
- 140 local Markdown links across the changed documents and both installed fixtures resolved;
  linked Markdown anchors were checked as well. External links are source-review inputs, not
  part of that local-link count.

The installer/checker implementation is unchanged from the base commit. SHA-256 below identifies
the working-tree material used in this follow-up, not a released version. Native runtime
validation, comparative model cost/quality and measured savings remain pending. No commit or
remote push was performed in this follow-up.

| Target | SHA-256 |
|---|---|
| templates/work/README.md | `81a6e5c08d7173e49da4aa12308886f9da0b29a1bf0ec3eae98770c0c5badeb0` |
| templates/work/verification.md | `78cf7a2d89c7600868bb04deb87b5d4a1076a391dc47073eb3706c1077ef0e45` |
| docs/agents/cursor.md | `69ec8eb6a6f9cc2b5fbee32759fc12352b150227bbcdcf89fde4b5ffb51a2f10` |
| docs/agents/kiro.md | `68b4e767a31b448f6fb98d2183e4b5e924ccbcf30874350daa7052a8ea904126` |
| docs/USAGE.md | `06be4bf84fc790e7235996b9396484ac88a18e88ea08e50f39c15a5d2a02d7d0` |


## Executable workflow follow-up

Executed 2026-09-06 on Windows / Python 3.12.14, with base commit f68db60 and this follow-up
uncommitted. This section supersedes the earlier completion scope where they conflict: installer
and checker changes are now implemented. Earlier observations and hashes above remain historical.

### Delivered behavior

- All 15 GUIDE stage/concern tables now map all five canonical agents, including surface limits
  and built-in versus installable features. Canonical inventories retain sources and evidence grades.
- README provides installation and task entry; docs/README.md maps each document family to a reader,
  consumer action and update trigger. Research is not routine agent context.
- Installation delivers START.md (262 words) and a standalone standard-library workflow.py.
  --activate-workflow explicitly appends the AGENTS.md trigger while retaining prior bytes.
  This repository uses that activation; it still installs only hr-onboard by default.
- The workflow records attempts, exact command argv, target/log hashes and elapsed execution time.
  It refuses exhausted budgets and unchanged duplicate passes; status detects stale selected inputs
  and evidence. Interrupted attempts require inspection. It does not validate Markdown artifacts.
- Work templates were shortened and linked to the executable consumer procedure. USAGE now includes
  actual commands and accounting boundaries, rather than reading guidance alone.

### Executed verification

| Check | Observed result |
|---|---|
| unittest discovery | 48 tests: 47 passed, one Windows symlink privilege skip |
| Installed workflow without distributor imports | Passed in a fresh Cursor/Kiro fixture; changed input invalidated evidence |
| Activation preservation | Explicit opt-in, preview read-only, original byte prefix preserved, repeat idempotent |
| Modified activation/runtime | Refused before unrelated installation writes; user changes preserved |
| Command failure, timeout, missing executable, interrupted state | Recorded or refused as specified; exhausted budget prevents another command |
| Target/log changes and command-mutated targets | Stale or unverified; cannot reuse as a current pass |
| GUIDE and human navigation | All five agents in all 15 tables; 166 local links/anchors resolved |
| Root check.py | Passed; five managed skill copies and three managed assets intact |
| Root install.py --check | No drift |
| Root installed workflow status | Current pass; repeated identical passing command refused without changing state |
| git diff --check | Passed |

The root workflow ran unittest discovery, check.py and install.py --check through a single composite
verification command. All three exit codes were zero. Local evidence remains at
work/workflow-adoption/workflow.json, run-001.log and status-after.json (ignored, retained).
Elapsed command time: 16.328 seconds; one of three allowed attempts consumed.
No model was launched by this check, and usage was null (unknown), not a measured cost saving.
The surrounding author session is shared-context; this is executable conformance evidence, not
an independent agent-quality evaluation. Latest-command freshness covers selected files, not
repository-wide environment state. Direct-child timeout is not process-tree enforcement.
Native Cursor/Kiro loading and comparative quality/cost remain pending for the reasons above.

### Current executable targets

SHA-256 identifies exact working-tree bytes; it is not a release or authenticity signature.

| Target | SHA-256 |
|---|---|
| install.py | `ac481160219eeebb0b20240cb36e53dccc7a6cc25023932ba97668131a3481a2` |
| check.py | `77ca3e5184db4ed507a7cdcd707b12c0e9370753741691edb7620e613df99a36` |
| templates/workflow.py | `8aca5fa1b1e3e28595dd136e28da826cdb535829e6cd5c644a441640000fd621` |
| templates/START.md | `16d329cb0a11f02a6b857d63bb7a8d62e34a4036352246a9135bebe6d5d7eb25` |
| tests/test_workflow.py | `783db717b073b039f22bfe7834292cb948b63c394ea4d6a7d33508ac4c7c0213` |
| tests/test_installation.py | `9c9e56b585a08302763ee7c688547e7634b12e3e8978b77aa32cdf161a144387` |
| tests/test_documentation.py | `597555a39d8537d13963683a050ab1c303e0421f62d182c76d870f1f325926c0` |
| docs/GUIDE.md | `803a32145601dbfb6358c89db358e8d64730640cf66f07485261ae50db796029` |
| local run-001.log | `22eed6f7cd81269ea06b45a60ad169cf0468b586200dd05b73524109642b9b13` |


### Compact status verification

A final refinement keeps routine run/status output short: attempt count and latest-log pointer
replace the full history dump. Complete argv/hashes/usage remain in workflow.json for explicit
inspection. The existing duplicate-pass regression also checks this output boundary.

The changed executable and test justified a second composite check under the same task budget.
Again, 48 tests ran (47 passed, one Windows symlink skip), check.py passed and install.py --check
reported no drift. Both attempts remain recorded; no task ID or budget was reset.
The second command took 15.719 seconds; combined execution time was 32.047 seconds.
Current status: verified, one attempt remaining. Source hashes below supersede the corresponding
entries above; other executable targets are unchanged.

| Target | SHA-256 |
|---|---|
| templates/workflow.py | `b56a5d70fd5bc1b8de83a14a34a27158c5e37d223ed05f52a358483dab51e4fc` |
| tests/test_workflow.py | `df644e14371f3f81b483005339c336de9bcab20b126f161bbda4efb7e26f14cd` |
| work/workflow-adoption/run-002.log | `682d568c4ffe3f28be635cab89c17e89f4d43b703a627c0e007b3ed54d5142a0` |


## Review R-010 remediation — 2026-09-06

Shared-context implementer verification. New rows below supersede the corresponding prior digest
rows for the current working tree; earlier tables and observations remain historical.
F-012 now excludes the entire work/ record area from new verification targets, with cross-task
preservation regressions. F-014 records Cursor nested skill discovery from the official skills
source rechecked via Context7 on this date, with runtime discovery still untested. F-016 explains
command result versus reusable verification in USAGE. F-017 adds a dangling-symlink regression.

Windows / Python 3.12.14: 50 tests, 48 passed, two symlink privilege skips; check.py and
install.py --check both passed. Linux Docker Engine 28.4.0 / Python 3.12.14: 50 passed, zero skips;
both gates passed. Removing `or dst.is_symlink()` in a separate Linux scratch copy caused the new
dangling-symlink test to fail (expected exit 1; mutant installer returned 0). Original source and
baseline tests remained unchanged by the mutation. No native agent loading or model evaluation ran.

Linux image: python@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea.
A snapshot excluding .git, work and the temporary review files was mounted read-only; all test and
mutation writes occurred in container-local copies, with network disabled. Local retained evidence:
work/review-fixes-20260906/linux_check.py and linux.log; Windows workflow record/log:
work/review-fixes/workflow.json and run-001.log. This is local Linux execution, not a remote CI run.

| Current target | SHA-256 (exact working-tree bytes) |
|---|---|
| docs/USAGE.md | `db5a207ec3c00d4f073133a19748281ed679577da7ea824ced66df42929bd718` |
| docs/agents/cursor.md | `4e713c4fa6dfd1051fffc3b2204bc95437e77be25dbb4e387bfa5f47b3546e71` |
| docs/agents/kiro.md | `1b0600a2af7b867729f76c7d478ee8c02edbefeae1b777a64835404c41d03d30` |
| templates/work/README.md | `4605b0f81a0efe93cbd1ab8996bfee33ea6cb6aecd3b32d75845c75c32f4c14f` |
| templates/workflow.py | `123b04596505d2deeffbdbe7f745ad0d05f79c343625ff375cf9e1b2c46f3ecf` |
| tests/test_workflow.py | `efc030b7fccd57e4fd2367ca22dcf1b17cbbe021743c70e8ff7ff029351fd2de` |
| tests/test_installation.py | `3a2d339b09d7c5f093e0b7e55befdb9bbceb5c0fdb13558588ae76c3898e4e60` |
| research/MATRIX.md | `956fc3c839037cebe25c2be29e1a8b4ae2ca3e9ab91ec0ae74e497c5566d516f` |
| work/review-fixes-20260906/linux_check.py | `58a7302c3893104e9f0576f564a9907eeecd57aa68db7ffcd0a95d08a61c639c` |
| work/review-fixes-20260906/linux.log | `a06b5c0d7865b8d2c69ee465890fef57ff09222bc99191e092258810dff5feaf` |
| work/review-fixes/run-001.log | `2c985f4210a3431b3cccc39283325d38cedc1c2b05fdb5e71af3c5456dbee6da` |
