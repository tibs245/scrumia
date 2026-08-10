# Execution policy

**Status**: active
**Stratum**: business

## In brief

Which model executes a ticket, decided from two labels the manager already sets at
refinement: `scope/*` — how far the change reaches — and `risk/*` — what it costs if
it is wrong. The two are independent questions, and their crossing is a grid the
project declares once and a tool reads for everyone.

This is the answer to the founding note's open question, *"who decides big-context
versus small-context?"*: a label set at refinement on verifiable questions, not a
judgement improvised when execution starts.

## Links

- Implemented by: no App feature. The policy is enacted by
  `plugins/scrumia-teams/scripts/pick-model.sh`, shipped by whichever module fills the
  `team` slot, and consumed by `scrumia-sprint` and by `scrumia-ticket`'s Step 0.
- The grid's cells and the capability order they climb are **project data**, declared
  in `.scrumia/config.yaml` under `settings.team.execution`. This spec states the
  invariant they must satisfy; it does not restate them.
- Related ADRs: `docs/adr/0015-scope-measures-reach.md` — why the scope axis is measured
  rather than estimated, the three questions it is measured by, and why the second one
  reads a rule's reach rather than a file's location. It supersedes
  `docs/adr/0006-ticket-routing.md`.
- Consumed beyond this feature: the blast-radius test in `business.md` § *The scope axis
  measures reach, not medium* is read by `features/business/agent-team/` for entry
  routing, and applied by the plugin prose and the `scope/*` label descriptions that a
  labeller works from. Changing it is a change other features and a tracker artefact
  feel — which is what makes such a change `scope/L` under the test itself.

## Files present

| File | Why it exists |
|---|---|
| `business.md` | the two axes, what the scope axis measures, the grid's invariant, the oversized fallback, the visible assumptions, vocabulary mapping, and what a deviation records — one venue for both kinds, fielded, and who reads it |
| `qa.md` | those rules as scenarios that can fail |
| `CHANGELOG.md` | history of changes to this feature |

No `legal.md`: the policy routes work between models — no personal data, payment,
user content or regulated sector. No `archi.md`: it touches neither `site` nor
`tools`, so there is no cross-app dialogue to describe. No `tech.md` or
`api-contract.md`: the mechanics of the script that enacts the policy are
deliberately out of this spec, and stating them here would be the second statement
`business.md` forbids.

## Open issues

- #4 — [EPIC] Spec the agent team: roles, triggers, routing, refusal lines (parent)
- #167 — the record has no reader: who counts repetition on a cell, and when. This
  feature requires the count to be possible and stops there, on purpose
- #47 — the residual implementation work: `pick-model.sh` detecting a grid that
  breaks the climbing invariant, and the templates that seed a grid carrying the
  order beside it
- #18 — the bootstrap gate refuses a ticket whose deliverable is its own parent
  feature; this feature was created under that gap, by the exception #12 set
