# Portability verdict

Derived from `MATRIX.md`. The question: **which capabilities survive when a team switches agent, and
what must the portable layer therefore carry?**

This matters because teams do switch. Measured in a prior scan of 91 mature adopters: **79% carry two
or more vendor surfaces, 31% have dropped one**, with dated arrivals and departures.

---

## 1. The ranking

| Mechanism | Portable? | Carries execution? | Verdict |
|---|---|---|---|
| **`AGENTS.md`** | ✅ **universal except Claude Code** — and that is a one-line fix | ❌ text only | **the carrier** |
| **MCP** | ✅ every vendor surveyed | ✅ callable tools | **the only portable capability** |
| **CI / git hooks** | ✅ agent-agnostic by construction | ✅ enforcement | **the only portable guarantee** |
| `SKILL.md` | ⚠️ **format yes, path no** — 7 agents, 4 different locations | ✅ procedures | portable content, needs an installer |
| Agent hooks | ❌ different schema, file and event names per vendor | ✅ | vendor-local |
| Subagents | ❌ | ✅ | vendor-local |
| Plugins / recipes / bundles | ❌ | ✅ | vendor-local |
| Built-in commands | ❌ each vendor's own set | ✅ | vendor-local |

## 2. What actually dies on a switch

**Every built-in command.** Claude Code's `/verify`, `/code-review`, `/batch`, `/doctor`,
`/security-review`, `/run-skill-generator` do not exist in Codex, Goose or Cursor. Codex has its own
`review` and `doctor`; the *capability* may be present but **the invocation, behaviour and depth
differ**, and nothing in the repository tells the new agent how the old one was being used.

**Every hook.** `.claude/settings.json` means nothing to `.cursor/hooks.json`, and neither means
anything to Codex or Goose.

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

A deterministic gate is genuinely valuable and hooks are the natural place for it — but hooks are the
least portable mechanism on the list. The resolution:

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
| **under 32 KiB total instruction budget** | Codex enforces `project_doc_max_bytes` = 32 KiB and truncates beyond it. The tightest documented limit found, so it is the one to design against |

## 6. Size and cost budget

| Limit | Source |
|---|---|
| **32 KiB** — Codex `project_doc_max_bytes`, instruction files truncate beyond it | Codex configuration |
| **~100 KiB tokens** — attention degradation begins well before advertised context windows | practitioner reports `(unverified)` |
| **>20%** — inference cost increase from carrying a context file, **whether or not it helps** | arXiv:2602.11988, abstract; 4 models, 438 tasks |

The third is the one that matters most: the cost is unconditional. **An entry that does nothing still
bills on every session, for every agent, for everyone on the team.**

### Source strength — stated so it is not over-used

`arXiv:2602.11988` is an **arXiv preprint** from ETH Zurich and LogicStar.ai. Not vendor
documentation, not a blog; peer-review status unknown. Read at source 2026-08-31, abstract and
section 4.2.

| Claim | Strength |
|---|---|
| context files do not generally improve success rates; cost >20% more; holds across LLM-generated **and** developer-written files | **established** — headline result, 4 models, 300 + 138 tasks |
| instructions in context files are well followed | established |
| **repository overviews are not helpful** | **suggestive, not isolated.** Section 4.2 measures *steps before the agent first touched the files the original patch modified* and finds a context file does not meaningfully reduce it. Correlational; **no ablation removed the overview section**. The abstract states this more strongly than section 4.2 supports |

Design decisions in this repository that omit overviews rest on the **established** row plus the
inclusion test's third condition (an agent can read the directory tree), **not** on the suggestive
row. Do not cite the suggestive row as if it were settled.

---

## Open items

- Goose and `AGENTS.md` — undocumented, needs a local test
- Whether Codex or Goose have a standalone hook mechanism at all
- Tier 2/3 rows are documentation-sourced and untested
