# Third-party content

houserules itself is MIT licensed — see [LICENSE](LICENSE).

Three optional, opt-in skills are adaptations of upstream work. Each ships its own upstream
`LICENSE` and a `NOTICE.md` recording the source URL, pinned revision, retrieval date and the
changes made. Those files travel with the skill: when the installer copies a skill into your
project, it copies the LICENSE and NOTICE alongside it. Keep them together.

| Skill | Upstream | License | Revision | Retrieved | Provenance |
|---|---|---|---|---|---|
| hr-tdd | Matt Pocock, `skills/engineering/tdd` | MIT | `3cca18b` | 2026-09-05 | [NOTICE](templates/skills/hr-tdd/NOTICE.md) |
| hr-diagnosing-bugs | Matt Pocock, `skills/engineering/diagnosing-bugs` | MIT | `3cca18b` | 2026-09-05 | [NOTICE](templates/skills/hr-diagnosing-bugs/NOTICE.md) |
| hr-code-review | Matt Pocock, `skills/engineering/code-review` | MIT | `3cca18b` | 2026-09-05 | [NOTICE](templates/skills/hr-code-review/NOTICE.md) |

Upstream repository: https://github.com/mattpocock/skills

`hr-tdd` retains `tests.md` and `mocking.md` from upstream without content changes; the other
adapted material is rewritten. None of this implies endorsement by the upstream author.

`hr-onboard`, `check.py`, `install.py`, `.houserules/workflow.py`, the work templates and all
documentation are original to this project and carry no third-party terms. They are still MIT,
so the installer writes the notice to `.houserules/LICENSE` in the adopting project and keeps a
copy inside the `hr-onboard` skill directory, which is also copied on its own. Neither touches
the adopting project's root LICENSE.
