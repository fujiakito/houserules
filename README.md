# houserules

**A portable agent layer for a repository — the part that does not ship with your agent, and does not
die when you switch.**

**Scope: the full SDLC, through portable contracts and optional, evaluated fallback skills.**
Today the installer supplies repository instructions, `hr-onboard`, `check.py` and its ownership
record. Six optional work templates are available separately as pilots; no new fallback skill
has been shipped or evaluated yet.
Coverage means each stage can communicate its inputs, outputs, evidence and next action when the
agent changes. Capability availability varies by surface; use the implementation that fits the task.
The shared layer carries:

1. **What is true about *this* repository** — the non-obvious rules an agent cannot read off the code
2. **What survives an agent switch** — decisions, work state and evidence another agent can consume
3. **Procedures for demonstrated gaps** — optional fallbacks when available tools or user skills
   do not satisfy the task contract; admitted under [these criteria](research/PORTABILITY.md#4-what-the-boilerplate-therefore-ships)

The name is what an entry has to answer before it goes in: **does this earn its place?**

> **Supported today: Claude Code and Codex.** Those are the two run against real installations,
> with versions recorded. Google Antigravity now has a full inventory derived from **official
> documentation only**; it is deliberately marked `documented`, not `tested`. Cursor, Copilot,
> Kiro, Goose and OpenCode remain matrix-only. See the evidence grades in `research/MATRIX.md`.

---

## Install

**Requires Python 3.9+ and nothing else** — both scripts are standard library only, on purpose. A
check that needs an install step is a check that gets skipped.

Run these from *this* repository, pointing at the repository you are adopting it into:

```bash
python install.py --repo /path/to/your-project --check
```

`--check` writes nothing. It prints exactly what would change and **exits non-zero if anything is
missing or has drifted** — so on a repository that has never been installed into, it exits 1 and
lists what it would create. "Nothing to do" is the only green state, which is what makes it usable
in CI. Read that output, then:

```bash
python install.py --repo /path/to/your-project
python check.py --repo /path/to/your-project
```

Omit `--repo` to act on the current directory. **Do not copy these files in by hand** — the
installer is what avoids overwriting an `AGENTS.md`, a `CLAUDE.md` or a skill you already have.

Then, inside your agent — `/hr-onboard` on Claude Code; **`$hr-onboard` on Codex**, which uses `$`
for skills and `/` for session commands; or mention `hr-onboard` by name on Antigravity 2.0/IDE
so progressive disclosure can load it. The installer does not create Antigravity CLI's flat-`.md`
slash-command variant; see the [Antigravity inventory §9](docs/agents/antigravity.md#9-skills).

<details>
<summary><b>If <code>python</code> is not found</b></summary>

On Windows, the launcher is usually installed even when `python` is not on `PATH`:

```bash
py install.py --repo /path/to/your-project --check
```

Otherwise use the full path to your interpreter, or the one bundled with your editor. On macOS and
Linux, `python3` may be the name.
</details>

<details>
<summary><b>To remove it</b></summary>

There is no uninstaller, because there is nothing to unwind: delete `AGENTS.md`, the `@AGENTS.md`
line from `CLAUDE.md`, `check.py`, and the `hr-onboard` directory under each agent's skills path.
Also remove `.houserules/skills.json` when removing the managed layer. Preserve your own content
in files you have edited. Everything this installs is a plain file (or an optional skill symlink).
</details>

## What it installs

| | |
|---|---|
| `AGENTS.md` | read natively by every surveyed agent **except Claude Code**. Verified by running Codex and Claude Code; the rest from official documentation, retrieved 2026-09-01 |
| `CLAUDE.md` containing `@AGENTS.md` | **required, not an adapter.** Without it Claude Code ignores `AGENTS.md` and raises no error |
| `hr-onboard` skill, in documented nested-Skill paths | one source is copied to each configured path. Antigravity CLI's documented flat `.md` variant is not synthesized; the current coverage and open test live in [`research/MATRIX.md` §2](research/MATRIX.md#2-skills--the-same-standard-three-different-paths) |
| `check.py` | the only portable enforcement: a script with an exit code binds regardless of which agent, or human, made the change |
| `.houserules/skills.json` | managed skill names, selected project paths and source digests; commit it with the installed layer |

Skill sync checks only those recorded copies. Foreign skills are preserved; local name and
frontmatter checks still apply. Digests normalize CRLF/LF in UTF-8 text so ordinary Git checkout
conversion does not cause drift; binary content stays byte-exact. Global/plugin discovery and runtime loading are outside this
offline check. Without a record, a path matching a shipped skill name fails with ownership
unknown; unrelated user skills only produce a warning. The name does not claim ownership.
Inspect the paths, then rerun the installer with your intended `--agents` selection to establish
the record. Later selections add paths; they do not uninstall previous ones. Known conflicts
stop installation before writes across the selected skill paths and root checker. For skill-path
conflicts, resolve the conflict or select only the non-conflicting agents. A root `check.py`
conflict applies to every selection: review and reconcile that file with the shipped source first.
User content stays untouched. This preflight does not provide rollback for filesystem errors or
concurrent edits.

When a skill's source changes, the shared digest can advance only if the selection covers all
previously recorded paths for that skill. Partial upgrades stop before writes, including with
`--force`; select agents covering those paths (or `--agents all`) and inspect content conflicts.
The installer does not automatically distinguish a safe old-version upgrade from user edits.

## What it deliberately does not install

Vendor hooks, subagent definitions, plugin bundles and a mandatory skill for every stage. Use your
preferred native, third-party or project capability when it satisfies the contract. Researching an
external skill does not make it a dependency or recommendation.

`hr-onboard` is the only shipped skill today. The [work templates](templates/work/README.md) are
optional pilots; full SDLC is the design scope, not a claim that every workflow has been validated.

## The rule everything follows

> Keep repository rules and work contracts portable. Use available tools to execute them, and
> deterministic checks to enforce what can be enforced. Add a fallback procedure only for a
> demonstrated gap; keep surface-specific adapters outside its core.

## Files

```
docs/GUIDE.md              the AI-native SDLC: 12 stages + 3 cross-cutting concerns — for you
docs/agents/claude-code.md the full Claude Code inventory: surfaces, bundled skills, subagents,
                           hooks, permission modes, artifacts, scheduling, plugins, limits
docs/agents/codex.md       the full Codex inventory: surfaces, commands, built-in skills,
                           marketplaces, AGENTS.md rules, hooks, config defaults, traps
docs/agents/antigravity.md the full documentation inventory: 2.0, CLI, SDK, IDE family,
                           Remote Control, managed API, Enterprise, extensions and conflicts
research/MATRIX.md         8 agents x 6 extension mechanisms, with check dates and a revision log
research/PORTABILITY.md    what dies on a switch, and what the portable layer must therefore carry
templates/AGENTS.md        mostly empty, with the inclusion test that keeps it that way
templates/CLAUDE.md        the required import line
templates/work/            optional handoff, spec, plan, review, findings and verification contracts
templates/skills/          hr-onboard — discovery by attempting, not by scanning
install.py                 one source of truth into every agent's path
check.py                   checks instruction integrity, skill names/frontmatter, sync and inventory drift
tests/                     installer/coexistence regressions and a worked contract pilot
```

## Evidence

Claims here carry a source and a date, or are tagged `(unverified)`. Where a claim is testable
locally it is **tested, not cited** — vendor documentation and secondary write-ups in this field
contradict each other often enough that a citation is not evidence.

Two examples, both settled by running them rather than reading about them:

- Claude Code v2.1.251 does not read `AGENTS.md`; with both files present and no import, it is
  ignored **silently**
- A skill in `.agents/skills/` is invisible to Claude Code while the same skill in `.claude/skills/`
  is found

The platform surfaces this describes change monthly. `research/MATRIX.md` carries a `recheck_by`
date, and the local tests take minutes.
