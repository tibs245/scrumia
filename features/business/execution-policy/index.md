# Execution policy

**Status**: active

## In brief

Which model executes a ticket, decided from two labels the manager already sets at
refinement: `scope/*` — how far the change reaches — and `risk/*` — what it costs if
it is wrong. The two are independent questions, and their crossing is a grid the
project declares once and a tool reads for everyone.

## Links

- Implemented by: no App feature. The policy is enacted by
  `plugins/scrumia-teams/scripts/pick-model.sh`, shipped by whichever module fills the
  `team` slot, and consumed by `scrumia-sprint` and by `scrumia-ticket`'s Step 0.
- The grid's cells and the capability order they climb are project data — see
  `business.md` § *The grid is project data; what it must satisfy is not*.
- Related ADRs: `docs/adr/0015-scope-measures-reach.md` — why the scope axis is measured
  rather than estimated, the three questions it is measured by, and why the second one
  reads a rule's reach rather than a file's location. It supersedes
  `docs/adr/0006-ticket-routing.md`.
- Consumed beyond this feature: the blast-radius test in `business.md` § *The scope axis
  measures reach, not medium* is read by `features/business/agent-team/` for entry
  routing, and applied by the plugin prose and the `scope/*` label descriptions that a
  labeller works from.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding or checking a model routing: the two axes, what the scope axis measures, the grid's invariant, the oversized fallback, the visible assumptions, the vocabulary mapping, or what a deviation records |
| `qa.md` | writing or checking a test against one of these rules |
| `CHANGELOG.md` | tracing when a rule in this policy last changed |

No `legal.md`: the policy routes work between models — no personal data, payment,
user content or regulated sector. No `archi.md`: it touches neither `site` nor
`tools`, so there is no cross-app dialogue to describe. No `tech.md` or
`api-contract.md`: the mechanics of the script that enacts the policy are
deliberately out of this spec, and stating them here would be the second statement
`business.md` forbids. No `security.md`: the policy carries no risk surface rated on
any of the four axes — a wrong routing costs a rerun, not an unrecoverable loss.

