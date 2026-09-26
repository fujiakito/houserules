# Prior art: how four upstream skill projects evaluate themselves

**Research snapshot: 2026-09-15.** Reader: a houserules maintainer deciding how to evaluate a
candidate skill. Next action: run the harness on one `hr-` skill, starting with `hr-tdd` as
[PORTABILITY](PORTABILITY.md#fallback-admission-criteria) already records. Revisit when an upstream
harness changes, or when this repository records its own first attempt. No skill is installed,
adapted or promoted by this study.

## Scope and evidence

The subject is the **evaluation machinery** of four widely-copied upstream projects, not their
rules. Section 2 explains why the rules are out of scope; that argument is the reason this study
exists, because without it the same four projects get re-surveyed every time someone notices their
star counts.

Sources, each pinned by full commit SHA resolved with `git ls-remote` on **2026-09-15**:

| Upstream | Pinned revision | License |
|---|---|---|
| [ponytail][pt-tree] | `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` | MIT |
| [caveman][cm-tree] | `4df4b03ba538751131d24415c59a1fad0d8c2c18` | MIT (skill) + BSL-1.1 (engine/proxy) |
| [andrej-karpathy-skills][ak-tree] | `2c606141936f1eeef17fa3043a72095b4765b9c2` | MIT |
| [i-have-adhd][adhd-tree] | `4092de07ce3ed88389d77c0d623b7af89b40ac0e` | MIT |

**This is source analysis.** Nothing here was installed, and no skill was executed on any agent.
Applying [MATRIX](MATRIX.md)'s three grades:

- **tested** — only the file sizes in section 2, measured locally with `wc` on the retrieved
  bodies, 2026-09-15.
- **documented** — every rule quotation and every benchmark figure below. These are the upstream
  authors' own published numbers about their own projects, retrieved 2026-09-15. Read them as
  vendor claims, not as independent measurements; where an author publishes a result against their
  own interest that is noted, because it changes how much weight the number carries, not its grade.
- `(unverified)` — the popularity figures, scraped from rendered GitHub pages on 2026-09-15 and
  not cross-checked against the API. They are recorded because the copy volume explains why these
  projects keep arriving in conversation, and for no other purpose. **Do not cite them as
  evidence of quality**; [SKILL-DESIGN](SKILL-DESIGN.md) already rules that packs are researched
  "by missing scenario, not by star count".

No comparative execution was performed. Nothing below establishes that any of these projects helps
or harms on any task on any surface.

## 1. What the four are

| Project | Governs | Distribution | Persistence |
|---|---|---|---|
| ponytail | which code gets written (a seven-rung YAGNI ladder) | skill + plugin + ~12 rules formats | `SessionStart`, `SubagentStart`, `UserPromptSubmit` hooks |
| caveman | output prose compression | skill + plugin + proxy/engine | `SessionStart` hook |
| andrej-karpathy-skills | four decision rules, derived from a third party's published observations and written by the repository's authors | a single `CLAUDE.md` | instruction-file discovery |
| i-have-adhd | output shape for an actionable reader | skill + plugin + several runtimes | `SessionStart` hook, gated on an opt-in flag file |

They are four segments of one axis, not four axes: every one ships Markdown whose mechanism is
"place text in the model's context and ask it to comply", and every one's value is realised inside
a single response. ponytail states the boundary itself — *"Ponytail governs what you build, not how
you talk (pair with Caveman for terse prose)"* — while its own output template contains a `→` that
caveman's rules forbid as costing a token without saving one. Composition across these projects is
not free, and none of them has measured it.

## 2. Why their rules are out of scope here

Measured locally with `wc`, 2026-09-15, on the bodies retrieved at the pinned revisions:

| Body | Words | Bytes |
|---|---:|---:|
| `skills/ponytail/SKILL.md` | 1,069 | 6,637 |
| `skills/caveman/SKILL.md` | 977 | 7,022 |
| `CLAUDE.md` (andrej-karpathy-skills) | 352 | 2,357 |
| `skills/i-have-adhd/SKILL.md` | 1,242 | 7,207 |
| naive concatenation of all four | 3,639 | 23,223 |

The [inclusion test](../templates/skills/hr-onboard/SKILL.md) this project applies to every
instruction requires all three of: instruction, **non-standard** ("a competent agent would assume
otherwise"), and non-obvious. *Write less code*, *do not over-abstract*, *skip the preamble*, *lead
with the next action* fail the second condition. A competent agent does not assume the opposite of
any of them.

That is the whole argument, and it applies to the content regardless of how well any of these
projects performs. It is also why the concatenated 23 KiB matters: under
[PORTABILITY §5](PORTABILITY.md#5-the-handoff-contract)'s 32 KiB combined instruction budget, four
overlapping behaviour documents would consume most of an adopting project's allowance to restate
what the model already does.

What survives the test is the *method* — how to find out whether an instruction earns its place.
That is not obvious, is not standard, and is exactly what this repository is missing.

## 3. What the upstream evidence actually shows

### 3.1 ponytail's rebuilt benchmark, and its control arms

ponytail's [agentic benchmark][pt-bench] was rebuilt in response to an external critique, and the
authors state the intent plainly: *"this run is built to be able to disprove ponytail, not just
flatter it."* Setup: Claude Code `2.1.177` headless, Haiku 4.5, `tiangolo/full-stack-fastapi-template`
at `cd83fc1`, fresh repo copy and fresh context per cell, `n=4`, LOC counted as `git diff` added
lines.

Four arms, and the arm design is the transferable part: `baseline` (no skill), `candidate`,
`caveman` as a **confound control** (if the effect were merely "be brief", this arm would match),
and `yagni-oneliner` as a **minimal-prompt control** (seven words appended to the system prompt).

Twelve feature tasks, relative to baseline:

| Arm | LOC | tokens | cost | time |
|---|--:|--:|--:|--:|
| confound control (caveman) | −20% | **+7%** | **+3%** | +2% |
| candidate (ponytail) | −54% | −22% | −20% | −27% |
| minimal prompt (seven words) | −33% | −14% | −21% | −30% |

Six safety tasks, scored by executing the produced function against adversarial input: baseline,
confound control and candidate each 100% safe (20/20); the **minimal-prompt arm 95% (19/20)**.

Three readings, each with the authors' own limitation attached:

1. The **confound control spent more tokens than baseline** while writing less code. Terseness is
   not the mechanism, and a compression instruction is not a cost saving inside an agentic loop.
   caveman's own README concedes the same: it shortens output only, its rules cost input tokens per
   turn, and *"Speed and readability are the product. The discount is the bonus."*
2. The **minimal-prompt arm reached most of the candidate's cost benefit** and beat it on time.
   What the full document bought over seven words was consistency and the safety floor — the
   minimal arm was erratic across tasks and was the only arm to drop a guard. This is the control
   that makes a long instruction document justify itself.
3. The −54% is an across-task aggregate spanning roughly 0% (irreducible backend CRUD) to −94%
   (a native `<input type="date">` replacing a hand-built component). The authors say so.

Limitations they state: one model; `n=4`; no confidence intervals; safety is a floor over six
tasks, not a security claim; the minimal-prompt wording is their own paraphrase of the critic's
argument.

### 3.2 ponytail's contamination bug

The finding worth carrying is not a number. An earlier agentic run showed a ~4% gap and was nearly
published; it was wrong, because ponytail and caveman are plugins firing a `SessionStart` hook and
that hook fired on **every arm, including baseline** — *"so the baseline was secretly running
ponytail."* The fix was per-arm isolation: exclude the operator's global plugins, load exactly one
plugin per arm.

### 3.3 i-have-adhd's published evaluation

[i-have-adhd's harness][adhd-evals] compares response quality rather than length, over 14 cases ×
3 trials × 2 conditions. Four of its design choices are the ones worth copying:

- **A rubric weighted against the candidate.** For an output-style skill, Concision carries 10% and
  Correctness 35%. The [results][adhd-results] note that the candidate improved on the two
  dimensions the rubric weights most heavily against a style change.
- **Structural blinding.** Conditions are relabelled `A`/`B`/`C` before the grading prompt is built
  and the label order is permuted per group from a digest of the group key, so a resumed run
  reproduces its labels. A marker pair confines what reaches the grader to the scoring region,
  because the release-gate text names the conditions and *"sending them to a blind grader would
  leak the vocabulary the blinding exists to hide."*
- **Isolation and a model pin as runner requirements, not advice.** The runners pass
  `--setting-sources ""` (Claude) and `--ignore-user-config --ephemeral` (Codex). The stated reason
  is that the project's own always-on flag *"would inject the full i-have-adhd ruleset into the
  baseline condition and make the comparison measure the skill against itself"*. A model pin is
  required because isolation drops the operator's saved model, and without a pin the eval *"silently
  runs whatever the operator (or the CLI release) defaults to"*.
- **A release gate that can fail, published failing.** The recorded run improves every dimension
  and still reports `Release gate: FAILED`, because one absolute rule (no blocking findings) is not
  satisfied; the authors then argue the gate's own design is the thing to decide on. They also
  publish a candidate regression, trace it to one numbered rule, and say three trials are too few
  to confirm the mechanism.

Limitations they state: three trials, per-case standard deviations up to 0.95, single-case deltas
below ~0.5 not to be read as signal, one judge model of the same family as the system under test,
and a residual artifact affecting both conditions.

### 3.4 What has no evaluation

andrej-karpathy-skills publishes no evaluation. It does state falsifiable success conditions —
fewer unnecessary changes in diffs, fewer rewrites from overcomplication, clarifying questions
arriving before implementation rather than after. Those are the shape a claim should take; they
have not been measured.

## 4. Convergence with this repository's own finding

This repository reached the same failure independently. Review finding **R-003 / F-001** on the
[prior-art packets](../tests/workflows/prior-art/v2/README.md) was an unequal-instruction control:
the baseline and candidate packets differed in more than the variable under test. The fix was to
make both packets carry identical consumer-protocol bytes so that *"only the session-note/handoff
presentation varies"*, and to add a rubric rule that quoting the protocol, naming a template or
invoking a skill earns no points.

ponytail's contaminated baseline and R-003/F-001 are the same class: **something other than the
declared variable differed between arms.** Two projects and this one hit it independently, and only
one of the three caught it before publishing. That is the argument for encoding isolation and
input-hash equality as things a runner refuses to proceed without, rather than as review notes.

It is also a direct instance of two rules this project already states: *"Files on disk are not
evidence of a loaded capability"* ([AGENTS](../AGENTS.md)) and *"never trust an agent's claim that a
check has run"* ([PORTABILITY §3](PORTABILITY.md#3-the-rule)).

## 5. What to adopt, and what not to

Adopt — all of it method, none of it content:

| Adopt | From | Why |
|---|---|---|
| A confound-control arm and a minimal-prompt arm alongside baseline and candidate | ponytail | Separates "this skill works" from "more instructions work" and from "one line would do". [PORTABILITY](PORTABILITY.md#fallback-admission-criteria)'s required direct-procedure arm is a third thing again, and all four can coexist |
| Per-arm isolation and an explicit model pin, enforced by the runner | i-have-adhd | The contamination class above; an unpinned model is not a controlled comparison |
| A rubric weighted against the candidate, with indicators scoring nothing | i-have-adhd, and this repository's own v2 rubric | A style or process skill must not win on process indicators |
| A gate that can fail, published failing | i-have-adhd | Matches this repository's existing posture of publishing indeterminate v1 results and marking its own figures `(unverified)` |
| Structural blinding of a human grader | i-have-adhd | Costs nothing, and addresses the weakness the v2 record already discloses |

Do not adopt:

- **Any of the four rule sets**, for the reason in section 2. A future admission still needs
  criterion 1: a concrete gap with an observed failure on a named surface and version.
- **The headline percentages as citable numbers.** −54%, −65%, +0.427 are each single-configuration
  self-reported results with the authors' own caveats attached.
- **LLM-as-judge, for now.** It is a second evaluation problem with its own validation burden, and
  i-have-adhd names the single-judge-family limitation as its own first outstanding control.
- **Always-on persistence via hooks.** [PORTABILITY §4](PORTABILITY.md#4-what-the-boilerplate-therefore-ships)
  already excludes agent hooks from the portable layer; note that these hooks are also what caused
  the contamination in 3.2.

## 6. What this does not establish

No claim here is evidence that any `hr-` skill helps or harms. Criterion 5 asks for a baseline and
candidate comparison on this project's own skills, on a named surface, with recorded outcomes and
cost. Reading four other projects' benchmarks is not that. It supplies the arm design and the
refusal conditions for a harness; the evidence still has to be produced.

[pt-tree]: https://github.com/DietrichGebert/ponytail/tree/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156
[pt-skill]: https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/skills/ponytail/SKILL.md
[pt-bench]: https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/benchmarks/results/2026-06-18-agentic.md
[pt-hooks]: https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/hooks/claude-codex-hooks.json
[cm-tree]: https://github.com/JuliusBrussee/caveman/tree/4df4b03ba538751131d24415c59a1fad0d8c2c18
[cm-skill]: https://github.com/JuliusBrussee/caveman/blob/4df4b03ba538751131d24415c59a1fad0d8c2c18/skills/caveman/SKILL.md
[cm-readme]: https://github.com/JuliusBrussee/caveman/blob/4df4b03ba538751131d24415c59a1fad0d8c2c18/README.md
[ak-tree]: https://github.com/multica-ai/andrej-karpathy-skills/tree/2c606141936f1eeef17fa3043a72095b4765b9c2
[ak-claude]: https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/CLAUDE.md
[adhd-tree]: https://github.com/ayghri/i-have-adhd/tree/4092de07ce3ed88389d77c0d623b7af89b40ac0e
[adhd-skill]: https://github.com/ayghri/i-have-adhd/blob/4092de07ce3ed88389d77c0d623b7af89b40ac0e/skills/i-have-adhd/SKILL.md
[adhd-evals]: https://github.com/ayghri/i-have-adhd/blob/4092de07ce3ed88389d77c0d623b7af89b40ac0e/evals/README.md
[adhd-results]: https://github.com/ayghri/i-have-adhd/blob/4092de07ce3ed88389d77c0d623b7af89b40ac0e/evals/RESULTS.md
[adhd-rubric]: https://github.com/ayghri/i-have-adhd/blob/4092de07ce3ed88389d77c0d623b7af89b40ac0e/evals/rubric.md
