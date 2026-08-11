# Agent team

**Status**: active

## In brief

Standing roles carry ScrumIA's execution: what each owns, what it explicitly
refuses, when it activates, and what escalates to the human regardless of how
autonomous the project is configured to be. Three come from the `team` slot —
manager, business, tech — and a fourth, designer, from whichever module fills the
`design` slot. The roles are permanent through project memory and externalized
board state, not through a live process (`docs/adr/0002-standing-roles.md`).
A role can also be reached outside a ticket: convening brings the enabled
roles up, hands the floor back to the human, and starts no sprint.

## Links

- Owner: `plugins/scrumia-teams` — three of the roles are subagent definitions in
  `plugins/scrumia-teams/agents/` (`scrumia-manager.md`, `scrumia-business.md`,
  `scrumia-tech.md`); `scrumia-designer.md` lives in `plugins/scrumia-design/agents/`
  and is registered in the same list. All are consumed by `scrumia-github-project`'s `scrumia-ticket` skill
  at Step 6, which routes the review by the diff's actual scope, not by the ticket's
  `scope/*` label (`docs/adr/0005-validation-gates.md`). Step 0 invokes no role — it runs the
  refusal gate and calls `scrumia-pick-model`, which enacts the execution policy specified
  in `features/business/execution-policy/`.
- No App feature implements this. `plugins/` is ScrumIA's own product and carries
  no implementation module (`CLAUDE.md`); the roles are not code under `site` or
  `tools`, they are the agent definitions themselves.
- Related ADRs: `docs/adr/0002-standing-roles.md` (why subagents, not team members;
  the sprint-loop constraint), `docs/adr/0015-scope-measures-reach.md` (how a ticket
  reaches a role).
- Roles: `business.md` — the Owns/Refuses table per role, and the rule that which
  roles exist is a property of the composition, not of one module.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Activation triggers per role, the escalation rules that hold regardless of the project's autonomy level, the Owns/Refuses table per role, and what a role's project memory may and may not hold |
| `qa.md` | Acceptance criteria for role activation, convening as an entry point, arbitration and the sprint-loop constraint |
| `CHANGELOG.md` | History of changes to this feature |

No `legal.md`: this feature governs the team's own workflow, not personal data,
payment, or user content. No `archi.md`: it does not touch `site` or `tools`, so
there is no cross-app dialogue to describe for this EPIC.

