# GitHub tracking — business rules

## Value

For whoever runs or reviews a ticket — a human or one of the standing roles. It brings
one place to see what is ready, what is running, and what already shipped, without
reconciling a second system against the code — issues, pull requests and reviews live
next to the diff itself. It matters because a ticket's status and its code never drift
apart from being tracked in two tools that someone has to keep in sync by hand.
Measured: every state transition — a card entering a column, an issue closing, a PR
opening — is a timestamped event on the board or the issue itself, so tracking quality
is queryable: how long a ticket sat in each column, how many tickets closed without a
PR ever opening, how many deviations landed on which cell — read straight off the
record, not estimated.

That issues and PRs travel together is also, today, a constraint the `tracker` slot
accepts rather than a free choice —
[ADR-0013](../../../docs/adr/0013-tracker-stays-one-slot.md) records it, with the
condition that would split the slot.

## Ticket lifecycle

A ticket crosses six columns, in order:

| Column | Meaning |
|---|---|
| `Backlog` | Raw intent, not yet refined |
| `Ready for dev` | Refined: criteria written, scope and risk set |
| `To dev` | Selected into the current sprint |
| `In progress` | Being executed |
| `In review` | PR open, awaiting review |
| `Done` | Merged |

A card just added to the board — `gh issue create --project` or `gh project item-add`
— carries **no Status at all**, not `Backlog`: it sits in none of the six until someone
places it. `scrumia-board read` reports that as its own `(no status)` group rather than
folding it into `Backlog`, because a card nobody placed is worth seeing, not papering
over.

Skills never move a card by naming a column directly, except for that first placement.
They name a **flow step**, and `settings.tracker.board.flow` in `.scrumia/config.yaml`
maps each step to this board's actual column name. That indirection is what lets
ScrumIA adopt a board that already exists — columns renamed, vocabulary already in use
— without renaming anything or touching a skill.

| Transition | Trigger | Flow step |
|---|---|---|
| (no status) → `Backlog` | a ticket is filed | none — the column name is used directly, once |
| `Backlog` → `Ready for dev` | `scrumia-refine` judges its four readiness conditions met | `ready` |
| `Ready for dev` → `To dev` | a ticket is selected into a sprint's batch | none named today — not automated today |
| `To dev` → `In progress` | execution starts on the ticket | `in_progress` |
| `In progress` → `In review` | the PR opens | `in_review` |
| `In review` → `Done` | the PR merges | `done` — not automated today either |

Only four flow steps exist in the config (`ready`, `in_progress`, `in_review`,
`done`). `Backlog` is entered by its literal column name, once, at filing. `To dev`
and the post-merge move to `Done` currently have no skill that performs them —
selecting a ticket into a sprint or merging its PR does not by itself move its card.

### Closed without a PR

A ticket can also leave the flow sideways instead of reaching `Done`: closed as
won't-fix from `Backlog`, or abandoned in `Ready for dev` or `In progress` with no PR
ever opened. No transition performs this — closing an issue does not move its card.
The card **keeps whatever Status it last had**; this is post-close residue, not a
seventh column, and not `Done` either — `Done` keeps its single meaning, "merged",
and routing a won't-fix ticket there would make the column answer two different
questions.

A reader trusts the issue's own `state` (open/closed), not the card's Status, to know
whether it still represents live work — the same rule this file applies below to an
epic's progress, read from its children's `state` rather than from where their cards
sit. `qa.md` specifies the board-reading scenario this implies.

## Vocabulary

**Milestone = sprint.** One milestone bounds one sprint. `scrumia-board ready --milestone
"<name>"` is a question with an answer — what is ready to start, for this sprint.
`scrumia-board ready` without a milestone is not a sprint, it is the whole ready column.

**Epic = a ticket whose children are native GitHub sub-issues**, linked with
`gh issue edit <parent> --add-sub-issue <child>`, never with a checklist typed into the
parent's body. GitHub computes the parent's progress itself
(`subIssuesSummary` → `{total, completed, percentCompleted}`), read through
`scrumia-board epic <n>`. A checklist is a second count: it stops matching the moment a
child closes without someone ticking the box, so recounting children by hand is not an
alternative reading, it is a bug waiting to happen.

The `epic` label marks an epic for a human scanning the board; no script reads it. What
makes a ticket an epic, for every consumer that matters, is having native sub-issues —
the label is a signal, not the source of truth.

## Labels and their consumers

| Label | Read by | For |
|---|---|---|
| `scope/*` | `scrumia-pick-model`, and `scrumia-manager` at entry (routes who is asked) | the scope × risk cell of the execution matrix |
| `risk/*` | `scrumia-pick-model` | the same matrix, the other axis |
| `epic` | nobody, programmatically | a human-facing marker only — see above |
| `discussion` | `scrumia-status`, which **subtracts** it — through the board read on the ordinary path, and on the label itself when it falls back to an issue list; the next-step reading, through the same board read | an issue holding something unresolved that is not work waiting to be started |

