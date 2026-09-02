# Portability verdict

Derived from `MATRIX.md`. The question: **which capabilities survive when a team switches agent, and
what must the portable layer therefore carry?**

This matters because teams do switch.

## 0. Provenance of the adoption figures

> ⚠️ **These numbers are not externally sourced.** A prior scan of **91 mature adopters** found
> **79% carrying two or more vendor surfaces and 31% having dropped one**, with dated arrivals and
> departures. The **2,424 repositories** figure in `templates/work/README.md` comes from the same
> scan.
>
> **The scan is unpublished and its method is not recorded here, so by this project's own evidence
> rule these are `(unverified)`.** They are retained because the design decisions they support —
> carry a portable layer, do not depend on vendor-local mechanisms — hold on the mechanism analysis
> in `MATRIX.md` alone, which *is* sourced and tested. **Do not cite the percentages as established.**
> Either publish the scan with its method and date, or drop the figures.

---

## 1. The ranking

| Mechanism | Portable? | Carries execution? | Verdict |
|---|---|---|---|
| **`AGENTS.md`** | ✅ **universal except Claude Code** — and that is a one-line fix | ❌ text only | **the carrier** |
| **MCP** | ✅ every vendor surveyed | ✅ callable tools | **the only portable capability** |
| **CI / git hooks** | ✅ agent-agnostic by construction | ✅ enforcement | **the only portable guarantee** |
| `SKILL.md` | ⚠️ **format yes, path mostly** — `.agents/skills/` covers 6 of 8 surveyed agents as of 2026-09-01; Claude Code and Kiro need their own. Three directories cover all. **Also read by Anthropic Managed Agents**, which is not a coding agent at all (`MATRIX.md` §2, 2026-09-02) | ✅ procedures | portable content, still needs an installer |
| Agent hooks | ⚠️ **schema and repo-level location both shared by Claude Code and Codex** — `.claude/settings.json` vs `<repo>/.codex/hooks.json`, ~10 event names in common. **Both can block, and more widely than this file once said: 11 of Claude Code's 33 events and 7 of Codex's 11.** `MATRIX.md` section 5, blocking sets re-read 2026-09-02; Goose untested | ✅ | vendor-local |
| Subagents | ❌ | ✅ | vendor-local |
| Plugins / recipes / bundles | ❌ | ✅ | vendor-local |
| Built-in commands | ❌ each vendor's own set | ✅ | vendor-local |

## 2. What actually dies on a switch

**Every built-in command.** Claude Code's `/verify`, `/code-review`, `/batch`, `/doctor`,
`/security-review`, `/run-skill-generator` do not exist in Codex, Goose or Cursor. Codex has its own
`review` and `doctor`; the *capability* may be present but **the invocation, behaviour and depth
differ**, and nothing in the repository tells the new agent how the old one was being used.

**Every hook.** `.claude/settings.json` means nothing to `.cursor/hooks.json`. Codex is the
partial exception — `<repo>/.codex/hooks.json` shares Claude Code's schema shape and about ten of
its event names (`MATRIX.md` section 5) — but the filename differs and the event sets are not
equal: 11 against 33.

**Every subagent definition, plugin and recipe.**

What survives is not capability. **What survives is knowledge about how to work in this repository** —
and the two are easy to confuse, because a vendor's built-in feels like part of the project when it is
part of the tool.

## 3. The rule

> **A capability that must survive an agent switch can be expressed as exactly three things:**
>
> 1. **text in `AGENTS.md`**
> 2. **an MCP server**
> 3. **a CI or git-hook check**
>
> Anything else is vendor-local convenience.

Vendor-local convenience is not a bad thing — it is usually better than what you would build, and it
is free. **Use it. Do not depend on it.** The test is whether the repository still works correctly
for someone arriving with a different agent.

### The corollary that resolves the hook question

A deterministic gate is genuinely valuable and hooks are the natural place for it — but a hook binds
only the agent that reads it. **Revised 2026-08-31:** Claude Code and Codex turned out to share a
hook schema closely enough that one file can often serve both (`MATRIX.md` section 5), so this is no
longer the *least* portable mechanism on the list. It is still not a guarantee: the file location
differs, Goose is untested, Codex documents 11 events against Claude Code's 33, and nothing
holds the overlapping ten together across releases.

**Revised again 2026-09-02, and in the same direction as every previous revision of this row:** the
blocking surface is wider on both sides than this file assumed. **7 of Codex's 11 events can halt a
turn**, not just `PreToolUse` — `PermissionRequest` approves or denies outright, and
`UserPromptSubmit`, `PreCompact`, `PostCompact`, `SubagentStop` and `Stop` can return
`continue: false`. That makes a hook a *more* capable gate than this section credited it with, on
both agents. It does not change the verdict, because capability was never the problem — **binding
only the agent that reads the file is.** The resolution is unchanged:

> **The portable expression is the contract; the vendor-local one is an accelerator.**

Write the gate as a CI check first — that is what binds, and it binds regardless of who or what made
the change. Then optionally mirror it as a vendor hook for fast local feedback. If the hook and the
check disagree, the check wins, because the check is what a reviewer and a different agent will both
see.

