---
description: Assemble a batch of ready tickets that can run in parallel without conflicting, present it, and once the human validates it, execute one isolated worktree per ticket.
argument-hint: [milestone]
---

Load the `scrumia-sprint` skill and follow it.

$ARGUMENTS

Treat any argument as the sprint's milestone — its boundary. Without one you are reading the whole ready column and calling it a sprint.

Stop once the batch is presented. Step 2 of the skill is a human decision, and running this command is not it: an agreement given to something else is not an agreement to launch.