`discussion` is the only label read as a subtraction, and that is what earns it a place
here rather than in a module's prose. An issue carrying it is not a ticket awaiting
refinement: counting it as one is how a backlog becomes unreadable, and a label nothing
queries would be documentation rather than a filter. What sends an issue there is
`features/business/knowledge-placement/`'s; that it is queryable, and by whom, is this
feature's.

**The subtraction is performed once, in the board read, not in each reading.** Both
readings that owe it reach the board through the same tool on the ordinary path, so a
subtraction written into their prose is a subtraction each of them can forget
independently — and the one that forgets is indistinguishable, in its output, from the one
that did not. Doing it in the read makes it unforgettable for both, and for any third
reading added later.

Where a reading cannot reach the board read at all — the status reading falls back to a
plain issue list when the board is unreachable or unconfigured — the exclusion falls back
to that reading, which applies it on the label itself and says in its report that it did.
That is the one place the subtraction is a reader's own, and it is stated rather than left
to be noticed.

**Subtracting is not dropping.** A discussion-labelled item leaves the columns and arrives
in a group of its own, named and counted — the same treatment this file already gives an
issue closed without a PR. A read that silently returned fewer items than the board holds
would be the filtered read that lies, which is the one failure the reading discipline
below exists to prevent; a reader looking for their own discussion issue still finds it.

**A discussion issue is filed off the board** — created without `--project`, so it takes
no card. The board carries what is in flight, and something nobody intends to start is
not; a card with no Status is a card someone has to place, which is work the issue was
filed to avoid creating. The subtraction in the board read is therefore a backstop: it
catches the issues a human carded by hand, which is the only way one arrives on the board.

That leaves the label queried on the path it actually takes, not only on the exceptional
one, which is the test it had to pass to be declared at all: off the board, `scrumia-status`
reads it directly on its issue-list fallback. A label whose only reader were the board-read
backstop would be the documentation this table refuses — it would be read only when someone
had carded the issue by hand, which is the case the tree is built to avoid producing.

That the label is also a filter anyone can hand `gh issue list` is a consequence of
declaring it, not a reader that earns it its place. It is worth having and it is not the
test.

This is the opposite of what an issue filed for work owes — a reservation raised during a
review, say, is not handled until its card exists, because a cardless ticket is exactly as
forgotten as no ticket. Both follow from the same rule rather than contradicting it: a card
is what makes an issue visible as work, so the issue that *is* work must have one and the
issue that is not must not.

`scope/*` has exactly one programmatic reader, `scrumia-pick-model`, and what its cell means
is specified once, in `features/business/execution-policy/`. Gate 2 — the agent review —
routes by the diff's actual scope, not by this label
(`docs/adr/0005-validation-gates.md`), because a wrong label is precisely the failure a
review guards against, and a label cannot guard against itself. The manager still reads the label at entry, to route who is asked while
the ticket runs (`features/business/agent-team/business.md`), and at exit it still says
which review to *expect* — a reader's convenience, not a gate. A label read two ways is
two labels, and the second one drifts without anyone naming it.

What happens when either label is absent — which default applies, and that the
assumption is stated rather than silently applied — belongs to the policy that reads
them, and is specified there for the same reason.

## A deviation is a structured comment on its own issue

`features/business/execution-policy/` requires that a **deviation** — a human overriding
the model the policy chose, or an executor refusing a split and taking the cell's fallback
— be recorded once, durably, in one venue for both kinds, fielded rather than written as
prose, and findable by the cell it happened on. That is the rule. Here is what it becomes
on GitHub.

**The venue is a comment on the ticket's own issue**, posted by whoever runs the ticket,
before the work starts rather than at PR time — `execution-policy` says why that moment and
not a later one. Two lines:

```
Deviation: <kind> — cell <scope>/<risk> — policy <decision> — ran <model> — by <who>
Reason: <why, in as many lines as it takes>
```

| Field | Values |
|---|---|
| `<kind>` | `override` — a human chose against the policy's answer. `split_refused` — a `split_or_<model>` cell preferred a split and the work proved indivisible |
| `cell` | the scope and risk the policy read, in the axes' own vocabulary — `L/low`, `XL/medium` — not the project's label spelling. `unlabeled/<risk>` where the ticket carried no scope label and the policy answered on its configured default |
| `policy` | what the policy answered, verbatim: a model name, `split_or_<model>`, or `split` for a cell that named no fallback |
| `ran` | the model the ticket actually executed on |
| `<who>` | for `override`, `human` and the handle whose decision it was; for `split_refused`, the skill that judged the work indivisible |

`Reason:` is not optional. A `Deviation:` line with no reason under it is the
non-compliant record `execution-policy`'s AC-7 describes, and is reported as such rather
than counted as a deviation somebody explained.

