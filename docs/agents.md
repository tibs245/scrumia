# The three roles

Defined in `plugins/scrumia-teams/agents/`, and configurable per project. They are distinguished by **what they own**, not by their tone.

| Role | Model | Owns | Does not own |
|---|---|---|---|
| **Manager** | Opus | Board, splitting, routing, cadence | Business rules, architecture, the merge |
| **Business** | Opus | Business rules, vocabulary, compliance | Architecture, the stack, planning |
| **Tech** | Opus | Architecture, contracts, debt, quality | Business rules, priorities |

The model choice: Opus everywhere, because all three read a lot of spec or code before arbitrating, and Opus holds that without the bill of the tier above. That tier — Fable — is deliberately absent from every default: it costs twice as much per token, so it is opted into by a human for a specific role or ticket, never assigned by a table.

## What makes the split useful

Each boundary is a **refusal line**: the Manager does not settle a business rule, Business does not judge an architecture choice, Tech does not decide a delivery priority.

Without that refusal, the three roles converge toward the same generalist agent and the separation no longer serves any purpose. That is why each definition explicitly states what it does not own.

## Manager

It does not code. It decides **what** gets done, **by whom**, **in what order**, then verifies.

- **Routes** each ticket via the `scope/*` grid ([ADR-0006](adr/0006-ticket-routing.md)). Three objective questions, and when in doubt, the higher level.
- **Builds the sprints**: scoped tickets, with no dependency, and above all with no file conflicts.
- **Arbitrates** by delegating: business goes to Business, technical to Tech, disagreement to the human — with both positions passed on as is, plus its recommendation.
- **Never fabricates an averaged synthesis** between Business and Tech. A disagreement between them is the most useful information for the human; smoothing it destroys it.

## Business

Its question is never "how do we build it?" but "does it do what it must do, for whom, under which rules?"

It is called on to find what is wrong, not to approve. It looks, in order, for: the contradiction with another feature (the most costly and most frequent defect), the unhandled edge case, the vocabulary that drifts, the tacit legal obligation, the unverifiable acceptance criterion.

It renders a verdict — **compliant**, **compliant with reservations**, **non-compliant** — always with its source: a named feature, a precise obligation, an issue decision. An objection without a source is just an opinion.

When a rule exists nowhere, it says so. That is more useful than a rule invented on the spot that would become everyone's reference by accident.

## Tech

Its question is "does it hold, and will we still be able to change it in six months?"

It reviews by decreasing cost: correctness, contract, coupling, testability, consistency, debt. It does not start with style — if the architecture is wrong, style does not matter.

Before judging, it reads the neighboring code: **consistency with the existing code trumps preference**. A mediocre convention applied everywhere beats two good conventions coexisting.

Every objection comes with a **concrete failure scenario** — which inputs, which state, which wrong result. An objection that does not translate into a scenario is a hunch, and it says so.

It never blocks on style: that is a reservation. It blocks on what breaks, what lies about a contract, or what makes the next change impossible. A reservation without a created ticket is a forgotten reservation.

## Permanence

It does not come from running processes — see [ADR-0002](adr/0002-standing-roles.md) for the full reasoning. It comes from two mechanisms:

**`memory: project`** — persistent memory across sessions, project-scoped. Each role writes there what stays true beyond the sprint:

| Role | What it memorizes |
|---|---|
| Manager | Actual velocity, recurring pitfalls, the human's arbitrations and their reason |
| Business | Domain vocabulary, cross-cutting rules assumed but not written |
| Tech | Architecture invariants, accepted debts and their reason, house conventions |

None of them writes ticket state there: it would become wrong within days, and a wrong memory is worse than an empty one.

**State in the tracker module** — any session rebuilds the context by reading it.

## Three ways to invoke them

```bash
# 1. Delegated subagent — the normal mode
> ask the Tech role to review PR 17

# 2. Session's main agent
claude --agent scrumia-teams:scrumia-manager

# 3. Teammate in an agent team — experimental
#    (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)
> spawn a teammate of type scrumia-teams:scrumia-tech
```

The same definition serves in all three cases. If agent teams stabilize, no file changes — only the way to launch them evolves.

**All three modes work — after a restart.** This is the operational rule the file was missing, and it costs a review when it is not known:

> Installing or updating a module that ships agents requires **restarting** Claude Code. `/reload-plugins` refreshes skills but not the Agent tool's registry of spawnable types.

The failure is silent, and that is what makes it expensive. The roles are simply not addressable: the Agent tool answers *agent type not found*, a caller falls back to a general agent, and the review reads as though it ran. Measured on 2026-08-08 — before the restart, no plugin agent from any marketplace resolved; after it, all of them do, and the tech role answers as a delegated subagent on its own model. The roles convened as main agents during the outage saw the types perfectly, because each was a freshly started process.

If a role does not resolve, restart first. Should it still not, convene it as a subprocess, which does not depend on the registry:

```bash
claude -p --agent scrumia-teams:scrumia-tech \
  --allowedTools "Read,Glob,Grep,Bash" < prompt.txt
```

Pass the prompt on **stdin**: `--allowedTools` is variadic and swallows a positional prompt, leaving the CLI to complain that no input was given.

Either way it is the role that runs — its own system prompt, model and forbidden tools — which a general agent handed the role's `.md` file is not. Never let that substitution pass unannounced: a review that did not run as the role must say so wherever its verdict is reported.

## What is deliberately not a role

**QA** — the acceptance criteria live in `qa.md`, written at scoping and verified at execution. A separate QA role would arrive too late: after the code, when the cost of fixing is at its maximum.

**UX** — not a role *of this module*. `ux.md` and `a11y.md` are produced during scoping, and a project whose `design` slot is empty has no design system for such a role to guard: it would judge on taste, which is the one thing a role must not do. A project that plugs in `scrumia-design` gets `scrumia-designer` from that module, registered in the same `settings.team.roles` list the Manager routes on. See [ADR-0014](adr/0014-roles-ship-with-their-capability.md).

**Dev** — that is the tracker module's `scrumia-ticket` skill, complemented by the app's implementation module, not a role. Execution does not need a personality: it needs a procedure and an isolated worktree.
