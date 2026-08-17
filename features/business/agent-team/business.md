# Business rules — agent team

## Value

For the humans steering the project and the agents executing its tickets — everyone who
needs to know who is asked, and who is not. It brings bounded ownership: each role's
Owns/Refuses table, its activation trigger, and the three escalations that reach the
human whatever the project's autonomy level. It matters because a manager that decides
a business rule itself, or a tech role that settles delivery priority, is exactly the
undifferentiated agent this feature exists to prevent — the roles are what keeps a
disagreement surfaced instead of averaged away. Not instrumented today: nothing counts
how often a role's stated refusal held versus was crossed; the Owns/Refuses table and
the escalation rule are checked by reading the spec and the transcripts, not by a
computed measure.

Vocabulary: **role** (manager, business, tech, and designer where the `design`
slot is filled), **activation trigger** (what
brings a role into a ticket), **convening** (bringing the enabled roles up
outside a ticket so each can state what it owns, distinct from starting a
sprint), **escalation** (what always reaches the human,
independent of configuration), **arbitration** (the manager surfacing a
disagreement between the other two to the human, with its own recommendation,
without settling it itself), **verdict** (a role's explicit answer:
approved / blocked, compliant / non-compliant, or their "with reservations"
variants — see § *The verdict vocabulary, posted by the role* below).

## Roles

Which roles exist is a property of the composition, not of one module.
`settings.team.roles` is the single list, and it stays a single shared list
rather than descending into any module's own settings: it declares the team,
which is the project's fact, not one module's configuration.

**An entry names the agent and says whether this project wants it.** Nothing
else — the agent's own file already carries its description and what it guards,
and a project that restated them would own the half that stops being updated.

```yaml
settings:
  team:
    roles:
      - { name: scrumia-manager,  enabled: true }
      - { name: scrumia-designer, enabled: true }
      - { name: acme-legal,       enabled: true }
```

The name is the **agent's** name, not a role label to be translated into one.
There is no provider field: an agent a module ships and an agent a project
writes for itself enter on the same line, and resolving the name to a runnable
agent is the harness's job rather than a convention this feature would have to
state and something would have to enforce. A role a project enables whose agent
does not resolve is a finding, reported with the restart that usually explains
it (§ *Reaching a role requires a restart after install*).

A role whose slot is empty does not exist: it would have nothing to guard but
its own taste.

Each role's scope and its explicit refusal — a role with no refusal line
would be indistinguishable from another and shouldn't exist as a separate
role.

| Role | Owns | Refuses |
|---|---|---|
| Manager | The board, splitting value into tickets, routing a ticket to the role it belongs to, sprint cadence, arbitration between business and tech | Deciding a business rule itself (routes to business); judging architecture or implementation quality itself (routes to tech); the final merge decision (belongs to the human alone) |
| Business | Business rules and domain vocabulary, consistency across business specs, legal/compliance constraints, business acceptance criteria | The architecture, the stack, delivery planning and priorities — those belong to tech and to the manager |
| Tech | Cross-cutting architecture, API contracts, technical debt, implementation quality | Business rules and delivery priorities — those belong to business and to the manager |
| Designer | Visual identity, design-system consistency, legibility and visual hierarchy, accessibility as far as it is visual | The message itself (business), the architecture (tech), delivery priorities (manager); and inventing a value the design system already answers |

Designer is present only where the `design` slot is filled — its definition
lives in that module (`plugins/scrumia-design/agents/scrumia-designer.md`),
not in `plugins/scrumia-teams/agents/`.

## Activation triggers

A role does not activate on every ticket. It activates when the ticket crosses
into what it owns.

**Manager** — always, first: it routes every ticket by giving it exactly one
`scope/*` label (`docs/adr/0015-scope-measures-reach.md`), prepares each sprint from
the ready tickets, and arbitrates whenever business and tech disagree.

