# Enforcement map

This maps current checks, not proposed gates. Source: local `check.py`, `install.py` and
work contracts inspected 2026-09-06. Mechanical success is limited to the predicate checked.

| Rule / contract | Current enforcement | Limit / remaining judgment |
|---|---|---|
| Claude instruction import | `check.py`: import marker present in either supported project file | Substring check only; does not parse imports or prove runtime loading |
| Instruction budget and empty sections | `check.py`: applicable instruction-chain size and empty headings | Independent nested Git repositories are excluded; inclusion value and semantic quality need review |
| Skill name coexistence | `check.py`: known reserved-name checks, with failures/warnings and generated-name exceptions | Not universal collision detection or enforcement of every `hr-` prefix |
| Skill trigger metadata | `check.py`: description-field pattern near the start of SKILL.md | Not a complete YAML/schema validator or a trigger-quality eval |
| Managed copies and ownership | `check.py`: manifest/digests; `install.py --check`: installation drift; installer preflight | Files on disk do not establish loaded capability; preflight is not transactional rollback |
| Documented command inventory | `check.py`: one-way inventory-to-reserved-name comparison | Does not establish exhaustive or current vendor coverage |
| Selected work assets | `check.py`: assets manifest/digests; installer preflight preserves modifications even with --force | Does not validate populated work records; untouched managed assets may update |
| Workflow activation | Installer explicitly appends an idempotent AGENTS.md block with --activate-workflow | Routes an agent to START; does not prove it followed instructions or enable a hook |
| Command attempt/time budgets | Installed workflow.py counts attempts and bounds total direct-command elapsed time | Only commands invoked through it; not chat/token/provider spend or detached process limits |
| Repeated passing check | workflow.py refuses the same latest argv at unchanged selected targets/log | Does not deduplicate arbitrary commands or failed attempts; budget bounds retries |
| Recorded check freshness | workflow.py status compares selected target and log hashes, including before/after command inputs | Latest command only, exact files only; no environment attestation or semantic acceptance |
| Five-agent GUIDE coverage | Documentation conformance test checks every stage/concern table against inventory files | Checks mapping presence, not vendor truth or runtime capability |
| External claims and evidence grades | Human/agent review under [evidence rules](../AGENTS.md) | No automated source/date or runtime-evidence audit |
| Work-artifact targets and finding resolution | [Consumer protocol](../templates/work/README.md#consumer-protocol) and review | No prose-artifact parser; workflow freshness covers separately selected files only |
| Review independence and authority | [Review protocol](../templates/work/README.md#review-by-artifact) and accountable owner | Identity labels do not authenticate sessions; evidence grade is separate |
| Optional fallback admission | [Admission criteria](../research/PORTABILITY.md#fallback-admission-criteria) | Explicit experimental trial is allowed; comparative fresh-session evidence required for recommendation/default promotion |

Run `python check.py` and `python install.py --check` before completing a change.
Script/test changes additionally require `python -m unittest discover -s tests -v`.
Neither command validates work-artifact semantics, authorizes release, or proves an agent loaded a skill.
