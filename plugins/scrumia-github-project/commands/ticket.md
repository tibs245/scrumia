---
description: Execute one ticket end to end — isolated worktree, spec updates before code, implementation, tests per acceptance criterion, review, PR. Merges nothing.
argument-hint: <issue number>
---

Load the `scrumia-ticket` skill and follow it.

$ARGUMENTS

The argument is the ticket to execute. Ask which one if none was given.

Before starting, ask the execution policy which model this ticket runs on — `scrumia-teams/scripts/pick-model.sh <n>` — and act on its `instruction` rather than re-reading the matrix yourself. A second reading of the policy drifts from the first.

Stop at the open PR. The merge is the human's, except for what `autonomy.auto_merge` explicitly allows.
