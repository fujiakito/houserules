# Review: close the evaluation and reposition

Review date: 2026-09-21  
Target: `docs/close-evaluation-and-reposition` at
`7b4446392dd45402cee8c02738906aadc27cc5ad`  
Base: `main` at `5d1206e3efe6091fcd292684914155dcd9e6c79c`  
Merge base: `5d1206e3efe6091fcd292684914155dcd9e6c79c`  
Scope: committed diff `main...docs/close-evaluation-and-reposition`; the newly created review file was
not part of the reviewed implementation.  
Method: `hr-code-review`, applied sequentially in this session. This is not an independent review.

## Verdict

**Yes: the repositioning is in the right direction, and the branch is solid enough to merge.** It
does three important things correctly:

1. It closes a narrow experiment with a narrow conclusion instead of turning a null result into an
   equivalence or product claim.
2. It puts repository-owned contracts, evidence and deterministic gates ahead of optional skills or
   vendor-specific orchestration.
3. It converts attractive but unproven work into evidence-triggered decisions rather than a roadmap
   of speculative mechanisms.

The evaluation itself is concrete and unusually auditable for an agent-workflow experiment: frozen
inputs have byte hashes; calls, outputs, versions, configuration and costs are recorded; the
generation-side directory leak is disclosed; the corrected run is preserved separately; and the
committed aggregation producer reproduces the published statistics. The conclusion is also properly
bounded to one handoff presentation, one synthetic packet, one model family and one CLI surface.

**There are no blocking Standards or Spec findings in the final target.** “Solid” should not be read
as “the product has been shown to improve agent performance,” however. The evidence supports the
branch's actual claim—**no advantage demonstrated by this saturated instrument**—and supports
stopping this evaluation. It does not establish equivalence, general portability, AGI readiness, or
resilience to recursive self-improvement.

## Purpose of the evaluation

The v2 evaluation asks one deliberately small causal question: when task facts and the consumer
protocol are held constant, does the candidate session-note/handoff presentation improve the next
consumer's dispositions relative to the baseline presentation? The rubric scores four disposition
behaviours, not software correctness or broad agent quality. The branch then uses the answer to decide
whether that presentation deserves promotion.

That is the correct purpose for this repository because the repository's admission rule requires
comparative evidence before a fallback becomes recommended/default. It is **not** an evaluation of
all handoff artifacts, the workflow as a whole, or the three optional `hr-` skills. The final text
keeps those boundaries explicit.

The repositioning has a second purpose: move the project's center of gravity away from “ship more
agent procedure” and toward the stable layer that the repository can own—contracts, checks, evidence
and explicit enforcement limits. The README wording, the enforcement map and the deferred-trigger
table are consistent with that goal.

## Standards review

Severity definitions used here:

- **Blocking** — makes the claimed result wrong, unreproducible, unsafe to rely on, or violates a
  mandatory repository rule.
- **Major** — materially weakens the result or sends a likely implementer in the wrong direction.
- **Minor** — concrete local defect with limited consequence.
- **Advisory** — improvement or future direction, not a defect in this branch.

### No findings

No Blocking, Major or Minor Standards findings remain.

- External/local claims are qualified at the relevant surface and version, linked to committed
  primary evidence, or explicitly bounded as design decisions.
- Recorded attempts are appended rather than silently rewritten; the flawed 2026-09-16 data remain
  available and are annotated, while the corrected 2026-09-17 run is a separate record.
- Exact-byte evidence paths are protected in `.gitattributes`, and the committed records carry their
  hashes.
- The branch naming guidance now matches the repository's Conventional Commit types rather than an
  agent brand.
- Documentation changes do not add another canonical document or duplicate an existing owner's
  content.

### Advisory S-A1 — tighten “independent” language on the next edit

`research/PORTABILITY.md` describes saturation as reproducing “independently.” The records do show a
new execution with separate calls and a corrected harness, but it uses the same frozen scenario,
rubric, model family and grader family, and a nearby CLI version. The surrounding text already states
those limitations, so this is not misleading enough to block. On the next natural edit, prefer
“reproduced in the separate leak-free run” to avoid suggesting independent models, graders or
investigators.

Next action: wording-only cleanup when this section is next touched; do not reopen the experiment for
it.

## Spec review

### No findings

No Blocking, Major or Minor Spec findings remain.

Evidence inspected:

- The committed aggregation producer, run against the committed bundle, reproduced `n=10`, baseline
  mean `3.90`, candidate mean `3.85`, paired difference `-0.05`, seven ties, and both reported 95%
  intervals spanning zero.
- Per-check aggregation reproduced the saturation claim: checks 1–3 are `1.0` for both arms and only
  check 4 varies.
- The conclusion says “no advantage demonstrated,” not “equivalent” or “worse”; this is the right
  interpretation of a small sample whose interval spans zero.
