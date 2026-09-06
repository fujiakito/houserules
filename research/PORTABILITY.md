# Portability verdict

Derived from `MATRIX.md`. The question: **which capabilities survive when a team switches agent, and
what must the portable layer therefore carry?**

This matters because teams do switch.

## 0. Provenance of the adoption figures

> ⚠️ **These numbers are not externally sourced.** A prior scan of **91 mature adopters** found
> **79% carrying two or more vendor surfaces and 31% having dropped one**, with dated arrivals and
> departures. The **2,424 repositories** figure came from the same scan and was removed from
> `templates/work/README.md` on 2026-09-05. It is retained here only as a historical, unverified
> claim; it no longer supports the template guidance.
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
| `SKILL.md` | ⚠️ **format broadly, paths and surface layouts vary** — the canonical coverage table is [`MATRIX.md` §2](MATRIX.md#2-skills--the-same-standard-three-different-paths). Antigravity CLI documents flat `.md` Skills rather than the nested layout installed here. **Also read by Anthropic Managed Agents**, which is not a coding agent at all (`MATRIX.md` §2, 2026-09-02) | ✅ procedures | portable content, still needs an installer |
| Agent hooks | ⚠️ **an inner schema is shared by Claude Code, Codex and Antigravity** — event → matcher → command handlers — but wrappers, paths, tool names and decision contracts differ. Antigravity uses `.agents/hooks.json` and documents five events; it has not been run. Current contracts are owned by the canonical [Claude Code](../docs/agents/claude-code.md#7-hooks), [Codex](../docs/agents/codex.md#8-hooks), and [Antigravity](../docs/agents/antigravity.md#11-hooks) inventories; Goose untested | ✅ | vendor-local |
| Subagents | ❌ | ✅ | vendor-local |
| Plugins / recipes / bundles | ❌ | ✅ | vendor-local |
| Built-in commands | ❌ each vendor's own set | ✅ | vendor-local |

## 2. What actually dies on a switch

**Every built-in command.** Claude Code's `/verify`, `/code-review`, `/batch`, `/doctor`,
`/security-review`, `/run-skill-generator` do not survive as contracts in Codex, Antigravity,
Goose or Cursor. Other agents have overlapping capabilities — Codex has `review` and `doctor`,
Antigravity has `/boost`, `/plan`, `/goal` and `/learn` — but **the invocation, behaviour, plan gate
and depth differ**, and nothing in the repository tells the new agent how the old one was used.

**Every hook.** `.claude/settings.json` means nothing to `.cursor/hooks.json`. Codex and Antigravity
are partial exceptions: `<repo>/.codex/hooks.json` and `.agents/hooks.json` share Claude Code's
event/matcher/command core (`MATRIX.md` section 5). The filenames, wrappers, tool names, event sets,
decision contracts and failure modes still differ.

**Every subagent definition, plugin and recipe.**

What survives is not capability. **What survives is knowledge about how to work in this repository** —
and the two are easy to confuse, because a vendor's built-in feels like part of the project when it is
part of the tool.

## 3. The rule

> **Project scope, adopted 2026-09-05: full SDLC coverage through portable contracts, with
> optional, evaluated fallback skills for demonstrated gaps.**
>
> Repository rules and work artifacts carry context; skills carry procedures; tools execute;
> deterministic checks enforce their encoded conditions. Loading and invocation may need a
> surface adapter. Portable content alone does not prove runtime compatibility.

Use an available native, third-party or user-owned implementation when it satisfies the contract.
The test is whether another agent can recover the inputs and produce acceptable outputs/evidence.

**Revised 2026-09-05:** the prior rule limited portable capabilities to `AGENTS.md` text, MCP
and CI checks, with "Use it. Do not depend on it" for vendor conveniences. Section 4 and
`AGENTS.md` also excluded every capability duplicating any agent built-in. That blanket exclusion
is now narrowed: a built-in on one surface does not fill a demonstrated gap on another. The
adopted scope keeps portable contracts central and admits optional fallbacks only under section
4's evidence and coexistence criteria. This is a project scope decision authorized by the user,
not a new claim that skill execution is universally portable. The earlier
[fallback analysis](MATT-POCOCK-SKILLS.md#does-a-portable-fallback-fit-the-project) records the
research rationale; it does not endorse or install that provider's skills.

### The corollary that resolves the hook question

A deterministic gate is genuinely valuable. Hooks are a useful place for fast local feedback, but
not the home of a hard guarantee: a hook binds only the agent that reads it, and configuration,
executability, timeout, or trust can fail open. **Revised 2026-08-31:** Claude Code and Codex turned
out to share a hook schema closely enough that one implementation can often serve both (`MATRIX.md`
section 5), so this is no longer the *least* portable mechanism on the list. It is still not a guarantee:
the file locations, event sets, decision contracts, and failure behavior differ across agents and
releases. Current mechanics are owned by the canonical inventories linked from `MATRIX.md`.

**Revised again 2026-09-02, and in the same direction as every previous revision of this row:** the
blocking surface is wider on both sides than this file assumed. That makes a hook a *more* capable
guardrail than this section credited it with. It does not change the verdict, because capability
was never the problem — **binding only the agent that reads the file is.**

**Revised 2026-09-03:** Claude Code's current hook contract makes the other missing dimension
explicit: several setup and runtime failures proceed without the intended block. Permission policy
and the OS sandbox provide different boundaries, while CI is the portable gate. A guarantee exists
only when the acting agent cannot modify, disable, or bypass the enforcing control. The resolution
is unchanged:

> **The portable expression is the contract; the vendor-local one is an accelerator.**

**Revised 2026-09-04:** Antigravity officially documents the same inner hook shape at
`.agents/hooks.json`, including `PreToolUse` allow/deny/modify output. This is documentation-only
and adds a third adapter, not a portable file. It strengthens the "shared contract, vendor-local
accelerator" reading without changing the guarantee boundary.

Write the gate as a CI check first — that is what binds, and it binds regardless of who or what made
the change. Then optionally mirror it as a vendor hook for fast local feedback. If the hook and the
check disagree, the check wins, because the check is what a reviewer and a different agent will both
see.

This also inherits a principle worth keeping from a surveyed project: **validate evidence and
execution state; never trust an agent's claim that a check has run.**

A green check proves only the assertions encoded in that check. It does not prove that those
assertions are sufficient, and it does not replace independent review.

## 4. What the boilerplate therefore ships

| Ships | Why |
|---|---|
| **`AGENTS.md`** — the template | universal carrier |
| **`CLAUDE.md` containing `@AGENTS.md`** | **correctness requirement, not an adapter.** Without it Claude Code ignores the file and raises no error |
| **`SKILL.md` files plus an installer** | the format is portable; the path is not. Copying into each vendor's location is the ecosystem's own working pattern |
| **Executable checks** | portable enforcement of explicit predicates, locally or in CI; see [ENFORCEMENT](../docs/ENFORCEMENT.md) |
| **MCP configuration** (optional) | the only portable capability |
| **A handoff contract** (see §5) | context does not cross sessions or agents; the file is the only channel |

| Does not ship | Why |
|---|---|
| agent hooks | per-vendor schema; ships as a CI check instead, optionally mirrored |
| subagent definitions | per-vendor format |
| plugin or recipe bundles | per-vendor format |
| **automatic replicas of built-ins or one skill per stage** | a stage is not a procedure; a new skill must pass the admission criteria below |

### Fallback admission criteria

Before promoting an optional `hr-` skill to recommended/default status, record:

1. **Concrete gap:** target operation/artifact, agent surface/version, expected contract and an
   observed failure. Missing from an inventory means unknown, not absent. An equivalent built-in
   on another surface does not disqualify a fallback here.
2. **Existing choices:** compare the user's preferred skill, available native/third-party options
   and a direct procedure. Assess outputs, authority and dependencies, not names alone.
3. **Small coherent procedure:** define trigger, inputs, outputs, completion/stop conditions and
   relevant rubric. Split skills when triggers or procedures differ substantially; spec review
   and code review can share a review contract while using different expertise.
4. **Portable core:** prefer dependency-free instructions and ordinary artifacts. Declare necessary
   tools; isolate surface bindings in adapters. Do not require a router or proprietary tracker.
5. **Evidence:** compare baseline and candidate on representative tasks with recorded outcomes,
   cost and failure cases. Validate consumption in fresh sessions on the claimed surfaces. A
   self-review pilot or file copy is not evidence of cross-agent execution.
6. **Coexistence and provenance:** optional selection, `hr-` identity, explicit installer ownership,
   preserved user skills, upstream revision/license notices for adapted material, and a maintainer
   and recheck trigger. Promote only where the evidence supports it.

Experimental candidates may be packaged for explicit opt-in before comparative promotion, with
provenance, declared dependencies and installation/usage checks. The three Matt Pocock adaptations
follow that path; see README for selections. They are not recommended replacements for native tools.
These are project design decisions, not a universally optimal architecture. Capability facts stay in `docs/agents/`;
dated research snapshots are revisited only when evaluating a concrete candidate.

### Experimental candidate comparison — 2026-09-06

Source review, not comparative execution. Native options below come from the dated
[Claude Code](../docs/agents/claude-code.md), [Codex](../docs/agents/codex.md) and
[Antigravity](../docs/agents/antigravity.md) inventories (retrieved through 2026-09-04).
This comparison does not refresh those vendor claims. Missing inventory entries do not
establish missing capability. Matt Pocock is the user's selected third-party baseline;
each candidate's NOTICE links the upstream source, pinned revision and retrieval date.

| Candidate / intended output | Existing choices and overlap | Candidate tradeoff / evaluation question |
|---|---|---|
| [hr-code-review](../templates/skills/hr-code-review/NOTICE.md): separate Standards and Spec findings bound to a revision | Claude Code's inventoried code-review and Codex's app/CLI review already inspect changes. Antigravity's inventory routes review through artifacts, custom agents and boost; no dedicated command is recorded. Matt's upstream procedure uses parallel reviewers and a tracker | Uses ordinary records and no mandatory tracker or subagents. A custom procedure may help on Antigravity, but no observed failure establishes a gap. Compare actionable findings, missed defects, false positives and cost against each target's available review workflow |
| [hr-tdd](../templates/skills/hr-tdd/NOTICE.md): a behavioral red/green regression plus implementation | All three can edit code and execute project tests. No dedicated TDD skill is recorded in these inventories; that is not proof of absence. Matt's upstream procedure includes companion-skill and seam-confirmation requirements | Retains vertical slices while reusing existing interface/task authorization. Compare regression quality, implementation correctness and cost against upstream and direct test-first instructions; lack of a named command alone earns no benefit |
| [hr-diagnosing-bugs](../templates/skills/hr-diagnosing-bugs/NOTICE.md): reproduced cause, correction and regression | Claude Code's debug overlaps directly. Codex's inventoried CI/incident integrations and Antigravity's general research/test tools cover parts of diagnosis. Matt's upstream procedure supplies a more prescriptive investigation workflow | Removes a mandatory Bash harness and condenses the procedure. Compare correct root cause, regression coverage, unnecessary changes and cost on the actual failure type; CI-specific tooling is not automatically a general-debugging substitute |

For every row, include a **direct-procedure arm**: ask for the same outcome using the project's
existing tests and ordinary files, without installing a skill. Compare identical task facts and
authority; candidate instructions grant no extra mutation, publishing or delegation permission.
Native options retain their own dependencies and surface restrictions from the inventories.
The candidates require the project's normal tools, not an additional execution runtime.

This records criterion 2's initial source comparison only. Criteria 1 and 5 remain open:
the Bottle walkthrough is shared-context acceptance, not evidence of superiority. Start a future
trial with hr-tdd as a bounded test-design experiment; evaluate review against the native option
on each claimed surface, not against all vendors simultaneously. No trial is scheduled here.

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

Practical budgets and observed run usage live in [docs/USAGE.md](../docs/USAGE.md). The research
figures below are source-specific historical measurements, not a prediction of savings or a
conversion between tokens and subscription allowance for an adopting project.

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

- **Artifact pilot validation:** the optional templates in
  [`templates/work/`](../templates/work/README.md) still need a real cross-session/agent
  trial. The [worked pilot](../tests/workflows/README.md) records this task's shared-context
  spec-review and code-fix evidence, including stale revisions; it does not establish fresh-context
  recovery or cross-host compatibility. No artifact-schema gate is claimed.
- Whether Goose has a standalone hook mechanism at all
- Antigravity has a full official inventory across four core products and its Remote/API/Enterprise
  modes but no local surface test; Cursor and Kiro now have dated inventories and local installer
  checks, but native capability execution remains untested. Remaining Tier 2/3 rows are
  documentation-sourced and untested
- **Managed Agents reads `.claude/skills/` from a mounted repository** (`MATRIX.md` §2). Two
  consequences are unresolved: whether the survey's frame should be "coding agents" at all rather
  than "anything that mounts the repo", and whether the portable layer should say anything about
  the trust boundary that creates — a skill committed here is loaded by a cloud agent **without a
  review step**. Documentation-sourced, never run.
