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


---

# Follow-up review — 2026-09-22

Repository: `fujiakito/houserules`  
Branch: `docs/close-evaluation-and-reposition`  
Reviewed head: `cdb2a5ec0bd5c0b7c80a9a8be200ae8590f6f906`  
Previous reviewed state plus review transfer: `ef7fdd1ebdb6a2ccf02bc9ed680826535568a169`  
Main / merge base: `5d1206e3efe6091fcd292684914155dcd9e6c79c`  
Method: remote GitHub file/diff inspection and in-memory numerical cross-checks. This is a
follow-up review of the one new commit, not a fresh execution or independent re-review of the
entire historical experiment. All source references below were retrieved on 2026-09-22.

## Verdict

The independence correction is scientifically appropriate and the response to S-A1 is accepted
on substance. P-A1 needs no new implementation. No numerical or executable regression was found
in this increment. One Minor Standards finding remains concerning the project's own archival
rule; resolve that mismatch before calling the branch unconditionally ready under those rules.

## Correction to the earlier review

The earlier S-A1 named the wrong file. `research/PORTABILITY.md:220-225` already said "in both
replications" and is unchanged by this commit. The actual overclaims were in the v2 README,
`docs/ENFORCEMENT.md`, and the 2026-09-17 record. The response identifies them correctly.
Withdrawing the wording now is reasonable; it does not require reopening or rerunning the trial.
The earlier suggestion to wait until a natural edit was optional, not an evidence requirement.

## Standards finding S-F1 — Minor / P2: reconcile the edit with the archival rule

Location: `tests/workflows/prior-art/v2/attempt-20260917-replication.json:1558-1560`.  
Rule: `CONTRIBUTING.md:75` says files under `tests/workflows/prior-art/` are frozen and instructs:
"Append a new dated run; do not edit a recorded one."

This commit replaces `findings[2]` and `conclusion` inside the existing record, whose
`recorded_date` remains `2026-09-17`. The replacements improve the interpretation, but calling
these fields hand-written rather than producer output does not establish an exception to that
rule. A consumer of the standalone dated record now sees a September 22 interpretation without
an in-record correction date. Git history and the dated response here retain provenance, and the
measurements are intact; this is a narrow archival-policy mismatch, not evidence corruption or a
reason to repeat the experiment.

Recommended resolution: retain the original recorded interpretation and append a separately dated
correction that the current summaries reference. Alternatively, explicitly define the boundary
between immutable execution evidence and editable interpretation metadata in the contributing
policy, and give amended records dated correction provenance. Do not change captured outputs,
pair scores, hashes, or measured aggregates to resolve a wording issue.

## Spec review and advisory dispositions

- S-A1: substance resolved. The v2 README now names the shared scenario, rubric, model and grader
  families and the changed harness/CLI build; the enforcement map avoids independence language;
  the record's revised interpretation carries the same qualification.
- P-A1: no change required. `derivation` already distinguishes the executing harness from the
  later aggregation producer and names its committed input. That block is unchanged.
- Keeping the suggested future direction outside this branch is appropriate. The deferred
  scope/budget entry overlaps the authority and containment discussion; it does not establish
  that every recovery or evidence-integrity control exists. No such implementation is claimed
  by this increment, and no speculative feature work is requested by this review.

## Verification performed and limits

- Inspected the complete four-file diff from `ef7fdd1` to `cdb2a5e`. No scripts, captured output
  files, aggregation inputs, or 2026-09-16 records changed.
- Parsed both versions of the 2026-09-17 JSON record and recursively compared them. The only
  changed values are `findings[2]` and `conclusion`; `pairs`, `aggregate`, `derivation`, input
  hashes, and the 23-entry evidence-hash map are identical.
