# Acceptance criteria — agent team

One scenario per case. Each scenario must be able to fail.

## Nominal

### AC-1 — A role activates on its documented trigger

```gherkin
Given a ticket labeled scope/L that changes a business rule consumed beyond
  one feature or app
When the manager routes it
Then the business role is asked at entry, alongside tech
```

### AC-2 — The manager routes without deciding the substance

```gherkin
Given a ticket raises a question about architecture or dependency choice
When the manager routes it
Then it delegates the question to the tech role rather than answering it itself
```

### AC-12 — Convening the team brings the roles up without starting a sprint

```gherkin
Given a project whose team slot is filled and whose roles are enabled
When a human asks to start the team
Then the enabled roles are convened and each states what it owns and what it
  refuses to rule on
And no sprint starts and no card moves
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
  docs/adr/0015-scope-measures-reach.md
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

### AC-13 — A role is declared but its module is not installed

```gherkin
Given the composition declares a role as enabled: true whose module is not
  installed
When the team is convened
Then that role is reported as a gap rather than silently convened as part of
  a smaller roster
And the install command is named, not a restart
```

### AC-14 — A non-business rule crossing the boundary does not convene business

```gherkin
Given a ticket labeled scope/L whose only change is an interface contract
  between two apps, with no business rule at stake
When the manager routes it
Then tech is asked at entry and the business role is not
```

AC-1 and AC-14 are the two halves of one trigger. `scope/L` is reached by any of the
axis's three questions (`docs/adr/0015-scope-measures-reach.md`), and only one of them
concerns a business rule; the label alone therefore does not convene business, and the
role's own condition in `business.md` — *and changes a business rule* — is what does.

### AC-15 — Two sessions write the same card: last-writer-wins holds

```gherkin
Given two sessions target the same ticket's card
When both write to it, one after the other
Then the write executed last is the one that stands, with no error or lock
  raised by the shared state today
```

### AC-16 — No compare-and-swap: a stale write still succeeds

```gherkin
Given a session decided its write from a read that is no longer current
When it writes anyway
Then the write is accepted regardless of the state read — no compare-and-swap
  exists in the shared state to reject it
```

## Role consultation as a reflex

The conditions under which a role is consulted — the rule itself — are stated once in
`business.md § When a role must be consulted`. These scenarios test that the skills which
route to a role apply it rather than inviting it.

### AC-17 — A refinement consults the role whose domain owns the blocker

```gherkin
Given a refinement whose blocker is a question a role owns — a business rule is
  ambiguous, the change reaches beyond one feature, two written statements
  contradict, or the same question blocks several tickets
When the refinement completes
Then the role was consulted and its answer is on the ticket
  Or the report names the role as unreachable and the gap that made it so
```

### AC-18 — A refinement that did not consult a role says so and says why

```gherkin
Given a refinement completes without consulting any role
When the refinement report is written
Then it names the roles it could have consulted and states which condition of
  business.md § When a role must be consulted did not apply — and a report that
  is silent on the question has not met this criterion
```

### AC-19 — An execution consults the same role the refinement did, or states why not

```gherkin
Given a ticket whose refinement consulted a role and recorded the answer on it
When the execution runs and the same question still conditions the change
Then the execution references the answer on the ticket rather than re-asking
  Or its report names the reason the previous answer no longer holds
```

### AC-20 — A review that could not run as the role names what did run

```gherkin
Given a PR's role review could not be reached — the agent type did not resolve,
  the shipping module was not installed, or the question lies outside every
  declared role
When the PR is opened
Then the PR description names the role as unreachable and what ran in its place
  — a general agent handed the role's definition is named as such, never as the
  role itself
```

### AC-21 — A repeated question is asked once and referenced

```gherkin
Given two tickets in the same refinement pass share a blocker on the same role's
  domain
When the first ticket's refinement convenes the role and records the answer
Then the second ticket's refinement references that answer rather than asking
  the role again
  And the role is convened once across the pass, not once per ticket

```


## Verdict attribution and the role-posted format

The verdict the role posts on the ticket's issue is identified by its format, and a record that does not match is read as absent. These scenarios test that the gate reads what the role wrote, and that what it cannot read it does not infer.

### AC-22 — A role's verdict carries the role's name, and is posted by the role

```gherkin
Given a role review that ran as the role and reached a verdict
When the verdict is recorded on the ticket's issue
Then the comment carries the `Verdict:` prefix, one of `Approved`, `Reservations`,
  `Blocked`, the ticket number, and the `by scrumia-<role>` token — the role is
  identified, the verdict is attributable, and the comment is the role's, not
  the executor's
```

```gherkin
Given a verdict posted on the ticket's issue that lacks the `by scrumia-*` token
When the gather reads the verdict
Then the verdict is treated as absent and the state is `not_run` — an unattributed
  verdict is not a role verdict, and the attribution clause exists for that
  reading
```

### AC-23 — A `not_required` verdict is derived from the scope label, not asserted by the executor

```gherkin
Given a ticket whose scope is `scope/S` and which therefore requires no review
When the gather reads the ticket
Then it reports `not_required` — derived from the scope label, not asserted by
  the executor; an executor that asserts `not_required` on a `scope/M` or
  `scope/L` produces a non-compliant record
```

### AC-24 — A `not_run` carries a cause in the same field the state is

```gherkin
Given a `not_run` outcome that the gather reports on the ticket
When the record is read
Then the cause is named in the same field the state is — "skipped",
  "unreachable", "self-applied", "agent type did not resolve" — and a state
  without a cause is non-compliant
```


## Out of scope

- Which model executes a given ticket, based on its scope and risk labels —
  that is the execution policy, specified separately in
  `features/business/execution-policy/`. This feature only establishes that a
  role's own model lives in its agent frontmatter.
- The mechanics and matrix of `scrumia-pick-model`.
- Any enforcement or claim mechanism for concurrent writes (session tags,
  leases, locks) — AC-15 and AC-16 document today's last-writer-wins behavior
  only; no change to `board.sh` or `scrumia-sprint` is implied or required.
