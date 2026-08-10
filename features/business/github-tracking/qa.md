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

Observed directly during the sprint that wrote this feature: immediately after moving
five cards to `Ready for dev`, the same filtered read by milestone returned 4 of 5 with
the suspect flag `false`; the fifth card appeared on a retry a few seconds later. A
sprint built from that first read would have silently dropped a ticket nobody noticed
was missing.

How `board.sh` satisfies this criterion is in `tech.md`.

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
  Status because closing an issue does not move it — see business.md's lifecycle
When the board is read
Then it is not reported as work in progress
```

A board read filters on the issue's own `state` (open/closed) before reporting live
work, not on the card's Status alone — the rule is `business.md`'s "Closed without a
PR"; the field shape this criterion checks is in `tech.md`.

### AC-9 — A deviation comment with no reason is reported, not counted

```gherkin
Given an issue carrying a `Deviation:` comment whose `Reason:` line is absent or empty
When the ticket's deviation record is read
Then the record is reported as non-compliant, and it is not counted as a deviation
  somebody explained — an entry that parses is not an entry that says why
```

### AC-10 — The record is on the issue, not in the PR that may never open

```gherkin
Given a ticket whose model a human overrode, whose run dies before opening a pull request
When someone later asks how that ticket ran against what the policy preferred
Then the answer is on the issue as a comment — the artefact that exists independently of
  the run — and not in a PR body, which for this ticket was never written
```

### AC-11 — A deviation is found by its cell without opening the tickets

```gherkin
Given several issues across the project carrying deviation comments on different cells
When the records for one cell are searched
Then they are returned by a search over comment text on the cell token, without
  enumerating the board or opening each issue, and a search term matching nothing returns
  nothing rather than the whole repository — this is what the fielded shape buys, and
  prose in a PR body is what fails it
```

## Out of scope

- Who reads the deviation records once they accumulate, and on what occasion — open.
  This feature materialises the record and makes the search possible; it appoints nobody.
- Creating the board's columns and the project itself (`scrumia-project-setup`) —
  setup-time, not the ongoing reading and moving this feature specifies.
- The code cycle's **process** — isolation per ticket, when work is committed, what
  is reviewed when, what may merge. `features/business/dev-flow/` owns those rules and
  is where they are stated in full. What stays in scope here is their
  **materialisation** on GitHub: that the reviewable proposal is a pull request,
  opened and linked to its issue this way, and that its progress shows as a column
  move. The module implements the cycle (`business.md`, per ADR-0013); it does not
  specify it.
- Composing a non-GitHub tracker with GitHub pull requests. Not a gap in this spec —
  a gap in the slot, per ADR-0013, closed only when that ADR is reopened.
- Authentication and reachability failures — `gh` not logged in, the `project` scope
  missing, the board unreachable. `board.sh doctor` names which one; that is
  operational resilience, not a tracking business rule.
