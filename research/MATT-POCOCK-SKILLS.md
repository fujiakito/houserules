# Matt Pocock skills: inventory, stage coverage and portability

**Status: dated research snapshot, not a recommendation or supported-skill catalog.** Preserve
this audit as evidence of what was inspected on its retrieval date. There is no routine refresh
commitment. Recheck a specific candidate only when evaluating it for adoption. Later guide changes
do not turn these historical mappings or proposals into current policy.

**Retrieved and inspected: 2026-09-05.** Scope: every `SKILL.md` under
[`mattpocock/skills` at commit `3cca18b`](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015),
including experimental and miscellaneous buckets. This is a source audit, not an installation
or an end-to-end test of these skills on any agent.

## Findings

The repository contains **37 skills: 18 Engineering + 7 Productivity + 8 In Progress + 4 Misc**.
The [plugin manifest](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/.claude-plugin/plugin.json)
(version **1.2.3**) includes exactly the first **25**. The
[In Progress bucket](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/README.md)
is beta and excluded from the plugin; the
[Misc bucket](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/README.md)
is also excluded. The
[Deprecated bucket](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/deprecated/README.md)
contains no skills. Counts and manifest membership were checked locally against the downloaded
Git tree and files on 2026-09-05.

Matt's strongest contribution is a repeatable engineering discipline from intent through
implementation, plus diagnosis and architecture maintenance. It is **not a complete operational
SDLC**, and **not uniformly dependency-free**. This is our assessment of the files below, not a
benchmark of skill quality.

