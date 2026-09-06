# Enforcement map

This maps current checks, not proposed gates. Source: local `check.py`, `install.py` and
work contracts inspected 2026-09-05. Mechanical success is limited to the predicate checked.

| Rule / contract | Current enforcement | Limit / remaining judgment |
|---|---|---|
| Claude instruction import | `check.py`: import marker present in either supported project file | Substring check only; does not parse imports or prove runtime loading |
| Instruction budget and empty sections | `check.py`: applicable instruction-chain size and empty headings | Independent nested Git repositories are excluded; inclusion value and semantic quality need review |
| Skill name coexistence | `check.py`: known reserved-name checks, with failures/warnings and generated-name exceptions | Not universal collision detection or enforcement of every `hr-` prefix |
| Skill trigger metadata | `check.py`: description-field pattern near the start of SKILL.md | Not a complete YAML/schema validator or a trigger-quality eval |
| Managed copies and ownership | `check.py`: manifest/digests; `install.py --check`: installation drift; installer preflight | Files on disk do not establish loaded capability; preflight is not transactional rollback |
| Documented command inventory | `check.py`: one-way inventory-to-reserved-name comparison | Does not establish exhaustive or current vendor coverage |
| Selected work assets | `check.py`: assets manifest/digests; installer preflight preserves modifications even with --force | Does not validate populated work records; untouched managed assets may update |
| External claims and evidence grades | Human/agent review under [evidence rules](../AGENTS.md) | No automated source/date or runtime-evidence audit |
| Exact targets, fresh evidence, finding resolution | [Consumer protocol](../templates/work/README.md#consumer-protocol) and review | No work-artifact parser; reassess changed inputs, preserve prior rounds |
| Review independence and authority | [Review protocol](../templates/work/README.md#review-by-artifact) and accountable owner | Identity labels do not authenticate sessions; evidence grade is separate |
| Optional fallback admission | [Admission criteria](../research/PORTABILITY.md#fallback-admission-criteria) | Explicit experimental trial is allowed; comparative fresh-session evidence required for recommendation/default promotion |

Run `python check.py` and `python install.py --check` before completing a change.
Script/test changes additionally require `python -m unittest discover -s tests -v`.
Neither command validates work-artifact semantics, authorizes release, or proves an agent loaded a skill.