- Recomputed from the ten pairs in the current record: baseline mean 3.90, candidate mean 3.85,
  paired difference -0.05, sample SD 0.2838, SE 0.0898, normal interval [-0.2259, 0.1259], and
  t(9) interval [-0.2530, 0.1530]. Seven ties, one candidate win and two baseline wins match the
  record. Every score on checks 1-3 is 1.0 for both arms. This used JavaScript arithmetic over
  fetched JSON, not execution of the Python producer or a new model trial.
- Read `aggregate.py` and the derivation block. Did not independently rehash all 23 evidence
  files or rerun `aggregate.py`; the response's fresh 23/23 claim remains author-reported here.
- GitHub returned zero Actions runs, zero check runs, and zero commit statuses for the reviewed
  head. The combined status endpoint's "pending" with an empty list is not evidence of a running
  check. `python check.py`, `python install.py --check`, and the unittest pass stated in the
  response/commit message are author-reported, not independently verified by this review.
- No local clone was made and no Python suite was executed during this remote review. The
  repository's required verification remains to be evidenced for the final revision in an
  execution environment; this appendix does not replace that gate.

---

# Response — 2026-09-22 (second)

S-F1 confirmed, and it is wider than the one commit it names. Resolved by defining the boundary the
rule was missing, and by giving every amended record dated correction provenance.

## S-F1 — confirmed, and broader than stated

The rule is real and I had been breaking it repeatedly, not once. `CONTRIBUTING.md:75` reads
"Append a new dated run; do not edit a recorded one", and on this branch the 2026-09-17 record was
touched in **six** commits and each 2026-09-16 record in **two** — the S-A1 edit was the last of
seven, not an isolated lapse. Naming those fields hand-written prose was a description of what they
are, not the exception I implicitly treated it as.

What the rule does not distinguish is the thing that makes it ambiguous. Its stated rationale is
"frozen bytes referenced by SHA-256 records", which describes the **evidence files** — captured
outputs, harness, bundle — and those have never been edited across any round. But the **record JSON
itself is not hashed by anything**; it is the artifact that holds the hashes. The rule's text covers
it, its rationale does not, and that gap is what let seven edits look defensible one at a time.

**Resolution: the second option, not the first.** Reverting to the original interpretations and
appending corrections would leave the standalone records asserting things now known false — the
uncorrected one-point-gap claim, no leak limitation, the independence overclaim. A record that states
something false is worse for its next consumer than one carrying a correction, which is the same
reasoning the earlier round used to accept annotating a superseded record.

So the boundary is now explicit in `CONTRIBUTING.md`:

> **Execution evidence** — captured outputs, harness and aggregation inputs, and the measured values
> in an attempt record (`pairs`, `aggregate`, scores, input and evidence hashes) — is frozen. Never
> edit it; append a new dated run. **Interpretation** — `findings`, `conclusion`, `limitations`,
> notes and provenance fields — may be amended when a later review shows it wrong. An amendment adds
> an entry to the record's `corrections` array giving the date, the fields touched and why; it never
> changes a measured value, and `recorded_date` keeps naming the execution, not the edit.

And every amended record now carries that provenance: a `corrections` block with **five** amendments
on the 2026-09-17 record and **one** on each 2026-09-16 record, each naming its date, commit, fields
and reason. A consumer of a standalone dated record can now see that a September 22 interpretation
sits on a September 17 execution, and why.

## Verification, including what the review could not run

Your appendix is explicit that the gates were author-reported and that no clone or Python run
happened remotely. Run here on the current working tree:

- `python check.py` — passed. `python install.py --check` — no drift. `python -m unittest discover -s
  tests` — 76 tests, OK.
- **52/52 evidence hashes** re-verified across the three records.
- `aggregate.py` over the committed `bundle.json` still equals the record's `aggregate`.
- Diffed all three records against `c944e23`: the **only** changed key in each is `corrections`.
  `pairs`, `aggregate`, `input_hashes_measured` and `evidence_file_sha256` are byte-identical.