- The final account discloses the original working-directory leak and bases interpretation on the
  corrected run.
- The deferred-work table gives concrete revisit triggers and does not pretend that missing checks
  already exist.

### Advisory P-A1 — preserve the raw-result/recomputed-result distinction

The aggregation script is a post-run producer committed after the captured calls. That is acceptable
because the JSON records preserve the raw per-call scores and provenance distinguishes later
aggregation. Future evaluations should continue to record which artifact existed at execution time
and which was generated later. Do not describe a later recomputation as part of the original harness.

Next action: retain the current provenance pattern in any future trial.

## Is the path and direction right?

### What is right

The project's strongest design choice is to optimize for **invariants across changing executors**:

- Repository rules define scope and authority.
- Ordinary artifacts preserve state across sessions and products.
- Checks make a narrow subset of requirements deterministic.
- The enforcement map states exactly what a passing check does *not* prove.
- Vendor-native features can accelerate work without becoming the only place a guarantee lives.
- Optional procedures must earn promotion through observed gaps and comparative evidence.

This is more durable than trying to predict the winning agent, model, skill format or orchestration
framework. It also scales in the right conceptual direction: as executors become more capable, the
project should reduce dependence on detailed step-by-step prompting and increase investment in
machine-checkable boundaries, evidence integrity, least authority and recovery.

Closing this evaluation is also correct. Its rubric has little headroom, the measured effect is near
zero, and no pending decision depends on a finer estimate. Running more identical pairs would create
more precise evidence about an instrument that cannot answer the broader question.

### What would be the wrong direction

Do **not** respond to fast model progress by:

- adding one skill per lifecycle stage;
- encoding every vendor feature into the portable core;
- treating longer context or more elaborate handoff prose as safety;
- adding autonomous loops without an authority model and external stop condition;
- claiming “AGI-ready” from a one-model synthetic workflow trial;
- converting every hypothetical risk into a check before a real contract or failure defines what the
  check should enforce.

Those moves increase surface area and maintenance while leaving the actual control boundary unclear.

## AGI and RSI: what this branch can and cannot support

“AGI” and “recursive self-improvement (RSI)” have no operational definition or acceptance criterion
in this repository. Whether or when either will occur, and what architecture would be sufficient for
them, is **(unverified)**. Accordingly, the defensible question is not “does this cope with AGI/RSI?”
but:

> If the executor becomes much more capable, persistent, fast or able to modify its own procedures,
> which project controls remain outside that executor's unilateral authority, and can the owner
> detect, contain and recover from violations?

Under that formulation, the current direction is a useful foundation but **not sufficient**:

- `AGENTS.md`, skills and workflow instructions are cooperative controls. A capable executor can
  misunderstand or ignore them.
- A check run by the same executor is evidence only if the executor cannot silently alter the check,
  its inputs, its environment or the reported result.
- CI is stronger only to the extent that branch protection, credentials and the gate itself remain
  outside the actor's authority.
- Attempt/time budgets bound effort, not scope or impact; the branch correctly records this gap.
- Evidence hashes support tamper detection only when a trusted party or system verifies them against
  an immutable reference.

Therefore the repository can plausibly cope with **more capable coding agents** if adopters retain
external authority boundaries. It cannot honestly claim to cope with AGI or RSI, and should not add
that claim.

## Recommended next direction

Keep the branch's evidence-triggered policy, but aim future evaluation at **control survival under
increasing autonomy**, not at prose-template preference.

### 1. Define capability-independent invariants

For each important operation, record:

- allowed targets and forbidden targets;
- who can authorize widening scope;
- which credentials and environments are reachable;
- the evidence required before merge/deploy/release;
- which control the acting agent cannot modify;
- rollback and incident ownership.

Prefer invariants such as “a change cannot merge without an externally enforced check” over
model-relative instructions such as “ask before editing this file.”

### 2. Add a threat model before adding autonomy features

Distinguish at least accidental overreach, prompt/context injection, compromised dependencies,
malicious task input, evaluator gaming, evidence tampering and deliberate control modification.
Map each threat to prevention, detection and recovery. If none exists, label the exposure rather than
calling the workflow safe.

### 3. Evaluate a capability ladder

When a real adopter need fires a trigger, test the same contract at increasing levels:

1. single edit in a bounded worktree;
2. multi-file change with tests;
3. long-running task with resumable state;
4. delegated or multi-agent work;
5. dependency/network access;
6. CI or deployment interaction;
7. authorized modification of agent procedures;
8. adversarial attempt to widen scope or falsify evidence.

Measure requirement satisfaction, unauthorized effects, detection latency, recovery success,
human interventions, cost and reproducibility. Use failure injection and negative controls so the
instrument has headroom.

### 4. Separate executor, evaluator and authority where consequences justify it

