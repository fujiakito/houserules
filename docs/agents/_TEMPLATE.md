<!--
  Copy to <agent-name>.md. Keep the section order — it is what makes two files comparable.
  Delete any section that genuinely does not apply, and say why rather than leaving it blank.

  Prefer a real installation. If the requested pass is documentation-only, say that at the top,
  name every documented surface/version, and include the exact local enumeration still required.
  A documentation inventory must never be described as tested or supported; see README.md.
-->

# <Agent>

**Evidence status:** `tested` or `documented, not tested`.
**Measured:** `<version>` on `<surface>`, `<YYYY-MM-DD>`, or `not run`.
**Surfaces:** which exist, and whether they were each checked or not.
**Docs:** `<url>`, retrieved `<YYYY-MM-DD>`.

> Lower bound — see [README](README.md). Absence means "not recorded", not "not there".

## 1. Commands

What you type. Note whether each is built-in.

| Command | Does what |
|---|---|

## 2. Built-in skills

**Only what ships with the agent.** Anything installed belongs in section 4.

| Skill | Does what |
|---|---|

## 3. Tools

The tool calls the model can make — file access, shell, search, web. Say how the list was obtained;
it is usually not documented.

## 4. Installable — official

From the vendor's own marketplace or catalogue. **Not available until installed**, however
pre-installed it looks on your machine. Flag anything additionally gated by account or plan.

| Name | Does what | How to install | Gated? |
|---|---|---|---|

## 5. Extension points

Where *your* content goes: instruction file, skills, MCP, hooks, subagents, plugins. Paths, and
whether each is project- or user-scoped. Cross-reference `../../research/MATRIX.md` rather than
restating the comparison.

## 6. How to enumerate this yourself

The exact command or step, per surface. This is the section that keeps the file honest — without
it, nobody can tell whether the lists above are current.

## 7. Surface differences

Where the surfaces disagree, and any known bugs. Cite the issue.
