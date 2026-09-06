# The AI-native SDLC, by stage

This guide maps a complete software lifecycle to the capabilities currently available in Claude
Code, Codex, and Google Antigravity:

`Onboard → Intent → Spec → Plan → Build → Verify → Review → Release → Deploy → Observe → Diagnose/Remediate → Maintain`

Three concerns apply across the whole lifecycle rather than forming more stages: **Control Plane &
Authority**, **Evidence & System of Record**, and **Human Governance**.

**This file is for people, not agents.** Anything an agent must act on belongs in `AGENTS.md`, a
skill, or a deterministic check, expressed as a trigger rather than background prose.

**Canonical tool facts live in [`agents/`](agents/)** — especially
[`claude-code.md`](agents/claude-code.md), [`codex.md`](agents/codex.md), and
[`antigravity.md`](agents/antigravity.md). The tables below are a routing layer only. Follow those
inventories for evidence grade, install state, feature flags, provider, version, plan, and surface
restrictions.

**Native mapping checked 2026-09-04; project-skill routing updated 2026-09-06.**
Claude Code and Codex are locally tested; Antigravity is official-documentation-only.
The inventories retain the surface versions and retrieval date for each claim.
Recheck policy is in `../research/MATRIX.md`.

## Choose the next action

Start with the stage that matches your **current problem**, then pick one row under **Choose by
purpose**. The tools in a stage serve different jobs; they are not a checklist to run in full.
Expand **Tools by agent** only when you need the exact native option and its availability limits.

