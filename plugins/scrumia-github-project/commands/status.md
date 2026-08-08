---
description: Take stock of the project — board state, features and their health, gaps between specs and code, and what deserves a human's attention.
argument-hint: [query or milestone]
---

Load the `scrumia-status` skill and follow it.

$ARGUMENTS

Treat any argument as the scope to report on — a milestone, or a board query. With none, report the whole project.

Read the board through `scripts/board.sh`, never a composed `gh project` call: an unfiltered read is silently truncated at 30 items, and a truncated board reads exactly like a short one.

Report state; change none of it. Moving a card is the job of the step that earns the move.