**Business** — a ticket is labeled `scope/L` and changes a business rule
(`docs/adr/0015-scope-measures-reach.md`; what counts as changing one is the
blast-radius test in `features/business/execution-policy/`, not the fact that a
file under `features/business/` moved); or the manager escalates a business-rule
ambiguity, a functional edge case, or a compliance question directly, outside
of a ticket's routing.

**Tech** — a ticket is labeled `scope/M` or `scope/L` (routed to tech at both);
or the manager escalates a doubt about architecture, a dependency, debt, or
implementation quality directly.

The label conditions who is asked at entry; ADR-0015 also holds that the diff's
actual scope conditions who reviews at exit, independent of the label.

## Convening the team

Being reached precedes being activated: a role can be brought up to state what
it owns before any ticket assigns it a trigger. Convening and executing a
sprint are distinct entry points. A request to start the team brings the
enabled roles up, each reports what it owns, its read of the current state,
and what it refuses to rule on with where that goes instead, and the floor
returns to the human — it never starts a sprint, moves a card, or refines a
ticket. Launching a sprint stays a separate, later, human decision, taken
with a batch of tickets in front of them.

Convening checks that each enabled role's module is **installed**, not merely
declared. A role is in one of three states: disabled, enabled with its module
installed, or enabled with its module absent — and the last is the worst of
the three: the composition claims the reviewer exists and nothing reaches it.
Convening reports that gap, naming the install command, rather than silently
bringing up a smaller roster — a partial team convened in silence would let a
project believe it has a reviewer it does not.

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

## When a role must be consulted

A role is not a courtesy. It is asked because its domain owns the question, and a question
left to the caller is either answered on taste or carried to the human — both losses the
team exists to prevent. The skills that route to a role — refinement, execution, review —
must therefore state **the conditions under which a role is consulted** rather than
invite one "when useful". An invitation with no trigger is a role never called, and the
evidence from a single refinement pass is unambiguous: most tickets that came back
blocked were blocked on a question a role would have answered in three minutes.

### The condition, stated once

A role is consulted when any of the following holds:

- A business rule is ambiguous, missing, or contradicted by two written statements
- The change reaches beyond one feature or one app — the rule it changes is read elsewhere
- An interface contract changes, or two apps disagree on what the contract says
- The same question blocks several tickets — one consultation, referenced by all of them

That is the entire condition. It does not enumerate every case; it names the shape the
case has to take to be one. Anything narrower turns the role into an exception list;
anything broader turns it back into an invitation.

### The rule applies to every entry point

The same condition holds for refinement, for execution, and for review — not just the
skill that touches a ticket first. A refinement that consulted the right role at entry
and an execution that ran without one are both partial applications of the rule, and the
report's silence on which role was asked is what makes them indistinguishable from a
run that asked none.

A report — a refinement report, an execution's PR description, a review's verdict —
states **which roles were consulted, their answers, and where the answer is recorded**,
or states that no role was needed and names the condition that made the call. A report
that is silent on the question has not met the rule, regardless of whether the role was
asked.

### Unreachable roles

A role that cannot be reached is reported as such — the agent type does not resolve,
the module shipping it is not installed, the question lies outside every declared role —
and the report names the gap rather than substituting a general agent in silence. A
fallback that reads as the role is worse than no consultation, because the role's
absence is no longer visible to the reader of the report. *Reaching a role requires a
restart after install* (`§ Reaching a role requires a restart after install`, below)
already covers the agent-type case; the report carries the rest.

### Repeated questions

A question that blocks several tickets is asked once. The first ticket that hits the
condition convenes the role; later tickets reference the answer rather than asking the
same role the same question again. A refinement that finds the answer on the ticket
cites it instead of re-asking, and an execution that needs the answer reads it from the
ticket it is closing rather than convening the role independently. Repeated questions
asked separately are repeated costs, and the rule's point is to surface the team's
domain — not its overhead.

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

