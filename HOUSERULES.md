# Using houserules in this project

Start with this project's AGENTS.md and existing task instructions.
This page lists installed choices; it does not authorize external actions.

## Installed skills

Ask your agent to use a skill by name, or open its local SKILL.md below.
Actual native discovery must be checked on your agent surface; files alone are not proof.

- **hr-onboard** (core): [.agents/skills](.agents/skills/hr-onboard/SKILL.md), [.claude/skills](.claude/skills/hr-onboard/SKILL.md), [.cursor/skills](.cursor/skills/hr-onboard/SKILL.md), [.kiro/skills](.kiro/skills/hr-onboard/SKILL.md), [.opencode/skills](.opencode/skills/hr-onboard/SKILL.md)

For test-first work use hr-tdd; for diagnosis use hr-diagnosing-bugs;
for code review use hr-code-review, **only if listed above**. Matt Pocock adaptations
carry their own NOTICE.md and MIT LICENSE beside SKILL.md. No companion skills,
tracker account or parallel agents are required.

## Carry work forward

No work templates selected. Use existing project records; templates are an optional install choice.

A small task needs no document set. Record the target, next action and actual verification
when another session needs them. Commit or explicitly transfer records to a fresh checkout;
ignored local files do not travel automatically.

## Verify and maintain

Run `python check.py` here after installation or changes. It checks managed copies,
instruction structure and selected work assets, not semantic correctness or runtime loading.
Run this project's tests separately. Keep existing project-owned files and foreign skills.

Re-run the houserules installer from its distribution for updates or additional selections;
preview first with --check. Nothing updates over the network in the background.
Keep HOUSERULES.md, .houserules manifests and installed material in Git; record your
customizations in project work files. Modified managed files are reported and preserved
until you reconcile them. Hooks and MCP connections are not installed by this layer.
