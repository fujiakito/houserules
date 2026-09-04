# The AI-native SDLC, by stage

This guide maps a complete software lifecycle to the capabilities currently available in Claude
Code and Codex:

`Onboard → Intent → Spec → Plan → Build → Verify → Review → Release → Deploy → Observe → Diagnose/Remediate → Maintain`

Three concerns apply across the whole lifecycle rather than forming more stages: **Control Plane &
Authority**, **Evidence & System of Record**, and **Human Governance**.

**This file is for people, not agents.** Anything an agent must act on belongs in `AGENTS.md`, a
skill, or a deterministic check, expressed as a trigger rather than background prose.

**Canonical tool facts live in [`agents/`](agents/)** — especially
[`claude-code.md`](agents/claude-code.md) and [`codex.md`](agents/codex.md). The tables below are a
routing layer only. Follow those inventories for install state, feature flags, provider, version,
plan, and surface restrictions.

**Mapping checked 2026-09-03.** The inventories retain the measured surface versions and the
retrieval date for each external claim. Recheck policy is in `../research/MATRIX.md`.

## How to read the tables

| Type | Means |
|---|---|
| **built-in** | ships with the agent or surface |
| **install** | official capability that must be installed or connected |
| ⚠️ **gated** | also requires account, plan, provider, or organization provisioning |
| **project** | supplied by this repository or the target repository |
| **N/A** | no purpose-built capability for this purpose; the general agent can still do the work |

Mixed rows list every applicable type. Assume one agent, not two: each stage must work with either
agent. Agents without a capability inventory are omitted rather than marked `N/A`.

---

## Lifecycle stages

### 1. Onboard & Context

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/init` | `/import`, `/context`, `/memory`, `/doctor`, `/hr-onboard` | built-in + project | `/import` has provider and feature-flag limits; `/context` confirms what loaded | Create and inspect the repository instruction context; discover non-obvious operating knowledge |
| Codex | `/init` | `$migrate-to-codex`, `codex debug prompt-input`, Local Environments, `$hr-onboard` | built-in + install + project | `/init` and Local Environments are surface-specific; Local Environments are desktop-only | Create/import `AGENTS.md`, inspect the model-visible prompt, and make setup repeatable |

Run the native initializer, then `python install.py`. Use `hr-onboard` for knowledge that repository
inspection cannot reveal, such as a command that only works from one directory or a test expected
to fail.

### 2. Intent

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/goal` | `/deep-research`, MCP/connectors | built-in + install + ⚠️ gated | `/deep-research` varies by plan, provider, settings, and surface | Persist the outcome and gather decision inputs before choosing a solution |
| Codex | `/goal` | `$define-goal`, `/apps`, MCP | built-in + install | `/goal` is documented from the desktop app surface; apps/MCP require a configured source | Persist or formalize the objective and bring external context into scope |

Record durable acceptance criteria in `work/<id>/`; a session goal is execution state, not the
project's system of record.

### 3. Spec & Architecture

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/plan` | `/deep-research`, Artifacts, `/design` | built-in + ⚠️ gated | Artifacts require an eligible plan/provider/surface; `/design` is for UI work, not a general architecture gate | Explore architecture, validate external assumptions, and communicate a proposed design |
| Codex | `/plan mode` | `documents`, `visualize`, MCP/apps | built-in + install | `/plan mode` is app-specific; plugins are not available in the IDE extension; no dedicated spec gate | Produce and inspect a spec or architecture artifact using general planning and document tools |

Neither agent supplies a mandatory specification format or acceptance gate. Keep the spec as small
as the change requires, and place durable output in `work/<id>/`.

### 4. Plan

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/plan` | Plan subagent, dynamic workflows | built-in + ⚠️ gated | Dynamic workflows have provider, plan, settings, and concurrency limits | Turn the accepted intent/spec into executable work and delegate bounded research |
| Codex | `/plan mode` | `/goal`, subagents | built-in | `/plan mode` and `/goal` are app commands; subagents are configuration- and concurrency-limited | Decompose the work while preserving the goal across turns |

Claude Code 2.1.251 plan mode was locally tested writing a machine-local file under
`~/.claude/plans/` on 2026-09-03. Use `work/<id>/handoff.md` when the plan must be repository-visible,
reviewable, or portable to another agent.

