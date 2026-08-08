# Acceptance criteria — github-tracking

One scenario per case. Each scenario must be able to fail.

## Nominal

### AC-1 — A newly filed card carries no status

```gherkin
Given a ticket created with `gh issue create --project` or `gh project item-add`
When its card is read before anyone sets a status
Then it is reported in its own "(no status)" group, not folded into "Backlog"
```

### AC-2 — A milestone scopes "ready" to one sprint

```gherkin
Given a project with tickets ready for dev across several milestones
When the ready tickets are read for one named milestone
Then only the tickets carrying that milestone are returned
```

## Edge cases

### AC-3 — A zero-item filtered read while the board is not empty is flagged suspect

```gherkin
Given a board with at least one item, and a filter that matches none of them —
  an unknown column, a misspelled milestone, or a typo all produce this
When a filtered read of the board returns zero items
Then the response is flagged suspect, and "nothing to do" is never reported from
  it without checking that flag first
```

### AC-4 — A short, non-empty read right after a write must not be trusted as complete

```gherkin
Given several cards were just moved to the same column
When the same filtered read runs again immediately, before GitHub's project search
  index has caught up, and returns fewer items than the true count
Then the read must be distinguishable from one taken at rest — not reported with
  the same confidence as a complete, current read
```

**Not yet enforced — currently fails.** The suspect-filter rule (AC-3) only triggers
on a *zero*-item result; a short but non-empty one passes through unflagged, and this
criterion is unmet by `board.sh` today. Observed directly during this sprint:
immediately after moving five cards to `Ready for dev`, the same filtered read by
milestone returned 4 of 5 with the suspect flag `false`; the fifth card appeared on a
retry a few seconds later. A sprint built from that first read would have silently
dropped a ticket nobody noticed was missing. Tracked in #26 — not fixed here, this
feature only specifies the requirement.

### AC-5 — An unfiltered read past the page size is reported as partial, not as the board

```gherkin
Given a board whose matching item count exceeds the read's page size
When the board is read without narrowing the query
Then the response states that it is truncated, together with the count actually
  returned, and no consumer reports it as the whole board
```

### AC-6 — A card is found by addressing the issue, not by enumerating the board

```gherkin
Given an issue that has a card on the board, regardless of the board's total size
When that card is looked up
Then it resolves through the issue's own link to its project item, not through a
  paginated scan of the board — board size stays irrelevant to finding one card
```

### AC-7 — The same issue on two boards resolves to the right one

```gherkin
Given an issue that is a card on two different project boards
When its card is looked up for one configured project
Then only the card belonging to that project resolves — not the first card found,
  and not the other board's card
```

### AC-8 — A ticket closed without a PR is not reported as work in progress

```gherkin
Given a ticket closed as won't-fix from `Ready for dev`, its card still carrying that
  Status because closing an issue does not move it — see index.md's lifecycle
When the board is read
Then it is not reported as work in progress
```

The rule that makes this pass: a board read filters on the issue's own `state`
(open/closed) before reporting live work, not on the card's Status alone — the same
field this feature already trusts for an epic's progress (`business.md`).

**Not yet enforced — currently fails.** `board.sh read`'s items carry the card's Status
and labels, but never the issue's own `state`; a closed ticket sitting in `Ready for
dev` or `In progress` reads identically to an open one, and nothing in the response
lets a consumer tell them apart. Tracked in #79 — not fixed here, this feature only
specifies the requirement.

## Out of scope

- Creating the board's columns and the project itself (`scrumia-project-setup`) —
  setup-time, not the ongoing reading and moving this feature specifies.
- The code-cycle half of the `tracker` slot — branches, worktrees, PR review routing,
  merge policy. This feature names that the slot owns it (`business.md`, per
  ADR-0013); the cycle itself belongs to the dev-flow spec.
- Composing a non-GitHub tracker with GitHub pull requests. Not a gap in this spec —
  a gap in the slot, per ADR-0013, closed only when that ADR is reopened.
- Authentication and reachability failures — `gh` not logged in, the `project` scope
  missing, the board unreachable. `board.sh doctor` names which one; that is
  operational resilience, not a tracking business rule.
