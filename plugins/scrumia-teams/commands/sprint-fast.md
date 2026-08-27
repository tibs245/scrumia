---
description: Assemble a batch of ready tickets that can run in parallel without conflicting, present it, and once the human validates it, execute one isolated worktree per ticket — each ticket merges on gate 1 alone, one global review at the end, fixups autosquashed under the orchestrator.
argument-hint: [milestone]
---

Load the `scrumia-sprint-fast` skill and follow it.

$ARGUMENTS

Treat any argument as the sprint's milestone — its boundary. Without one you are reading the whole ready column and calling it a sprint.

Stop once the batch is presented. Step 3 of the skill is a human decision, and running this command is not it: an agreement given to something else is not an agreement to launch. Gate 3 is human too — once the global review has run and the sprint PR is open, the merge is the human's, not this command's.