| I need to… | Start here |
|---|---|
| Understand the repo or clarify the request | [Onboard](#1-onboard--context) → [Intent](#2-intent) |
| Define behavior, architecture or UI | [Spec & Architecture](#3-spec--architecture) |
| Turn an accepted design into executable work | [Plan](#4-plan) → [Build](#5-build) |
| Check behavior or critique an artifact/change | [Verify](#6-verify) / [Review](#7-review) |
| Deliver or operate the system | [Release](#8-release) → [Deploy](#9-deploy) → [Observe](#10-observe) |
| Fix a failure or recurring friction | [Diagnose](#11-diagnose--remediate) / [Maintain](#12-maintain-the-engineering-system) |
| Switch agents or resume after feedback | [Work artifacts](../templates/work/README.md) |

A **tool** executes an action; a **skill** supplies a procedure; a **plugin** distributes capabilities;
a **template** carries output to its next consumer. Choose an implementation already available to
you that meets the task's needs, including your own or preferred third-party skill. Native tools
and project procedures below are options with known provenance, not a requirement to replace yours.

These purpose tables describe **jobs to do**, not a recommended third-party skill catalog. Researching
a skill does not add it to the project's supported or recommended set. Project-owned skills must
also justify their value and coexist with the user's choices. New research should improve a task
contract or validate a specific gap; it should not automatically expand this guide's tool list.

The project covers the full SDLC through contracts. Recommended/default fallbacks require
[evaluated gaps](../research/PORTABILITY.md#fallback-admission-criteria); experimental candidates
can be explicitly selected before promotion. The
[candidate comparison](../research/PORTABILITY.md#experimental-candidate-comparison--2026-09-06)
records alternatives and open evidence requirements. A stage does not require
its own skill, and missing native tooling does not prevent using a direct procedure.

The [work artifact templates](../templates/work/README.md) are optional pilot drafts.
Use your existing spec, plan or review format when it carries the information the next consumer needs.

## How to read the tables

| Type | Means |
|---|---|
| **built-in** | ships with the agent or surface |
| **install** | official capability that must be installed or connected |
| ⚠️ **gated** | also requires account, plan, provider, or organization provisioning |
| **project** | supplied by this repository or the target repository |
| **N/A** | no purpose-built capability for this purpose; the general agent can still do the work |

The three optional `hr-` candidates below are experimental and off by default.
Select them with the [installer](../README.md); use the installed `HOUSERULES.md` for local paths.
Their table placement does not establish native loading on each surface; see the
[acceptance record](../tests/workflows/toolkit-adoption/README.md).

Mixed rows list every applicable type. Assume one agent, not a combination: each stage must work
with whichever inventoried agent is active. Agents without a capability inventory are omitted
rather than marked `N/A`.

---

## Lifecycle stages

### 1. Onboard & Context

Create useful context and make setup reproducible.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Initialize the repo | Use the active agent’s initializer/context tools below, then the project installer. | Loaded project instructions. |
| Capture a non-obvious operating rule | Use the existing `hr-onboard` procedure after real work exposes friction. | One scoped instruction or deterministic check. |
| Complete human-only provisioning | Use an existing setup runbook or have the agent prepare the manual steps a person must perform. | A repeatable manual setup procedure. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/init` | `/import`, `/context`, `/memory`, `/doctor`, `/hr-onboard` | built-in + project | `/import` has provider and feature-flag limits; `/context` confirms what loaded | Create and inspect the repository instruction context; discover non-obvious operating knowledge |
| Codex | `/init` | `$migrate-to-codex`, `codex debug prompt-input`, Local Environments, `$hr-onboard` | built-in + install + project | `/init` and Local Environments are surface-specific; Local Environments are desktop-only | Create/import `AGENTS.md`, inspect the model-visible prompt, and make setup repeatable |
| Antigravity | `AGENTS.md` + Rules | `/learn`, `/skills`, `hr-onboard` | built-in + project | CLI documents `AGENTS.md`/`GEMINI.md`; `.agents/rules` adds activation modes; no local loading test | Load repository context and turn session corrections into durable, scoped guidance |

Run the native initializer, then `python install.py`. Use `hr-onboard` for knowledge that repository
inspection cannot reveal, such as a command that only works from one directory or a test expected
to fail.

</details>

### 2. Intent

Resolve what should be achieved before selecting a solution.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Persist an agreed outcome | Use the active host’s goal feature when available. | Execution objective; durable criteria belong in the work record. |
| Expose uncertain requirements | Use the host’s interview capability or your preferred requirements procedure. | Agreed scope, open questions and domain terms. |
| Collect missing facts or stakeholder answers | Use research tools for evidence; draft a questionnaire when another person holds the missing knowledge. | Cited findings or an unsent questionnaire. |
| Process incoming requests | Use the project’s triage workflow to verify the report, scope the request and identify its next owner. | Ready work or a clearly stated information gap. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/goal` | `/deep-research`, MCP/connectors | built-in + install + ⚠️ gated | `/deep-research` varies by plan, provider, settings, and surface | Persist the outcome and gather decision inputs before choosing a solution |
| Codex | `/goal` | `$define-goal`, `/apps`, MCP | built-in + install | `/goal` is documented from the desktop app surface; apps/MCP require a configured source | Persist or formalize the objective and bring external context into scope |
| Antigravity | `/goal` | `/grill-me`, `/btw`, MCP | built-in | `/goal` continues autonomously; `/grill-me` is the explicit requirements interview | Persist the objective, expose ambiguity, and gather context before implementation |

Record durable acceptance criteria in `work/<id>/`; a session goal is execution state, not the
project's system of record.

</details>

### 3. Spec & Architecture

Describe behavior and design decisions; use visual design only when the problem is visual.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Write the specification | Use native planning/general writing or an existing spec-authoring skill. | A small spec with verifiable criteria; [optional pilot template](../templates/work/spec.md). |
| Resolve architecture or terminology | Use the agent and the project’s domain/architecture references; select specialist guidance when needed. | Recorded trade-offs, interfaces and test seams. |
| Explore screens or interaction | Use a UI design capability below or your preferred prototyping skill. Claude’s `/design` is visual design, not general specification writing. | Mockup/prototype plus the decision it resolves. |
| Review a spec before building | Ask for a separate artifact critique against intent, contradictions, edge cases and testability; use the spec rubric in [work artifacts](../templates/work/README.md#review-by-artifact). | Findings tied to the exact spec revision. No assumed `design-review` command. |
| Specify a recurring workflow | Describe triggers, actions, evidence and any human checkpoints before choosing an execution tool. | Workflow definition; scheduling is a later implementation choice. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/plan` | `/deep-research`, Artifacts, `/design` | built-in + ⚠️ gated | Artifacts require an eligible plan/provider/surface; `/design` is for UI work, not a general architecture gate | Explore architecture, validate external assumptions, and communicate a proposed design |
| Codex | `/plan mode` | `documents`, `visualize`, MCP/apps | built-in + install | `/plan mode` is app-specific; plugins are not available in the IDE extension; no dedicated spec gate | Produce and inspect a spec or architecture artifact using general planning and document tools |
| Antigravity | `/grill-me` | `/plan`, Artifacts, `/boost` | built-in + ⚠️ gated | `/boost` is paid; `/plan` produces a reviewable Implementation Plan, not a mandatory spec gate | Interview for constraints and communicate the proposed architecture before edits |

No inventoried agent supplies a mandatory specification format or acceptance gate. Keep the spec as small
as the change requires, and place durable output in `work/<id>/`.

</details>

### 4. Plan

Turn accepted decisions into work that can be picked up and verified.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Sequence a bounded change | Use native planning or your existing task workflow; preserve output when another session will consume it. | Tasks linked to spec criteria; [optional pilot template](../templates/work/plan.md). |
| Create independently executable tickets | Use the project’s task tracker or local task files, with deliverables and blocking dependencies. | Self-contained tasks; not a mandatory tracker migration. |
| Investigate a large unresolved effort | Map the unanswered decisions and investigate their dependencies before decomposing implementation. | Resolved decisions before implementation tickets. |
| Review the plan | Use a fresh artifact review when dependencies, feasibility, migration order or verification strategy are uncertain. | Missing coverage and unsafe sequencing identified before Build. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/plan` | Plan subagent, dynamic workflows | built-in + ⚠️ gated | Dynamic workflows have provider, plan, settings, and concurrency limits | Turn the accepted intent/spec into executable work and delegate bounded research |
| Codex | `/plan mode` | `/goal`, subagents | built-in | `/plan mode` and `/goal` are app commands; subagents are configuration- and concurrency-limited | Decompose the work while preserving the goal across turns |
| Antigravity | `/plan` | Implementation Plan Artifact, subagents, `/boost` | built-in + ⚠️ gated | `/boost` is paid; children can inherit, branch into a worktree, or share storage | Produce a reviewable plan and delegate isolated research before implementation |

Claude Code 2.1.251 plan mode was locally tested writing a machine-local file under
`~/.claude/plans/` on 2026-09-03. Use `work/<id>/handoff.md` when the plan must be repository-visible,
reviewable, or portable to another agent.

</details>

### 5. Build

Implement the chosen task using the runtime and isolation your current host provides.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Build one bounded change | Use the general coding agent or your preferred implementation procedure. | Code plus evidence against the agreed task. |
| Work test-first | Use a meaningful failing test and implement one behavior at a time; add a TDD skill only if it improves the method. | A failing test followed by a passing implementation. |
| Implement independent tasks concurrently | Use available worktrees/subagents, or work sequentially when isolation or delegation is unavailable. | Isolated changes integrated against the same spec. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/batch` | `/subtask`, `/background`, `/worktree`, LSP plugins, `hr-tdd` (experimental, opt-in) | built-in + install + project | `/batch` requires Git; plugin language servers are separately installed and unavailable in cloud sessions | Implement in isolated units with optional language-server feedback |
| Codex | `codex exec` + Git worktrees | managed Worktrees, `/new playground worktree`, subagents, Local Environments, `hr-tdd` (experimental, opt-in) | built-in + project | `codex exec` is CLI/non-interactive; managed Worktrees, the slash command, and Local Environments are desktop capabilities | Isolate parallel changes, reproduce setup, and automate bounded implementation tasks across surfaces |
| Antigravity | `/goal` | worktree subagents, `/teamwork-preview`, `agy -p`, Remote Control, `hr-tdd` (experimental, opt-in) | built-in + ⚠️ gated + project | `/teamwork-preview` is paid/preview; headless CLI is scriptable; Remote Control drives a host session rather than supplying another runtime | Implement interactively, in isolated parallel children, headlessly, or through a remote host control channel |

Use one worktree per parallel write stream. All three agents can coordinate concurrent work; none
is limited to a single isolated chat.

</details>

### 6. Verify

Produce evidence that the changed behavior works.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Run project checks | Use shell/CI and the project’s actual check commands. Test-design guidance does not replace a runner. | Commands, results, failures and skipped checks; [optional pilot record](../templates/work/verification.md). |
| Exercise the running application | Use the available verify/run/browser capability below; store a reusable launch recipe if needed. | Observed behavior at the relevant runtime/UI surface. |
| Prove a bug was fixed | Re-run the original failing scenario and a relevant regression check. | Before/after evidence for the actual symptom. |
| Add targeted automated gates | Use the stack’s test/lint/boundary tooling for a recurring, machine-testable failure. | A check that demonstrably rejects a known violation. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/verify` | `/run`, `/run-skill-generator`, Bash, `hr-tdd` (experimental, opt-in) | built-in + project | Availability and launch-recipe path are disputed across official pages; confirm on the active surface before relying on them | Build and run the changed system, then capture a reusable launch recipe |
| Codex | **N/A — no dedicated verify command** | shell, Local Environments, `@Browser`, `$playwright`, `hr-tdd` (experimental, opt-in) | N/A + built-in + install + project | Local Environments and Browser are desktop-specific; Playwright is installable | Execute project tests and runtime checks through general tools |
| Antigravity | `/boost` | shell, `/browser`, Artifacts, `hr-tdd` (experimental, opt-in) | built-in + ⚠️ gated + project | `/boost` explicitly documents tests and independent verification but requires a paid plan; sandbox is opt-in | Run tests and UI checks, then expose results as reviewable artifacts |

A tool invocation is not evidence by itself. Record the command, surface, version, result, and
relevant artifact. If Claude's launch skill is unavailable, an existing project procedure can
serve as the fallback. A Claude-only skill belongs under `.claude/skills/<name>/SKILL.md`; see
the [Claude skill inventory](agents/claude-code.md) for discovery details. For a cross-agent
procedure, use a canonical source with agent-specific destinations, following the
[installer pattern](../README.md#what-it-installs); `.agents/skills/` alone does not cover Claude.
Any new project-owned fallback still needs to meet the project's admission criteria.

</details>

### 7. Review

Choose the question the review must answer. Add specialist passes only for relevant risks.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Find implementation defects | Use an available code reviewer or your preferred review procedure; declare the target and relevant criteria. | Located findings against a declared diff/revision. |
| Check requirements coverage | Compare the implementation against the accepted spec independently of style/standards concerns. | Missing, incorrect or out-of-scope behavior. |
| Check security-sensitive changes | Use the available security reviewer/scan below, with access to the relevant threat context. | Validated security findings; not replaced by style review. |
| Reduce unnecessary complexity | Use a focused simplification pass when complexity is the concern. | Concrete simplifications; not a compulsory second full review. |
| Review a spec, plan or prior fix | Use the artifact-specific rubric and [review → fix → verify protocol](../templates/work/README.md#review-fix-verify). | Stable finding IDs and independently verified dispositions. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/code-review` | `/security-review`, `/simplify`, `hr-code-review` (experimental, opt-in) | built-in + project | Interactive-first; `--fix` mutates and `--comment` posts externally | Review correctness, security, and unnecessary complexity before integration |
| Codex | `/code review`, `codex review` | `review-agent`, `codex-security` plugin (`$security-scan`), `hr-code-review` (experimental, opt-in) | built-in + install + ⚠️ gated + project | App and CLI surfaces differ; `review-agent` is delegated internally; Codex Security needs access beyond installation | Review interactively or in CI, with an optional staged security pipeline |
| Antigravity | **N/A — no dedicated code-review command** | `/diff`, Artifact Review, custom `code-auditor` agent/skill, `/boost`, `hr-code-review` (experimental, opt-in) | N/A + built-in + project + ⚠️ gated | `/diff` is a viewer, not a reviewer; `/boost` is paid | Inspect changes and delegate review, then bind recurring findings in tests/checks |

Use review to find issues; move requirements that must bind into deterministic CI checks.

</details>

### 8. Release

Prepare an identifiable release candidate and let repository policy decide readiness.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Prepare commit/PR work | Use the existing Git/PR helpers below or the project’s delivery workflow. | A reviewable change and associated evidence. |
| Resolve an in-progress conflict | Trace both changes to their intent, resolve the conflict and run project checks; scope staging to the requested work. | A completed merge/rebase verified by project checks. |
| Version and release | Use the repository’s release workflow and CI. | Version/tag/artifact provenance and release decision. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | **N/A — no built-in atomic ship command** | `commit-commands`, `/install-github-app`, GitHub/GitLab integrations, Git/CI | N/A + built-in + install | Plugins/integrations must be installed and authenticated | Prepare commits and PRs, then let the repository's release gates decide readiness |
| Codex | `$yeet` | GitHub plugin/action, `$gh-address-comments`, Git/CI | install | `$yeet` and `$gh-address-comments` are curated skills; the GitHub Action is CI-only | Stage, commit, push, open or refine a PR, and run release gates |
| Antigravity | **N/A — no built-in atomic ship command** | headless `agy -p`, custom Skills/Plugins, Git/CI | N/A + built-in + project | Headless mode is scriptable, but release policy and credentials remain external | Prepare release work while CI and repository policy decide readiness |

Wire `python check.py` and `python install.py --check` into CI for this repository. Convenience
commands do not replace branch protection, release policy, or reproducible checks.

</details>

### 9. Deploy

Deploy through a provider or CI/CD identity with a known recovery path.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Execute a deployment | Use the relevant provider integration below or the project’s CI/CD pipeline. | Target environment, deployed revision and health evidence. |
| Prepare manual setup or cutover | Use an existing runbook or prepare a manual procedure when the remaining steps require a human. | Named steps, owner and observable completion. |
| Decide rollout/rollback readiness | Review the project’s operational runbook and evidence. | Recovery path, health criteria and owner. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | **N/A — no built-in deploy command** | `vercel`, `firebase`, `supabase` plugins | N/A + install | Provider plugins require installation, credentials, and their target service | Invoke provider-specific deployment workflows |
| Codex | **N/A — no built-in deploy command** | `$vercel-deploy`, `$netlify-deploy`, `$render-deploy`, `$cloudflare-deploy` | N/A + install | Skills must be installed; plugin-bundled alternatives are unavailable in the IDE extension | Invoke provider-specific deployment workflows |
| Antigravity | **N/A — no generic deploy command** | Firebase, Android, Data Agent Kit, Maps bundles; custom Skills/MCP | N/A + install | Google bundles must be enabled and authenticated; they are not fresh-install built-ins | Invoke provider-specific deployment workflows with scoped credentials |

Production approval remains outside the agent. Prefer a CI/CD deployment identity and an explicit
environment approval over credentials embedded in an interactive session.

</details>

### 10. Observe

Inspect signals and decide when action is needed.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Investigate runtime signals | Use a configured telemetry connector/MCP or the underlying service. | Trace/log/metric evidence; a skill cannot supply a telemetry backend. |
| Run recurring inspections | Use an available scheduler below after defining the observation workflow. | Signal, threshold, owner and durable event/alert. |
| Respond to an actionable failure | Continue to [Diagnose](#11-diagnose--remediate). | An owned investigation, not another overlapping monitor. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `sentry` integration | OpenTelemetry, `/schedule` Routines with GitHub/API triggers, Analytics dashboard/API, `/loop` | install + built-in + ⚠️ gated | Routines and analytics vary by plan, provider, and surface; scheduling runtimes have different persistence and credentials | Inspect delivery/runtime telemetry and react to repository or API events |
| Codex | `sentry`/`posthog` plugins | Scheduled Tasks, externally scheduled `codex exec` | install + built-in | These are plugin names; Scheduled Tasks are ChatGPT/desktop capabilities, while CLI and IDE need an external scheduler | Inspect telemetry and run recurring observation tasks |
| Antigravity | `/schedule` | Sidecars, Remote Control notifications, MCP, SDK/API hooks, headless `agy -p` | built-in + install | Sidecars are off until enabled; Remote Control monitors host tasks; neither supplies telemetry storage or alert ownership | Run recurring inspections, monitor host agents, and connect to an external observability system |

Monitoring must emit durable events or alerts. A recurring agent prompt is orchestration, not an
observability backend.

</details>

### 11. Diagnose & Remediate

Find the cause, correct it and preserve the evidence.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Diagnose an unclear bug | Use native debug/tools or your preferred diagnosis procedure to reproduce the symptom and test hypotheses. | Minimal repro and supported causal explanation. |
| Repair a known CI/review/security failure | Use the matching fix capability below and the source finding; clarify incomplete reports first. | Scoped correction linked to the original finding. |
| Verify remediation | Re-run the original failure and relevant regression checks; use a separate reviewer when independence matters. | Verified finding disposition and remaining limitations. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/debug` | `/autofix-pr`, `/code-review --fix`, `/security-review --fix`, `/simplify --fix`, `sentry`, `hr-diagnosing-bugs` (experimental, opt-in) | built-in + install + project | `/autofix-pr` is a cloud/GitHub workflow; mutation and external comments need authority | Reproduce failures, trace runtime evidence, and prepare a reviewed fix |
| Codex | `$gh-fix-ci` | `$gh-address-comments`, `codex-security` fix pipeline, `sentry`/`posthog` plugins, `hr-diagnosing-bugs` (experimental, opt-in) | install + ⚠️ gated + project | GitHub skills require repository access; Codex Security requires separately provisioned access | Diagnose CI, review, security, and production signals and prepare remediation |
| Antigravity | `/boost` | `/codesearch`, `research`/`browser` subagents, MCP, Artifacts, `hr-diagnosing-bugs` (experimental, opt-in) | built-in + install + ⚠️ gated + project | `/boost` is paid; external incident data requires MCP or another integration | Reproduce failures, compare hypotheses, verify a correction, and preserve evidence |

Feed incident findings into `work/<id>/findings.md`, tests, and checks. Do not leave the only causal
record in a vendor conversation.

</details>

### 12. Maintain the engineering system

Improve the engineering system in response to observed friction.

**Choose by purpose**

| When you need to… | Use | Keep / check |
|---|---|---|
| Inspect client health or loaded extensions | Use native doctor/context/config tools and the canonical inventory for that surface. | Actual availability and drift evidence. |
| Improve repo instructions | Use `hr-onboard` for non-obvious repo friction, or an existing procedure that serves the same need. | A pruned instruction, procedure or deterministic check. |
| Address architectural friction | Investigate a recurring maintenance problem, compare design options and select one supported by evidence. | One justified improvement rather than a general rewrite. |
| Improve stack-specific checks or tests | Use existing test/lint/boundary tools or a suitable stack-specific skill. | Targeted tooling, with declared dependencies. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/doctor` | `/context`, `/memory`, `/reload-skills`, `/reload-plugins`, `/claude-api prompt-audit`, `/claude-api cost-optimize` | built-in | Availability varies; terminal-dialog commands are not on every surface | Audit setup and loaded context, trim instructions, reload extensions, and inspect prompt/cost drift |
| Codex | `codex doctor` | `codex debug prompt-input`, plugin/hooks/features inspection, Scheduled Tasks | built-in | `codex doctor` covers startup/connectivity/performance, not Claude's instruction-trimming workflow | Diagnose client health and manually audit what is installed, enabled, and model-visible |
| Antigravity | `/learn` | `/skills`, `/agents`, `/hooks`, `/mcp`, `/config`, `/usage` | built-in | No documented doctor command; `/learn` output path conflicts across official pages | Convert repeated corrections into Rules/Skills and manually audit loaded extensions and quotas |

Move procedures out of always-loaded instruction files and into project-prefixed skills. Use
scheduled audits only when their output has an owner and a durable destination.

</details>

---

## Cross-cutting architecture concerns

### Control Plane & Authority

Use host permissions and protected CI for enforceable controls. A third-party or project skill
can describe a procedure; it does not create a cross-agent permission boundary.

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | permission rules | hooks, sandbox, managed settings | built-in | Hooks are often fail-open; the OS sandbox covers Bash descendants but is unavailable on native Windows. See the canonical inventory's enforcement boundary | Separate advisory instructions from enforceable tool and OS boundaries |
| Codex | permission profiles | hooks, native sandbox, `requirements.toml`, project trust | built-in | Native Windows has OS-level sandboxing; an untrusted project skips project `.codex/` layers; full access flips web search to live, while apps bypass the command-network proxy/allowlist | Bound tools, filesystem/network access, escalation, and organization policy |
| Antigravity | Deny/Ask/Allow permissions | Terminal Sandbox, hooks, project settings, artifact review | built-in | `Deny > Ask > Allow`; sandbox is opt-in/preview. CLI Features says Windows `AppContainer`, while the dedicated Sandbox pages omit Windows | Bound files, commands, URLs, MCP tools, host escape, and review points |

Model prompts express intent; they are not the security boundary. On native Windows, Codex has a
documented OS command sandbox, Claude Code does not, and Antigravity's official pages conflict over
`AppContainer` support. Put irreversible or privileged actions behind controls the acting agent
cannot silently redefine.

### Evidence & System of Record

Use an existing durable work record when another session must continue, fix or verify the result.
The optional [work artifact pilot](../templates/work/README.md) illustrates the required pointers;
a repository-visible handoff must still be transferred to a new checkout or host.

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | Git + CI + `work/<id>/` | project tests/checks | project | **N/A** for a purpose-built agent-configuration evaluation suite | Preserve decisions, changes, verification, and operational findings outside the conversation |
| Codex | Git + CI + `work/<id>/` | project tests/checks | project | **N/A** for a purpose-built agent-configuration evaluation suite | Preserve decisions, changes, verification, and operational findings outside the conversation |
| Antigravity | Git + CI + `work/<id>/` | Artifacts, project tests/checks | project + built-in | Artifacts improve review but are not the repository's durable system of record by default | Preserve decisions, changes, verification, and operational findings outside the conversation |

Build project-specific CI for agent configuration where its behavior matters. A deterministic gate
provides a guarantee only when the current agent cannot modify, disable, or bypass that gate.
Prove a blocking control by attempting the action it is meant to block, and repeat that test after
relevant instruction, hook, permission, sandbox, or CI configuration changes. A green check proves
only its encoded contract; it does not replace independent review.

### Human Governance

Questionnaires, explanation and learning procedures may help the people making decisions.
They are optional support, not required lifecycle gates.

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | **N/A by design** | permissions, hooks, review, deployment approvals | N/A | Intent acceptance, authority maps, production approval, and accountability stay human-owned | Enforce a human decision without transferring responsibility to the tool |
| Codex | **N/A by design** | permissions, hooks, review, deployment approvals | N/A | Intent acceptance, authority maps, production approval, and accountability stay human-owned | Enforce a human decision without transferring responsibility to the tool |
| Antigravity | **N/A by design** | permissions, Artifact Review, hooks, deployment approvals | N/A | `/goal`, `/boost`, and teams expand execution, not accountability | Enforce a human decision without transferring responsibility to the tool |

Tools can enforce an authority decision; they cannot supply the accountable owner.
Scope authority by blast radius and reversibility, not by model capability. A stronger model may
need less assistance, but it does not inherit human accountability.

---

## Placement rule

| Layer | Cost | Trigger | Put here |
|---|---|---|---|
| `AGENTS.md` | every session | always | short, non-standard, non-obvious repository instructions |
| Path-scoped rule | matching context only | matching file/path | local instructions for one part of the tree; vendor-specific (Claude Code and Antigravity use different formats) |
| Project-prefixed skill | metadata always, body on selection | description match or explicit invocation | procedures and reference material |
| Deterministic check | when the gate runs | CI, hook, or explicit command | machine-testable requirements |

Push knowledge down to the least expensive layer that still triggers reliably. A CI rule needs no
duplicate sentence in `AGENTS.md` unless the agent needs that sentence to avoid wasted work before
the gate.

Use a project prefix for every shipped skill. An unprefixed name can collide with or silently
replace a vendor capability; `check.py` catches known collisions, but the inventories are lower
bounds.

Before adding anything framework-shaped, read [`PORTABILITY.md`](../research/PORTABILITY.md). Use
vendor capabilities where they help, but keep only the minimum contract that must survive an agent
switch in the portable layer.
