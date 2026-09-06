# Documentation: read it, then act

Start with the [installation guide](../README.md). In an adopting project, start with its generated
HOUSERULES.md. Agents should load the short local START instructions, the chosen skill and task
inputs; the research collection is not a default context bundle.

## Human entry points

| Document | Reader / decision | Result of using it | Update trigger |
|---|---|---|---|
| [README](../README.md) | Adopter choosing an installation | Installed local entry and selected assets | Installer behavior changes |
| [GUIDE](GUIDE.md) | User choosing the next action or capability | One stage, agent surface and procedure selected | Agent added or a mapped capability changes |
| [USAGE](USAGE.md) | User setting execution bounds | A task record, bounded checks and honest usage accounting | Workflow behavior or provider accounting changes |
| [ENFORCEMENT](ENFORCEMENT.md) | Reviewer deciding what a pass establishes | Mechanical evidence separated from human judgment | Checks or contracts change |
| [Agent inventories](agents/README.md) | User/maintainer checking one surface | Correct discovery path, feature type and installation requirement | Vendor change, local observation or due recheck |
| [CONTRIBUTING](../CONTRIBUTING.md) | Contributor preparing a change | Gates run, admission criteria applied, required companion edits made | Gates, admission criteria or the companion-edit list changes |
| [SECURITY](../SECURITY.md) | Reporter deciding whether a behavior is a bug | A private advisory, or a designed-behavior answer without a report | Path containment, execution surface or the reporting channel changes |

Every GUIDE agent must appear in every stage/concern table and link its inventory. The documentation
conformance test checks that coverage. Inventory sources remain canonical; GUIDE explains selection,
not another exhaustive feature list. An inventory entry is not an installed dependency.

## Agent inputs and executable consumers

| Material | Consumer / action | Mechanism |
|---|---|---|
| AGENTS.md / CLAUDE.md | Active agent follows repository rules | Native instruction discovery/import; check.py checks structure, not obedience |
| [START](../templates/START.md) | Active agent starts or resumes bounded work | Optional AGENTS.md routing block; local workflow commands |
| [Skills](../templates/skills/) | Agent performs one selected procedure | Installed discovery paths; capability loading needs native evidence |
| [Work templates and protocol](../templates/work/README.md) | Producer writes necessary artifacts; next agent reconciles them | Copies in the task location; references, revisions and outcome review |
| workflow.json and run logs | Agent/reviewer checks attempts and evidence | workflow.py verifies selected file/log hashes and command budgets |
| skills.json / assets.json | Installer/checker verifies owned files | Recorded digests and preflight conflict checks |
| HOUSERULES.md | Human or explicitly directed agent finds installed choices | Generated links; not another auto-loaded instruction file |

Templates are optional, not forms to complete at every stage. The workflow tool does not parse
their prose. Task acceptance, reviewer independence and authority remain explicit review decisions.

## Maintainer evidence, not routine agent context

| Material | Purpose / resulting action | Maintenance rule |
|---|---|---|
| [MATRIX](../research/MATRIX.md) | Compare discovery/extension mechanisms; choose installer paths | Recheck changed or due claims before relying on them |
| [PORTABILITY](../research/PORTABILITY.md) | Decide which behavior belongs in the shared layer | Apply admission criteria to a proposed fallback; revise when evidence changes |
| [Matt Pocock study](../research/MATT-POCOCK-SKILLS.md) and [skill design](../research/SKILL-DESIGN.md) | Preserve rationale/provenance for skill decisions | Historical evidence; add corrections when reused, not periodic full rereads |
| [Workflow reports](../tests/workflows/README.md) | Reproduce or challenge a particular result | Retain dated scope/hashes; append new results rather than silently upgrading old claims |
| Skill LICENSE / NOTICE files | Preserve upstream terms, revision and adaptation history | Update with imported content/revision changes |
| [THIRD-PARTY](../THIRD-PARTY.md) | Reader checking what is original and what is adapted | Update when a skill's upstream source, revision or license changes |
| Inventory _TEMPLATE.md | Maintainer adds another agent | Follow the inventory schema, then extend GUIDE and MATRIX |
| PRIOR-ART-PLAN.md / review.md | Temporary local research/review notes | User-owned working notes, excluded from delivery/commit |

There is no automatic research refresh service. Research earns its place by supporting an installation,
admission or test decision. A new document should identify its reader, next action and update trigger;
otherwise extend the canonical document or keep it as a dated experiment record.