**Why an issue comment.** A label is queryable and carries no reason, and the reason is the
substance. A Projects v2 field is structured but moves the record into board-side state,
against ADR-0009's "documented composition, no dynamic resolution". A comment carries the
reason, lives beside the ticket, survives the executor, and reuses a carrier the project
already writes to rather than inventing a third.

**How it is read back.** One ticket: `gh issue view <n> --json comments`, the same read a
role-signed verdict uses. Across the project — which is what the record exists for — by
the **`cell` token**, not by the `Deviation:` prefix: the prefix matches prose about
deviations as readily as records, so counting one cell means trusting the cell token and
reading what comes back, not the label. A search that folds the qualifier into the query
silently returns everything — reads are filtered or they lie, the same rule this file
states below for the board itself; the command and the exact failure mode are in
`tech.md`.

The search reaches issues only, so a deviation posted on a pull request is not findable
this way. That is consistent — the venue is the issue — but it means a record written in
the wrong place is not merely misfiled, it is invisible.

Nothing runs any of this on a schedule; per `execution-policy`, whose job that is remains
open.

**The PR body echoes it, and stops being the record.** A PR whose ticket carries a
deviation restates it for a human reading the diff, and that echo is a courtesy. Five PR
bodies were the whole record once, in the sprint whose repeated overrides on the same
cell went uncounted for it; the comment is now the record and the PR is its copy.

## The reference is on every commit; the close is on the pull request, once

`features/business/dev-flow/` states the abstract rule — every commit references the work
item it belongs to, and exactly one closing statement per change, carried by the reviewable
proposal. Here is what it becomes on GitHub.

| Form | Where | What it does |
|---|---|---|
| `Refs: #<n>` | a trailer on **every commit** of the branch | nothing to GitHub. It is the lookup path: `git log --grep '#<n>'` |
| `Closes #<n>` | **exactly once**, in the pull request body | GitHub closes the issue when the pull request merges |

The keywords GitHub acts on are `close`, `closes`, `closed`, `fix`, `fixes`, `fixed`,
`resolve`, `resolves`, `resolved`. **The closing is GitHub's act, not a skill's:** no skill
calls `gh issue close` for a ticket a pull request delivers, because a second closer is a
second source of truth about when the work landed.

**A closing keyword works wherever GitHub finds it**, a commit message reaching the default
branch included. That is exactly why repeating it per commit is a defect rather than
harmless redundancy: several artefacts each claim the close, which one performed it stops
being answerable, and a commit cherry-picked or merged outside its pull request closes a
ticket its change does not deliver. A `Refs:` trailer, conversely, closes nothing and must
never be written as though it might.

The same trap has a quieter form: **a keyword and an issue number in a subject line close
the issue too**, whether or not that was the intent — and `fix`, `fixes` and `fixed` are
both closing keywords and a commit type. `fix(core): fixes #<n>'s lock contention` closes
that ticket the moment it reaches the default branch. A commit that mentions another
ticket names it without a keyword, or in the `Refs:` trailer, which has none.

What the trailer buys is measurable, and its absence is what the lookup costs while it is
missing. Measured on one already-merged ticket of this repository before the rule existed,
`git log --grep` returned five commits: one of the four its pull request delivered, and
four belonging to other tickets — 25% recall, 20% precision, from a search whose output
reads complete. Redundant references are fine; incomplete ones are what break the lookup.

## Reading discipline: a board is read through a filter, never whole

This is a product rule, not an implementation footnote. `gh project item-list` returns
its **first 30 items** by default — not an error, not a warning, a first page shaped
exactly like a complete answer. A board past that size read without an explicit limit
or filter is silently half-read, and nothing in the raw output says so.

Consequently: no skill composes `gh project` calls directly. Every board read goes
through `scrumia-board`, which always passes an explicit limit, compares the result against
GitHub's own `totalCount`, and reports `truncated: true` the moment the two disagree.
A widened `--limit` is a workaround for one read, not a fix — the rule is to filter
(by milestone, by status, by query), not to keep raising a number that a bigger board
will outgrow again.

The corollary trap — an invalid or stale filter reading as legitimately empty — is
specified in `qa.md`.

**The board and the issues are two surfaces, and looking for something already settled
reaches only the second.** Settled work is out of every ordinary board read — `Done` is
filtered by default, and a discussion issue was never carded at all — so a board search
for it comes back empty and reads as "nothing like this was ever raised": wrong, silently,
and in the one direction that matters to anyone checking whether a question has been asked
before. The card itself survives the close, per § *Closed without a PR* above; what does
not survive is its reachability through a read that exists to show live work. The module therefore publishes an issue search alongside
the board read, covering open and closed together, and it is not a board read with a wider
filter: the surfaces differ, and the answer names which one it read so the two can never
be mistaken for each other. What sends a reader there is
`features/business/knowledge-placement/`'s BR-6; that the two surfaces are distinct, and
that the issue one exists, is this feature's.

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
