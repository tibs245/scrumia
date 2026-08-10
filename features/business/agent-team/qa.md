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

### AC-15 — The four-channel split and its membership test are stated once

```gherkin
Given a feature needs to say what its own channel may hold
When it applies the membership test — "would a new human contributor need to
  know this?"
Then it cites business.md § "Four channels, one home each" rather than restating
  the split or the test
And a second statement of the test anywhere in the repo is a defect, not a
  convenience
```

### AC-16 — A memory entry points at a rule instead of carrying it

```gherkin
Given a role writes an entry to .claude/agent-memory/<role>/
When the entry concerns a rule a spec, ADR or ticket owns
Then it names that document and says what to watch for when applying it
And a reader cannot act on the entry without opening what it cites
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

### AC-17 — An existing entry that carries a rule is moved out of memory

```gherkin
Given an entry in .claude/agent-memory/ states a rule no spec, ADR or ticket owns
When the channel is audited
Then the rule is relocated to the channel the membership test names, and the
  entry is reduced to a pointer to it — or, where relocating it is work of its
  own, the entry names the ticket that will carry it
And an entry whose rule has no home anywhere is not left as the rule's record
```

### AC-18 — One role's memory is tracked and another's is not

```gherkin
Given .claude/agent-memory/<role-a>/ is tracked by git and
  .claude/agent-memory/<role-b>/ is not
When the channel is validated
Then it fails as partially tracked — git status reading clean while two machines
  hold different beliefs is the failure, not "some files are in git"
```

### AC-19 — An entry that no condition can invalidate

```gherkin
Given a memory entry carries no metadata.stale_when, or an empty one
When the channel is validated
Then it fails, because nothing could ever retire the belief it holds
```

### AC-20 — A conclusion no human reached is marked as the role's own

```gherkin
Given a role writes an entry from its own inference rather than a human ruling
When the entry is written
Then metadata.source reads agent, and only an entry sourced to a named human on
  a date may be treated as settled
```

### AC-21 — Two roles hold standing instructions on the same question

```gherkin
Given two roles' directories each carry an entry with the same metadata.topic
When the channel is validated
Then the pair is reported so the contradiction can be judged — neither role
  reads the other's directory, so an unreported pair is undetectable
And carrying the same topic is not itself a failure: two roles may hold
  complementary halves of one question
```

### AC-22 — An index and the files beside it disagree

```gherkin
Given a role's MEMORY.md names a file that is not present, or a file is present
  that MEMORY.md does not name
When the channel is validated
Then it fails in both directions — an unnamed file is invisible to the role, and
  a named absent file sends it to nothing
And the check takes the tree and its index filename as arguments, so a second
  indexed tree reuses it rather than growing a second check
```

AC-1 and AC-14 are the two halves of one trigger. `scope/L` is reached by any of the
axis's three questions (`docs/adr/0015-scope-measures-reach.md`), and only one of them
concerns a business rule; the label alone therefore does not convene business, and the
role's own condition in `business.md` — *and changes a business rule* — is what does.

## Out of scope

- Which model executes a given ticket, based on its scope and risk labels —
  that is the execution policy, specified separately in
  `features/business/execution-policy/`. This feature only establishes that a
  role's own model lives in its agent frontmatter.
- The mechanics and matrix of `scrumia-teams/scripts/pick-model.sh`.
