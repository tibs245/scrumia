# Business rules — agent team

Vocabulary: **role** (manager, business, tech, and designer where the `design`
slot is filled), **activation trigger** (what
brings a role into a ticket), **convening** (bringing the enabled roles up
outside a ticket so each can state what it owns, distinct from starting a
sprint), **escalation** (what always reaches the human,
independent of configuration), **arbitration** (the manager surfacing a
disagreement between the other two to the human, with its own recommendation,
without settling it itself), **verdict** (a role's explicit answer:
approved / blocked, compliant / non-compliant, or their "with reservations"
variants), **channel** (one of the four places this project writes durable
content an agent later acts on — skills, indexes, specs/ADRs/tickets, memory),
**entry** (one file of a role's memory), **index** (the file a channel is
entered through, which names what is there and nothing else).

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

## Four channels, one home each

This project writes durable content — content an agent later reads and acts on —
into four channels. Each answers a different question, and a given sentence
belongs to exactly one:

| Channel | Answers | Where it lives here |
|---|---|---|
| Skills | *when* to look, and *what* to check | `plugins/*/skills/` |
| Indexes | *where* it lives | a feature's `index.md`, `docs/adr/README.md`, `CLAUDE.md`, a role's `MEMORY.md` |
| Specs, ADRs, tickets | *what is true* | `features/`, `docs/adr/`, the tracker |
| Memory | what no document owns and no index can point to | `.claude/agent-memory/<role>/` |

**The membership test is one question: would a new human contributor need to know
this?** If yes it belongs in the repo or the tracker — a spec, an ADR or a ticket,
reachable from an index. Only what is useful solely to an agent doing its work,
and would clutter a spec, is memory: a human's working preferences, an
environment constraint, a pitfall that costs an hour to rediscover.

Two rules fall out of the split, and they hold for **every** channel:

- **An index navigates, it never rules.** A rule found in an index is misfiled by
  construction, whichever index it is.
- **A rule is stated in exactly one channel.** Another channel may point at it.
  Pointing is not restating: what must live in one place is the rule's *normative*
  half — the obligation and the trigger that fires it. A second copy of its
  *premise* or its motivation creates no second rule, because no one can be judged
  compliant against a reason. The drift test is whether two copies could ever
  command different behaviour, and a text carrying zero motivation gets skipped by
  an agent that never opens the link.

This section is the split's single statement, for all four channels. A feature
applying it to one channel — this one applies it to memory, below — **cites this
section rather than restating it**: a second statement of the membership test is
the defect the split exists to remove.

## What role memory may hold

Each role declares `memory: project` in its own frontmatter, and the harness gives
it a directory under `.claude/agent-memory/<role>/`. Those files load at the start
of every invocation of that role and steer what it believes. It is the only
channel that writes durable, behaviour-steering content through **none** of
ADR-0005's three gates, and each role reads only its own directory — so what it
may hold is governed here rather than left to whoever wrote it.

**Memory holds pointers, never rules.** An entry may name the spec, ADR or ticket
that owns a rule and say what to watch for when applying it. It may not carry the
rule. An entry a reader could act on without opening what it cites has restated a
rule, and a rule nobody voted is what this channel keeps producing when nothing
says otherwise.

Five further properties govern the channel. Each is carried in the entry's own
frontmatter, under `metadata:`, so that a check can see it rather than a reviewer
having to remember:

```yaml
---
name: scope-axis-entry-exit
description: <one line — what this entry is about>
metadata:
  type: project
  topic: scope-axis                                  # the question it speaks to
  source: agent                                      # or: human @handle 2026-08-09
  stale_when: ADR-0015 is superseded, or #191 closes
  cites: docs/adr/0015-scope-measures-reach.md       # optional
---
```

**The channel is tracked whole, or not at all.** `.claude/agent-memory/` is
versioned like any other deliverable, and *uniformly*: one role's directory cannot
be tracked while another's is not. A partially-tracked channel is worse than an
untracked one — `git status` reads clean while two machines hold different beliefs
about what the roles know, and nothing signals the gap.

**An entry says what would make it obsolete.** `stale_when` states the condition
under which it stops being true: a ticket closing, a spec rewritten, an ADR
superseded. An entry that no stated condition can invalidate never expires, and a
channel of never-expiring entries is a channel of beliefs nobody can retire.

**A human's ruling and a role's own inference are marked apart.** `source` is
`human`, with the handle and the date, for something a human decided; `agent` for
something a role concluded on its own. Only the first is settled. An agent's
inference is a working belief and the next role to look may re-open it — without
the mark, "never re-litigate this" attaches to conclusions no human ever made.

**Two roles on the same question are detectable.** `topic` names the question the
entry speaks to. Two roles carrying the same topic is not forbidden — they often
hold complementary halves of it — but it is reported, because a contradiction
between two standing instructions is otherwise invisible: neither role ever reads
the other's directory, and no gate sees both.

**The index names exactly what is there.** A role's `MEMORY.md` is this channel's
index and the role's only entry point into it. It must name every file present
beside it, and name no file that is absent. A file the index omits is not stale
and not wrong, it is *invisible*; a file the index names and that does not exist
sends the role to nothing.

These are checked, not merely stated: `tools/validate.py` walks the channel on
every run and in CI. The index-versus-tree half takes **the tree it walks as an
argument**, so the same check serves any indexed tree rather than this one alone.

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
