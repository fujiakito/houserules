# Cursor

**Evidence status:** capabilities `documented`, not runtime-tested. **Measured:** Windows IDE
launcher 3.19.13, build `dd066f332fcea7382764400fde902f61920648d0`, x64, 2026-09-06.
**Surfaces:** IDE, agent CLI, cloud; only launcher version/help executed locally.
Official pages linked below were retrieved **2026-09-06** using Context7 and direct page review.

> Lower bound — see [README](README.md). Installed files and launcher output do not prove loading.

## 1. Commands

| Surface / grade | Entry | Purpose |
|---|---|---|
| IDE launcher, tested | `cursor --version`, `cursor --help` | Identify this installed editor and its launcher options |
| IDE, documented | `/` skill picker | Select an explicit skill for a message |
| Agent CLI, documented | `agent --help`, `agent mcp list` | Inspect agent options and configured MCP status |

The [CLI reference](https://cursor.com/docs/cli/reference/parameters) describes agent commands;
they are not evidence that the IDE launcher invokes the same binary. Locally,
`cursor agent --version` printed the IDE version too, so it did not identify an agent runtime.

## 2. Built-in skills

The official [skills page](https://cursor.com/docs/skills) identifies these shipped names;
this is a documentation inventory, not local enumeration:

| Purpose | Names |
|---|---|
| Review | review, review-bugbot, review-security |
| Author extensions | create-hook, create-rule, create-skill, create-subagent, migrate-to-skills |
| Delivery / repetition | automate, autopilot, loop, split-to-prs |
| Other workflows | canvas, cursor-blame, sdk, shell, statusline, update-cli-config, update-cursor-settings |

The hr-code-review candidate therefore overlaps a documented native review workflow; compare
outputs before recommending it. Names here do not imply every account or surface enables them.

## 3. Tools

The [Agent overview](https://cursor.com/docs/agent/overview) documents file/codebase search,
web search, reading, editing and terminal execution. Exact model-visible schemas were not captured.
Permission rules and model instructions are different boundaries; this inventory does not test
permission enforcement. The [CLI permission reference](https://cursor.com/docs/cli/github-actions)
provides scoped read/write/shell examples, not a guarantee for every IDE or cloud operation.

## 4. Installable — official

[Plugins](https://cursor.com/docs/plugins) bundle rules, skills, agents, commands, hooks and MCP
integrations. Install/enabled state is separate from catalog availability. This pass installed no
plugin or external server. Existing user extensions were not inventoried or modified.

Documented examples on the [plugin page](https://cursor.com/docs/plugins), re-read 2026-09-06:
Hex Canvas supports data visualization and Atlassian Canvas surfaces Jira/Confluence work.
They are installed plugin components, not built-in skills. Native Cursor Plugins can also package
rules, agents, commands and hooks; the Agent Plugins format covers skills and MCP. Check the
selected package's components, installation scope and provider access before routing work to it.

## 5. Extension points

| Mechanism | Documented location / boundary | Source |
|---|---|---|
| Instructions | Root/nested AGENTS.md; scoped .cursor/rules/*.mdc; User Rules are separate | [Rules](https://cursor.com/docs/rules) |
| Skills | .agents/skills and .cursor/skills; matching user roots; Claude/Codex compatibility roots | [Skills](https://cursor.com/docs/skills) |
| MCP | .cursor/mcp.json or ~/.cursor/mcp.json; separate server setup/authentication | [MCP](https://cursor.com/docs/mcp) |
| Hooks | .cursor/hooks.json or ~/.cursor/hooks.json; event-specific command/prompt actions | [Hooks](https://cursor.com/docs/hooks) |

houserules writes .cursor/skills for a Cursor selection. Multiple compatibility copies may be
visible; same-name precedence is `(unverified)` here. Do not infer the loaded copy from its presence.
The [skills source](https://cursor.com/docs/skills), rechecked 2026-09-06 via Context7, also
documents discovery in nested project subdirectories, automatically scoped to files beneath
that subdirectory. Root skills remain repository-wide. This is documented, not locally load-tested.
Hooks can fail open; a post-edit action is not a universal pre-write gate. No hook is installed here.

## 6. How to enumerate this yourself

Use the [local acceptance record](../../tests/workflows/cursor-kiro/README.md) for measured
installation and the remaining runtime protocol. In the IDE, open Customize → Skills, record the
discovered names/roots, then invoke the selected hr- skill in a fresh fixture session. Capture the
actual invocation and loaded body; use empty and alternate-path controls. Test implicit triggering
separately. A self-reported skill list alone is insufficient.

## 7. Surface differences

The skills page now documents optional sync of ~/.cursor/skills for Cloud Agents. It does not
sync ~/.agents/skills or all local compatibility roots; repo skills travel through the repo.
This corrects the older matrix's blanket no-copy statement. Cloud hooks have a narrower event
set and do not run during initial read-only turns ([hooks](https://cursor.com/docs/hooks)).
Neither cloud sync nor native hr- loading was tested here. Keep `documented` status until a named
surface completes the runtime protocol; editor installation alone does not promote support.

| Surface | Native capability route | Extension route / boundary |
|---|---|---|
| IDE | Agent editing/testing; skill picker with native review and extension-authoring skills | Customize installs plugins/skills/MCP; user and project scopes differ |
| Agent CLI | Interactive/headless Agent; terminal and MCP inspection | CLI configuration and permissions are separate from IDE launcher options |
| Cloud | Repository task execution and selected project hooks | Personal Cursor skills require optional sync; local compatibility roots are not automatically transported |

This table is a route summary of the dated sources above, not new execution evidence.