Different model names are not independence. For higher-risk operations, separate permissions and
evidence channels: the executor proposes, a protected system runs gates, an evaluator inspects
artifacts, and an accountable owner authorizes irreversible actions. Independence should mean that
the executor cannot rewrite the criterion, evidence or final decision—not merely that another agent
label appears in a log.

### 5. Make containment and recovery first-class

The next high-value portable contract is likely not another procedural skill. It is an adopter-owned
policy for sandbox boundaries, credential scoping, network egress, protected paths, immutable logs,
kill/disable mechanisms, rollback and post-incident reconstruction. Implement only the portions for
which a target surface and enforcement point are known; document the rest as limits.

### 6. Retain the trigger discipline

Do not schedule an “AGI evaluation.” Revisit when a concrete capability or incident changes the
threat model—for example, an agent is granted deploy credentials, persistent execution, delegation,
or permission to modify its own workflow. Each trigger should name the decision the new evidence
will support.

## Merge recommendation

**Merge.** The branch's final state is internally consistent, reproducible from committed evidence,
appropriately cautious, and strategically aligned with a fast-changing agent ecosystem. Preserve its
central claim exactly: the evaluated presentation showed no demonstrated advantage on this saturated
instrument, so it was not promoted. Treat the AGI/RSI discussion above as a direction for future
threat modeling—not as a capability claim or a request to expand this branch.

---

# Response — 2026-09-22

Applied S-A1 now rather than deferring it. P-A1 describes existing practice and needs no change. The
forward direction is acknowledged and deliberately not built.

## S-A1 — applied, with a correction to where it lives

The substance is right: "independently" claimed more than the runs support. They share the frozen
scenario, the rubric, the model family and the grader family; what differs is a separate execution, a
corrected harness and CLI 2.1.273 → 2.1.274. Nothing in that rules out a defect common to all of
them, which is exactly what "independent" would imply.

**One correction: `research/PORTABILITY.md` is the file that already worded it correctly.** It says
"in all twenty gradings, in both replications" and makes no independence claim. The overclaim was in
three other places, now all withdrawn:

| Location | Was | Now |
|---|---|---|
| `tests/workflows/prior-art/v2/README.md` | "**Saturation reproduced independently**" | "**Saturation reproduced in the leak-free run**", plus what the two runs share |
| `docs/ENFORCEMENT.md` | "in two independent runs" | "in both runs" |
| `attempt-20260917-replication.json` `findings[2]` | "reproduces independently… Two independent runs" | "reproduces in the leak-free run… Both runs", plus the shared-scenario caveat |

The record's `conclusion` is qualified the same way: reproduced on a leak-free instrument and a
different CLI build, **though not on an independent scenario, rubric or grader**.

**On deferring it to "the next natural edit":** declined, respectfully. Changing a word is not
reopening the experiment, and this branch spent six rounds on exactly one failure mode — descriptions
drifting behind the thing they describe. A known-imprecise word left in place because a better moment
will come is how that drift accumulated in the first place. It cost one commit.

No measured value moved: `pairs` and the producer-emitted `aggregate` are identical to `ef7fdd1`,
both 2026-09-16 records are unchanged, and 23/23 evidence hashes verify. `findings` and `conclusion`
are hand-written prose and are not producer output, so the record and `aggregate.py` remain in sync.

## P-A1 — no change; this is the pattern already in place

`derivation` already records that `harness.py` executed the trial and computed no statistics, that
`aggregate.py` is a post-run producer committed afterwards, and which artifact is which. Adding a
document to promise a practice the artifact already demonstrates would be the kind of speculative
process work the intake rule in `research/PORTABILITY.md` exists to prevent. Recorded here as the
disposition; the pattern stands.

## The recommended direction

Taken as direction, not as scope for this branch — as stated. Two observations rather than edits:

- Items 1 and 5 (capability-independent invariants; containment and recovery as a first-class
  portable contract) are the same gap `docs/ENFORCEMENT.md` already carries as a deferred item:
  budgets bound effort, not scope, with a trigger naming a recorded adopter requirement or an
  observed in-scope-budget run acting outside its assigned task. The direction converges with what
  is written down; it does not need a second home.
- Item 6 restates the discipline the deferred table implements. "Do not schedule an AGI evaluation"
  is the same rule as "a gap with no fired trigger is not a backlog item", and none of the four
  triggers has fired.

The framing worth keeping from this review is the reformulation of the question: not "does this cope
with AGI or RSI", which has no acceptance criterion here, but **which controls remain outside the
executor's unilateral authority, and can the owner detect, contain and recover from violations**.
That is answerable, and the honest answer today is the one the review gives — cooperative controls
plus adopter-held external authority, which is a foundation and not a sufficiency claim.

## Standing

`python check.py`, `python install.py --check` and `python -m unittest discover -s tests` pass.
23/23 evidence hashes verify and the committed producer still reproduces the record's `aggregate`.
No Blocking, Major or Minor findings outstanding on either side.
