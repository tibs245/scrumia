---
name: scrumia-sprint-fast
description: A sprint-fast mode for a small batch of ready tickets — each ticket merges on gate 1 alone, one global review at the end, fixups autosquashed under the orchestrator. Use it when the batch is small enough that N per-ticket role reviews cost more than they protect, and a single sprint-level verdict on the sprint PR is acceptable for the cost it carries.
---

# sprint-fast — one global review, fixups autosquashed

A `sprint-fast` sprint is the normal sprint with two changes:

- Each ticket runs `scrumia-ticket` **without its per-ticket role review**, and its
  PR merges into the sprint branch as soon as CI is green — gate 1 alone.
- When every ticket is merged, **one global review** runs on the sprint branch.
  Findings land as `fixup!` commits on fix branches cut from the sprint branch's
  tip. The orchestrator alone autosquashes, exactly once, after every ticket
  worktree is closed and no ticket branch cut from the sprint branch is live.

The rule is stated once in [`features/business/dev-flow/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/dev-flow/business.md)
§ *sprint-fast*. This skill cites it and owns the steps that differ from
`scrumia-sprint` — Steps 1–3 of the normal sprint are not restated here.

## Steps 1–3 are the normal sprint's — cite, don't restate

Steps 1–3 of [`plugins/scrumia-teams/skills/scrumia-sprint/SKILL.md`](https://github.com/tibs245/scrumia/blob/main/plugins/scrumia-teams/skills/scrumia-sprint/SKILL.md)
apply unchanged:

- **Step 1 — Build the batch.** `scrumia-board ready --milestone "<sprint>"`,
  discard the conflicts, run `scrumia-pick-model <n>` on each surviving ticket.
  A `split_or_model` ticket enters on its fallback model, with the refused split
  recorded on the ticket. A `split` ticket returns to refinement.
- **Step 2 — Load what this project batches against.** `scrumia-extends sprint`.
- **Step 3 — Get the batch validated.** Present the batch with the model each will
  run on; the human launches.

**The one addition is the sprint label.** Every ticket of the batch carries
`process/sprint-fast` from the moment it is selected, set by the orchestrator —
not by `scrumia-ticket`, because the orchestrator is the one that decided this
is a sprint-fast sprint. The label is what tells the gather and the
retrospective where to find the gate-2 record (the sprint PR, not each
ticket's issue), and the absence of it is the failure `features/business/github-tracking/`
AC-42 names by name. Add the label here, before any ticket worktree is cut.

## Step 4 — Create and push the sprint branch, once

Step 4a of `scrumia-sprint` — the sprint branch itself — applies unchanged. The
trigger, the obligation, the close form, and the deletion rule are stated once
in [`features/business/dev-flow/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/dev-flow/business.md)
§ *The sprint branch*; this skill cites it.

```bash
git fetch origin <default-branch>
git checkout -b sprint/<milestone-slug> origin/<default-branch>
git push -u origin sprint/<milestone-slug>
```

The first ticket worktree runs only after the push returns.

## Step 5 — Cut one worktree per ticket, from the sprint branch

