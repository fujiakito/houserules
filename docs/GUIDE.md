# Choose the next step

Use this guide when deciding **what to do and which capability to use**. It covers Claude Code,
Codex, Antigravity, Cursor and Kiro across all 12 stages. You do not need to run every stage or
install every tool. Start with the current problem; expand its agent table only when needed.

## Choose the next action

| Your task | Go to |
|---|---|
| Set up the project | [Onboard](#1-onboard--context) |
| Clarify the outcome | [Intent](#2-intent) |
| Design or plan | [Spec](#3-spec--architecture) / [Plan](#4-plan) |
| Implement and test | [Build](#5-build) / [Verify](#6-verify) |
| Critique a result | [Review](#7-review) |
| Ship and operate | [Release](#8-release) / [Deploy](#9-deploy) / [Observe](#10-observe) |
| Fix a failure | [Diagnose](#11-diagnose--remediate) |
| Improve the workflow | [Maintain](#12-maintain-the-engineering-system) |
| Resume with another agent | Read the existing handoff; check [workflow status](USAGE.md#run-a-bounded-check) |

## How to read the tables

**built-in** is supplied by the agent; **install** means a plugin, Power or integration must be
installed/configured; **project** is your repository's procedure; **gated** needs separate account,
plan or organization access. N/A means no dedicated option is recorded, not that the task is impossible.
A skill describes a procedure; tools execute it; plugins/Powers package capabilities.

Agent-name links open the canonical inventory for exact commands, sources, versions and constraints.
Claude/Codex mappings retain their 2026-09-04 evidence; Cursor/Kiro mappings were checked against
2026-09-06 official sources. Antigravity, Cursor and Kiro capability mappings are documented,
not runtime-tested. A tool shown for one surface is not promised on every surface.

## Apply the method in your project

After [installation](../README.md#install), give the agent the task and the short
`.houserules/START.md` entry. With `--activate-workflow`, a small AGENTS.md trigger routes relevant
tasks there. The agent reads the selected skill and current inputs, not this entire guide.
The installed workflow command records attempts and rejects exhausted budgets, unchanged duplicate
checks and stale evidence. See [Usage](USAGE.md) for actual limits and commands.

The optional hr-tdd, hr-diagnosing-bugs and hr-code-review skills are experimental; use your
preferred/native procedure when it fits. Work templates are optional outputs, not a document quota.

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/init` | `/import`, `/context`, `/memory`, `/doctor`, `/hr-onboard` | built-in + project; `/import` has provider and feature-flag limits; `/context` confirms what loaded |
| [Codex](agents/codex.md) | `/init` | `$migrate-to-codex`, `codex debug prompt-input`, Local Environments, `$hr-onboard` | built-in + install + project; `/init` and Local Environments are surface-specific; Local Environments are desktop-only |
| [Antigravity](agents/antigravity.md) | `AGENTS.md` + Rules | `/learn`, `/skills`, `hr-onboard` | built-in + project; CLI documents `AGENTS.md`/`GEMINI.md`; `.agents/rules` adds activation modes; no local loading test |
| [Cursor](agents/cursor.md) | AGENTS.md + rules | /create-rule, /create-skill, hr-onboard | built-in + project; IDE: Customize; CLI reads project rules; loading pending |
| [Kiro](agents/kiro.md) | Steering + skills | Agent Steering & Skills, hr-onboard | built-in + project; IDE/CLI: verify the selected agent resources; inheritance disputed |

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/goal` | `/deep-research`, MCP/connectors | built-in + install + ⚠️ gated; `/deep-research` varies by plan, provider, settings, and surface |
| [Codex](agents/codex.md) | `/goal` | `$define-goal`, `/apps`, MCP | built-in + install; `/goal` is documented from the desktop app surface; apps/MCP require a configured source |
| [Antigravity](agents/antigravity.md) | `/goal` | `/grill-me`, `/btw`, MCP | built-in; `/goal` continues autonomously; `/grill-me` is the explicit requirements interview |
| [Cursor](agents/cursor.md) | Agent conversation | search; Atlassian plugin for issue context | built-in + install; IDE/CLI; plugin needs installation and provider access |
| [Kiro](agents/kiro.md) | Feature Spec requirements | Plan agent; configured MCP | built-in + install; IDE/CLI; Plan reads context but excludes MCP/tools that mutate |

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/plan` | `/deep-research`, Artifacts, `/design` | built-in + ⚠️ gated; Artifacts require an eligible plan/provider/surface; `/design` is for UI work, not a general architecture gate |
| [Codex](agents/codex.md) | `/plan mode` | `documents`, `visualize`, MCP/apps | built-in + install; `/plan mode` is app-specific; plugins are not available in the IDE extension; no dedicated spec gate |
| [Antigravity](agents/antigravity.md) | `/grill-me` | `/plan`, Artifacts, `/boost` | built-in + ⚠️ gated; `/boost` is paid; `/plan` produces a reviewable Implementation Plan, not a mandatory spec gate |
| [Cursor](agents/cursor.md) | Agent design/planning | /canvas; relevant plugins | built-in + install; IDE: canvas is visual output, not a specification gate |
| [Kiro](agents/kiro.md) | Feature Spec / Quick Spec | Figma Power for design context | built-in + install; IDE/CLI/Web workflows differ; Power needs installation/access |

Kiro offers native specification workflows; other agents can use existing specs or the optional
template. Pick a format that serves the next consumer and keep business acceptance explicit.

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/plan` | Plan subagent, dynamic workflows | built-in + ⚠️ gated; Dynamic workflows have provider, plan, settings, and concurrency limits |
| [Codex](agents/codex.md) | `/plan mode` | `/goal`, subagents | built-in; `/plan mode` and `/goal` are app commands; subagents are configuration- and concurrency-limited |
| [Antigravity](agents/antigravity.md) | `/plan` | Implementation Plan Artifact, subagents, `/boost` | built-in + ⚠️ gated; `/boost` is paid; children can inherit, branch into a worktree, or share storage |
| [Cursor](agents/cursor.md) | Agent planning | /create-subagent; project plan | built-in + project; IDE/CLI; delegate only when authorized and independently useful |
| [Kiro](agents/kiro.md) | Plan agent / Spec tasks | requirements and design artifacts | built-in; IDE/CLI: Plan is read-only; hand off accepted work for execution |

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/batch` | `/subtask`, `/background`, `/worktree`, LSP plugins, `hr-tdd` (experimental, opt-in) | built-in + install + project; `/batch` requires Git; plugin language servers are separately installed and unavailable in cloud sessions |
| [Codex](agents/codex.md) | `codex exec` + Git worktrees | managed Worktrees, `/new playground worktree`, subagents, Local Environments, `hr-tdd` (experimental, opt-in) | built-in + project; `codex exec` is CLI/non-interactive; managed Worktrees, the slash command, and Local Environments are desktop capabilities |
| [Antigravity](agents/antigravity.md) | `/goal` | worktree subagents, `/teamwork-preview`, `agy -p`, Remote Control, `hr-tdd` (experimental, opt-in) | built-in + ⚠️ gated + project; `/teamwork-preview` is paid/preview; headless CLI is scriptable; Remote Control drives a host session rather than supplying another runtime |
| [Cursor](agents/cursor.md) | Agent implementation | /shell; hr-tdd | built-in + project; IDE/CLI/cloud have different execution environments; hr-tdd is opt-in |
| [Kiro](agents/kiro.md) | Default agent / Spec tasks | hr-tdd; relevant technology Power | built-in + project + install; Use an execution-capable agent; Powers in CLI require v3 |

Use one worktree per parallel write stream. Use the concurrency available on the active surface; a general
capability does not establish permission to delegate or a benefit from doing so.

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/verify` | `/run`, `/run-skill-generator`, Bash, `hr-tdd` (experimental, opt-in) | built-in + project; Availability and launch-recipe path are disputed across official pages; confirm on the active surface before relying on them |
| [Codex](agents/codex.md) | **N/A — no dedicated verify command** | shell, Local Environments, `@Browser`, `$playwright`, `hr-tdd` (experimental, opt-in) | N/A + built-in + install + project; Local Environments and Browser are desktop-specific; Playwright is installable |
| [Antigravity](agents/antigravity.md) | `/boost` | shell, `/browser`, Artifacts, `hr-tdd` (experimental, opt-in) | built-in + ⚠️ gated + project; `/boost` explicitly documents tests and independent verification but requires a paid plan; sandbox is opt-in |
| [Cursor](agents/cursor.md) | Agent + project tests | hr-tdd; workflow run | built-in + project; IDE/CLI: preserve command output; cloud setup is separate |
| [Kiro](agents/kiro.md) | Default agent + project tests | Postman Power; workflow run | built-in + project + install; Plan cannot execute checks; Power installation does not imply test success |

A tool invocation is not evidence by itself. Record the command, surface, version, result, and
relevant artifact. If Claude's launch skill is unavailable, an existing project procedure can
serve as the fallback. A Claude-only skill belongs under `.claude/skills/<name>/SKILL.md`; see
the [Claude skill inventory](agents/claude-code.md) for discovery details. For a cross-agent
procedure, use a canonical source with agent-specific destinations, following the
[installer pattern](../README.md#what-arrives-in-your-project); `.agents/skills/` alone does not cover Claude.
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
| Review a spec, plan or prior fix | Use the artifact-specific rubric and [consumer protocol](../templates/work/README.md#consumer-protocol). | Stable finding IDs, verified dispositions and disclosed reviewer context. |

<details>
<summary>Tools by agent — availability and constraints</summary>

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/code-review` | `/security-review`, `/simplify`, `hr-code-review` (experimental, opt-in) | built-in + project; Interactive-first; `--fix` mutates and `--comment` posts externally |
| [Codex](agents/codex.md) | `/code review`, `codex review` | `review-agent`, `codex-security` plugin (`$security-scan`), `hr-code-review` (experimental, opt-in) | built-in + install + ⚠️ gated + project; App and CLI surfaces differ; `review-agent` is delegated internally; Codex Security needs access beyond installation |
| [Antigravity](agents/antigravity.md) | **N/A — no dedicated code-review command** | `/diff`, Artifact Review, custom `code-auditor` agent/skill, `/boost`, `hr-code-review` (experimental, opt-in) | N/A + built-in + project + ⚠️ gated; `/diff` is a viewer, not a reviewer; `/boost` is paid |
| [Cursor](agents/cursor.md) | /review | /review-bugbot, /review-security; hr-code-review | built-in + project; Native review routing is documented; project alternative remains experimental |
| [Kiro](agents/kiro.md) | Scoped review request | custom reviewer; hr-code-review | built-in + project; No dedicated review skill established here; capture actual findings and revision |

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | **N/A — no built-in atomic ship command** | `commit-commands`, `/install-github-app`, GitHub/GitLab integrations, Git/CI | N/A + built-in + install; Plugins/integrations must be installed and authenticated |
| [Codex](agents/codex.md) | `$yeet` | GitHub plugin/action, `$gh-address-comments`, Git/CI | install; `$yeet` and `$gh-address-comments` are curated skills; the GitHub Action is CI-only |
| [Antigravity](agents/antigravity.md) | **N/A — no built-in atomic ship command** | headless `agy -p`, custom Skills/Plugins, Git/CI | N/A + built-in + project; Headless mode is scriptable, but release policy and credentials remain external |
| [Cursor](agents/cursor.md) | Git + review | /split-to-prs, /autopilot | built-in + project; Remote PR actions require repository access and task authority |
| [Kiro](agents/kiro.md) | Git + project CI | custom delivery procedure | built-in + project; No atomic ship capability established; release decision remains separate |

Wire `python check.py` and `python install.py --check` into CI for this repository. In an adopting
project, `install.py --ci` writes a GitHub Actions workflow running the installed
`.houserules/check.py`; drift against the upstream templates is not gateable from there, because
the installer is never copied into a project. Convenience commands do not replace branch
protection, release policy, or reproducible checks.

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | **N/A — no built-in deploy command** | `vercel`, `firebase`, `supabase` plugins | N/A + install; Provider plugins require installation, credentials, and their target service |
| [Codex](agents/codex.md) | **N/A — no built-in deploy command** | `$vercel-deploy`, `$netlify-deploy`, `$render-deploy`, `$cloudflare-deploy` | N/A + install; Skills must be installed; plugin-bundled alternatives are unavailable in the IDE extension |
| [Antigravity](agents/antigravity.md) | **N/A — no generic deploy command** | Firebase, Android, Data Agent Kit, Maps bundles; custom Skills/MCP | N/A + install; Google bundles must be enabled and authenticated; they are not fresh-install built-ins |
| [Cursor](agents/cursor.md) | Project deployment command | provider MCP/plugin when configured | project + install; Use the target environment credentials and existing release gates |
| [Kiro](agents/kiro.md) | Project deployment command | Netlify Power; configured provider tools | project + install; IDE/CLI v3/Web: install/connect Power; deploying still needs authority |

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `sentry` integration | OpenTelemetry, `/schedule` Routines with GitHub/API triggers, Analytics dashboard/API, `/loop` | install + built-in + ⚠️ gated; Routines and analytics vary by plan, provider, and surface; scheduling runtimes have different persistence and credentials |
| [Codex](agents/codex.md) | `sentry`/`posthog` plugins | Scheduled Tasks, externally scheduled `codex exec` | install + built-in; These are plugin names; Scheduled Tasks are ChatGPT/desktop capabilities, while CLI and IDE need an external scheduler |
| [Antigravity](agents/antigravity.md) | `/schedule` | Sidecars, Remote Control notifications, MCP, SDK/API hooks, headless `agy -p` | built-in + install; Sidecars are off until enabled; Remote Control monitors host tasks; neither supplies telemetry storage or alert ownership |
| [Cursor](agents/cursor.md) | Configured telemetry tools | Hex Canvas; /automate, /loop | install + built-in; Visualization and automation do not provide telemetry storage or credentials |
| [Kiro](agents/kiro.md) | Configured telemetry tools | Datadog / Dynatrace Powers | install; Powers are catalog options; verify actual tools and account access |

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/debug` | `/autofix-pr`, `/code-review --fix`, `/security-review --fix`, `/simplify --fix`, `sentry`, `hr-diagnosing-bugs` (experimental, opt-in) | built-in + install + project; `/autofix-pr` is a cloud/GitHub workflow; mutation and external comments need authority |
| [Codex](agents/codex.md) | `$gh-fix-ci` | `$gh-address-comments`, `codex-security` fix pipeline, `sentry`/`posthog` plugins, `hr-diagnosing-bugs` (experimental, opt-in) | install + ⚠️ gated + project; GitHub skills require repository access; Codex Security requires separately provisioned access |
| [Antigravity](agents/antigravity.md) | `/boost` | `/codesearch`, `research`/`browser` subagents, MCP, Artifacts, `hr-diagnosing-bugs` (experimental, opt-in) | built-in + install + ⚠️ gated + project; `/boost` is paid; external incident data requires MCP or another integration |
| [Cursor](agents/cursor.md) | Agent diagnosis | /review-bugbot; hr-diagnosing-bugs | built-in + project; Reproduce the failure; review findings alone do not identify root cause |
| [Kiro](agents/kiro.md) | Bugfix Spec + execution | hr-diagnosing-bugs; telemetry Power | built-in + project + install; Keep current/expected/unchanged behavior; verify in execution-capable mode |

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

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | `/doctor` | `/context`, `/memory`, `/reload-skills`, `/reload-plugins`, `/claude-api prompt-audit`, `/claude-api cost-optimize` | built-in; Availability varies; terminal-dialog commands are not on every surface |
| [Codex](agents/codex.md) | `codex doctor` | `codex debug prompt-input`, plugin/hooks/features inspection, Scheduled Tasks | built-in; `codex doctor` covers startup/connectivity/performance, not Claude's instruction-trimming workflow |
| [Antigravity](agents/antigravity.md) | `/learn` | `/skills`, `/agents`, `/hooks`, `/mcp`, `/config`, `/usage` | built-in; No documented doctor command; `/learn` output path conflicts across official pages |
| [Cursor](agents/cursor.md) | Customize inventory | /update-cli-config, /update-cursor-settings; workflow status | built-in + project; IDE settings and agent CLI settings are different surfaces |
| [Kiro](agents/kiro.md) | Agent Steering & Skills | CLI /guide; agent/profile configuration; workflow status | built-in + project; Guide is CLI-only; inspect effective resources before changing configuration |

Move procedures out of always-loaded instruction files and into project-prefixed skills. Use
scheduled audits only when their output has an owner and a durable destination.

</details>

---

## Cross-cutting architecture concerns

### Control Plane & Authority

Use host permissions and protected CI for enforceable controls. A third-party or project skill
can describe a procedure; it does not create a cross-agent permission boundary.

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | permission rules | hooks, sandbox, managed settings | built-in; Hooks are often fail-open; the OS sandbox covers Bash descendants but is unavailable on native Windows. See the canonical inventory's enforcement boundary |
| [Codex](agents/codex.md) | permission profiles | hooks, native sandbox, `requirements.toml`, project trust | built-in; Native Windows has OS-level sandboxing; an untrusted project skips project `.codex/` layers; full access flips web search to live, while apps bypass the command-network proxy/allowlist |
| [Antigravity](agents/antigravity.md) | Deny/Ask/Allow permissions | Terminal Sandbox, hooks, project settings, artifact review | built-in; `Deny > Ask > Allow`; sandbox is opt-in/preview. CLI Features says Windows `AppContainer`, while the dedicated Sandbox pages omit Windows |
| [Cursor](agents/cursor.md) | Permission configuration | hooks and scoped CLI rules | built-in + project; Hook coverage differs in cloud; hook failure can be fail-open |
| [Kiro](agents/kiro.md) | Agent permissions | tools/resources; PreToolUse hooks | built-in + project; Use the active surface/schema; a permission allowlist is not a tool inventory |

Model prompts express intent; they are not the security boundary. On native Windows, Codex has a
documented OS command sandbox, Claude Code does not, and Antigravity's official pages conflict over
`AppContainer` support. Put irreversible or privileged actions behind controls the acting agent
cannot silently redefine.

### Evidence & System of Record

Use an existing durable work record when another session must continue, fix or verify the result.
The optional [work artifact pilot](../templates/work/README.md) illustrates the required pointers;
a repository-visible handoff must still be transferred to a new checkout or host.

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | Git + CI + `work/<id>/` | project tests/checks | project; **N/A** for a purpose-built agent-configuration evaluation suite |
| [Codex](agents/codex.md) | Git + CI + `work/<id>/` | project tests/checks | project; **N/A** for a purpose-built agent-configuration evaluation suite |
| [Antigravity](agents/antigravity.md) | Git + CI + `work/<id>/` | Artifacts, project tests/checks | project + built-in; Artifacts improve review but are not the repository's durable system of record by default |
| [Cursor](agents/cursor.md) | Git + workflow state | logs, revision hashes and work records | project; Record explicit runtime load traces; files alone do not prove discovery |
| [Kiro](agents/kiro.md) | Git + workflow state | Spec artifacts, logs and resource settings | project + built-in; Preserve portable outputs; do not treat machine-local state as transferred |

Build project-specific CI for agent configuration where its behavior matters. A deterministic gate
provides a guarantee only when the current agent cannot modify, disable, or bypass that gate.
Prove a blocking control by attempting the action it is meant to block, and repeat that test after
relevant instruction, hook, permission, sandbox, or CI configuration changes. A green check proves
only its encoded contract; it does not replace independent review.

### Human Governance

Questionnaires, explanation and learning procedures may help the people making decisions.
They are optional support, not required lifecycle gates.

| Agent / inventory | Start with | Optional support | Availability / surface |
|---|---|---|---|
| [Claude Code](agents/claude-code.md) | **N/A by design** | permissions, hooks, review, deployment approvals | N/A; Intent acceptance, authority maps, production approval, and accountability stay human-owned |
| [Codex](agents/codex.md) | **N/A by design** | permissions, hooks, review, deployment approvals | N/A; Intent acceptance, authority maps, production approval, and accountability stay human-owned |
| [Antigravity](agents/antigravity.md) | **N/A by design** | permissions, Artifact Review, hooks, deployment approvals | N/A; `/goal`, `/boost`, and teams expand execution, not accountability |
| [Cursor](agents/cursor.md) | Accountable owner | permission controls and reviewed release process | project + built-in; Native automation does not authorize publication or deployment |
| [Kiro](agents/kiro.md) | Accountable owner | Spec decisions and permission controls | project + built-in; Quick Spec convenience does not replace business acceptance |

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
