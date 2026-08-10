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
| Retrospective | a human call at a boundary, when at least one record was written since the last read | the period's deviation records (override or refused split), gate-2 blockers, label/diff gaps, reopened tickets | a grid cell, a spec rule, an ADR or an issue — and always a mark of how far it read | async |
| Debt audit | a human call on a named area | that area's specs, code, filed issues and reported spec/code gaps | situated issues on the tracker, left for refinement to label | async |

The refactor session is dropped, and `business.md` says why rather than leaving its
absence to be re-litigated: refactoring is work, work is a ticket, and a "session" is
execution without the acceptance criterion that makes execution refusable. That drops the
occasion, not the paired refactor skills, which resolve a finding already filed.

Two occasions the composition already ships are judged rather than left ambiguous: the
debt audit's **reading** is already enacted per slot by the five audit skills, which end
at a list in the session — the filing that makes it a ceremony is still its own step;
`scrumia-sprint`'s closing gather is **not** a ceremony, because everything it reports is
a second copy of something already recorded and the gather itself survives nothing.

## Links

- Implemented by: none, and not by a module either. `business.md` § *Where the ceremonies
  live* states the decision: no `scrumia-ceremonies`, no `ceremonies` slot. Both
  ceremonies are practices enacted through the plugged-in modules — the debt audit's
  reading partly by the five audit skills already shipped in the `practices`,
  `implementation` and `design` slots. Any future automation lands in the module that
  owns the knowledge the ceremony needs, which is how those five are placed: the `team`
  slot for the retrospective, and for the debt audit's remaining part the `specs` slot,
  whose knowledge the spec/code gap requires.
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
- #198 — BR-6 requires a queryable mark of how far a retrospective read, and no venue
  holds one yet; until it closes, that rule states an obligation nothing accepts
- #199 — the decision not to open a `ceremonies` slot has no ADR, so no stated cost and
  no reopen condition, unlike the negative slot decision in ADR-0013
- #18 — the bootstrap gate refuses a ticket whose deliverable is its own parent feature;
  this feature was created under that gap, by the exception the sprint set
