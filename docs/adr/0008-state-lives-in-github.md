# ADR-0008 — State lives in GitHub, never in the repo

**Status**: accepted — 2026-08-07

## Context

BMAD writes progress state into versioned files: `sprint-status.md`, implementation artifacts, story statuses. Over six months of use, the observed flaw is constant — **these files diverge from reality within days, then keep being read as if they were right**.

The mechanism is mechanical: a state file has two writers (the agent and the human), no lock, and no consistency constraint. It can only drift. And a wrong state is worse than no state, because you stop checking it.

## Decision

**Nothing in the repo describes a state that moves.**

| Nature | Where it lives |
|---|---|
| What needs doing | GitHub issue |
| Progress | Issue state and labels |
| Who is working on it | Issue assignment |
| The *why* of a one-off decision | Issue comment |
| What changed, when | Commits + feature `CHANGELOG.md` |
| The durable *what* | `features/` |
| A structuring decision | `docs/adr/` |
| Project configuration | `.scrumia/config.yaml` — describes the project, not its state |

Progress views are **computed on demand** (`scrumia-status`) and never written.

A `PreToolUse` hook actively blocks the creation of `sprint-status.md`, `backlog.md`, `sprint.md`, `todo.md`, `tasks.md` and variants, in any project containing `.scrumia/config.yaml`. The message explains where to put the information instead.

> **Erratum** — this ADR originally placed the hook in `scrumia-core`. It ships with `plugins/scrumia-github-project`: "state lives in the tracker" is the tracker module's opinion, and a composition using a different tracker must be able to drop it. The decision itself — enforce the rule with a hook — is unchanged.

## Consequences

**What we gain**

- A single source of truth for state, with a single write mechanism.
- Every session and every agent sees the same state, without coordinating. That is what makes the two-parallel-session setup described in ADR-0002 viable.
- The repo contains only durable material, so spec diffs are readable: they are no longer drowned in status updates.
- The hook makes the rule enforceable rather than documentary. An untooled convention gets violated within the month.

**What we accept**

- *Hard dependency on GitHub.* Without an authenticated `gh`, this module does not work. Owned: that is already where the code and the PRs live.
- *No offline state.* A session without network cannot read the board.
- *The GitHub API has rate limits.* No effect at this scale.
- *The hook can block a legitimate file* that bears one of these names without being state. The message says so and suggests renaming. The hook only activates if `.scrumia/config.yaml` exists, and does nothing without `jq` — a safeguard must never break a session.

## Rejected alternatives

**State in the repo, synchronized with GitHub.** That stacks the drawbacks: the divergence remains, plus a synchronization mechanism to maintain and debug. Synchronization does not remove the second writer, it makes it harder to see.

**State in the repo, GitHub as a mirror.** Inverts the source of truth toward the medium that has no lock, no consistency constraint, no assignment, no notifications.
