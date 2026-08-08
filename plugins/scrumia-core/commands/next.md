---
description: Read the composition and the tracker, then say which step of the workflow comes next and why. Recommends; launches nothing.
---

Answer where this project stands and what to do next. You recommend — you do not execute.

## Read, in this order

1. `.scrumia/config.yaml` and the ScrumIA section of `CLAUDE.md`: which module fills which slot, and which slots are empty.
2. The board, through the module in the `tracker` slot. With `scrumia-github-project` that is `scripts/board.sh read`, never a composed `gh project` call — an unfiltered read is silently truncated at 30 items. Another module fills the slot differently: ask it in its own terms rather than assuming this one's layout.

There is no state file in the repo to read, and there must not be: duplicated state diverges within a week and then keeps being believed.

## Then say three things

**Where the project stands** — what sits in each column, and which one is the constraint. An empty ready column against a full backlog means refinement is the bottleneck, not execution, and recommending a sprint there would be recommending nothing.

**The step you recommend, and why** — one step, not a menu:

| What the board shows | The step |
|---|---|
| Nothing ready, backlog full | `refine` — take tickets to ready |
| Tickets ready, no file conflict between them | `sprint` — run the batch |
| A PR open | `review` |
| A rule missing, a ticket ambiguous, a disagreement | `standup` — put it to the roles |
| Behaviour undecided before any code | `feature` — specify it first |

**What blocks it, if anything does.** A slot with no module is a capability this project does not have: name the module that fills it and say the step is unavailable, rather than improvising it. An empty slot is a declared absence, not an oversight.

Report any drift you notice between what the composition declares and what is actually installed — a role enabled whose module is absent is the case that silently costs a review.

Then stop. Taking the step is the human's decision.
