# Agent team

**Status**: active
**Stratum**: business

## In brief

Three standing roles — manager, business, tech — carry ScrumIA's execution: what
each owns, what it explicitly refuses, when it activates, and what escalates to
the human regardless of how autonomous the project is configured to be. The roles
are permanent through project memory and externalized board state, not through a
live process (`docs/adr/0002-standing-roles.md`).

## Links

- Owner: `plugins/scrumia-teams` — the three roles are subagent definitions in
  `plugins/scrumia-teams/agents/` (`scrumia-manager.md`, `scrumia-business.md`,
  `scrumia-tech.md`), consumed by `scrumia-github-project`'s `scrumia-ticket` skill
  (Step 0 for routing, Step 6 for review).
- No App feature implements this. `plugins/` is ScrumIA's own product and carries
  no implementation module (`CLAUDE.md`); the roles are not code under `site` or
  `tools`, they are the agent definitions themselves.
- Related ADRs: `docs/adr/0002-standing-roles.md` (why subagents, not team members;
  the sprint-loop constraint), `docs/adr/0006-ticket-routing.md` (how a ticket
  reaches a role).

## Roles

Each role's scope and its explicit refusal — a role with no refusal line would be
indistinguishable from another and shouldn't exist as a separate role.

| Role | Owns | Refuses |
|---|---|---|
| Manager | The board, splitting value into tickets, routing a ticket to the role it belongs to, sprint cadence, arbitration between business and tech | Deciding a business rule itself (routes to business); judging architecture or implementation quality itself (routes to tech); the final merge decision (belongs to the human alone) |
| Business | Business rules and domain vocabulary, consistency across business specs, legal/compliance constraints, business acceptance criteria | The architecture, the stack, delivery planning and priorities — those belong to tech and to the manager |
| Tech | Cross-cutting architecture, API contracts, technical debt, implementation quality | Business rules and delivery priorities — those belong to business and to the manager |

## Files present

| File | Why it exists |
|---|---|
| `business.md` | Activation triggers per role, and the escalation rules that hold regardless of the project's autonomy level |
| `qa.md` | Acceptance criteria for role activation, arbitration and the sprint-loop constraint |
| `CHANGELOG.md` | History of changes to this feature |

No `legal.md`: this feature governs the team's own workflow, not personal data,
payment, or user content. No `archi.md`: it does not touch `site` or `tools`, so
there is no cross-app dialogue to describe for this EPIC.

## Open issues

- #4 — [EPIC] Spec the agent team: roles, triggers, routing, refusal lines (parent)
- #13 — Spec the execution policy: scope x risk to model. Referenced, not
  specified here: this feature documents that a role's model lives in its agent
  frontmatter, not the policy that assigns a model per ticket.
- #18 — The bootstrap case: a ticket whose deliverable is the parent feature is
  refused at Step 0. This feature was itself created under that gap, by exception.
