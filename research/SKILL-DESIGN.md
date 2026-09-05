# Skill design: tasks, artifacts and coexistence

**Status: dated design proposal and evidence record; not adopted policy.** This file has no
routine refresh commitment. Current task selection belongs in GUIDE.md, capability facts in the
agent inventories, and the optional artifact contract in templates/work/README.md. Retain the
research rationale here without keeping duplicate live procedures in sync. Revisit only for a
specific adoption decision or when evidence invalidates a recorded conclusion.

This snapshot predates adoption of the scope in [PORTABILITY.md section 4](PORTABILITY.md#4-what-the-boilerplate-therefore-ships)
and the installer changes demonstrated by the [worked pilot](../tests/workflows/README.md).
Its descriptions of the original scripts remain historical evidence.

**Research and local inspection: 2026-09-05.** This is a design recommendation, not a claim that
new skills or a cross-agent runtime have been implemented. [GUIDE.md](../docs/GUIDE.md) is the
human entry point; [agent inventories](../docs/agents/README.md) own capability facts;
[work artifacts](../templates/work/README.md) define the optional consumer-facing pilot.

## What the project actually provides

Source inspection and a temporary-directory test on **native Windows, Python 3.12.14**,
2026-09-05, establish the following. This measures the repository scripts, not a running agent.

| Surface | Current behavior | Design implication |
|---|---|---|
| [install.py](../install.py) | Discovers templates/skills and copies them to configured project paths; seeds root instructions/check.py. A fresh fixture installed hr-onboard; no work directory was created. | Work templates are opt-in references. Adding one does not silently impose a pipeline on adopters. |
| [check.py](../check.py) | Checks known directory-name collisions, frontmatter presence and cross-path content consistency within the supplied repo. | It is not a complete catalog of user/global/plugin skills and does not prove skill execution or semantic equivalence. |
| Foreign project skills | Adding only .claude/skills/foreign-example to the installed fixture made check_sync report it missing from four other locations. | Legitimate vendor-specific user skills are currently treated as portable-layer drift. Fix ownership tracking before claiming seamless coexistence. |
| [Work templates](../templates/work/README.md) | Original handoff is a short state/pointer; findings are append-only. The new optional pilot adds artifact identity, actions and review dispositions. | Keep state, stage output and historical evidence separate. Avoid expanding handoff into an omnibus spec. |
| [Canonical inventories](../docs/agents/README.md) | Human/reference tables with source grades and surface constraints; not loaded capability manifests. | Agent readers need a targeted lookup protocol, not every inventory in their prompt. |

The fixture did not overwrite an existing skill or use force mode. The scripts remain unchanged
by this design pass. The foreign-skill failure is a known implementation gap, not a recommendation
to replicate user skills or run the installer's destructive replacement path.

## A stage is a navigation category

The useful design unit is a **coherent task with a recognizable trigger and output**. Classify it
by operation, artifact, risk and required capability; map it to one or more stages afterward.

| Same stage, different purpose | Difference | Run all of them? |
|---|---|---|
| Goal / interview / research | Persist execution intent / decide requirements / gather facts | Only the missing part. Research cannot decide a stakeholder's preference. |
| General spec / architecture / UI design | Describe behavior / resolve technical trade-offs / explore visible interaction | UI work may need all three; a backend change may need no visual design. |
| Plan / ticket decomposition / decision mapping | Sequence known work / make work independently assignable / resolve unknowns | A bounded change needs no wayfinding map. |
| Code review / security review / simplify | Find implementation defects / analyze security concerns / reduce unnecessary complexity | Choose relevant review questions. Equivalent full reviews can duplicate cost without adding evidence. |
| Test design / test runner / browser check | Decide meaningful assertions / execute checks / observe a running interface | Complementary capabilities, not interchangeable skills. |
| Skill / plugin / template | Procedure / distribution package that may contain tools and skills / output shape | Installing a plugin is not executing every skill inside it. |

Native tool roles are sourced through the existing inventories' **2026-09-04 baseline**;
[Matt's individual skill bodies](MATT-POCOCK-SKILLS.md) were inspected at the pinned snapshot.
No vendor command was executed merely to fill this comparison, and gated capabilities have not
been benchmarked. In particular, Claude's UI design capability is not a general spec authoring
contract, and an implementation reviewer is not automatically a spec or plan reviewer.

### When to split a skill

Keep a single procedure when the same trigger leads to the same objective, inputs and output,
with only a small reference branch. Split when there are independent invocation needs, materially
different expertise/tools/authority, or a genuine context/role boundary.

For example, a proposed artifact-review procedure could share target identification, finding IDs
and verdict rules, loading a spec or plan rubric as needed. Split into separate spec-review and
plan-review skills only if their triggers or procedures become substantially different. A code
security scanner needs different capabilities and should remain a specialist.

The [Agent Skills authoring guidance](https://agentskills.io/skill-creation/best-practices)
(retrieved 2026-09-05) recommends coherent units, warns against both excessive splitting and overly
broad scope, and supports conditional references, templates and validation loops. It does not
prescribe a skill per SDLC stage.

**Agent-first does not remove review.** It lets the agent select an appropriate route inside the
task's contract. Humans still decide intended outcomes and authority. A review earns its place
when it can find a meaningful defect against explicit criteria, or when project policy requires
it. Routine work can use a direct self-check; uncertain/high-consequence work can use a separate
review context. See [artifact-specific rubrics](../templates/work/README.md#review-by-artifact).

A spec-author → spec-reviewer → planner → plan-reviewer route is valid when the risk warrants it.
It is not four compulsory skills. The same capable host may perform those roles in separate
sessions; different agents/models are optional, not evidence of independence by themselves.

## Portable core, explicit dependencies, optional adapters

Recommended boundaries:

| Layer | Owns | Avoid |
|---|---|---|
| Portable procedure | Task method, trigger, inputs, outputs, evidence, stopping conditions | Hard-coded host commands, mandatory tracker accounts, hidden sibling-skill dependencies |
| Artifact contract | IDs, revisions, decisions, review findings and next consumer | A second copy of an adopter's existing spec/tracker |
| Project/stack configuration | Real test commands, domain constraints, tool versions, release policy | Generic templates that silently dictate the adopter's language or architecture |
| Host/provider adapter | Skill discovery/invocation, sandbox, worktrees, scheduler, external integrations | Claiming a prompt supplies missing runtime capability |
| Protected check | Machine-testable requirements and required evidence | Treating an advisory skill as enforcement |

Prefer an instruction-only core when it is sufficient. **Dependency-free is a useful default,
not the overriding objective.** A small declared script or existing project test runner can be
more reliable than a long prompt. Keep stack packages optional; specify minimum capabilities
such as file access, shell execution or an independent review session.

houserules may offer a default work layout while accepting equivalent artifacts elsewhere.
That preserves adoption flexibility. A skill that only works after installing the whole
houserules ecosystem would require stronger evidence than a focused procedure.

The [existing portability analysis](PORTABILITY.md#3-the-rule) already separates contracts from
vendor conveniences. The [Matt audit](MATT-POCOCK-SKILLS.md#does-a-portable-fallback-fit-the-project)
records why the blanket exclusion of built-in duplicates is too broad for host-specific gaps.
That exclusion remains the current shipping rule; this pass adds no replacement built-in skills.

## Handoff, spec and review are different artifacts

The implemented **optional pilot**, including the A → B → A example, is defined once in
[Work artifacts](../templates/work/README.md). Its design choices are:

- Keep handoff as current state and routing. Add the next action independently of the stage.
- Give acceptance criteria, tasks, reviews, findings and verification runs stable IDs.
- Bind findings and verdicts to exact revisions, including working-tree scope when relevant.
- Let review reports record coverage and link findings; let the append-only ledger own findings
  and their proposed-fix/verified/reopened/decision events.
- Treat a fixer's completion claim as a proposed fix until the relevant evidence is checked.
- Reuse existing documents by reference and create only artifacts a later consumer needs.

These are proposed project contracts, not a standard schema certified by a vendor. No automated
schema gate currently enforces them, and a live cross-host trial remains necessary. Merely putting
files in a working directory does not transfer them to another clone or remote environment.

## Existing skills and duplicates

Three different problems need different handling:

| Situation | Detect / resolve |
|---|---|
| Same source installed in several paths | Compare canonical source identity, resolved paths, version and content hash. Confirm what the host actually loads before treating every copy as independently active. |
| Same name, different contents/source | Inspect the host's resolution rules and selected source. An hr- prefix lowers collision risk; it does not prove uniqueness or fix a mismatched frontmatter name. |
| Different names, overlapping behavior | Compare triggers, inputs, outputs, side effects and evidence. Names/hashes cannot decide semantic equivalence. Prefer the user's chosen provider when it meets the contract. |

**Inspect availability in the active environment**, not only the repository. Use the host's skill
listing/selector and plugin state when available, then inspect documented project, ancestor,
personal/global and admin roots within the accessible scope. Examples include Claude's personal
`~/.claude/skills/` and Codex's `~/.agents/skills/`; vendor-specific system/plugin locations may
also exist. Exact surface paths and enumeration methods stay in
[Claude](../docs/agents/claude-code.md#15-skill-loading-precedence-and-where-it-differs-by-surface),
[Codex](../docs/agents/codex.md#6-extension-points) and
[Antigravity](../docs/agents/antigravity.md#9-skills).

Current official documentation, retrieved 2026-09-05:

- [Claude skill resolution](https://code.claude.com/docs/en/skills): enterprise/personal/project
  source precedence can shadow a bundled name; plugin namespacing avoids that name collision.
- [Codex local discovery](https://learn.chatgpt.com/docs/build-skills): repo/user/admin/system roots
  can contribute skills; duplicate names are not merged and can both appear in selectors.

Neither behavior prevents two differently named skills from giving conflicting advice.
Documentation of a path is not proof that its contents are loaded. Distinguish **on disk**,
**enabled**, **exposed to the session**, and **successfully invoked**. Inaccessible global state,
remote account skills and unenumberated plugins stay **unknown**, not absent. Do not scan unrelated
personal files or require users to disclose their whole global configuration.

Recommended adoption behavior, **not implemented yet**:

1. Ask the host for available candidates; inspect only relevant skill metadata/bodies.
2. Honor an explicit user choice. Otherwise compare the task contract and recommend one provider.
3. Reuse an existing fit; add only the missing artifact/evidence supplement.
4. Install an optional fallback only for a confirmed gap. Do not automatically disable, rename,
   overwrite or uninstall user skills.
5. Manage only files this installer owns. A future ownership manifest should record source and
   hash; checks should leave foreign skill directories outside the managed sync contract.
6. Recheck relevant availability at invocation/update time. Do not persist every local/global skill
   into repository instructions, or promise deterministic selection from an incomplete scan.

Current limitations include project-root-only directory-name checks, no semantic duplicate
detector, no complete global/plugin inventory and no user-selectable per-skill install profile.
A green `check.py` result must not be presented as “no other skills conflict.”

## Does the project need an ask-matt equivalent?

**Not yet as a required skill.** There is currently one shipped hr- procedure. The revised human
guide supplies task selection; good skill descriptions supply the host's normal discovery.
A router earns its own place only if real users repeatedly choose the wrong procedure or cannot
find the correct one.

If that happens, a small optional `hr-help` is a better scope than a universal workflow controller.
Its input is the user's problem, current artifact/action and active-host capabilities. Its output
is one next action, one selected implementation, the required inputs/output and a short reason.
It should say “no extra skill needed” when that is the right answer.

The router should read the same canonical capability descriptions; it should not maintain a
second catalog of vendor facts, invoke every stage, recursively invoke routers, install packages
or perform external writes merely because it recommended them. The name here is a design candidate,
not an installed or callable skill.

## What evidence supports this design?

All sources below were retrieved **2026-09-05**. They support parts of the recommendation;
**none proves this project's exact skill boundaries, router or artifact schema is optimal**.

| Source / grade | Supports | Does not establish |
|---|---|---|
| [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices), maintainer guidance | Coherent tasks, clear defaults, proportionate instructions, conditional references and validation | The ideal number of skills for this repository |
| [Agent Skills evaluations](https://agentskills.io/skill-creation/evaluating-skills), maintainer guidance | Compare with/without a skill using realistic cases and fresh contexts; inspect outcomes and cost | That a syntactically valid skill helps |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), Anthropic engineering guidance, 2024-12-19 | Simple composition; routing; evaluator/optimizer loops when criteria are clear and iteration adds value | Mandatory reviewers at every stage; its tooling examples are historical |
| [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), Anthropic engineering guidance, 2026-01-09 | Outcome/trajectory evidence and a mix of deterministic, model and human grading | A universal automatic quality score |
| [SkillsBench v4](https://arxiv.org/html/2602.12670v4), research preprint, 2026-06-14 | 87 tasks, 18 model/harness configurations; curated skills raise aggregate pass rate from 33.9% to 50.5%; gains vary | Arbitrary market packs helping equally. The paper notes curated selection and limited transfer to GUI/multi-agent/long-horizon work; compact-bundle observations are not a universal three-skill limit |
| [SWE-Skills-Bench v1](https://arxiv.org/html/2603.15401v1), research preprint, 2026-03-16 | 39 of 49 tested skills show no pass-rate improvement; version/context mismatch can hurt | All skills being useless. Experiments use one configuration, Claude Code + Claude Haiku 4.5, and preselected one-skill-per-task use |

The studies examine different tasks and configurations. Their contrast is a reason to test the
actual task/host combination, not to pick the more convenient headline. Peer-review status is not
established here; do not describe these as vendor certification or settled universal results.

### A practical evaluation before adding skills

Start with a real failure. Compare the **same task, repo revision, host/model version, permissions
and tool availability** under: baseline, existing candidate skill, and proposed supplement/fallback.
Use fresh contexts and repeat enough to expose variability; never infer portability from one success.

Include: a positive trigger, a near-miss that should not trigger, a small task needing no added
process, an unavailable dependency, a conflicting user skill, a stale spec/plan revision, and a
review → fix → verify handoff. Observe actual selected source and behavior, not just the final claim.

Grade delivered behavior, missed/false findings, requirement coverage, handoff recovery, authority
violations, tool/token cost and human effort. Use execution checks for executable criteria; use
independent human judgment for ambiguous product/design quality. Keep test expectations independent
of the implementation and inspect traces when they disagree with outcomes.
This follows the [paired evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills)
and is still a proposed experiment, not results from this pass.

## Reusing Matt's work and researching other packs

The pinned [Matt license](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/LICENSE)
is **MIT**, with **Copyright (c) 2026 Matt Pocock**. It permits copying/modifying/distributing subject
to retaining the copyright and permission notice in copies or substantial portions. A source
hyperlink by itself does not replace those notices. The
[OSI MIT text](https://opensource.org/license/mit) states the same notice condition.
Both were checked 2026-09-05.

| Reuse | Repository treatment |
|---|---|
| Copy/adapt skill prose, templates or scripts | Preserve the full upstream license and copyright notice with the distributed material. Record original URL, pinned commit and our changes. Place notices inside the adapted skill directory if that directory is installed/copied independently. |
| Independently implement a general method | Write original instructions; record methodological inspiration for provenance. Do not label close paraphrases of a copied procedure as independent merely because wording changed. |
| Include other bundled assets or dependencies | Check their own licensing; the repository-level MIT label is not evidence about separately sourced material. |

The method/expression distinction is described by the
[US Copyright Office](https://www.copyright.gov/help/faq/faq-protect.html) (retrieved 2026-09-05):
methods and ideas are distinguished from their protectable expression. This is US guidance;
a specific reuse/jurisdiction can require a separate legal assessment. This pass creates original
project templates and links to upstream; it does not vendor Matt's skills.

Research other packs **by missing scenario**, not by star count or stage coverage claims.
For each candidate, record source/version/license, trigger, output contract, dependencies,
side effects, invocation restrictions, host assumptions, maintenance status and a task-level
baseline comparison. First compare available official capabilities and the user's own skills.
Review a whole framework only if the task needs its orchestration; do not adopt its ecosystem
just to obtain one useful procedure.

## Recommended next implementation decision

Trial the optional artifact protocol on one real spec review and one code fix, then measure whether
a procedure or router is actually missing. Before expanding installer scope, address managed-file
ownership and foreign-skill sync. Add a small optional fallback only after demonstrating its value
on a named host/surface; keep future-host support explicitly unknown until tested.