This also inherits a principle worth keeping from a surveyed project: **validate evidence and
execution state; never trust an agent's claim that a check has run.**

## 4. What the boilerplate therefore ships

| Ships | Why |
|---|---|
| **`AGENTS.md`** — the template | universal carrier |
| **`CLAUDE.md` containing `@AGENTS.md`** | **correctness requirement, not an adapter.** Without it Claude Code ignores the file and raises no error |
| **`SKILL.md` files plus an installer** | the format is portable; the path is not. Copying into each vendor's location is the ecosystem's own working pattern |
| **CI checks** | the only portable enforcement |
| **MCP configuration** (optional) | the only portable capability |
| **A handoff contract** (see §5) | context does not cross sessions or agents; the file is the only channel |

| Does not ship | Why |
|---|---|
| agent hooks | per-vendor schema; ships as a CI check instead, optionally mirrored |
| subagent definitions | per-vendor format |
| plugin or recipe bundles | per-vendor format |
| **anything that duplicates a built-in** | `/init`, `/verify`, `/code-review`, `/doctor` already exist and are better integrated. Rebuilding them is the mistake the surveyed frameworks made |

## 5. The handoff contract

Context does not survive a session boundary and certainly not an agent boundary. When session 1
plans, session 2 reviews the plan, a Codex session implements and a third session commits, **the
on-disk artifact is the only channel**.

That makes it a **wire format, not documentation** — which is the distinction that decides whether a
template is worth having:

> **A template that only gets read is overhead. A template another session must parse and act on is a
> contract.**

Constraints, each derived rather than chosen:

| Constraint | Why |
|---|---|
| markdown with YAML frontmatter | the only format every agent reads |
| lives in the repository | the only location every agent sees |
| machine-readable state | the next session must be able to tell whether this step is done and whether it is the one to pick it up |
| carries only what the next step needs | instructions are followed (established); every line costs on every session regardless of use |
| **under 32 KiB total instruction budget** | `project_doc_max_bytes` — **32 KiB by default, configurable**. Two official pages disagree on whether it bounds the combined root-to-cwd chain or each file individually (`MATRIX.md` section 2). **This project deliberately enforces the stricter combined-chain reading**, so it is conservative rather than wrong if the other is right |

## 6. Size and cost budget

| Limit | Source |
|---|---|
| **32 KiB** — Codex `project_doc_max_bytes`, **default and configurable**. Enforced here against the **combined** chain, the stricter of two contradictory official readings | Codex docs, retrieved 2026-09-01 |
| **~100 KiB tokens** — attention degradation begins well before advertised context windows | practitioner reports `(unverified)` |
| **>20%** — inference cost increase from carrying a context file, **whether or not it helps** | arXiv:2602.11988, abstract; 4 models, 438 tasks |

The third is the one that matters most: the cost is unconditional. **An entry that does nothing still
bills on every session, for every agent, for everyone on the team.**

### Source strength — stated so it is not over-used

`arXiv:2602.11988` is an **arXiv preprint** from ETH Zurich and LogicStar.ai. Not vendor
documentation, not a blog; peer-review status unknown. Read at source 2026-08-31 — full text extracted from the PDF, including
Appendix B.

| Claim | Strength |
|---|---|
| context files do not generally improve success rates; cost >20% more; holds across LLM-generated **and** developer-written files | **established** — headline result, 4 models, 300 + 138 tasks |
| instructions in context files are well followed | established |
| **repository overviews are not helpful** | **isolated, and null.** §4.3 finds a context file does not reduce *steps before the agent first touched the files the original patch modified*. **Table 7 (Appendix B, reached from §4.4) ablates the overview category directly**: CTXBench accuracy 68.12% → 62.32% (**p = 0.15**), SWE-bench 54.36% → 54.20% (**p = 0.73**), McNemar's test. **Not significant in either direction.** Caveats that keep this off "settled": one model (GPT-5.2), LLM-generated context files only, and a null result is not a demonstration of uselessness — on CTXBench the point estimate moved *against* the "overviews are dead weight" reading. The abstract states this more strongly than the body supports |

Design decisions in this repository that omit overviews rest on the **established** row plus the
inclusion test's third condition (an agent can read the directory tree), **not** on the overview
row. Do not cite the overview row as if it were settled.

> **The condition that decision depends on.** The same paper reports that context files **do** act
> as effective overviews **when the repository has no documentation** — the case where there is
> nothing else for an agent to read. So "omit the overview" is advice for a *documented* repository.
> A repository with little or no documentation is the case where an overview earns its place, and
> this project's inclusion test should not be read as denying that.

---

## Open items

- Goose and `AGENTS.md` — undocumented, needs a local test
- Whether Goose has a standalone hook mechanism at all (Codex: resolved, it does)
- Tier 2/3 rows are documentation-sourced and untested
- **Managed Agents reads `.claude/skills/` from a mounted repository** (`MATRIX.md` §2). Two
  consequences are unresolved: whether the survey's frame should be "coding agents" at all rather
  than "anything that mounts the repo", and whether the portable layer should say anything about
  the trust boundary that creates — a skill committed here is loaded by a cloud agent **without a
  review step**. Documentation-sourced, never run.
