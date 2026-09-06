# Kiro

**Evidence status:** capabilities `documented`, not runtime-tested. **Measured:** Windows IDE
launcher 1.0.437, build `5349479558af37fecbfcdb58c199ee59d86d4dd3`, x64, 2026-09-06.
**Surfaces:** IDE 1.x, CLI 3.x, Web and Mobile in current documentation; only IDE launcher
version/help measured here. Official pages below retrieved **2026-09-06** via Context7/direct review.

> Lower bound — see [README](README.md). A CLI 2.x example is not automatically a CLI 3.x result.

## 1. Commands

| Surface / grade | Entry | Purpose |
|---|---|---|
| IDE launcher, tested | `kiro --version`, `kiro chat --help` | Identify editor; chat help opens an IDE workflow rather than proving headless execution |
| Agent CLI, documented | `kiro-cli --help`, `kiro-cli version` | Enumerate the separate terminal runtime |
| Agent CLI, documented | `kiro-cli whoami` | Inspect authentication; redact personal identifiers from evidence |

The [CLI reference](https://kiro.dev/docs/reference/cli-commands/) documents an optional command
router, so `kiro` can mean different surfaces. Here the resolved kiro.cmd launches the IDE;
`kiro-cli` was not on PATH. No authentication or agent task was attempted through that launcher.

## 2. Built-in skills

No complete named built-in **skill** inventory was established by this pass. Do not relabel
agents or Powers as shipped skills. [Built-in agents](https://kiro.dev/docs/custom-agents/built-in/)
document Default, read-only Plan, and CLI Guide workflows. [Specs](https://kiro.dev/docs/specs/)
provide feature/bugfix analysis, design and task artifacts; these overlap parts of our optional
spec/plan/diagnosis procedures. Prefer existing artifacts that satisfy the contract.

## 3. Tools

The [tool reference](https://kiro.dev/docs/tools/) names fs_read, file_search, grep_search,
fs_write, str_replace and execute_bash, plus process tools with surface restrictions. These
are documentation-derived names, not a captured tool schema. The Plan agent's documented tool
set excludes writes, shell execution and MCP; do not use it as a test of implementation ability.

## 4. Installable — official

[Powers](https://kiro.dev/docs/powers/) package specialized context/tools and require installation;
catalog presence does not establish local availability. MCP services require their own setup
and credentials. This pass installed no Powers, custom agent or server.

The [Powers page](https://kiro.dev/docs/powers/), re-read 2026-09-06, names Figma, Postman,
Netlify, Datadog, Dynatrace, Supabase and Stripe among registry examples. Their catalog presence
does not establish account access or installation here. Powers package skills and optional MCP
tools; use a design/API-test/deploy/observe integration only after checking its actual components.
The page marks Powers available in IDE, CLI v3 and Web, not Mobile. This is documentation-only.

## 5. Extension points

| Mechanism | Documented location / boundary | Source |
|---|---|---|
| Instructions | AGENTS.md in workspace root/subdirectories; .kiro/steering, plus global steering | [Steering](https://kiro.dev/docs/steering/) |
| Skills | .kiro/skills and ~/.kiro/skills; workspace takes precedence; explicit slash invocation or relevance activation | [Skills](https://kiro.dev/docs/skills/) |
| Custom agents | .kiro/agents or ~/.kiro/agents; JSON/Markdown, resources and tool/permission configuration | [Agents](https://kiro.dev/docs/custom-agents/) |
| MCP | Agent mcpServers; includeMcpJson can include .kiro/settings/mcp.json and its global counterpart | [Configuration](https://kiro.dev/docs/custom-agents/configuration-reference/) |
| Hooks | .kiro/hooks/*.json; event/action support varies across IDE/CLI/Web | [Hooks](https://kiro.dev/docs/hooks/) |

**Disputed default-resource inheritance:** the steering page says custom agents need explicit
resources. The configuration reference says custom agents inherit steering, skills and AGENTS.md
unless the CLI setting chat.disableInheritingDefaultResources is true. Both were retrieved on the
same date. Record the selected agent, version and effective resources; do not preserve the old
matrix's unconditional claim that every custom agent needs a skill:// entry. Explicit skill://
resources are documented, but this installer does not edit custom-agent configurations.

## 6. How to enumerate this yourself

Follow the [acceptance protocol](../../tests/workflows/cursor-kiro/README.md). In the IDE, inspect
Agent Steering & Skills and invoke the exact hr- name in a fresh fixture. Record the actual loaded
body and source path, not just a directory listing. Test Default and a custom agent separately,
including effective resource inheritance. The current session has no native IDE inspection tool;
the UI steps and agent execution remain pending.

## 7. Surface differences

The skills page distinguishes workspace skills on IDE/CLI/Web/Mobile from global skills on
IDE/CLI, and identifies argument substitution as CLI-only. The custom-agent page limits Web
agents to project subagent use and excludes custom agents on Mobile. These are documented
capabilities, not local results. Hooks expose different events on each surface. Do not infer
runtime compatibility from our passing Python installer checks or from an installed IDE.

| Surface | Native capability route | Extension route / boundary |
|---|---|---|
| IDE 1.x | Default/Plan; Feature, Bugfix and Quick Spec workflows; project tests | Skills, custom agents, Powers, MCP and IDE-specific hook events |
| CLI 3.x | Default/Plan/Guide; terminal and headless workflows | Powers supported in v3; record profile/resource settings and CLI permission rules |
| Web | Repository tasks and spec artifacts | Project skills; custom agents for delegation rather than primary selection; installed Powers |
| Mobile | Built-in agents and workspace skills | No custom agents, global skills or Powers in the cited capability tables |

This table summarizes the dated sources above. It does not claim the local IDE launcher has
exercised any of these model capabilities.
