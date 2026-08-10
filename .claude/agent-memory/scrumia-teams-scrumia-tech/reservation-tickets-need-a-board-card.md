---
name: reservation-tickets-need-a-board-card
description: An issue filed to carry a review reservation is not on the board unless someone adds the card — gh issue create alone leaves it invisible to board.sh read and ready
metadata:
  type: feedback
---

When a review reservation is converted into a ticket, check the card, not just the issue:
`plugins/scrumia-github-project/scripts/board.sh find <n>` must report `found: true`.
Issues created with `gh issue create` land with the `scrumia` label and **no project card**.

**Why:** the whole point of "a reservation without a ticket is a forgotten reservation" is
that the next sprint prep sees it. `board.sh read` and `board.sh ready` only see cards, so
a cardless issue is exactly as forgotten as no issue at all — and `board.sh move` then
fails on it too. Observed on #198/#199 (filed for a ceremonies review) and on #191; #167
and #11 do have cards, so this is a lapse rather than a house convention.

**How to apply:** when accepting a deferral, verify the card exists before calling the
reservation handled; if it does not, ask for `gh project item-add` and say which issues.
Related: [[negative-slot-decisions-are-adrs]].