### 5. Build

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/batch` | `/subtask`, `/background`, `/worktree`, LSP plugins | built-in + install | `/batch` requires Git; plugin language servers are separately installed and unavailable in cloud sessions | Implement in isolated units with optional language-server feedback |
| Codex | `codex exec` + Git worktrees | managed Worktrees, `/new playground worktree`, subagents, Local Environments | built-in | `codex exec` is CLI/non-interactive; managed Worktrees, the slash command, and Local Environments are desktop capabilities | Isolate parallel changes, reproduce setup, and automate bounded implementation tasks across surfaces |

Use one worktree per parallel write stream. Both agents can coordinate concurrent work; neither is
limited to a single isolated chat.

### 6. Verify

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/verify` | `/run`, `/run-skill-generator`, Bash | built-in | Availability and launch-recipe path are disputed across official pages; confirm on the active surface before relying on them | Build and run the changed system, then capture a reusable launch recipe |
| Codex | **N/A — no dedicated verify command** | shell, Local Environments, `@Browser`, `$playwright` | N/A + built-in + install | Local Environments and Browser are desktop-specific; Playwright is installable | Execute project tests and runtime checks through general tools |

A tool invocation is not evidence by itself. Record the command, surface, version, result, and
relevant artifact. If Claude's launch skill is unavailable, store the procedure as a project skill
under `.agents/skills/`.

### 7. Review

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/code-review` | `/security-review`, `/simplify` | built-in | Interactive-first; `--fix` mutates and `--comment` posts externally | Review correctness, security, and unnecessary complexity before integration |
| Codex | `/code review`, `codex review` | `review-agent`, `codex-security` plugin (`$security-scan`) | built-in + install + ⚠️ gated | App and CLI surfaces differ; `review-agent` is delegated internally; Codex Security needs access beyond installation | Review interactively or in CI, with an optional staged security pipeline |

Use review to find issues; move requirements that must bind into deterministic CI checks.

### 8. Release

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | **N/A — no built-in atomic ship command** | `commit-commands`, `/install-github-app`, GitHub/GitLab integrations, Git/CI | N/A + built-in + install | Plugins/integrations must be installed and authenticated | Prepare commits and PRs, then let the repository's release gates decide readiness |
| Codex | `$yeet` | GitHub plugin/action, `$gh-address-comments`, Git/CI | install | `$yeet` and `$gh-address-comments` are curated skills; the GitHub Action is CI-only | Stage, commit, push, open or refine a PR, and run release gates |

Wire `python check.py` and `python install.py --check` into CI for this repository. Convenience
commands do not replace branch protection, release policy, or reproducible checks.

### 9. Deploy

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | **N/A — no built-in deploy command** | `vercel`, `firebase`, `supabase` plugins | N/A + install | Provider plugins require installation, credentials, and their target service | Invoke provider-specific deployment workflows |
| Codex | **N/A — no built-in deploy command** | `$vercel-deploy`, `$netlify-deploy`, `$render-deploy`, `$cloudflare-deploy` | N/A + install | Skills must be installed; plugin-bundled alternatives are unavailable in the IDE extension | Invoke provider-specific deployment workflows |

Production approval remains outside the agent. Prefer a CI/CD deployment identity and an explicit
environment approval over credentials embedded in an interactive session.

### 10. Observe

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `sentry` integration | OpenTelemetry, `/schedule` Routines with GitHub/API triggers, Analytics dashboard/API, `/loop` | install + built-in + ⚠️ gated | Routines and analytics vary by plan, provider, and surface; scheduling runtimes have different persistence and credentials | Inspect delivery/runtime telemetry and react to repository or API events |
| Codex | `sentry`/`posthog` plugins | Scheduled Tasks, externally scheduled `codex exec` | install + built-in | These are plugin names; Scheduled Tasks are ChatGPT/desktop capabilities, while CLI and IDE need an external scheduler | Inspect telemetry and run recurring observation tasks |

Monitoring must emit durable events or alerts. A recurring agent prompt is orchestration, not an
observability backend.

### 11. Diagnose & Remediate

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/debug` | `/autofix-pr`, `/code-review --fix`, `/security-review --fix`, `/simplify --fix`, `sentry` | built-in + install | `/autofix-pr` is a cloud/GitHub workflow; mutation and external comments need authority | Reproduce failures, trace runtime evidence, and prepare a reviewed fix |
| Codex | `$gh-fix-ci` | `$gh-address-comments`, `codex-security` fix pipeline, `sentry`/`posthog` plugins | install + ⚠️ gated | GitHub skills require repository access; Codex Security requires separately provisioned access | Diagnose CI, review, security, and production signals and prepare remediation |

