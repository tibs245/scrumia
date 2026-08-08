# Business rules — agent team

Vocabulary: **role** (manager, business, tech), **activation trigger** (what
brings a role into a ticket), **escalation** (what always reaches the human,
independent of configuration), **arbitration** (the manager resolving a
disagreement between the other two), **verdict** (a role's explicit answer:
approved / blocked, compliant / non-compliant, or their "with reservations"
variants).

## Activation triggers

A role does not activate on every ticket. It activates when the ticket crosses
into what it owns.

**Manager** — always, first: it routes every ticket by giving it exactly one
`scope/*` label (`docs/adr/0006-ticket-routing.md`), prepares each sprint from
the ready tickets, and arbitrates whenever business and tech disagree.

**Business** — a ticket is labeled `scope/L` and touches `features/business/**`
(`docs/adr/0006-ticket-routing.md`); or the manager escalates a business-rule
ambiguity, a functional edge case, or a compliance question directly, outside
of a ticket's routing.

**Tech** — a ticket is labeled `scope/M` or `scope/L` (review is required at
both); or the manager escalates a doubt about architecture, a dependency, debt,
or implementation quality directly.

The label conditions who is asked at entry; ADR-0006 also holds that the diff's
actual scope conditions who reviews at exit, independent of the label.

## Escalation to the human

Three things escalate to the human, and this holds **regardless of the
project's `autonomy.level`** (`.scrumia/config.yaml`: `guided`, `assisted` or
`autonomous`) — autonomy level changes how much of the routine work runs
unattended, never whether these three reach the human:

- A disagreement between roles (see the arbitration rule below).
- A missing business rule — a case nothing written settles.
- A contract change consumed by another app.

If a role is disabled in `.scrumia/config.yaml`'s `team.roles`, the question
that would have gone to it goes straight to the human instead: the manager does
not settle it on the grounds that no one else is available.

## Arbitration does not average

When business and tech disagree on the same ticket or PR, the manager does not
produce a compromise position and does not pick a side on their behalf. It
relays both positions as given, adds its own recommendation, and escalates to
the human. Averaging two verdicts ("half-approved") would hide the disagreement
instead of surfacing it — the opposite of why roles report to the manager
rather than negotiating with each other directly (`docs/adr/0002-standing-roles.md`).

## Models live in the agent, not in configuration

Each role's model is declared in its own agent's frontmatter
(`plugins/scrumia-teams/agents/scrumia-manager.md`,
`scrumia-business.md`, `scrumia-tech.md`) — currently manager on `opus`,
business and tech on `fable`. `.scrumia/config.yaml`'s `team.roles` carries
only `enabled` per role. A `roles[].model` key existed there previously; it
governed nothing and was removed. This spec does not reintroduce it: a second
place claiming to hold the model would drift from the frontmatter that actually
runs it.

Which model executes a given *ticket* (as opposed to which model a *role*
runs as) is a separate policy, keyed on the ticket's scope and risk labels —
specified in #13, not here.

## The sprint loop's real constraint

The target was a team preparing sprint N+1 while sprint N's tickets execute.
`docs/adr/0002-standing-roles.md` records why that does not hold within a
single session: a subagent cannot spawn subagents, so the Manager-as-subagent
that would need to launch sprint N's parallel executions cannot also be, at the
same time, the one scoping N+1.

What holds instead: **two Claude Code sessions against the same repository**,
not one — one session executes the current sprint, another prepares the next.
They do not coordinate directly; they stay consistent because the board is the
shared state (`docs/adr/0002-standing-roles.md`), read fresh by each session
rather than held in memory by either.
