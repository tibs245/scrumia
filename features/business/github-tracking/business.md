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

**A card is what makes an issue visible as work, so an issue that is work takes one and an
issue that is not takes none.** Both halves bite. A ticket filed without a card is exactly
as forgotten as no ticket — `scrumia-board read` and `ready` only see cards, so it reaches
no status reading, no sprint and no reviewer, whatever its body says. And an issue that
nobody intends to start does not take a card, because a card with no Status is work
someone has to triage, which is the cost the filing was meant to avoid. This is one rule
with two consequences, not two conventions that happen to point opposite ways; the
`discussion` label below is where the second consequence is worked out, and a reservation's
ticket is where the first one is.

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

**This table is the ticket's lifecycle, not every issue's.** A ticket is an issue filed as
work to be done; an issue that is not work — one holding a discussion — is filed, takes no
card, and enters this table nowhere. That is not a gap in the table: an issue nobody
intends to start has no state to be in, and giving it one would mean answering "where is
this up to?" about something nobody is doing. The two words are used precisely from here
on, and where this file says *ticket* it means the first kind.

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
| `discussion` | `scrumia-board issues --search "label:discussion"`, which finds them; `scrumia-status` and the next-step reading, which **subtract** them — through the board read where one was carded, and on the label itself where the status reading falls back to an issue list | an issue holding something unresolved that is not work waiting to be started |

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

**Its own group, and not the one for a ticket closed without a PR.** A discussion is
normally closed once it is settled and never had a pull request, so it matches that
group's shape exactly while being the opposite of what that group means — an abandoned
ticket is a question about someone's unfinished work, and a settled discussion is nobody's.
The label decides first, and what that costs to get wrong is a report claiming abandoned
work that never existed.

**A discussion issue is filed off the board** — created without `--project`, so it takes
no card. The board carries what is in flight, and something nobody intends to start is
not; a card with no Status is a card someone has to place, which is work the issue was
filed to avoid creating. The subtraction in the board read is therefore a backstop: it
catches the issues a human carded by hand, which is the only way one arrives on the board.

So on the ordinary path the label is not what removes the issue from the readings — being
uncarded already did that. What the label buys there is that the issue stays **findable**:
`scrumia-board issues --search "label:discussion"` returns every one of them, open and
closed, which is the only way to see what has been left unresolved. The subtraction is the
backstop for the carded exception, and the search is the ordinary reader.

That is what the declaration test asks for and it is worth stating exactly, because the
weaker claim is the tempting one: this label is not queried on every path by a skill that
runs unprompted. It is queried by a published command with a documented argument, and by
`scrumia-status` directly when it falls back to an issue list. A label whose only reader
were the board-read backstop would be read only when someone had carded the issue by hand
— the case the tree exists to avoid producing — and that would be the documentation this
table refuses.

That is the second consequence of the card rule stated in the lifecycle section above, and
a reservation raised during a review — not handled until its card exists — is the first.
Neither is a convention of its own.

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

**Gate 2's scoping signal is a comment on the ticket's own issue; the pull request body
echoes it.** `features/business/dev-flow/` states when the signal is owed, to whom, and
that it is recorded against the work item. Here is what that becomes on GitHub: the record
is a comment on the issue, posted when the gap is found; the pull request body carries a
copy of it for whoever is reading the diff, and that copy is a courtesy. Same split, and
for the same reason, as the deviation record below — a run that dies before `gh pr create`
leaves the record behind it, where a signal living only in a PR body would have gone with
it. The two records differ in what they hold, not in where they live, which is why this
file states one venue rule and not two.

What that record's fielded shape is, and the token a project-wide read finds it by, is not
written yet — unlike the deviation record below, which carries both. Until it is, the
signal is findable on the ticket it belongs to and not across the project.

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

## A role review verdict is a comment on the ticket's own issue

