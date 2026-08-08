# The three roles

Defined in `plugins/scrumia-teams/agents/`, and configurable per project. They are distinguished by **what they own**, not by their tone.

| Role | Model | Owns | Does not own |
|---|---|---|---|
| **Manager** | Opus | Board, splitting, routing, cadence | Business rules, architecture, the merge |
| **Business** | Fable | Business rules, vocabulary, compliance | Architecture, the stack, planning |
| **Tech** | Fable | Architecture, contracts, debt, quality | Business rules, priorities |

The model choice: Opus for the Manager, who arbitrates and orchestrates constantly; Fable for Business and Tech, whose work is to ingest a lot of spec or code before giving an opinion.

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
# 1. Delegated subagent — does NOT resolve from a standard session, see below
> ask the Tech role to review PR 17

# 2. Session's main agent — the verified way
claude --agent scrumia-teams:scrumia-manager

# 3. Teammate in an agent team — experimental
#    (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)
> spawn a teammate of type scrumia-teams:scrumia-tech
```

The same definition serves in all three cases. If agent teams stabilize, no file changes — only the way to launch them evolves.

**Only mode 2 is verified.** Measured on 2026-08-08: from a standard session, the Agent tool resolves neither `scrumia-teams:scrumia-manager` nor `scrumia-manager` — it answers *agent type not found*, and no plugin agent appears in its list at all. The roles convened through mode 2 report the opposite from inside their own session: there, the plugin agent types do show up. So resolution depends on the spawn context, and mode 1 — the one this file used to call "the normal mode" — cannot be relied on. Which of the two contexts is wrong is still open: it is [#33](https://github.com/tibs245/scrumia/issues/33)'s AC-1.

Until it closes, convene a role as a subprocess:

```bash
claude -p --agent scrumia-teams:scrumia-tech \
  --allowedTools "Read,Glob,Grep,Bash" < prompt.txt
```

Pass the prompt on **stdin**: `--allowedTools` is variadic and swallows a positional prompt, leaving the CLI to complain that no input was given.

This runs the role itself — its own system prompt, model and forbidden tools — which a general agent handed the role's `.md` file does not. Never let that substitution pass unannounced: a review that did not run as the role must say so wherever its verdict is reported.

## What is deliberately not a role

**QA** — the acceptance criteria live in `qa.md`, written at scoping and verified at execution. A separate QA role would arrive too late: after the code, when the cost of fixing is at its maximum.

**UX** — not a role *of this module*. `ux.md` and `a11y.md` are produced during scoping, and a project whose `design` slot is empty has no design system for such a role to guard: it would judge on taste, which is the one thing a role must not do. A project that plugs in `scrumia-design` gets `scrumia-designer` from that module, registered in the same `settings.team.roles` list the Manager routes on. See [ADR-0014](adr/0014-roles-ship-with-their-capability.md).

**Dev** — that is the tracker module's `scrumia-ticket` skill, complemented by the app's implementation module, not a role. Execution does not need a personality: it needs a procedure and an isolated worktree.
