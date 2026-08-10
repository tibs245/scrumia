# Ceremonies

**Status**: active
**Stratum**: business

## In brief

Which occasions beside the ticket path are kept, and on what terms. A ceremony is
admitted only if it passes three tests: a trigger that is not a calendar, an input that
is already recorded, and an artefact of its own that outlives it. Two pass —
the **retrospective** and the **debt audit**, both asynchronous. One is dropped: the
**refactor session**, whose only output is the pull request a ticket already produces.
None of them becomes a module: they read and write what existing slots already own.

## The admitted ceremonies

| Ceremony | Fires on | Reads | Leaves behind | Mode |
|---|---|---|---|---|
| Retrospective | a human call at a boundary, when at least one fact was recorded since the last read | the period's deviation records, gate-2 blockers, label/diff gaps, reopened tickets, refused splits | a grid cell, a spec rule, an ADR or an issue — and always a mark of how far it read | async |
| Debt audit | a human call on a named area, or the same area accumulating out-of-scope findings across tickets | that area's specs, code, filed issues and reported spec/code gaps | issues on the tracker, scope- and risk-labelled | async |

The refactor session is dropped, and `business.md` says why rather than leaving its
absence to be re-litigated: refactoring is work, work is a ticket, and a "session" is
execution without the acceptance criterion that makes execution refusable.

## Links

- Implemented by: none, and not by a module either. `business.md` § *Where the ceremonies
  live* states the decision: no `scrumia-ceremonies`, no `ceremonies` slot. Both
  ceremonies are practices enacted through the plugged-in modules, and any future
  automation lands as one more skill in the module that already owns the ceremony's
  output — the `team` slot for the retrospective, the `tracker` slot for the debt audit.
- Parent path: `features/business/dev-flow/` owns the two paths and the three gates, and
  defers the ceremonies here. A gate is not a ceremony; the two are kept apart on
  purpose.
- Reads, without owning: `features/business/execution-policy/`'s deviation record. The
  retrospective is named as a venue where it is read; who is accountable for reading it,
  and at what threshold, stays open in #167.
- Related ADR: [`docs/adr/0005-validation-gates.md`](../../../docs/adr/0005-validation-gates.md)
  — the gates this feature is careful not to be confused with.

## Files present

| File | Why it exists |
|---|---|
| `business.md` | the three admission tests, each ceremony through them, and why no module or slot is created |
| `qa.md` | those rules as scenarios that can fail, including the two candidates' refusals |
| `CHANGELOG.md` | history of changes to this feature |

No `legal.md`: a ceremony reads the project's own records — no personal data, payment,
user content or regulated sector. No `archi.md`: this feature's enactment touches neither
`site` nor `tools`. No `tech.md`, `api-contract.md`, `ux.md`, `a11y.md` or `devx.md`: it
specifies occasions and their artefacts, with no interface, no exposed library and no
implementation of its own.

## Open issues

- #3 — [EPIC] Spec the dev flow: brainstorming vs execution, gates, ceremonies (parent)
- #167 — who counts deviations on a cell, at what threshold, and whether anything
  surfaces the record unprompted. This feature names the retrospective as a venue where
  the record is read and settles none of those three
- #18 — the bootstrap gate refuses a ticket whose deliverable is its own parent feature;
  this feature was created under that gap, by the exception the sprint set