`features/business/dev-flow/` requires that a ticket at gate 2 carry the outcome of its
review as a record that survives the executor's death — one of `run`, `not_required`,
or `not_run` with a cause. Three properties no other carrier has: **unfalsifiable by
omission** (no role-signed comment = no review, whatever the executor's report says),
**survives the executor** between review and PR, and **machine-readable** for the
gather. Here is what that becomes on GitHub.

**The venue is a comment on the ticket's own issue**, posted by the reviewing role's
agent at the end of its review. The format is the role's, fixed:

```
Verdict: Approved | Reservations | Blocked — #<n> — by scrumia-<role>
```

`Approved`, `Reservations` and `Blocked` are the three outcomes the role can sign;
the ticket number ties the verdict to its work item; the `by scrumia-*` token names
the role that produced it. The format is not negotiated per role or per ticket — it
is the vocabulary the gate reads, and a verdict that does not match the format is
read as absent (`not_run`).

**Why an issue comment.** Same trade-off as the deviation record above: a label is
queryable and carries no verdict, and the verdict is the substance. A Projects v2 field
is structured but moves the record into board-side state, against ADR-0009's
"documented composition, no dynamic resolution". A structured field in the agent's
return dies with the session and is written by the executor — exactly the failure mode
the role-posted verdict exists to remove. A comment carries the verdict, lives beside
the ticket, survives the run, and reuses a carrier the project already writes to
rather than inventing a third.

**Who posts it.** The reviewing role's agent, not the executor. The executor is the
*convener* of the review (`features/business/dev-flow/`), and is not the reviewer — the
roles are distinct agents with their own definitions, and "the author reviews their own
work" was never the defect. The executor running a general agent handed the role's
`agents/` file is not a role review, and the verdict it could write is not a role
verdict: the `claude -p --agent` subprocess is `run` when it ran as the role, and
`not_run` when it did not. This is the substance the attribution clause names, and
what the substitution path closes.

**How it is read back.** One ticket: `gh issue view <n> --json comments`, the same
read a deviation record uses. Across the project — which is what the gather needs:

```bash
gh search issues --repo <owner>/<repo> --match comments 'Verdict:' 'by scrumia-*'
```

The two terms are ANDed, and the `by scrumia-*` token is what discriminates a role
verdict from a comment that happens to match the prefix; without it, a search over
`Verdict:` alone returns every issue that quotes the word. The exact failure mode if
the qualifier is folded into the query string is the same as the deviation record's
(`tech.md`'s *"The deviation search command"*): GitHub discards what it cannot parse
and answers with the whole repository, exit code 0, no warning.

**The PR body echoes it, and stops being the record.** A PR whose ticket carries a
role verdict restates it for a human reading the diff, and that echo is a courtesy.
The orchestration that reports the verdict from the PR body alone is the orchestration
that cannot tell a review that ran from one that was skipped — the executor wrote
both, and the executor's report is what failed on the 2026-08-08 sprint. The comment
is now the record; the PR is its copy.

**The orchestrator reading the gate is the one that triggers the net.** Where the
ticket's issue carries no `Verdict: … by scrumia-*` comment at gate 3, the
orchestrator runs the role review on that absence — a checkable fact, not a
declaration by the executor. "The executor says no review ran" is exactly the report
that is not trusted: an executor that wrote the absence would have written a verdict
in the same place, and both are the same record. The net is the checkable fact, and
the gather's report is what closes the substitution path.

## Gate 3 reads the verdict and the file set through two tracker-side artefacts

`features/business/dev-flow/` states the four cumulative conditions gate 3 opens
on and the predicate over `settings.autonomy.auto_merge`. Whether a change
satisfies condition (2) — every path matched by an active category — needs the
change's **full file set**, and condition (4) needs the **attributable verdict
on the record**. Here is what each becomes on this tracker.

**The full file set is the change's commit history on the branch, evaluated at
the head it actually merges.** A file the change touched and then reverted
still counts — the file appeared in the diff set, and a partial-credit reading
is what condition (2) explicitly refuses. A label the change carried and
dropped does not; a commit message does not. What is read is the set of paths
the branch's commits introduce or modify, at the merge target — obtained
through the same artefact the diff passes to gate 2 (`gh pr diff <n>` for the
plain listing, `gh pr view <n> --json files` for the structured one), whichever
the caller chooses, with the same reading discipline. Reading the change off
the working tree instead of the branch would evaluate a tree the branch may
already have moved past; the merge target is the only state the merge actually
merges.

**The verdict is a comment on the ticket's own issue, sourced from the
reviewer that wrote it.** Gate 3 reads it the same way every other artefact on
the issue is read — `gh issue view <n> --json comments` — and finds it by the
reviewer's signed verdict, not by a count of comments: the same rule that
finds a deviation by the `cell` token rather than the `Deviation:` prefix,
because a prefix matches prose about verifiers as readily as verifier records,
and a reader that trusts the prefix counts prose as a verdict. The verdict
itself is a separate shape from the deviation record named just above — it
names whether the change is mergeable, mergeable with reservations, or
blocked, and who said so — and what gates reading it is what the sibling
implementation sub-issue's eligibility script does on top of this read.

**Why the verdict and the file set, and not the labels.** Gate 3 does not read
`scope/*` or `risk/*` at all. A wrong label is exactly the failure a review
guards against, and the eligibility decision depends on what the change
actually touched, not on what the manager's refinement assumed it would
(`features/business/dev-flow/business.md` § *Gate 2's scoping signal*). The
trace here is, like the one for deviations, the bare minimum the predicate
needs to evaluate on — what `scrumia-review` and the eligibility script do
with these artefacts is theirs, not this feature's.


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
not survive is its reachability through a read that exists to show live work. The module
therefore publishes an issue search alongside
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
