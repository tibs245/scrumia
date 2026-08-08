# Agent team

**Status**: active
**Stratum**: business

## In brief

Standing roles carry ScrumIA's execution: what each owns, what it explicitly
refuses, when it activates, and what escalates to the human regardless of how
autonomous the project is configured to be. Three come from the `team` slot —
manager, business, tech — and a fourth, designer, from whichever module fills the
`design` slot. The roles are permanent through project memory and externalized
board state, not through a live process (`docs/adr/0002-standing-roles.md`).

**Which roles exist is a property of the composition, not of one module.**
`settings.team.roles` is the single list, and an entry names its provider with
`from:` when that provider is not the team module
(`docs/adr/0014-roles-ship-with-their-capability.md`). A role whose slot is empty
does not exist: it would have nothing to guard but its own taste.

## Links

- Owner: `plugins/scrumia-teams` — three of the roles are subagent definitions in
  `plugins/scrumia-teams/agents/` (`scrumia-manager.md`, `scrumia-business.md`,
  `scrumia-tech.md`); `scrumia-designer.md` lives in `plugins/scrumia-design/agents/`
  and is registered in the same list. All are consumed by `scrumia-github-project`'s `scrumia-ticket` skill
  at Step 6, which routes the review by scope. Step 0 invokes no role — it runs the
  refusal gate and calls `pick-model.sh`, which enacts the execution policy specified
  in `features/business/execution-policy/`.
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
| Designer | Visual identity, design-system consistency, legibility and visual hierarchy, accessibility as far as it is visual | The message itself (business), the architecture (tech), delivery priorities (manager); and inventing a value the design system already answers |

Designer is present only where the `design` slot is filled — its definition lives in
that module (`plugins/scrumia-design/agents/scrumia-designer.md`), not in
`plugins/scrumia-teams/agents/`.

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
- #18 — The bootstrap case: a ticket whose deliverable is the parent feature is
  refused at Step 0. This feature was itself created under that gap, by exception.