That covers reads. Writes carry no equivalent guarantee: no session may assume
its write was conditional on what it last read. The shared state is written
**last-writer-wins**, with no compare-and-swap and no lock — a session that
writes the same card as another does not get an error or a rejection back, and
whichever write lands last is the one that stands. Two sessions targeting the
same card race rather than corrupt anything, and the mitigation is the same as
for reads: decide from a fresh read at the point of decision, not from a value
held since earlier in the session. This does not introduce a claim, a lease or
a lock — none of those exist in the shared state today, and none is implied by
stating this.

## The verdict vocabulary, posted by the role

A role review produces one of three states, of which one is a failure:

- **`run`** — the review ran *as the role*, and a verdict is attached. The
  transport that reached the role is not a state in itself: a `claude -p --agent`
  subprocess is `run` when it ran as the role, and `not_run` when it did not —
  what matters is who answered, not how the answer was reached.
- **`not_required`** — the ticket's scope prescribes no review (`scope/S`).
  This is a label-derived state: the executor does not declare it. An executor
  that asserts `not_required` on a `scope/M` or `scope/L` is asserting a
  substitution the gate refuses, and the record is read as non-compliant.
- **`not_run`** — a required review did not run as its role. **Cause is
  mandatory** in the carrier: the same record that names the state names the
  reason — the role's agent type did not resolve, the role disclaimed, the
  executor fell back to a self-applied review, the review was unreachable for
  whatever reason. "Skipped" and "unreachable" are *causes* of `not_run`, not
  states: at gate 3 the human takes the same decision for any required-and-absent
  review, regardless of cause.

A self-applied review — the executor running its own diff through a general
agent handed the role's `agents/` file — is not a role review. The difference
is measured: on one sprint's five PRs, the self-applied reviews returned five
approvals and two reservations where the actual roles returned one blocker and
nine. At the role gate, a self-applied review counts as `not_run` with that
cause; the verdict the gate reads is the role's, and a verdict that came from
no role is no verdict.

**The verdict is posted by the role, not by the executor.** The role's agent
writes its own verdict on the ticket's issue, in a form a later reader can find
without having to re-run the review. The format is:

```
Verdict: Approved | Reservations | Blocked — #<n> — by scrumia-<role>
```

`Approved`, `Reservations` and `Blocked` are the three outcomes the role can
sign; the ticket number ties the verdict to its work item; the `by scrumia-*`
token names the role that produced it. Three properties no other carrier has:

- **Unfalsifiable by omission.** No role-signed comment = no review, whatever
  the executor's report says. A summary in the pull-request body that the
  executor wrote is not a verdict and is not what the gate reads.
- **Survives the executor's death.** A record that lives on the ticket's issue
  outlives the run that created it; a structured field in the agent's return
  dies with the session.
- **Machine-readable.** A read can find the verdict by filtering the issue's
  comments for the `Verdict:` prefix and the `by scrumia-*` token, in the same
  call the board read uses for the deviation record.

**Attribution is required.** A verdict that does not name the role that
produced it is treated as absent: `not_run`. The `by scrumia-<role>` token is
not a courtesy — it is what lets the gate tell a role verdict from a comment
that happens to match the format, and closes the substitution path a structured
field written by the executor's return would reopen.

**The orchestrator runs the review as a net, on the absence of the carrier.**
Where the role's verdict is not on the ticket at gate 3, the orchestrator
triggers the review on that absence — a checkable fact, not a declaration by
the executor. A PR for which the tracker holds no role-signed verdict goes
through the net. The net is the immune system to the executor's report failing
twice, and the way it triggers is the only one that does not trust the same
record that already failed.

This rule is not new in substance — it is the same falsifiability the
deviation record and the scoping signal already enforce on the same surface.
The deviation record is on the issue so the record survives the run; the
scoping signal is on the issue so the gap survives the run; the verdict is on
the issue so the review outcome survives the run. Three records, one venue,
one reason. The venue and the read are
[`features/business/github-tracking/`](../github-tracking/)'s to materialise; the
vocabulary and the rule that the role posts its own verdict are this feature's,
and `features/business/dev-flow/` cites rather than restates them.