Step 4b of `scrumia-sprint` applies unchanged: each worktree is `.worktrees/<branch>`
relative to the orchestrator's cwd, cut with `git worktree add .worktrees/<branch>
-b <branch> sprint/<milestone-slug>`, and dispatched as `scrumia-ticket` on its
ticket number. The branch is named after the ticket's final intent per ADR-0017
§3; the worktree's `.lock` retry policy is the same.

**Tell each execution: skip the per-ticket role review at Step 6.** The ticket
skill normally spawns a role review by the diff's actual scope
(`scrumia-ticket` Step 6); `sprint-fast` skips it, and a ticket's PR is
expected to land with no role-signed verdict on its issue. The ticket skill
itself is not modified — it always reads a clean verdict at Step 6 if its scope
requires one. This skill's instruction overrides that for the run by setting
the ticket's effective review policy to "none, the verdict will land on the
sprint PR." The instruction travels with the dispatch, in the deviation slot
`scrumia-sprint` Step 4 already names for other model-or-split refusals:

```bash
scrumia-ticket <n> --review skipped
```

A skill reading this argument runs its diff through the role routing logic and
records the result in the gate-2 trace, but does not spawn the role review;
the trace's `not_run` cause is "sprint-fast review skipped, verdict on sprint
PR". The trace is internal — the issue carries no verdict comment, and the
gate-2 completeness check (`features/business/dev-flow/` AC-18) reads the
sprint PR for the carrier instead.

## Step 6 — Wait for every ticket to merge into the sprint branch

Each ticket's PR targets `sprint/<slug>` per `features/business/dev-flow/`
§ *The sprint branch* and merges on green CI alone. The intermediate state — a
ticket's PR merged into the sprint branch while the sprint is not yet
validated — is read off the PR, not off the board; the card stays `in_review`
until the sprint's own PR lands. That is `scrumia-sprint`'s behaviour, not a
new rule, and is cited rather than restated.

Wait until **every ticket of the batch** is merged. A ticket that failed or
sent back is not "merged into the sprint branch" and stops the global review;
the gather surfaces it instead, and the orchestrator decides whether to retry
or close. The human at gate 3 keeps the merge either way.

## Step 7 — Run the global review

The global review's diff base is `git diff sprint/<slug>...HEAD` after the last
ticket PR is merged, plus any commits the orchestrator added to the sprint
branch itself. The review runs once on the aggregate.

**The reviewers are the union of gate 2's answers over each ticket's own file
set.** Each ticket's file set is still knowable because its PR is merged, not
lost — the routing table in `scrumia-review` applies per ticket and the
reviewers are the union. A single ticket touching a business feature draws the
business role for the whole review; a `scope/S` ticket draws no one.

**The review also reads the aggregate diff for what no per-ticket review
could see.** Two tickets that each pass alone and contradict each other, a
rule changed by one and consumed by another, a style drift visible only across
five diffs — those findings exist only at the aggregate, and the global review
is where they surface. One pass, both readings.

Spawn the role by its agent type. If the type does not resolve, the failure is
silent and a `claude -p --agent scrumia-teams:scrumia-tech --allowedTools
"Read,Glob,Grep,Bash" < review-prompt.txt` subprocess is the fallback; what
that fallback reads is a role review only when the agent runs as the role,
never when a general agent is handed the role's `.md`. The synthesis names
which path ran and which verdict is on the record.

## Step 8 — Apply the findings as `fixup!` commits on fix branches

Findings become `fixup!` commits on **fix branches cut from the sprint branch's
tip**, in fix agents' own worktrees — never on the sprint branch itself. The
sprint branch is rewritten by the orchestrator alone, exactly once, in
Step 9.

```bash
git fetch origin sprint/<slug>
git worktree add .worktrees/fix-<n> -b fix/<n>-<slug> origin/sprint/<slug>
```

A `fixup!` commit carries the **same scope as the commit it corrects** — the
subject of a fixup is autosquashed into its target's, and the scope that lands
in the post-squash history is the target's scope. A fix that widens the scope
is a commit of its own, not a fixup. `docs/adr/0017` §9 states the rule; this
step names the practical consequence for the fix agent.

Multiple findings on the same target commit are stacked as multiple `fixup!`
commits with the same `<sha>` prefix; autosquash folds them in order.

## Step 9 — Verify the preconditions and autosquash

**The autosquash does not start until every ticket worktree of the sprint is
closed and no ticket branch cut from the sprint branch is live.** That is a
precondition to verify, not an assumption: the gather is what answers it. A
force push on the sprint branch while a sibling holds it invalidates every
ticket branch cut from it, which is the work-loss failure `docs/adr/0017` §9
names. The check, before any `git rebase`:

```bash
git worktree list                            # no sprint ticket worktree still open
git for-each-ref --format='%(refname)' refs/heads | grep -E '^refs/heads/(feat|fix|specs|chore)/<n>-'
# empty for every ticket of the sprint
```

The check is explicit because the precondition is the rule — a check that
returns "looks fine" is not the rule being held. If any ticket branch is live,
close the worktree that holds it before proceeding; the failure here stops the
autosquash, and the gather surfaces it.

```bash
git checkout sprint/<slug>
git rebase --autosquash origin/sprint/<slug>
git push --force-with-lease origin sprint/<slug>
```

`--force-with-lease` is the lease, not the rule: the rule is that only the
orchestrator runs this command, and only after Step 9's check. A second run
after a sibling rebased locally is a finding — the lease protects against the
common case, the rule protects against the rest.

## Step 10 — Re-check on the post-squash state

A green CI taken before the squash is not a certification of the state after
it. Re-run:

1. **Gate 1** on the post-squash `sprint/<slug>`.
2. **The global review** on the post-squash diff. Same routing, same
   reviewers, same aggregate read. Findings on the post-squash state that did
   not exist on the pre-squash state are fixed in a second fixup pass —
   the same Step 8 mechanics, bounded again by Step 9's precondition.

The sprint PR opens only when this re-check is clean. A red CI or a new
finding sends the sprint back to Step 8.

## Step 11 — Open the sprint PR

```bash
gh pr create --base <default-branch> --head sprint/<slug> --title "<type>(teams,*): <milestone>: sprint batch" --body "..."
```

The PR body carries **one closing keyword per ticket of the sprint** — `Closes
#<n>` once per ticket, on its own line. None of the ticket PRs carries a
closing keyword; the close is carried by this PR and performed by GitHub on
its merge.