The [GUIDE](../docs/GUIDE.md#lifecycle-stages) now routes by task purpose without selecting Matt as
a default provider. The inventory below preserves this audit’s historical stage mapping.
Vendor availability remains owned by [the agent inventories](../docs/agents/README.md),
using their 2026-09-04 baseline and recorded surface/version limits. This audit does not
retest those inventories or imply support for uninventoried agents.

## Complete inventory, grouped by primary stage

Each skill appears once; the final column records important secondary stages. **Core** means
included in the plugin, not proven reliable. **Beta / stub** preserves upstream's maturity label.
Stage assignments are our interpretation. Each skill link is its exact inspected source;
**all upstream links in this report were retrieved on 2026-09-05**.

Productivity and writing skills do not become engineering gates merely because they can help
communicate at a stage. Cross-cutting concerns remain separate from the 12 lifecycle stages.

### 1. Onboard & Context

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [setup-matt-pocock-skills][setup-matt-pocock-skills] | Core | Configure tracker, triage labels and domain-document locations. | Writes project instructions; GitHub/GitLab need authenticated CLI; local Markdown supported. |

### 2. Intent

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [ask-matt][ask-matt] | Core | Recommend a skill and route through the workflow. | References the wider skill set and host session commands; advises rather than launches user-only skills. |
| [grill-with-docs][grill-with-docs] | Core | Interview while recording domain terms and architectural decisions. | Calls grilling + domain-modeling through a named Skill tool. |
| [research][research] | Core | Investigate primary sources and save cited findings. | Requires a background agent and source access as written. |
| [triage][triage] | Core | Verify incoming requests and move them through readiness roles. | Tracker/labels; grilling + domain-modeling; may post comments and close issues. Also stages 6, 11. |
| [grill-me][grill-me] | Core | Start a stateless requirements/design interview. | Thin wrapper around grilling; no durable output itself. |
| [grilling][grilling] | Core | Resolve dependent decisions in question rounds. | Human answers; delegates factual exploration to subagents when needed. |
| [to-questionnaire][to-questionnaire] | Core | Draft an asynchronous questionnaire for the person holding missing knowledge. | Local Markdown; prepares the document, does not send it. |

### 3. Spec & Architecture

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [domain-modeling][domain-modeling] | Core | Resolve domain vocabulary and record significant trade-offs. | CONTEXT.md/context map + ADR templates; creates documents lazily. |
| [codebase-design][codebase-design] | Core | Design deep modules, small interfaces and testable seams. | Plain guidance; optional design-it-twice reference uses parallel subagents. Also stages 5, 12. |
| [prototype][prototype] | Core | Explore logic/state in HTML or compare UI variants. | Browser/project runtime and Git branch capture; disposable code is not production validation. |
| [to-spec][to-spec] | Core | Synthesize the conversation into a spec with testing decisions. | Tracker/labels; explicitly confirms test seams despite its no-interview description. |
| [loop-me][loop-me] | Beta | Specify recurring workflows, triggers and human checkpoints. | Grilling and local workflows/*.md; creates specifications, not a scheduler. |

### 4. Plan

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [to-tickets][to-tickets] | Core | Split work into verifiable slices with blocking dependencies. | Tracker/labels; local files supported; expand-contract exception for wide refactors. |
| [wayfinder][wayfinder] | Core | Resolve a large effort through a map of decision tickets. | Tracker, claims/dependencies, grilling/domain-modeling, research/prototype and subagents; default output is decisions. |

### 5. Build

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [implement][implement] | Core | Implement a ticket, check it, review it and commit. | tdd + code-review, project test/typecheck tools and Git; commits the current branch. |
| [implement-spec][implement-spec] | Beta | Coordinate a ticket graph into one complete PR. | Background implementers, isolated worktrees, merger agent, code-review and PR access. Also stage 8. |
| [scaffold-exercises][scaffold-exercises] | Misc | Create course exercise folders, problems, solutions and explainers. | Course-specific layout, pnpm ai-hero-cli internal lint and Git; not a general application builder. |

### 6. Verify

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [tdd][tdd] | Core | Write behavior tests and implement one red-to-green slice at a time. | Project test runner and agreed seams; codebase-design as needed. Body assigns refactoring to review. Also stage 5. |

### 7. Review

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [code-review][code-review] | Core | Report Standards and Spec findings separately. | Fixed-point Git diff, tracker setup, spec/standards and parallel reviewers; see tested diff limitation below. |

### 8. Release

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [resolving-merge-conflicts][resolving-merge-conflicts] | Core | Resolve merge/rebase hunks by intent and complete integration. | Git, original issue/PR context and project checks; broad staging/commit instructions. Also stage 5. |

### 9. Deploy

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [wizard][wizard] | Core | Generate a human-operated setup, credential or migration wizard. | Bundled Bash template; GitHub writes use gh and may be skipped if unavailable; not a deploy engine. Also stage 1. |

### 10. Observe

No dedicated skill in this snapshot. `loop-me` can specify an observation workflow; it does not execute monitoring or provide telemetry.

### 11. Diagnose & Remediate

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [diagnosing-bugs][diagnosing-bugs] | Core | Build a failing feedback loop, minimise, test hypotheses and regress the fix. | Project runtime/tools; optional Bash human loop. It stops when a usable repro loop cannot be built. |

### 12. Maintain the engineering system

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [improve-codebase-architecture][improve-codebase-architecture] | Core | Find architectural friction and discuss a chosen deepening opportunity. | Subagent, codebase-design/grilling/domain-modeling; HTML report uses Tailwind/Mermaid CDN. Also stage 3. |
| [writing-for-agents][writing-for-agents] | Core | Write clear triggered procedures and prune redundant agent documents. | Mostly text/reference; invocation mechanics require host-specific interpretation. Also stage 1. |
| [retro][retro] | Beta / stub | Suggest environment improvements from session failures. | writing-for-agents and accessible session evidence; bucket README explicitly says not functional yet. |
| [setup-ts-deep-modules][setup-ts-deep-modules] | Beta | Configure TypeScript import boundaries and demonstrate a failing violation. | Installs dependency-cruiser; project layout/config and codebase-design. Also stages 3, 6. |
| [migrate-to-shoehorn][migrate-to-shoehorn] | Misc | Replace TypeScript test assertions with partial-data helpers. | Installs @total-typescript/shoehorn and needs typechecking. Also stages 5, 6. |
| [setup-pre-commit][setup-pre-commit] | Misc | Configure commit-time formatting, typechecking and tests. | Husky, lint-staged, Prettier and Node package tooling. Also stages 6, 8. |

### Control Plane & Authority

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [git-guardrails-claude-code][git-guardrails-claude-code] | Misc | Install a hook intended to block selected dangerous Git commands. | Claude-specific settings/PreToolUse/Bash matcher; Bash + jq + grep. Not a portable enforcement boundary. |

### Evidence & System of Record

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [handoff][handoff] | Core | Summarize context and point a new agent to existing artifacts. | Writes to OS temp, with suggested skills; transfer and durability remain the caller's job. |
| [claude-handoff][claude-handoff] | Beta | Seed a fresh background Claude session with a summary. | Explicit claude --bg and claude agents; vendor-specific execution. |

### Human Governance and adjacent communication

| Skill / source | Status | What it does | Dependencies and scope |
|---|---|---|---|
| [teach][teach] | Core | Teach across sessions using a stateful learning workspace. | Local learning records, reference sources and HTML lessons; adjacent to Onboard, not repo setup. |
| [wait-what][wait-what] | Core | Re-explain the last message using shared domain vocabulary. | Requests Simplified Technical English; adapt language preferences; not a lifecycle gate. |
| [writing-fragments][writing-fragments] | Beta | Capture raw writing ideas without imposing structure. | Human conversation and an append-oriented Markdown document; optional Intent support. |
| [writing-beats][writing-beats] | Beta | Build an article through user-selected narrative beats. | Raw material, human choices and an article file; optional communication support. |
| [writing-shape][writing-shape] | Beta | Turn raw material into an article paragraph by paragraph. | Human editorial decisions and separate input/output files; optional communication support. |

## Portability audit

| Dimension | Observed source contract | Consequence for houserules |
|---|---|---|
| Content and metadata | All 37 skill directories have `agents/openai.yaml`; all 22 with `disable-model-invocation: true` also set `allow_implicit_invocation: false`. Locally checked from this snapshot. | Upstream already carries Claude/Codex metadata. This is evidence of packaging effort, not evidence of loaded capability or identical behavior. |
| Cross-skill execution | `grill-with-docs` and `grill-me` explicitly name a Skill tool; `implement` invokes `tdd` and `code-review`. | Preserve the referenced skill set or rewrite calls to portable file references/host invocation. Copying one wrapper alone is insufficient. |
| Concurrency | `research`, `code-review`, `improve-codebase-architecture` and `implement-spec` require delegated execution; `grilling` delegates fact finding. | A basic agent needs an explicit sequential variant. Sequential review loses the stated independent-context property; report that limitation. |
| Project configuration | `to-spec`, `to-tickets`, `triage` and `code-review` depend on tracker configuration. Setup supports local Markdown as well as external trackers. | External accounts are avoidable for some flows; configuration dependencies remain. Prefer existing `work/<id>/` conventions rather than adding a second record system. |
| Instruction placement | `setup-matt-pocock-skills` chooses `CLAUDE.md` first when both instruction files exist. | In this project's [import arrangement](../research/PORTABILITY.md#4-what-the-boilerplate-therefore-ships), shared pointers should live in the common source. Copying setup unchanged can leave them vendor-local. |
| Durable handoff | `handoff` saves to OS temp; `claude-handoff` launches Claude directly. | Keep the useful summary/pointer discipline; use [the existing handoff contract](../templates/work/handoff.md) for a repository-visible transfer. |
| Runtime and OS | `wizard` uses Bash; the Git guard uses Bash/jq/grep; architecture reports use CDN libraries; several Misc/Beta skills install packages. | “No hosted backend required for some skills” is defensible; “all skills have no dependencies” is not. Markdown portability does not imply shell portability. |
| Names and authority | Upstream includes `code-review`; integration skills contain commit, staging, issue-write and worktree cleanup instructions. | Any future adapted skill needs an `hr-` name, rewritten internal references and scoped authority. A skill cannot authorize its own external writes or broaden a user's task. |

The official [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)
(retrieved 2026-09-05) describes the portable skill directory and optional OpenAI metadata.
Context7 was queried for `/mattpocock/skills` and `/openai/codex`; some returned Matt paths were
older than this snapshot, so pinned files take precedence. Invocation/loading behavior for this
specific pack on Claude Code, Codex and Antigravity is **unverified**. Antigravity's unresolved
surface/layout differences remain in [MATRIX §2](MATRIX.md#2-skills--the-same-standard-three-different-paths).

### Two source-level traps worth preserving

1. **Review before commit can miss the work.** `implement` runs `code-review` before committing,
   but `code-review` specifies `git diff <fixed-point>...HEAD`. A local fixture on **native Windows
   Git CLI 2.51.0.windows.1**, 2026-09-05, created two commits and then changed the tracked file
   without committing. The three-dot command included the committed change and omitted the working
   edit; `git diff HEAD` included the edit. This tests the Git command, not a live agent invocation.
   **Inference:** that composed workflow needs an explicit review scope for staged/unstaged work.
   A review contract should record the base, reviewed revision and working-tree inclusion.
2. **Descriptions can overpromise the body.** The [README](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/README.md)
   calls `tdd` red-green-refactor, but the current body explicitly moves refactoring to review.
   `to-spec` says no interview yet asks for test-seam confirmation. Adapt the actual steps and
   completion criteria; do not treat catalog summaries as execution contracts.

### Historical names are not additional available skills

The [changelog](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/CHANGELOG.md)
records `writing-great-skills → writing-for-agents` and `to-prd → to-spec`.
It removes `ubiquitous-language` (domain-modeling), `design-an-interface` (codebase-design),
`qa` (triage/to-tickets), `request-refactor-plan` (to-spec/improve-codebase-architecture),
`edit-article` and `obsidian-vault`. Replacement names in parentheses are upstream's routing,
not automatic aliases. They are excluded from the 37-file count.

## Does a portable fallback fit the project?

The follow-up [skill design analysis](SKILL-DESIGN.md) develops task-level composition, review
loops, existing-skill coexistence, license handling and evaluation. The optional artifact pilot
is defined in [Work artifacts](../templates/work/README.md).

**Yes, the purpose fits; the literal blanket exclusion needs reconsideration.**
The project's [portable contract principle](PORTABILITY.md#3-the-rule) supports keeping knowledge
and outputs usable after an agent switch. Its
[blanket exclusion of built-in duplicates](PORTABILITY.md#4-what-the-boilerplate-therefore-ships)
goes further: it can reject a useful fallback merely because a different agent has a similar
feature. This is a proposed policy refinement, not a change to the current instruction or shipping rules.

A built-in on Claude Code does not close a gap on another host. An installable plugin does not
close a gap until that surface supports it and the user has installed, enabled and provisioned it.
Conversely, lacking a named command does not mean the general agent cannot perform the task.

Use this decision rule for future work:

1. Define the **task contract**: inputs, expected result, evidence, stop conditions and authority.
2. If the current host has an available capability that meets it, use that implementation.
3. If the capability misses only an output or evidence requirement, add a small contract supplement.
4. If the capability is absent or unsuitable, use a portable procedure over available file/shell tools.
5. If required execution tools, credentials or independent review are absent, report the remaining
   limitation or hand off to a human/CI. A skill cannot manufacture missing execution capability.

The same contract can survive switching agents without forcing the same internal implementation.
If the team specifically wants Matt's interview or review method everywhere, that method is part
of its contract; merely having a command named plan/review does not establish equivalence.
Whether the extra method earns its cost must be tested against a baseline on the target surface.

### Suggested order of work

These are **candidate gaps**, not new skills approved or installed by this research.

| Priority | Contract to trial | Starting point | Acceptance evidence |
|---|---|---|---|
| First | Durable cross-agent handoff | Existing `work/<id>/handoff.md`; borrow Matt's pointer-only summaries | A fresh session on a second host resumes correctly from the repository alone. Extend the existing contract before creating another skill. |
| First | Intent → Spec → Plan continuity | grilling, domain-modeling, to-spec, to-tickets | Acceptance criteria, unresolved decisions and blocking edges remain recoverable without a tracker account. Keep interviews/spec length proportional to the task. |
| Next, for an observed host gap | Verification and review fallback | tdd, diagnosing-bugs, code-review | A known regression fails; the changed behavior passes; the report identifies the exact diff and missing evidence. No requirement to rebuild native review orchestration. |
| Next | Diagnosis record and maintenance learning | diagnosing-bugs, writing-for-agents; compare existing hr-onboard before adding anything | Repro, causal evidence and fix survive handoff; recurring mistakes become a check or one scoped procedure. Treat retro as a stub. |
| When operational work actually needs it | Release / Deploy / Observe contracts | Existing Git/CI, provider tooling and telemetry; little complete coverage from Matt | Release candidate and checks are identifiable; deploy has environment/rollback evidence; observation has a signal, threshold, owner and durable event. |
| Per stack only | Enforced architecture and commit feedback | setup-ts-deep-modules or setup-pre-commit patterns | A deliberately bad change fails a protected check. Keep language/package dependencies in an optional stack-specific layer. |

For agents with very few built-ins, the portable procedure layer is especially useful **if** the
host can read the files and execute the required tools. Start with one real target agent and one
failure; verify skill discovery, explicit invocation, reference loading and a representative task
on its exact surface/version. Mark future agents **unknown**, not unsupported or covered by assumption.

Avoid a mandatory skill for every stage. Add the smallest optional procedure that closes a measured
gap, keep dependencies explicit, and retain CI as the enforceable gate. Upstream's
[MIT license](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/LICENSE)
allows adaptation subject to its notice requirements; preserve attribution if code/text is copied.
No upstream skills, dependencies or integrations were installed by this audit.

[setup-matt-pocock-skills]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/setup-matt-pocock-skills/SKILL.md
[ask-matt]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/ask-matt/SKILL.md
[grill-with-docs]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/grill-with-docs/SKILL.md
[research]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/research/SKILL.md
[triage]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/triage/SKILL.md
[grill-me]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/grill-me/SKILL.md
[grilling]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/grilling/SKILL.md
[to-questionnaire]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/to-questionnaire/SKILL.md
[domain-modeling]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/domain-modeling/SKILL.md
[codebase-design]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/codebase-design/SKILL.md
[prototype]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/prototype/SKILL.md
[to-spec]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/to-spec/SKILL.md
[loop-me]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/loop-me/SKILL.md
[to-tickets]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/to-tickets/SKILL.md
[wayfinder]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/wayfinder/SKILL.md
[implement]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/implement/SKILL.md
[implement-spec]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/implement-spec/SKILL.md
[scaffold-exercises]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/scaffold-exercises/SKILL.md
[tdd]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/tdd/SKILL.md
[resolving-merge-conflicts]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/resolving-merge-conflicts/SKILL.md
[code-review]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/code-review/SKILL.md
[wizard]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/wizard/SKILL.md
[diagnosing-bugs]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/diagnosing-bugs/SKILL.md
[improve-codebase-architecture]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/improve-codebase-architecture/SKILL.md
[writing-for-agents]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/writing-for-agents/SKILL.md
[retro]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/retro/SKILL.md
[setup-ts-deep-modules]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/setup-ts-deep-modules/SKILL.md
[migrate-to-shoehorn]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/migrate-to-shoehorn/SKILL.md
[setup-pre-commit]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/setup-pre-commit/SKILL.md
[git-guardrails-claude-code]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/misc/git-guardrails-claude-code/SKILL.md
[handoff]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/handoff/SKILL.md
[claude-handoff]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/claude-handoff/SKILL.md
[teach]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/teach/SKILL.md
[wait-what]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/wait-what/SKILL.md
[writing-fragments]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/writing-fragments/SKILL.md
[writing-beats]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/writing-beats/SKILL.md
[writing-shape]: https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/writing-shape/SKILL.md
