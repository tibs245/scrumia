# Acceptance criteria — agent team

One scenario per case. Each scenario must be able to fail.

## Nominal

### AC-1 — A role activates on its documented trigger

```gherkin
Given a ticket labeled scope/L that modifies a file under features/business/**
When the manager routes it
Then the business role is asked at entry, alongside tech
```

### AC-2 — The manager routes without deciding the substance

```gherkin
Given a ticket raises a question about architecture or dependency choice
When the manager routes it
Then it delegates the question to the tech role rather than answering it itself
```

## Edge cases

### AC-3 — Two roles disagree

```gherkin
Given the business role finds a PR non-compliant and the tech role approves
  the same PR
When the manager arbitrates
Then it escalates to the human with both positions summarized and its own
  recommendation, and it does not average or overrule either verdict into a
  compromise
```

### AC-4 — A role is disabled

```gherkin
Given the tech role is set to enabled: false in .scrumia/config.yaml's team.roles
When a question that would normally activate the tech role arises
Then it goes straight to the human, not settled by the manager on the grounds
  that no one else is available
```

### AC-5 — A ticket carries no scope label

```gherkin
Given a ticket has no scope/* label
When the manager prepares a sprint from the ready tickets
Then the ticket is excluded from the sprint as unscoped, per
  docs/adr/0006-ticket-routing.md
```

### AC-6 — Escalation holds at any autonomy level

```gherkin
Given .scrumia/config.yaml's autonomy.level is set to autonomous
When a role disagreement, a missing business rule, or a cross-app contract
  change occurs
Then it still escalates to the human — the autonomy level changes how much
  routine work runs unattended, never whether these three escalate
```

### AC-7 — Preparing the next sprint while the current one executes

```gherkin
Given a single Claude Code session is executing sprint N's tickets as
  subagents
When that same session is asked to also scope and prepare sprint N+1
Then it cannot in one session — a subagent cannot spawn subagents
  (docs/adr/0002-standing-roles.md) — and preparing N+1 requires a second
  session against the same repository, kept consistent with the first through
  the board's externalized state rather than through direct coordination
```

### AC-8 — A role provided by another module survives a team reconfiguration

```gherkin
Given .scrumia/config.yaml's team.roles carries an entry with from: scrumia-design
When scrumia-team-setup is re-run to adjust the team
Then the entry is reported as active and left untouched, not dropped as unknown
  to the team module
```

### AC-9 — A role whose slot is empty is not offered

```gherkin
Given a project whose design slot is null
When a question about visual identity arises
Then no designer role is invoked, and the absence of the capability is stated
  rather than answered on taste
```

### AC-10 — A role review that could not run as the role says so

```gherkin
Given a sprint is executing a ticket and reaches its role review
When the role's agent type does not resolve
Then the verdict reports that the review did not run as that role, and a
  general agent handed the role's definition is never reported as the role
```

### AC-11 — A module shipping agents is not usable before a restart

```gherkin
Given a module providing standing roles has just been installed or updated
When the roles are addressed without restarting Claude Code
Then they do not resolve — a hot reload refreshes skills but not agent types —
  and the answer names the restart rather than falling back silently
```

## Out of scope

- Which model executes a given ticket, based on its scope and risk labels —
  that is the execution policy, specified separately in
  `features/business/execution-policy/`. This feature only establishes that a
  role's own model lives in its agent frontmatter.
- The mechanics and matrix of `scrumia-teams/scripts/pick-model.sh`.