The PR body also carries the role-signed verdict from the post-squash global
review — `Verdict: … — #<sprint-pr> — by scrumia-<role>` — for the human
reading the diff. The verdict is on the PR as a **comment**, posted by the
role's agent at the end of Step 10's re-check, and the body echo is a
courtesy: the comment is the record. Without the comment, the gather reads
`not_run` for every ticket of the sprint; without the body, the human reads
nothing about the verdict.

## Step 12 — Move cards, gather, hand to the human

Each ticket's card moves to `done` when the sprint PR merges, by the same
transition any merged PR triggers. The intermediate state — `in_review` while
the sprint PR is open — is the normal sprint's behaviour and is cited, not
restated.

The gather at the sprint's PR reads one role-signed verdict and reports every
ticket of the sprint as `run` at gate 2; an absent verdict reports every
ticket as `not_run` with the cause "no role-signed comment on the sprint PR".
The dev-flow `AC-18` gate-2 completeness scenario applies to the whole batch
from one read.

Gate 3 stays human on the sprint's PR. `sprint-fast` is not a category that
opens it unattended — `settings.autonomy.auto_merge` does not list it, and
`features/business/dev-flow/` AC-46 says so in the spec. The human at gate 3
decides; the skill stops.

## What this skill does not do

- It does not weaken the normal sprint. `scrumia-sprint` is unchanged in its
  review policy: a per-ticket role review and a per-issue verdict remain its
  path. Anything that copies that prose here is restating a rule
  `features/business/dev-flow/business.md` already states, which is the drift
  the "stated once" form exists to refuse.
- It does not merge unattended. Gate 3 is human on the sprint PR, whatever
  the autonomy level and whatever `auto_merge` lists.
- It does not allow a fix agent to write on the sprint branch. The orchestrator
  rewrites the sprint branch, once, after the gather has verified Step 9's
  preconditions.
- It does not close the ticket on the ticket PR's merge into the sprint
  branch. The close is carried by the sprint PR, once per ticket.

## When a sprint-fast sprint should not have been one

The choice is the orchestrator's, made with the human in Step 3, and it is
recorded on every ticket by the `process/sprint-fast` label. A sprint that
turns out to need per-ticket attention — a single ticket that, mid-run, draws
a `Blocked` finding the orchestrator cannot resolve at the aggregate — sends
that ticket back to refinement, the rest of the sprint continues under the
same mode, and the next sprint runs as a normal sprint unless the human says
otherwise. The label is on every ticket and tells the next reader that the
mode was deliberate, not a mislabelled normal sprint.
