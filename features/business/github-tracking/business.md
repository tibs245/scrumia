# GitHub tracking — business rules

## Vocabulary

**Milestone = sprint.** One milestone bounds one sprint. `board.sh ready --milestone
"<name>"` is a question with an answer — what is ready to start, for this sprint.
`board.sh ready` without a milestone is not a sprint, it is the whole ready column.

**Epic = a ticket whose children are native GitHub sub-issues**, linked with
`gh issue edit <parent> --add-sub-issue <child>`, never with a checklist typed into the
parent's body. GitHub computes the parent's progress itself
(`subIssuesSummary` → `{total, completed, percentCompleted}`), read through
`board.sh epic <n>`. A checklist is a second count: it stops matching the moment a
child closes without someone ticking the box, so recounting children by hand is not an
alternative reading, it is a bug waiting to happen.

The `epic` label marks an epic for a human scanning the board; no script reads it. What
makes a ticket an epic, for every consumer that matters, is having native sub-issues —
the label is a signal, not the source of truth.

## Labels and their consumers

| Label | Read by | For |
|---|---|---|
| `scope/*` | `scrumia-teams/scripts/pick-model.sh` | the scope × risk cell of the execution matrix |
| `risk/*` | `scrumia-teams/scripts/pick-model.sh` | the same matrix, the other axis |
| `epic` | nobody, programmatically | a human-facing marker only — see above |

`scope/*` has exactly one programmatic reader, `pick-model.sh`, and what its cell means
is specified once, in `features/business/execution-policy/`. It had a second until
#130 — `scrumia-ticket` Step 6, which gated the required review on the tier. Gate 2
routes by the diff's actual scope instead (`docs/adr/0005-validation-gates.md`), because
a wrong label is precisely the failure a review guards against, and a label cannot guard
against itself. The manager still reads the label at entry, to route who is asked while
the ticket runs (`features/business/agent-team/business.md`), and at exit it still says
which review to *expect* — a reader's convenience, not a gate. A label read two ways is
two labels, and the second one drifts without anyone naming it.

What happens when either label is absent — which default applies, and that the
assumption is stated rather than silently applied — belongs to the policy that reads
them, and is specified there for the same reason.

## Reading discipline: a board is read through a filter, never whole

This is a product rule, not an implementation footnote. `gh project item-list` returns
its **first 30 items** by default — not an error, not a warning, a first page shaped
exactly like a complete answer. A board past that size read without an explicit limit
or filter is silently half-read, and nothing in the raw output says so.

Consequently: no skill composes `gh project` calls directly. Every board read goes
through `board.sh`, which always passes an explicit limit, compares the result against
GitHub's own `totalCount`, and reports `truncated: true` the moment the two disagree.
A widened `--limit` is a workaround for one read, not a fix — the rule is to filter
(by milestone, by status, by query), not to keep raising a number that a bigger board
will outgrow again.

The corollary trap — an invalid or stale filter reading as legitimately empty — is
specified in `qa.md`.

## Scope of this slot

Two planes, easily conflated and separated on purpose: what the **module** implements,
and where the **rules** it enacts are specified.

**What the module implements.** Per `docs/adr/0013-tracker-stays-one-slot.md`, the
`tracker` slot — filled here by `scrumia-github-project` — implements three concerns at
once, by decision rather than by necessity: the work items (issues, labels, milestones,
epics), the board (columns, the Status field, transitions), and **the code cycle**
(branches, worktrees, PR creation, review routing, merge). The first two are "what is
to be done and where it stands"; the third is "how the change reaches `main`" — related
only because GitHub happens to offer all three under one product.

**Where the rules are specified.** The code cycle's *process* is
`features/business/dev-flow/`'s, not this feature's: that feature owns it, and this one
traces it — it says which concrete artefact each of its steps becomes on GitHub. Where
the two disagree, `dev-flow` governs and this feature is what changes. The replacement
test that files any given rule on exactly one side is in `dev-flow`'s `business.md`
§ *The code cycle*; it is stated there once and not restated here.

The module implementing the cycle and `dev-flow` specifying it are both true, because
they speak on different planes. Why ADR-0013 does not settle this — and why no
superseding ADR is owed — is argued once, in `dev-flow`'s `business.md`.

The practical consequence: **issues in one tracker, pull requests on GitHub is not
composable today.** A module filling `tracker` with Jira, Linear or a local file store
would have to reimplement branches, worktrees and PR creation — mechanics that have
nothing to do with the tracker it replaces — or leave ticket execution with no way to
open a PR at all. ADR-0013 defers the split rather than rejecting it, and names the
conditions that reopen it: a real project blocked by exactly this, a file-based tracker
module being written, or `scrumia-review` and `scrumia-status` observed diverging in
what they each need from the slot.
