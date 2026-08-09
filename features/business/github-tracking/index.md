# GitHub tracking

**Status**: active
**Stratum**: business

## In brief

How ScrumIA tracks work when the `tracker` slot is filled by `scrumia-github-project`:
the ticket's lifecycle across the board's six columns, what a milestone and an epic
mean, which label is read by which consumer, and the reading discipline that keeps a
partial board read from being reported as a complete one. Per ADR-0013, the module
filling this slot also implements the code cycle (branches, worktrees, PRs) — a scope
wider than its name suggests — but the cycle's process is specified by
`features/business/dev-flow/`. This feature traces that process onto GitHub: it says
which artefact each step becomes here, and redefines none of them.

## Ticket lifecycle

A ticket crosses six columns, in order:

| Column | Meaning |
|---|---|
| `Backlog` | Raw intent, not yet refined |
| `Ready for dev` | Refined: criteria written, scope and risk set |
| `To dev` | Selected into the current sprint |
| `In progress` | Being executed |
| `In review` | PR open, awaiting review |
| `Done` | Merged |

A card just added to the board — `gh issue create --project` or `gh project item-add`
— carries **no Status at all**, not `Backlog`: it sits in none of the six until someone
places it. `board.sh read` reports that as its own `(no status)` group rather than
folding it into `Backlog`, because a card nobody placed is worth seeing, not papering
over.

Skills never move a card by naming a column directly, except for that first placement.
They name a **flow step**, and `settings.tracker.board.flow` in `.scrumia/config.yaml`
maps each step to this board's actual column name. That indirection is what lets
ScrumIA adopt a board that already exists — columns renamed, vocabulary already in use
— without renaming anything or touching a skill.

| Transition | Trigger | Flow step |
|---|---|---|
| (no status) → `Backlog` | a ticket is filed | none — the column name is used directly, once |
| `Backlog` → `Ready for dev` | `scrumia-refine` judges its four readiness conditions met | `ready` |
| `Ready for dev` → `To dev` | a ticket is selected into a sprint's batch | none named today — see #23 |
| `To dev` → `In progress` | execution starts on the ticket | `in_progress` |
| `In progress` → `In review` | the PR opens | `in_review` |
| `In review` → `Done` | the PR merges | `done` — not automated today either, see #23 |

Only four flow steps exist in the config (`ready`, `in_progress`, `in_review`,
`done`). `Backlog` is entered by its literal column name, once, at filing. `To dev`
and the post-merge move to `Done` currently have no skill that performs them —
selecting a ticket into a sprint or merging its PR does not by itself move its card.

### Closed without a PR

A ticket can also leave the flow sideways instead of reaching `Done`: closed as
won't-fix from `Backlog`, or abandoned in `Ready for dev` or `In progress` with no PR
ever opened. No transition performs this — closing an issue does not move its card.
The card **keeps whatever Status it last had**; this is post-close residue, not a
seventh column, and not `Done` either — `Done` keeps its single meaning, "merged",
and routing a won't-fix ticket there would make the column answer two different
questions.

A reader trusts the issue's own `state` (open/closed), not the card's Status, to know
whether it still represents live work — the same rule this feature's `business.md`
already applies to an epic's progress, read from its children's `state` rather than
from where their cards sit. `qa.md` specifies the board-reading scenario this implies.

## Links

- Implemented by: `plugins/scrumia-github-project/` (the `tracker` slot). Not an App
  feature under `features/app/`: the plugin is the product ScrumIA ships, not one of
  this project's own `site`/`tools` apps — see `.scrumia/config.yaml`'s `apps` table.
- Traces: `features/business/dev-flow/` — that feature specifies the code-cycle
  process; this one binds it to GitHub's artefacts. How the two planes divide, and
  which governs, is in `business.md` § *Scope of this slot*.

## Files present

| File | Why it exists |
|---|---|
| `business.md` | milestone/epic vocabulary, label consumers, where a deviation from the execution policy is recorded, the slot's scope per ADR-0013 |
| `qa.md` | the board-reading discipline as falsifiable scenarios |
| `CHANGELOG.md` | history of this feature's changes, one entry per notable change |

## Open issues

- #5 — parent epic, stays open until its other children merge
- #18 — the bootstrap gate refuses a ticket whose deliverable is its own parent
  feature; this ticket was executed by exception, tracked there
- #23 — the `To dev` / `Done` transitions named in the lifecycle above have no
  automated move yet, found while writing this feature
- #26 — the suspect-filter rule in `qa.md` (AC-3) doesn't catch a short, stale read
  right after a write; specified as a known gap in AC-4, not fixed