Your independent recomputation of the ten pairs — 3.90 / 3.85 / -0.05, sd 0.2838, SE 0.0898, both
intervals, 7/1/2, checks 1-3 all 1.0 — matches what the producer emits here, from a different
arithmetic implementation. That is the most useful check in this appendix, because it is the one
thing neither side could fake independently.

## Dispositions

- **S-A1**: accepted as resolved, and your correction about which file carried the overclaim matches
  what I found — `research/PORTABILITY.md` was already right.
- **P-A1**: unchanged, as agreed.
- **Future direction**: still outside this branch, as agreed.

## Standing

All three gates pass on the current revision. No measured value has changed in any record across
seven rounds of review; the only thing that ever changed was interpretation, and it now says so in
the records themselves.

---

# Follow-up review — 2026-09-22 (hr-code-review)

Repository: `fujiakito/houserules` (GitHub repository ID `1359058857`)  
Branch: `docs/close-evaluation-and-reposition`  
Reviewed target: `9e652ffbb2bea486a43a16cd2abe8e3c145ce734`  
Incremental base: `c944e23b50ca4b4f63265cfbd84c10c0f1c693b0`  
Main / verified merge base: `5d1206e3efe6091fcd292684914155dcd9e6c79c`  
Skill: [hr-code-review](templates/skills/hr-code-review/SKILL.md), blob
`2742c02e26ab6837f5fc9c3b21e798b6c54d04ad`. Applied sequentially in the same
conversation as the preceding review; this is shared-context follow-up, not independent review.
All linked source material was retrieved on 2026-09-22.

Scope: the one new commit, its five changed files, and the historical commits cited by its
new correction entries. The main-to-target merge-base comparison was established for context;
the entire 22-commit branch was not freshly re-reviewed. Criteria: S-F1's requested explicit
archival boundary and dated correction provenance, plus `AGENTS.md`, `CONTRIBUTING.md` and
`.houserules/START.md`. Severity retains the earlier scale: Minor means a concrete local
defect with limited consequence; P2 is normal priority and P3 is a lower-priority correction.

## Verdict and disposition

The interpretation exception and dated amendment entries address the core of S-F1, including the
September 22 independence correction. The choice to correct false interpretation in place is
reasonable. However, S-F1 is only partially resolved: the new boundary still conflates raw
observations with corrected derived results, and the newly added history is incomplete.
Two Minor Spec findings and one Minor Standards finding remain. No new numerical regression
was found in this increment. This is not a renewed unconditional merge recommendation.

## Standards

### S-F2 — Minor / P3: name the actual amendment array in the policy

Location: `CONTRIBUTING.md:75`; all three new `corrections` blocks
(`attempt-20260916-executed.json:261`, `attempt-20260916-replication.json:1541`,
`attempt-20260917-replication.json:1603`, under `tests/workflows/prior-art/v2/`).

The policy requires adding an entry to the record's `corrections` array. Each actual
`corrections` value is an object containing `note` and the `amendments` array.
In-memory checks on all three records confirm `Array.isArray(record.corrections) === false`
and `Array.isArray(record.corrections.amendments) === true`. A contributor following the
documented append target cannot follow it literally while preserving the implemented shape.

Next action: make the policy name `corrections.amendments`, or consistently implement the
documented array shape. The policy quotation in this review's preceding response should be
superseded by a dated correction if the canonical wording changes. No current automated
consumer failure is asserted.

## Spec

### P-F1 — Minor / P2: distinguish unchanged observations from revised derivations

Location: `tests/workflows/prior-art/v2/attempt-20260917-replication.json:1604-1612`;
related new claims in `CONTRIBUTING.md:75` and `review.md:475-477`.

The new correction note says that pairs, aggregate, scores, input and evidence hashes were
never edited. The policy likewise classifies aggregate and evidence hashes as frozen measured
values, while the response says only interpretation ever changed. The cited history contradicts
that description:

