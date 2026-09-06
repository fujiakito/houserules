# Superpowers: stage coverage and portable fallback analysis

**Research snapshot: 2026-09-06.** Reader: a houserules maintainer choosing a procedure to
evaluate. Next action: select one candidate and a named target surface for comparison.
Revisit when that candidate, its host adapter or its target model changes; this is not a
second live vendor inventory. No skills are installed or promoted by this study.

## Scope and evidence

The subject is **obra/superpowers**, not every plugin in its marketplace or the separate
historical superpowers-skills repository. GitHub's recursive tree was enumerated at
[`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`][tree]; it contains **14**
`skills/<name>/SKILL.md` entry points. All 14 bodies were retrieved, together with the
reviewer/implementer templates and Codex/Antigravity tool references used below.
The [plugin manifest][manifest] declares **6.3.0**; this identifies the inspected source,
not the latest released package or an installed runtime. All upstream links below use
that revision, retrieved **2026-09-06**. Context7 supplied initial discovery; pinned source
bodies settle differences with indexed summaries. This is source analysis, not a Superpowers
runtime test or a quality/cost benchmark.

Project understanding comes from [README](../README.md), [GUIDE](../docs/GUIDE.md),
[PORTABILITY](PORTABILITY.md#3-the-rule), the four canonical skill bodies under
[`templates/skills/`](../templates/skills/), and the
[work artifact protocol](../templates/work/README.md). houserules already permits evaluated,
optional fallbacks for a gap on one surface even when another surface has a built-in.
Its durable contribution is shared task context, procedures and evidence across agent switches.

Native comparisons reuse GUIDE's dated inventories:
[Claude Code](../docs/agents/claude-code.md), [Codex](../docs/agents/codex.md),
[Antigravity](../docs/agents/antigravity.md), [Cursor](../docs/agents/cursor.md),
[Kiro](../docs/agents/kiro.md). Their evidence dates and runtime limitations remain in those
files; this study does not refresh every vendor claim. Catalog availability, installation,
session exposure and successful execution are different states.

## All 14 skills, grouped by primary GUIDE stage

The stage assignment and comparisons are this study's analysis. Secondary stages show reuse;
a skill appearing at a stage does not cover every operation in that stage.

| Primary stage | Skill / source | Trigger and result | Dependencies / secondary stages |
|---|---|---|---|
| 1. Onboard & Context; cross-cutting | [using-superpowers][using-superpowers] | Session bootstrap: select relevant skills before responding or acting; process skills precede implementation skills. | Host discovery/bootstrap and sibling skills; spans the lifecycle. It does not discover repository operating rules. |
| 2. Intent | [brainstorming][brainstorming] | Refine intent and compare approaches. Classifies spike, bounded and architectural work; uses chat designs for bounded changes and a written spec for architectural work. | Human approval on every path; optional visual companion; architectural path calls writing-plans. Also 3. Spec & Architecture. |
| 4. Plan | [writing-plans][writing-plans] | Convert accepted requirements into tasks with paths, interfaces, implementation/test details and global constraints; self-check coverage and consistency. | Plan/spec files; directs execution to SDD or executing-plans. Also 3/5; no task-tracker backend. |
| 5. Build | [executing-plans][executing-plans] | Inspect a written plan, execute its tasks and checks, stop on blockers and finish the branch. | Worktree and finishing skills; prefers SDD if subagents exist. Also 4/6/8; sequential fallback. |
| 5. Build | [subagent-driven-development][subagent-driven-development] | Fresh implementer per task, combined task review with spec/quality verdicts, scoped fix reviews and final branch review; maintains a plan ledger. | Subagents, model routing, Git, helper scripts, sibling skills and templates. Implementers run sequentially. Also 4/6/7/8. |
| 5. Build | [dispatching-parallel-agents][dispatching-parallel-agents] | Divide independent investigations/tasks, provide focused contexts, then inspect and integrate results. | Actual concurrent subagents and non-conflicting state. Also 6/11; inappropriate for coupled failures. |
| 5. Build | [using-git-worktrees][using-git-worktrees] | Detect existing isolation, prefer host worktree tools, otherwise use Git; perform setup and establish a test baseline. | Git/shell or native tools, project setup commands. Also 1/4; respects an existing worktree preference. |
| 5. Build | [test-driven-development][test-driven-development] | Observe a meaningful failing behavior test, implement minimally, pass and refactor. Includes testing anti-pattern guidance. | A runnable test seam; broad test-first policy with human-approved exceptions. Also 6/11. |
| 6. Verify | [verification-before-completion][verification-before-completion] | Match a completion claim to an executed command, read the result and distinguish tests, builds, requirements and bug evidence. | Shell/project checks; text guidance, not a runner or enforced gate. Also 7/8/11. |
| 7. Review | [requesting-code-review][requesting-code-review] | Prepare requirements and a Git range, dispatch a reviewer, triage severity and respond to findings. | Reviewer subagent and bundled code-reviewer template. Also 5/8; it orchestrates review rather than supplying a scanner. |
| 7. Review | [receiving-code-review][receiving-code-review] | Validate feedback against the code, clarify uncertainty, reject incorrect suggestions with evidence, implement and test accepted changes. | Code/tests and supplied feedback; forge tools only for online replies. Also 11. |
| 8. Release | [finishing-a-development-branch][finishing-a-development-branch] | Verify, identify branch/worktree state, offer merge/PR/keep choices and perform selected integration/cleanup. | Git, forge access for PRs and user choice. Also 6; branch integration is only part of Release. |
| 11. Diagnose & Remediate | [systematic-debugging][systematic-debugging] | Reproduce and trace the cause; compare working patterns, test hypotheses, fix and verify. Reassess architecture after repeated failed fixes. | Actual diagnostic signals and test tools; links TDD/verification and tracing/waiting references. Also 6. |
| 12. Maintain the engineering system | [writing-skills][writing-skills] | Author discoverable skills using baseline failure scenarios, candidate runs and wording tests; choose instruction form for the observed failure. | Fresh-context eval capability, TDD background and optional authoring helpers. Does not prove another host loads the skill. |

Supporting files such as `root-cause-tracing.md`, `condition-based-waiting.md`,
`testing-anti-patterns.md`, `code-reviewer.md` and SDD reviewer prompts are references/templates,
not additional independent skill entry points. The first three are linked by
[systematic-debugging][systematic-debugging] and [TDD][test-driven-development]; the
[review template][review-template] supplies the actual general review rubric.

## Comparison across all 12 GUIDE stages

Existing choices are representative, not another exhaustive command inventory. Follow each
GUIDE stage for all five agents and exact availability. **Added structure** means a procedure
is more explicit in Superpowers; it is not evidence that the native agent cannot do it.

| GUIDE stage | Superpowers grouping / contribution | Existing skill/tool comparison | Still needed / gap type |
|---|---|---|---|
| [1. Onboard & Context](../docs/GUIDE.md#1-onboard--context) | using-superpowers; worktrees support setup. | hr-onboard extracts rules from actual friction; native initializers, Rules and Steering load context. A bootstrap router does a different job. | Provisioning, discovery validation and reproducible project setup remain project/host work. No Superpowers equivalent to hr-onboard's friction filter. |
| [2. Intent](../docs/GUIDE.md#2-intent) | brainstorming gives a repeatable interview and option comparison. | Goals persist execution intent; Antigravity's interview and Kiro requirements overlap; research/MCP obtain external facts. | Stakeholder decisions, incoming-request triage and evidence collection. A goal command alone is not an interview. Candidate for a procedural fallback where direct interaction demonstrably misses requirements. |
| [3. Spec & Architecture](../docs/GUIDE.md#3-spec--architecture) | brainstorming writes the architectural spec and self-checks it. | Native planning/Kiro Specs author artifacts; design/visualization tools explore UI; project spec rubric critiques requirements. | Specialist architecture, domain/security constraints and independent spec critique when warranted. Visual companion does not replace a design system or specialist analysis. |
| [4. Plan](../docs/GUIDE.md#4-plan) | writing-plans; execution preflight inspects feasibility. | Native plan modes and Kiro tasks already sequence work; project plan/handoff can preserve it. | Portable acceptance links, unresolved decisions, migration order and tracker ownership. Detailed code-in-plan is a choice to evaluate, not automatically better than a concise plan. |
| [5. Build](../docs/GUIDE.md#5-build) | executing-plans, SDD, parallel dispatch, worktrees and TDD. | Native coding/worktrees/subagents execute; hr-tdd already supplies a focused test-first procedure. | Stack expertise, permissions and execution runtime. Select one implementation route; layering two controllers or two TDD procedures needs evidence of added value. |
| [6. Verify](../docs/GUIDE.md#6-verify) | verification-before-completion plus TDD and execution checks. | Claude verify/run, shell/CI/browser and hr-tdd supply execution or test method; workflow.py checks recorded evidence freshness. | Appropriate test selection, UI/runtime access and protected gates. No dedicated verify command does not mean no verification capability. Superpowers adds claim discipline, not missing tooling. |
| [7. Review](../docs/GUIDE.md#7-review) | requesting/receiving-code-review, SDD task and final reviews. | hr-code-review already separates Standards/Spec and pins working-tree scope; native reviewers and security tools answer different review questions. | General review is not dedicated security scanning, accessibility or an independent spec/plan review. Feedback disposition is a possible supplement; never count a proposed fix as verified. |
| [8. Release](../docs/GUIDE.md#8-release) | finishing-a-development-branch; review/verification prerequisites. | Git/CI, commit plugins, Codex yeet and native PR capabilities overlap integration mechanics. | Versioning, changelog, package publication, provenance and release policy. An integration menu does not implement the whole Release stage. |
| [9. Deploy](../docs/GUIDE.md#9-deploy) | No dedicated skill; planning/checking methods are only supporting processes. | Provider plugins/skills/Powers and project CI/CD execute deployment. | Environment readiness, rollout, migration, rollback and health contract may need a portable runbook; credentials/provider tools remain necessary. |
| [10. Observe](../docs/GUIDE.md#10-observe) | No dedicated skill; debugging consumes observations after a problem. | Telemetry integrations supply signals; schedulers trigger work. | Signal selection, thresholds, ownership and incident routing may benefit from a procedure. A skill cannot create telemetry storage, access or a scheduler. |
| [11. Diagnose & Remediate](../docs/GUIDE.md#11-diagnose--remediate) | systematic-debugging; receiving review; TDD/verification; parallel investigation when independent. | hr-diagnosing-bugs already covers causal hypotheses and verified fixes; native debug/CI repair and Kiro Bugfix Spec overlap parts. | Telemetry access, domain diagnosis and operational mitigation. A repair command is not a complete root-cause method; a method is not an incident-response platform. |
| [12. Maintain the engineering system](../docs/GUIDE.md#12-maintain-the-engineering-system) | writing-skills; using-superpowers supports discovery. | hr-onboard improves repo guidance; skill-creator/create-skill tools author skills; doctor/config tools inspect the client. | Cross-host loading tests, comparative quality/cost evaluation and maintained adapters. Authoring, runtime health and architectural maintenance are separate tasks. |

**Coverage verdict:** Superpowers provides a broad development workflow through branch integration,
with debugging and skill authoring. It does **not** supply the complete 12-stage contract defined by
GUIDE. Deploy and Observe lack dedicated skills; Onboard and Release have partial coverage.
This is a conclusion from the complete entry-point inventory above, not a claim that its agents
cannot perform those tasks.

The three cross-cutting concerns also remain: host/CI controls enforce authority, repository-visible
records preserve evidence, and accountable people own decisions. See GUIDE's
[cross-cutting concerns](../docs/GUIDE.md#cross-cutting-architecture-concerns).
Labels such as HARD-GATE and Iron Law express instructions; neither the label nor a bootstrap hook
proves compliance. Evaluate actual behavior, and use protected controls for enforceable conditions.
This distinction does not make a procedural instruction useless.

## What is useful to carry over, and what needs adaptation?

| Finding in inspected source | Implication for houserules |
|---|---|
| [Worktree skill][using-git-worktrees] explicitly prefers native tooling and supplies a Git fallback. | Superpowers itself demonstrates that a shared method and native execution can coexist. Preserve host-managed state and project setup commands. |
| [Brainstorming][brainstorming] scales artifacts but still requires fresh approval on every path. | Its default interaction can conflict with already-authorized autonomous work. Adapt approval rules to task authority and risk; do not import the gate automatically. |
| [Verification][verification-before-completion] asks for a command run in the current message; [task reviewer][task-reviewer] discourages rerunning existing checks without a specific doubt. | Reconcile freshness explicitly. The existing workflow status/hash mechanism can support reuse for unchanged inputs; rerun when evidence is stale or insufficient. A prose report alone is not authenticated execution. |
| [Receiving review][receiving-code-review] stops all implementation when any item is unclear. | Independent, already-clear fixes can proceed under this project's task contract while the genuinely dependent item waits. Avoid making unrelated uncertainty block everything. |
| [TDD][test-driven-development] says to delete implementation written before tests. | Keep the behavioral red/green method; never discard user work to satisfy a ritual. Scale tests to behavior and project policy. |
| [SDD][subagent-driven-development] routes model tiers, caps fix loops and keeps scratch evidence in a git-ignored plan workspace, then deletes it on clean completion. | Preserve the user's model choice, stop limits and durable evidence. Its recursive cleanup conflicts with this repository's deletion rule. These are adoption changes, not instructions executed by this study. |
| [Writing skills][writing-skills] uses baseline comparisons and distinguishes rule violations from malformed outputs. | Useful evaluation ideas; observed obedience is still not sufficient evidence of task quality or cross-agent compatibility. Do not generalize upstream anecdotes or cost claims to this project. |
| [Bootstrap][using-superpowers] aggressively invokes potentially relevant skills. | An always-on router needs its own benefit test; GUIDE and focused descriptions may already select the right procedure with less overhead. |

Source drift matters: [README][readme] still describes batch checkpoints and a four-choice finish
menu. The inspected [execution body][executing-plans] directs all-task execution, and the
[finish body][finishing-a-development-branch] offers three normal options, with discard only
after an explicit request. Current [task-reviewer template][task-reviewer] combines two verdicts
in one reviewer. [Plan writing][writing-plans] and [brainstorming][brainstorming] use self-review;
there are no separate spec-review or plan-review SKILL.md entry points. Evaluate the pinned
body and dependencies, not a familiar description of an older release.

## Cross-agent adoption decision

**The proposed direction aligns with current project scope.** A less-equipped agent is a valid
fallback target. Another vendor's rich plugin catalog does not fill that target's gap. Equally,
an absent dedicated command does not prove a gap: direct agent work with shell/files may already
meet the contract. Even an official marketplace plugin is an installable choice, not automatically
a fresh-install built-in.

The [upstream README][readme] documents **14 installation routes**: Claude Code, Antigravity,
Codex App, Codex CLI, Cursor, Devin CLI, Factory Droid, Gemini CLI, GitHub Copilot CLI,
Grok Build CLI, Kimi Code, OpenCode, Pi and Hermes Agent. This makes
Superpowers an existing cross-agent candidate worth testing before maintaining a fork. It does
not establish that those routes work here, or that an unlisted future agent is supported.

The [porting guide][porting] separates shared actions, host tool mappings and startup delivery.
Its full-pack acceptance requires automatic startup activation; explicit per-session use is not
accepted as a complete upstream port. houserules can still support explicitly selected procedures.
Do not equate 14 installation routes with 14 independently tested adapters or a session-start hook
on every host: the pinned [Codex manifest][codex-manifest] sets `hooks` to an empty object.
Kiro is not among the 14 named README routes. All are source observations, retrieved 2026-09-06.

| Target situation | Selection recommendation |
|---|---|
| User's chosen native or installed skill meets the task contract | Reuse it; add only missing durable evidence. No universal native-over-third-party ranking. |
| No dedicated skill, but direct execution works reliably | A short direct procedure can be the baseline; installation may add no value. |
| Repeated method failure despite sufficient tools | Compare direct execution, an existing Superpowers/other skill, and a small hr- fallback. |
| No subagents | Use a sequential procedure; do not promise SDD by copying its Markdown. Independent review can be a separate session when available. |
| No shell, browser, provider access or telemetry | Identify the required adapter/tool/human step. A procedural fallback alone cannot complete execution. |
| Future host supports reading files but no native skills | Explicitly provide the selected procedure and artifacts; label automatic discovery unsupported until demonstrated. |

The [Codex adapter][codex-adapter] and [Antigravity adapter][agy-adapter] are themselves
host-specific assumptions. For example, the pinned Codex reference allows overrides on
full-history forks, whereas this Codex desktop session's exposed collaboration schema forbids
them. This is a **session schema observation on 2026-09-06**, not an executed spawn test;
desktop app version was not captured. The live schema must win. Tool-name mapping is not proof
of runtime compatibility; Gemini CLI and Antigravity are separate surfaces.

Keep three concerns separate in any candidate: **portable procedure and artifact contract**,
**host adapter** (loading/tools/permissions), and **optional model guidance**. Switching agents
should preserve intent, criteria, revision, findings and next action even if execution changes.
One canonical skill body can serve multiple hosts; identical tool calls are not required.

## Candidate priorities, not a one-skill-per-stage backlog

1. **Test the existing overlap first:** compare hr-tdd, hr-diagnosing-bugs and hr-code-review
   with the corresponding Superpowers procedures and the active native/direct baseline.
   Avoid creating three additional competing implementations without a measured benefit.
2. **Evaluate focused gaps:** requirements clarification, portable planning, artifact critique,
   review-feedback disposition and evidence handoff are possible experiments. Existing templates
   may be sufficient; spec and plan review can initially share a contract with separate rubrics.
3. **Study operational tasks separately:** deployment readiness/rollback and observation triage
   need project/provider evidence. Superpowers is not enough source material for these stages.
4. **Defer a universal controller:** first demonstrate that users/agents choose the wrong next
   procedure. Extend host support through actual adapter/loading tests rather than blanket claims.

For promotion, apply [the existing admission criteria](PORTABILITY.md#fallback-admission-criteria).
A useful trial holds repository revision, task, host/model, permissions and tools constant across
baseline and candidates, using fresh contexts and repeated runs. Include a small no-skill task,
a missing dependency, conflicting user guidance and stale handoff evidence. Then run a fresh
session handoff across the claimed hosts. Measure delivered behavior, missed/false findings,
unnecessary pauses, recovery, tool calls, elapsed time and reported usage; unknown cost stays unknown.
These are proposed trials, not results of this research.

The machine-local Claude plan path reported in [GUIDE](../docs/GUIDE.md#4-plan) establishes a
transfer concern, not that the plan is unreadable, cannot be reviewed or cannot be exported.
Compare an explicit repository-visible output request and the existing plan/handoff templates
before claiming a demonstrated need for a new planning skill.

Two possible debugging references were inspected at the same revision on 2026-09-06:
[root-cause tracing][tracing] and [condition-based waiting][waiting]. They offer concrete techniques,
but are not ready to copy as dependency-free additions: tracing calls a sibling `find-polluter.sh`,
and waiting links a TypeScript example. The waiting example uses polling and permits justified
delays for timing behavior; it does not prohibit every sleep. A future adaptation should preserve
relevant dependencies/provenance or replace those bindings, then test its added value over the
existing diagnosis procedure. No reference files were imported by this review.

The inspected [license][license] is MIT. If material is later adapted, follow this project's
[provenance requirements](../CONTRIBUTING.md#proposing-a-skill), including pinned source and
LICENSE/NOTICE beside shipped skills. This study links and analyzes upstream; it vendors no skills.

## GPT-6 Astra and Claude Fable 5.1 prompting

The official guidance and operational tuning summary now live in
[USAGE: Model differences](../docs/USAGE.md#model-differences), with their 2026-09-06 retrieval dates.
For this adoption decision, the consequence is to evaluate the complete model/host/task combination:
stronger instruction following can amplify conflicting skill rules, and changing the model cannot
supply a missing tool or loader. No model quality or token-saving improvement was measured here.

[tree]: https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills
[manifest]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.claude-plugin/plugin.json
[readme]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md
[license]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/LICENSE
[brainstorming]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md
[dispatching-parallel-agents]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/dispatching-parallel-agents/SKILL.md
[executing-plans]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/executing-plans/SKILL.md
[finishing-a-development-branch]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/finishing-a-development-branch/SKILL.md
[receiving-code-review]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/receiving-code-review/SKILL.md
[requesting-code-review]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/requesting-code-review/SKILL.md
[subagent-driven-development]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md
[systematic-debugging]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/systematic-debugging/SKILL.md
[test-driven-development]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/SKILL.md
[using-git-worktrees]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-git-worktrees/SKILL.md
[using-superpowers]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-superpowers/SKILL.md
[verification-before-completion]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/verification-before-completion/SKILL.md
[writing-plans]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md
[writing-skills]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-skills/SKILL.md
[task-reviewer]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/task-reviewer-prompt.md
[review-template]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/requesting-code-review/code-reviewer.md
[codex-adapter]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-superpowers/references/codex-tools.md
[agy-adapter]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-superpowers/references/antigravity-tools.md
[porting]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/porting-to-a-new-harness.md
[codex-manifest]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.codex-plugin/plugin.json
[tracing]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/systematic-debugging/root-cause-tracing.md
[waiting]: https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/systematic-debugging/condition-based-waiting.md
