# Business rules — agent team

Vocabulary: **role** (manager, business, tech, and designer where the `design`
slot is filled), **activation trigger** (what
brings a role into a ticket), **escalation** (what always reaches the human,
independent of configuration), **arbitration** (the manager surfacing a
disagreement between the other two to the human, with its own recommendation,
without settling it itself), **verdict** (a role's explicit answer:
approved / blocked, compliant / non-compliant, or their "with reservations"
variants).

## Activation triggers

A role does not activate on every ticket. It activates when the ticket crosses
into what it owns.

**Manager** — always, first: it routes every ticket by giving it exactly one
`scope/*` label (`docs/adr/0006-ticket-routing.md`), prepares each sprint from
the ready tickets, and arbitrates whenever business and tech disagree.

**Business** — a ticket is labeled `scope/L` and changes a business rule
(`docs/adr/0006-ticket-routing.md`; what counts as changing one is the
blast-radius test in `features/business/execution-policy/`, not the fact that a
file under `features/business/` moved); or the manager escalates a business-rule
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

If business or tech is disabled in `.scrumia/config.yaml`'s `team.roles`, the
question that would have gone to it goes straight to the human instead: the
manager does not settle it on the grounds that no one else is available.

The manager is not symmetrical with the other two here, because this rule is
carried out by the manager. Disabling it does not silently disable escalation:
the skill that would have routed to it escalates to the human directly, and says
the manager is off. What a project cannot get is a composition where a question
reaches nobody.

## Arbitration does not average

When business and tech disagree on the same ticket or PR, the manager does not
produce a compromise position and does not pick a side on their behalf. It
relays both positions as given, adds its own recommendation, and escalates to
the human. Averaging two verdicts ("half-approved") would hide the disagreement
instead of surfacing it — the opposite of why roles report to the manager
rather than negotiating with each other directly (`docs/adr/0002-standing-roles.md`).

## Models live in the agent, not in configuration

Each role's model is declared in its own agent's frontmatter — the three this
module ships (`plugins/scrumia-teams/agents/scrumia-manager.md`,
`scrumia-business.md`, `scrumia-tech.md`) and any a plugged-in module registers
beside them, such as `designer`
(`plugins/scrumia-design/agents/scrumia-designer.md`,
`docs/adr/0014-roles-ship-with-their-capability.md`). All of them on `opus`,
which is the ceiling this project assigns without being asked. A stronger model
exists above it (`fable`, twice the per-token price) and no default reaches for
it: moving a role there is an explicit human decision, taken case by case. What
a *ticket* may reach is not this feature's rule — see `execution-policy`.
`.scrumia/config.yaml`'s `team.roles` carries
only `enabled` per role. A `roles[].model` key existed there previously; it
governed nothing and was removed. This spec does not reintroduce it: a second
place claiming to hold the model would drift from the frontmatter that actually
runs it.

Which model executes a given *ticket* (as opposed to which model a *role*
runs as) is a separate policy, keyed on the ticket's scope and risk labels —
specified by `features/business/execution-policy/`, not here.

## Reaching a role requires a restart after install

The same definition serves three ways — delegated subagent, session main agent,
teammate in an agent team — and `docs/adr/0002-standing-roles.md` treats them as
interchangeable. They are, with one operational condition that is not optional:
**a module that ships agents is not usable until Claude Code restarts.** A hot
reload refreshes skills and leaves the registry of spawnable agent types stale.

This is specified rather than left to the tooling because of how it fails. The
roles are not degraded, they are unaddressable, and a caller that cannot reach
its reviewer falls back to a general agent whose verdict reads exactly like the
role's. One sprint measured the difference on the same five diffs: the
self-applied reviews returned five approvals and two reservations, the actual
roles one blocker and nine.

So a review that could not run as its role reports that it did not. A fallback
that reads as the real thing is worse than no review, because nobody
compensates for a gate they believe ran.

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