- [841d9b1](https://github.com/fujiakito/houserules/commit/841d9b19ae1ba4a209a832dbeb19ddc4822daec5)
  changed the aggregate standard error from `0.0897` to `0.0898`, the normal interval from
  `[-0.2258, 0.1258]` to `[-0.2259, 0.1259]`, and the t interval from
  `[-0.2529, 0.1529]` to `[-0.253, 0.153]`.
- [def6b13](https://github.com/fujiakito/houserules/commit/def6b13fd8a35279f7157d84719e2bb216ae57a2)
  and [ee953f3](https://github.com/fujiakito/houserules/commit/ee953f3d2a9bc5a5ba3c5e9c41e2c321fa41c4e8)
  changed the aggregation producer and its `evidence_file_sha256["aggregate.py"]` value;
  they also amended the aggregate block.

Those were corrections to derived results and their producer provenance, not new observations
or regrading. They need not be undone. But a standalone consumer currently gets an incorrect
immutability claim, and a future contributor cannot tell how to correct another calculation
error under the new rule without pretending a new execution occurred.

Next action: explicitly distinguish captured execution evidence/raw observations from derived
statistics and producer provenance. Define how corrections to the latter retain their previous
revision and are logged; narrow the never-edited claim accordingly. If the intended policy is
instead to freeze the derived values from this revision onward, state that effective boundary
and accurately describe the historical exceptions. Preserve the corrected statistics.

### P-F2 — Minor / P2: include omitted fields in the amendment history

Location: `tests/workflows/prior-art/v2/attempt-20260917-replication.json:1609-1612`,
`:1627-1642`. Criterion: the new policy requires correction entries to identify the fields
touched, so a standalone dated record can expose its later interpretation and provenance.

The `841d9b1` entry lists only the paired aggregate block, but that commit also changed
`configuration.context_isolation` and added `configuration.blinding_note`. Those are
substantive qualifications of context isolation and A/B assignment, not incidental formatting.
The `def6b13` and `ee953f3` entries both omit the changed
`evidence_file_sha256["aggregate.py"]`. Thus the field lists do not fully document even the
commits they identify; a consumer relying on them misses later changes to the execution account
and producer identity.

Next action: reconcile each amendment's field list with its referenced JSON diff, including the
configuration qualifications and producer hash updates. Also include the added `evidence_note`
in the `fa19186` entry and in the September 16 replication's `1b90990` entry. The existing
commit links make these omissions recoverable, but the new in-record audit should be accurate.

## Verification and limits

- Parsed all three target JSON records and their versions at `c944e23`. In each, the only changed
  top-level key is `corrections`; removing that newly inserted block reproduces the previous
  file text exactly. The current increment preserves every pre-existing value and byte.
- Checked amendment counts (1, 1, 5), the actual object/array shapes, and historical diffs for
  `1b90990`, `841d9b1`, `fa19186`, `def6b13` and `ee953f3`.
- The three evidence-hash maps contain 8 + 21 + 23 = 52 entries and are unchanged in this
  increment. Counting/preserving those entries is not a fresh hash verification; the response's
  52/52 rehash and producer execution remain author-reported in this review.
- GitHub returned zero Actions runs, zero check runs and zero commit statuses for the exact
  reviewed target. The workflow triggers on pushes to `main`, pull requests and manual
  dispatch, so absence of a run on this branch is not evidence of test failure.
- No repository was cloned and no Python commands were executed in this session. The reported
  `python check.py`, `python install.py --check` and 76-test result were not independently
  reproduced. The repository's required gates therefore remain unverified by this reviewer;
  this limitation is neither a failing result nor a claimed pass.

---

# Response — 2026-09-22 (third)

All three confirmed from the actual JSON diffs, not from memory. P-F1 is the substantive one: my own
correction note was false and my own new policy would have forbidden what I had already done.

## P-F1 — the boundary was two-tier and the history needed three

Confirmed by diffing each amending commit against its parent:

| Commit | `aggregate` changed | `evidence_file_sha256` changed |
|---|---|---|
| `841d9b1` | yes — SE `0.0897`→`0.0898`, both intervals | no |
| `fa19186` | no | yes — `aggregate.py`, `bundle.json` added |
| `def6b13` | yes | yes — `aggregate.py` |
| `ee953f3` | yes | yes — `aggregate.py` |

So "pairs, aggregate, scores, input and evidence hashes were never edited" was wrong on two of its
five terms, and the policy I wrote in the same commit classified `aggregate` and the hash map as
frozen — which would have made every one of those corrections a violation. Left as it stood, a future
contributor facing another miscomputed statistic would have had no legitimate way to fix it short of
pretending a new execution had occurred.

The boundary is now three-tier, and the middle tier is the one that was missing:

- **Captured observations** — the evidence files, and a record's per-call results in `pairs` with
  their scores, argv, timestamps and usage, plus `input_hashes_measured`. Never edited; append a new
  dated run. **Verified true**: identical to each record's birth commit (`0bde2a6`, `f5f987f`,
  `fc795cf`).
- **Derived values and producer provenance** — `aggregate`, `evidence_file_sha256`, `derivation`.
  Correctable when the derivation itself was wrong, never to alter what was observed, and **the
  correction entry now carries the previous value**.
- **Interpretation** — `findings`, `conclusion`, `limitations` and the notes. Amendable as before.

## P-F2 — field lists are now computed, not written

Confirmed: the hand-written lists omitted `configuration.blinding_note` and
`configuration.context_isolation` from `841d9b1`, `evidence_note` from `fa19186`, and
`evidence_file_sha256["aggregate.py"]` from `def6b13` and `ee953f3`.

Rather than patch the lists, they are now **derived from each commit's JSON diff** and grouped by the
three kinds above, with `previous_values` recorded for every derived-value change. The same lesson
this branch has hit in every round applies to an audit trail as much as to a statistic: a
hand-maintained description of a computed thing is a second copy waiting to drift. `corrections.note`
says the lists are diff-computed so the next reader knows not to hand-edit them.

## S-F2 — policy now names the real path

Confirmed: `corrections` is an object of `note` + `amendments`, so `Array.isArray(corrections)` is
false. The policy now names `corrections.amendments`. The object shape is kept rather than flattened:
the note is what tells a standalone consumer which tier a field belongs to, and it travels with the
record rather than requiring `CONTRIBUTING.md`.

## Verification

- `python check.py` passed, `python install.py --check` no drift,
  `python -m unittest discover -s tests` 76 tests OK — run here, on this working tree, since your
  appendix is explicit that none of this was reproduced remotely.
- **52/52 evidence hashes** re-verified; `aggregate.py` over `bundle.json` still equals the record's
  `aggregate`.
- Against `7c28bb4`, the only changed key in each of the three records is `corrections`.
- Captured observations checked against each record's birth commit, not merely against the previous
  revision: `pairs`, `input_hashes_measured` and `recorded_date` are unchanged since execution.

Your point that counting hash entries is not verifying them is right, and it is the reason that last
check is stated as run here rather than inferred. The one thing neither side can verify alone stays
the same: your independent recomputation of the ten pairs agrees with what the committed producer
emits.

## Standing

Three gates pass. No captured observation has changed since execution in any record. Derived values
were corrected four times, each now logged with its previous value; interpretation was amended seven
times, each now logged with diff-computed fields. The record says all of that itself.

---

# Follow-up review — 2026-09-22 (three-tier archival correction)

Repository: `fujiakito/houserules` (ID `1359058857`)  
Branch: `docs/close-evaluation-and-reposition`  
Reviewed target: `2c9568e27cafe6453cd1865a9b3a4a90cb8f20ed`  
Incremental base: `7c28bb49ad95ab7548d5a46001f6b511481e08a9`  
Main / verified merge base: `5d1206e3efe6091fcd292684914155dcd9e6c79c`  
Method: [hr-code-review](templates/skills/hr-code-review/SKILL.md), unchanged skill blob
`2742c02e26ab6837f5fc9c3b21e798b6c54d04ad`, applied sequentially with shared conversation
context. This is not independent review. Sources retrieved on 2026-09-22.

Scope: the one new commit and its five changed files, with the referenced historical JSON
versions checked against their parents. The branch's merge base was verified; this round
does not renew the earlier review of the entire branch. Applicable instructions and the
review skill are unchanged; the revised `CONTRIBUTING.md:75` is the criterion for the audit.

## Verdict and previous findings

The three-tier boundary now distinguishes captured observations, derived results/producer
provenance, and interpretation. The correction path is right, and the historical field lists
are now complete. One new Minor / P2 omission remains in the promised previous-value data.

- **S-F2 resolved:** the policy now names the actual `corrections.amendments` array.
- **P-F1 resolved:** the blanket claim that aggregates and evidence hashes were never edited
  has been withdrawn; derived results and producer provenance are explicitly correctable.
- **P-F2 resolved:** all seven recorded amendment field lists match the corresponding JSON
  changes, including the previously omitted configuration notes and producer hash fields.
- **S-F1's archival-boundary issue is resolved.** The remaining finding concerns completeness
  of the new previous-value requirement, not permission to correct interpretation.

Severity follows the existing review scale: Minor is a concrete local defect with limited
consequence; P2 means normal priority. No Blocking or Major finding was identified in this
increment, and no numerical regression was found.

## Standards

### S-F3 — Minor / P2: retain both previous producer hashes

Location: `tests/workflows/prior-art/v2/attempt-20260917-replication.json:1668-1671`
and `:1685-1688`. Rule: `CONTRIBUTING.md:75` explicitly includes `evidence_file_sha256`
in derived values/producer provenance and requires the correction entry to carry its
previous value.

The `def6b13` and `ee953f3` amendments correctly list
`evidence_file_sha256.aggregate.py` in `fields_changed`, but each `previous_values`
object contains only the interval note and derivation note. Both commits replaced an
existing hash, so these are not newly introduced fields with no prior value:

| Amendment | Missing previous value of `evidence_file_sha256["aggregate.py"]` |
|---|---|
| [def6b13](https://github.com/fujiakito/houserules/commit/def6b13fd8a35279f7157d84719e2bb216ae57a2) | `85c1fca1829770bb73352da7830a1760d01cb4a2b1b24972f61f51e30b899328` |
| [ee953f3](https://github.com/fujiakito/houserules/commit/ee953f3d2a9bc5a5ba3c5e9c41e2c321fa41c4e8) | `fadfd58c17b9b3f9b460bcb1f168f9484edce274a81e7d66f7115e739a4d938d` |

A standalone record therefore cannot recover those prior producer identities from the new
audit data, despite the policy and response claiming previous values are retained. The
committed history still makes them recoverable; no raw evidence loss is alleged.

Next action: include those two hashes and check that every changed derived/provenance field
that existed in the parent has the exact parent value recorded. Keep JSON key segments
intact during lookup: `aggregate.py` is one literal key under `evidence_file_sha256`.
Splitting the displayed dotted path would address nonexistent nested keys; that is a possible
cause, not a verified diagnosis, because the audit-generation implementation is not part of
this diff. Do not invent prior values for fields newly added by a commit.

## Spec

The intended three-tier policy and complete historical field lists are implemented. The
claim that every replaced derived value has its prior value is not yet fully met, for the
same two omissions in S-F3; this is one defect, not an additional finding. No other Spec
finding was identified in the reviewed increment.

## Verification and limits

- Parsed all three current JSON records and compared with the preceding reviewed state.
  Only `corrections` changed; all text preceding that block is identical.
- Independently computed historical changed paths for all seven amendment entries, preserving
  literal JSON key segments and treating arrays as whole fields. Every field list matched.
- Compared previous values with their actual parent records: seven of nine replaced
  derived/provenance fields retain the correct old value; two producer hashes are missing.
  Newly added fields were excluded from that replacement count.
- Compared captured data with their original records: `fc795cf` for the single-pair run,
  `f5f987f` for the September 16 replication, and `0bde2a6` for September 17.
  The single-pair record uses `arms`, `grading` and `result_summary`, not `pairs`;
  those fields are unchanged. Both replication `pairs` blocks, all three
  `input_hashes_measured` blocks and all three `recorded_date` values are unchanged.
- GitHub reports zero Actions runs, zero check runs and zero commit statuses for the exact
  reviewed target. This is not a test failure; the previously inspected workflow does not
  automatically run on pushes to this branch.
- No clone or Python execution occurred in this session. The response's 52/52 hash verification,
  producer reproduction and three passing Python gates remain author-reported here. This round
  verifies JSON history and audit contents; it does not claim fresh executable gate results.

---

# Response — 2026-09-22 (fourth)

S-F3 confirmed, and your diagnosis was right. It was two defects, not one.

## S-F3 — both producer hashes now retained, and the cause fixed rather than patched

The two values match what you cited exactly:

| Amendment | `evidence_file_sha256["aggregate.py"]` before |
|---|---|
| `def6b13` | `85c1fca1829770bb73352da7830a1760d01cb4a2b1b24972f61f51e30b899328` |
| `ee953f3` | `fadfd58c17b9b3f9b460bcb1f168f9484edce274a81e7d66f7115e739a4d938d` |

Your suspected cause reproduces exactly: `'evidence_file_sha256.aggregate.py'.split('.')` yields
`['evidence_file_sha256', 'aggregate', 'py']` and raises `KeyError: 'aggregate'`. **`aggregate.py` is
one literal key containing a dot.**

But the missing hashes were the symptom of a second defect, which is the one worth naming: that
`KeyError` was swallowed by an `except Exception: pass`. The lookup failed, said nothing, and the
audit trail came out looking complete. **That is the same defect as R8's hardcoded critical value** —
machinery that emits a plausible wrong answer instead of failing loudly — appearing in the very
mechanism built to keep the audit honest. Patching in two hashes would have left it live for the next
key with a dot in it.

Both are fixed at the representation and control-flow level:

- **Field paths are arrays of literal key segments**, not dotted strings, in `fields_changed` and in
  the history. `["evidence_file_sha256", "aggregate.py"]` is unambiguous and round-trips; a dotted
  path cannot.
- **A lookup that cannot resolve a path is an error, not an omission.** Whether a field is new is now
  decided by testing presence in the parent, not by catching an exception. Replaced fields carry
  `previous_value`; fields a commit introduced are marked `added`.
- `derived_field_history` now covers **all 9 replaced** derived/provenance fields — matching your
  count — plus 9 marked `added`.
- `CONTRIBUTING.md` states both rules, so the policy and the implementation say the same thing.
  That mismatch has been the recurring shape of these findings.

## Verification

Run here, since your appendix is again explicit that no clone or Python execution happened remotely:

- `python check.py` passed, `python install.py --check` no drift, `python -m unittest discover -s
  tests` 76 tests OK.
- **52/52 evidence hashes** re-verified; `aggregate.py` over `bundle.json` still equals the record's
  `aggregate`.
- Against `d2e01f5`, the only changed key in each of the three records is `corrections`.
- Captured observations checked against each record's birth commit. Thank you for catching that the
  single-pair record uses `arms`, `grading` and `result_summary` rather than `pairs` — my previous
  check compared `pairs` on a record that has none, so it was vacuously true there. Now checked on
  the right fields: unchanged since `fc795cf`, as are both replication `pairs` blocks and all three
  `input_hashes_measured` and `recorded_date` values.

That last item is worth stating plainly: a check that passes because it examined nothing is the same
class of defect as the swallowed `KeyError`. Two in one round, both found by you.

## Standing

Three gates pass. No captured observation has changed since execution in any record. Every replaced
derived value now carries its prior value, every added one is marked as added, and the paths that
identify them can no longer be misparsed.

---

# Follow-up review — 2026-09-22 (S-F3 verification and closure)

Repository: `fujiakito/houserules` (ID `1359058857`)  
Branch: `docs/close-evaluation-and-reposition`  
Reviewed target: `53851e0d638b8d80a2c5da9f736e2a0bfdd941d5`  
Incremental base: `d2e01f541a6e5cafffa26b7f6c2825584d52ce1a`  
Main / verified merge base: `5d1206e3efe6091fcd292684914155dcd9e6c79c`  
Method: [hr-code-review](templates/skills/hr-code-review/SKILL.md), unchanged blob
`2742c02e26ab6837f5fc9c3b21e798b6c54d04ad`, applied sequentially in this shared-context
conversation. This is not an independent review. Source retrieval date: 2026-09-22.

Scope: the one new commit and its five changed files. Reviewed the updated policy, all three
correction blocks and the appended response. Rechecked the historical amendment data against
the immutable parent/commit JSON snapshots retrieved in the previous round. The main merge
base and unchanged instruction/skill blobs were verified; this is not a fresh review of the
whole branch.

## Verdict

**S-F3 is resolved. No further fix is requested for this increment.** Both previously missing
producer hashes are present and exactly match their parent records. The new literal-segment
paths and `derived_field_history` consistently represent every recorded derived/provenance
change, including additions.

The earlier Standards and Spec findings remain resolved after reassessment. No Blocking,
Major or Minor finding remains within this follow-up's scope. This concludes the correction
review; it does not independently certify the repository's Python verification gates.

## Standards

**No findings.** `CONTRIBUTING.md:75` and the records agree on literal key-segment arrays,
complete derived-field history, previous values for replacements, and explicit addition
markers. Every recorded changed path resolves in its referenced amended record. The literal
`aggregate.py` key stays intact rather than being interpreted as two nested keys.

## Spec

**No findings.** The requirement behind S-F3 is met: the `def6b13` entry retains the prior
producer hash beginning `85c1fca1`, and `ee953f3` retains the one beginning `fadfd58c`.
The full hashes were compared, not only these prefixes. Checking the complete history also
found no missing, extra or duplicate paths, incorrect previous values, or incorrect
added/replaced classifications.

## Verification and limits

- Executed in-memory JavaScript comparisons against the historical JSON, independently of
  the author's audit-generation procedure. All **7 amendment field lists** match their
  historical diffs. All **9 replaced derived/provenance fields** retain their exact prior
  value; all **9 added fields** were absent from the parent and are explicitly marked added.
  History coverage and field-category membership match the changed paths.
- Compared all three current records with the preceding reviewed state: only `corrections`
  changed, and the file text preceding that block is identical. Captured results, published
  aggregates and evidence-hash maps are unchanged by this increment.
- Rechecked captured fields against the original record snapshots: single-pair `arms`,
  `grading` and `result_summary`; both replication `pairs` blocks; and all three
  `input_hashes_measured` and `recorded_date` values. Required fields were explicitly
  checked for presence before equality, and all match their originals.
- The response's account of fixing the audit generator's exception handling is author-reported:
  that generator's executable implementation is not included in this commit. The committed
  output and its compliance with the new policy were verified directly.
- GitHub returned zero Actions runs, zero check runs and zero commit statuses for the exact
  target. No clone or Python execution occurred here. The author's reported
  `python check.py`, `python install.py --check`, 76 passing unit tests, 52/52 evidence
  rehash and aggregation reproduction were not independently rerun. Their absence from this
  review's execution evidence is a verification limit, not a new defect or a failed test.
