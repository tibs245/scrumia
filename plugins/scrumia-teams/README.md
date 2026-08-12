# scrumia-teams

The team slot: configurable standing roles — manager, business, tech, plus any role
another module contributes — and the sprint that turns a batch of ready tickets into one
isolated worktree each.

## What it answers

Who arbitrates when business and tech disagree, what model a ticket runs on before it
starts, and how many tickets a sprint can run at once without saturating human review.

## What it refuses

- No role with write access. Manager, business and tech read the board and the code; none
  of them holds `Write`/`Edit` — a role judges, it does not implement.
- No automatic "next sprint while this one runs." A sprint is one session, one team;
  running two concurrently is a tooling limit this module states rather than works around.
- No `sprint.parallel` setting. Every sprint runs one isolated worktree per ticket,
  unconditionally — a setting nothing reads is worse than no setting.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-standup` | Brings up the enabled roles to answer a question or give a state read. Launches nothing. |
| `scrumia-sprint` | Assembles a batch of ready, non-conflicting tickets, gets human validation, then launches one isolated worktree per ticket. |
| `scrumia-team-setup` | Configures which roles are active, on which models, and the execution-policy matrix. |
| `scrumia-pick-model` | Published on `PATH`. Given a ticket, reads its scope and risk labels and returns which model runs it, or that it should split. |
| `scrumia-manager` (agent) | Owns the board, ticket routing, sprint cadence; arbitrates business vs. tech and escalates what it cannot resolve. |
| `scrumia-business` (agent) | Owns business rules, vocabulary consistency, legal and compliance constraints. |
| `scrumia-tech` (agent) | Owns cross-app architecture, API contracts, technical debt, implementation review. |
| `/sprint`, `/standup` | Slash commands — each loads the matching skill above and passes its arguments through. |

## Settings it reads

Under `settings.team` in `.scrumia/config.yaml`: `roles`, `execution` (the model-policy
matrix by scope × risk, plus label prefixes and aliases), `escalation.to_human`,
`sprint.max_tickets`.

## What it expects to find

A tracker module publishing a `scrumia-board`-style name on `PATH` — this module never
hardcodes a path into one. `CLAUDE.md`'s specs contract, if a specs module is present, so
the roles read spec files rather than guessing at them.
