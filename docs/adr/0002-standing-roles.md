# ADR-0002 — Three standing roles, without depending on agent teams

**Status**: accepted — 2026-08-07

## Context

The initial target was: three standing agents as an Agent Team (Manager, Business, Tech), the Manager launching execution workflows in parallel, and the team preparing the next sprint while the current sprint runs.

Checking the Claude Code documentation invalidates several assumptions of that setup:

- Agent teams are **experimental and disabled by default** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
- **One team per session**, tied to the session, not shareable.
- **No nested teams**: a teammate cannot spawn others. The Manager-teammate therefore cannot launch the sprint.
- **The lead is fixed** for the duration of the session.
- **`/resume` and `/rewind` do not restore teammates.** After resuming, the lead talks to agents that no longer exist.
- The team configuration file is execution state: *"don't edit it by hand or pre-author it"*. There is no such thing as a team declared at the project level.
- No background subagent from an in-process teammate.

In other words: "three standing agents" in the sense of processes that live continuously and coordinate across sessions is not achievable today, and a project built on that would break at the first session resume.

## Decision

**The three roles are subagent definitions in the team module's `agents/` directory, not team members.**

> **Erratum** — this ADR originally placed the roles in `scrumia-core/agents/`. They live in `plugins/scrumia-teams/agents/`: the roles are an opinion of the `team` slot, not of the kernel, and moving them made the slot replaceable. The decision itself — subagents rather than team members — is unchanged.

Their permanence comes from two stable mechanisms:

1. **`memory: project`** — persistent memory across sessions, project-scoped. This is what makes a role *remember*: actual velocity, recurring pitfalls, trade-offs already settled, architecture invariants.
2. **State externalized in GitHub** — the board is the shared memory. Any session, at any moment, rebuilds the state by reading it.

**Execution parallelism goes through subagents in `isolation: worktree`**, not through teammates. It's stable, it supports backgrounding, and git isolation is exactly what parallel ticket execution calls for.

The same definition remains usable in three ways, without rewriting:

- Delegated subagent — the normal mode
- Session main agent — `claude --agent scrumia-core:scrumia-manager`
- Teammate in an agent team — when the experimental flag is on; teammates honor a subagent definition's `tools` and `model`

## Consequences

**What we gain**

- The system works without an experimental flag, and survives `/resume`.
- Permanence is real rather than simulated: it rests on durable state, not on live processes.
- If agent teams stabilize, the same files become teammates. No migration.

**What we accept**

- *The "prepare sprint N+1 while sprint N executes" loop is not automatable within one session.* You get it with two Claude Code sessions on the same repo: one executes, the other scopes. Since the state lives in GitHub, they stay consistent without coordinating. It's less elegant than the target, and it works today.
- *Roles don't talk to each other directly.* A subagent reports to its caller. The Manager therefore routes explicitly to Business or Tech and relays their positions — which has the advantage of making disagreements visible to the human instead of letting them get resolved in a private exchange.
- *Project memory must be disciplined.* It contains only what is durable. Writing ticket state into it would make it wrong within days. This is written into every role definition.

## Rejected alternatives

**Building on agent teams right now.** The deal-breaker is not the experimental flag, it's that a teammate cannot spawn others: the Manager could not launch the sprint, which is its main function. On top of that, teammates are lost on session resume.

**A daemon process outside Claude Code that would keep the three agents alive.** Brings back a runtime to maintain, which ADR-0001 rules out, and for uncertain gain.

## To revisit

When agent teams leave experimental status, especially if nested teams or session resume appear. The role definitions won't have to change; only how they are launched will evolve.