Feed incident findings into `work/<id>/findings.md`, tests, and checks. Do not leave the only causal
record in a vendor conversation.

### 12. Maintain the engineering system

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | `/doctor` | `/context`, `/memory`, `/reload-skills`, `/reload-plugins`, `/claude-api prompt-audit`, `/claude-api cost-optimize` | built-in | Availability varies; terminal-dialog commands are not on every surface | Audit setup and loaded context, trim instructions, reload extensions, and inspect prompt/cost drift |
| Codex | `codex doctor` | `codex debug prompt-input`, plugin/hooks/features inspection, Scheduled Tasks | built-in | `codex doctor` covers startup/connectivity/performance, not Claude's instruction-trimming workflow | Diagnose client health and manually audit what is installed, enabled, and model-visible |

Move procedures out of always-loaded instruction files and into project-prefixed skills. Use
scheduled audits only when their output has an owner and a durable destination.

---

## Cross-cutting architecture concerns

### Control Plane & Authority

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | permission rules | hooks, sandbox, managed settings | built-in | Hooks are often fail-open; the OS sandbox covers Bash descendants but is unavailable on native Windows. See the canonical inventory's enforcement boundary | Separate advisory instructions from enforceable tool and OS boundaries |
| Codex | permission profiles | hooks, native sandbox, `requirements.toml`, project trust | built-in | Native Windows has OS-level sandboxing; an untrusted project skips project `.codex/` layers; full access flips web search to live, while apps bypass the command-network proxy/allowlist | Bound tools, filesystem/network access, escalation, and organization policy |

Model prompts express intent; they are not the security boundary. On native Windows, Codex has an
OS command sandbox and Claude Code does not. Put irreversible or privileged actions behind controls
the acting agent cannot silently redefine.

### Evidence & System of Record

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | Git + CI + `work/<id>/` | project tests/checks | project | **N/A** for a purpose-built agent-configuration evaluation suite | Preserve decisions, changes, verification, and operational findings outside the conversation |
| Codex | Git + CI + `work/<id>/` | project tests/checks | project | **N/A** for a purpose-built agent-configuration evaluation suite | Preserve decisions, changes, verification, and operational findings outside the conversation |

Build project-specific CI for agent configuration where its behavior matters. A deterministic gate
provides a guarantee only when the current agent cannot modify, disable, or bypass that gate.
Prove a blocking control by attempting the action it is meant to block, and repeat that test after
relevant instruction, hook, permission, sandbox, or CI configuration changes. A green check proves
only its encoded contract; it does not replace independent review.

### Human Governance

| Agent | Primary tool | Supporting tools | Type | Surface / constraint | Purpose |
|---|---|---|---|---|---|
| Claude Code | **N/A by design** | permissions, hooks, review, deployment approvals | N/A | Intent acceptance, authority maps, production approval, and accountability stay human-owned | Enforce a human decision without transferring responsibility to the tool |
| Codex | **N/A by design** | permissions, hooks, review, deployment approvals | N/A | Intent acceptance, authority maps, production approval, and accountability stay human-owned | Enforce a human decision without transferring responsibility to the tool |

Tools can enforce an authority decision; they cannot supply the accountable owner.
Scope authority by blast radius and reversibility, not by model capability. A stronger model may
need less assistance, but it does not inherit human accountability.

---

## Placement rule

| Layer | Cost | Trigger | Put here |
|---|---|---|---|
| `AGENTS.md` | every session | always | short, non-standard, non-obvious repository instructions |
| Path-scoped rule | matching context only | matching file/path | local instructions for one part of the tree; Claude Code-specific |
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
