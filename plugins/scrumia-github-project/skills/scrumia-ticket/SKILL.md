---
name: scrumia-ticket
description: Executes a GitHub ticket end to end — isolated branch, spec updates, implementation, tests, review, PR. Use it to handle a specific issue autonomously.
---

# Execute a ticket

A ticket goes in, a PR comes out. The human validates at the end of the chain, not in the middle.

Usage: `/scrumia-github-project:scrumia-ticket 42`

## Preconditions — this skill does not isolate

**This skill does not create a worktree.** It assumes the calling agent already sits
on a working tree checked out to the ticket's branch. Whoever invoked it — the
sprint orchestrator, a sub-agent it dispatched, or a human invoking the skill
directly outside any sprint — is the orchestrator for that call and is the one that
decides whether to isolate and how.

The rule is stated once in [`features/business/dev-flow/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/dev-flow/business.md) §
*Isolation: the orchestrator decides the execution mode, the executor does not
isolate itself*. A second `git worktree add` here would nest the ticket inside
itself; this skill refuses to be that second layer and cites the rule instead.

A relative worktree path the orchestrator used (`.worktrees/<type>/<n>-<slug>`)
resolved against its own cwd — a directory Claude Code may own and tear down at the
end of the session or on a sibling's return. **What carries the run's output is the
branch, not the directory:** commit to the ticket's branch before yielding control
to anyone — a role review, a sub-agent, a human verdict, a wait on a check —
because a branch survives a torn-down tree and uncommitted work in one does not.
That is the commit-before-yield rule applied here; it is not isolation, it is the
durability of whatever isolation the orchestrator chose.

**Invoked directly, outside any sprint.** The skill does not fail obscurely and does
not isolate on its own. If the calling agent is a human invoking the skill directly,
the human is the orchestrator: the working tree they hand the executor is whatever
they chose (the main tree, a manually-created worktree, a fresh clone on a feature
branch — all equivalent here). If the executor finds itself on the wrong branch or
on no branch at all, it stops and comments on the issue rather than silently
creating one.

## Step 0 — Refuse what isn't executable

Read the issue (`gh issue view <n> --json title,body,labels`). Stop immediately if:

- No verifiable acceptance criterion
- The ticket names no feature at all — absent a name, the intent cannot be checked

A ticket whose deliverable is the parent feature itself — the bootstrap case, an
empty `specs_root` on the project's first ticket being the canonical instance — is
not refused: it names the feature, and the acceptance criteria carry the intent. The
refusal fires on a ticket that never said which feature it belongs to, not on one
that names a feature that does not yet exist.

In those cases (no acceptance criterion, or no named feature), comment on the issue
stating precisely what's missing, and point back to the Manager or to
`scrumia-brainstorm`. **Do not guess the intent.** A ticket executed on an assumed
intent produces a PR to throw away, and that costs more than asking for clarification.

Then, if a team module is plugged in, ask what this ticket's size and risk imply. `scrumia-teams` ships the policy as a script it publishes by name on the session's PATH:

```bash
scrumia-pick-model <n>
```

Run the name. This skill holds no path to that module and must not construct one: where it is installed is not knowable from here, which is the whole point of it publishing a name ([ADR-0018](https://github.com/tibs245/scrumia/blob/main/docs/adr/0018-modules-reach-by-name.md)).

**If the name is not found** — a different team module fills the slot, or that module is not enabled — don't hunt for the file and don't reimplement the policy from the labels: execute on the current model and say so in the PR. This skill must not depend on another module's layout.

Do what `instruction` says; don't re-derive it from the labels. Three answers are possible:

- `decision: "model"` — execute here, on the model named.
- `decision: "split_or_model"` — the ticket is oversized. **Try to split it first** (`scrumia-refine` Step 4, or the discovery module). Splitting is the preferred outcome, not a formality. If the work is genuinely indivisible — one migration, one contract that cannot be delivered by halves — execute it on the fallback model and record the refused split as a deviation, below. An oversized ticket is a reason to think again, not a wall.
- `decision: "split"` — return it to refinement; this cell allows no fallback.

If no team module is plugged in, there is no policy to read: execute on the current model and say so in the PR.

### Record a deviation before the work starts

Two things make this run deviate from the policy: **a human overrode the model** — you were told to run on something other than what `scrumia-pick-model` answered — or **you refused the split** a `split_or_<model>` cell preferred. Either one gets one comment on the issue, posted **now**, before Step 2:

```bash
gh issue comment <n> --body-file - <<'EOF'
Deviation: override — cell L/low — policy opus — ran sonnet — by human @<handle>
Reason: <why, in the words of whoever decided it>
EOF
```

Use the heredoc, not `--body '…'`: a reason is English prose and the first apostrophe in it ends the quote and breaks the command.

- `<kind>` is `override` or `split_refused`. An **override is a human's decision by definition** — if nobody chose it, you have not overridden the policy, you have failed to follow it. Do not file that as an override.
- `cell` is the scope and risk `scrumia-pick-model` read back, in the axes' own vocabulary (`L/low`), not the project's label spelling. Where it reports `scope_rated: false`, write `unlabeled/<risk>`.
- `policy` is what it answered, verbatim — a model name, `split_or_<model>`, or `split`.
- `ran` is the model you are actually executing on.
- `by` is `human` and the handle whose decision it was for an override; for a refused split it is you — name this skill.
- **`Reason:` is mandatory.** A deviation with no reason cannot be reviewed and cannot be told apart from a mistake; a record missing it is non-compliant, not a note to complete later.

Now, not at PR time: the record has to survive a run that dies before opening one. The PR echoes it in Step 7 for a human reading the diff, and the echo is a copy — this comment is the record. Prose in five PR bodies is exactly what this replaces.

**If the comment cannot be posted, stop** — same discipline as any other failing `gh` call in this step, and for a sharper reason: a deviation that runs unrecorded is the exact failure this record exists to end, and it is invisible afterwards. Report it and let the human decide.

This record is written and never read back. It is evidence for editing the grid in `.scrumia/config.yaml`, not a precedent that changes what a cell answers today — the policy's answer stays the only way a model is chosen.

**If `gh` fails** — not authenticated: say so and point to `gh auth login`; the human runs it, this skill doesn't. Network or API error: retry once, then report and stop, don't loop on a flaky call. No repo or no remote: name the missing prerequisite (`.git`, a GitHub remote) and stop. This is the ticket's first `gh` call — stop here, before touching the board: nothing half-started is easier to clean up than a stray branch and a stuck card.

## Step 1 — Load the context, not the repo

Read `CLAUDE.md`'s `## Specs contract` section first — it names the specs module's own vocabulary (`specs_root`, `feature_index`, `acceptance_file`, `ac_id_format`, `changelog`, `catalog`), written there by `scrumia-init` from that module's own `## Composition block` (`docs/adr/0012-specs-contract.md`). Never assume `scrumia-specs`'s file names directly: a different module can occupy the `specs` slot with a different layout, and this step must keep working unchanged.

**If the section is absent** — no specs module documented, or `scrumia-init` not yet run — say so: *"no specs module documented — ask the human or proceed without spec updates"*, and go straight to the code neighboring the area to modify. Degraded, not blocked.

Otherwise, read, in this order, and stop as soon as you know enough:

1. The parent feature's file named by `feature_index` — it says which files exist and why
2. The file named by `acceptance_file` — the criteria you must satisfy, identified in `ac_id_format`
3. Whichever other files listed under `catalog` the index marks relevant — a rule, an interface, or a technical choice the ticket touches
4. The code neighboring the area to modify

Do not load all of the directory named by `specs_root`. The format exists so you don't have to.

## Step 2 — Confirm the branch and move the card

The branch and the worktree are the calling agent's responsibility (see *Preconditions*
above) — this skill neither creates them nor cleans them up. Confirm the executor sits
on the ticket's branch before touching anything else:

```bash
git rev-parse --abbrev-ref HEAD
```

If the branch is wrong, or there is no branch, **stop and comment on the issue**: a ticket
that finds itself on the wrong branch has been handed an inconsistent invocation, and
isolating here would be the drift the precondition refuses. The comment names what the
calling agent was supposed to provide so the next reader can fix the call rather than
guessing one.

The branch naming follows the project's commit-type vocabulary from
[`docs/adr/0017-version-bump-and-commit-signal.md`](https://github.com/tibs245/scrumia/blob/main/docs/adr/0017-version-bump-and-commit-signal.md) § *The type vocabulary* —
`<type>/<n>-<slug>` — but writing that branch is the orchestrator's job, not this skill's.

Once the branch is right, move the card to the `in_progress` step:

```bash
scrumia-board move <n> in_progress
```

The flow step maps to this board's actual column name through the config ([`projects-v2.md`](${CLAUDE_SKILL_DIR}/../scrumia-status/references/projects-v2.md)). If the move fails, continue anyway and say so in the final report: a dead column is not a blocked ticket.

## Commit before you yield

From here on, what carries this run's output is the ticket's branch the calling agent put
the executor on — not the working tree the orchestrator may later tear down. The branch
survives a torn-down tree; uncommitted work in one does not. So commit to the ticket's
branch before the run hands control to anyone else:

```bash
git add -A && git commit -m "<type>(<scope>): <what changed>

Refs: #<n>"
```

The scope is not optional, and the `Refs:` trailer goes on **every** commit of the branch — a lookup returning some of a ticket's commits reads exactly like one returning all of them. `<scope>` names what the commit changes: a module (its plugin name with the vendor prefix dropped), an app (from `apps[]` in `.scrumia/config.yaml`), a feature (the directory holding its `index.md` under the specs root), or the literal `repo` for what belongs to none of the three. **A change atomic across several of them names them all, comma-separated** — this generalizes past ADR-0017 §2's original module-only form and its closing "nothing else carries two tokens," which the ADR is not re-edited to say but no longer governs on this point (`features/business/dev-flow/business.md` § *What a commit carries*). Only the module tokens named still bump, at that level and no other; naming an app, a feature or `repo` alongside one buys it nothing, and none of them may hide a module — every module a commit changes is still named individually. Once a commit spans more scopes than are worth naming individually — typically past three — `<type>(*):` covers the rest without listing them; `*` derives no bump on its own and never stands in for a module, so a module that must bump is still named alongside it (`refactor(specs,*):`). Why the scope is mandatory, and what each token buys, are in [`features/business/dev-flow/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/dev-flow/business.md) § *What a commit carries* and [ADR-0017](https://github.com/tibs245/scrumia/blob/main/docs/adr/0017-version-bump-and-commit-signal.md) § *The signal*.

**If the project documents no such convention**, keep the shape but read the alphabet off its own history rather than importing this one: this paragraph describes ScrumIA's, and a consuming project may spell its scopes differently.

The rule, and what counts as yielding control, are stated once in [`features/business/dev-flow/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/dev-flow/business.md) § *Who decides, on each path* → **Execution**. Read it there rather than inferring it from this skill: it is written as the general case, so it covers yields the steps below do not name — including ones added to this skill after this sentence.

This sits before Step 3 because Step 2 is where the branch starts existing and Step 3 can already yield. The steps that name it — 3, 5, 6, and *When you're blocked* — are where it bites in practice, not the extent of it.

## Step 3 — Update the spec first

Skip this step in the degraded case from Step 1: no specs module documented, no spec to update — go straight to Step 4.

Otherwise, if the ticket changes a behavior, the spec changes **before** the code — not after:

- Consult the feature's `feature_index` file for which of its `catalog` files covers what changed — its "why this file exists" listing is what points you there without this skill assuming a fixed name. On the producer side if it's an interface contract.
- **Before writing a word into that file, load the specs module's own authoring rules** — not just which file to open, but how it wants that file written. For `scrumia-feature`, that's the skill of that name — invoke it, or read the `SKILL.md` the harness resolves for it; this skill holds no path into another module ([ADR-0018](https://github.com/tibs245/scrumia/blob/main/docs/adr/0018-modules-reach-by-name.md)) — §§ *Never put history in a spec* and *`business.md`'s boundary*: the must/must-not checklist that keeps a spec stating current truth rather than narrating how it got there. A different specs module without a documented authoring checklist degrades to "no authoring checklist documented — proceed on judgment" rather than silently skipping this bullet.
- Update that file, and the file named by `acceptance_file` if the criteria themselves move.
- In every case, add an entry to the file named by `changelog`, with the issue number.

Writing the spec first surfaces contradictions before they get encoded in code. That's where the cost is lowest.

**If the ticket also changes a shipped module**, that module's own changelog gets a line under its `[Unreleased]` heading — one line per change, in the words of someone deciding whether to take it, never the commit subject. A module whose entries are written only at release time is a module whose entries are reconstructed from the log, which is the practice the format refuses. This is a different file from the spec changelog above and answers to a different reader; if the composition ships no module of its own, there is nothing to do here.

If while writing the spec you discover a contradiction with another feature: stop, commit the spec changes you have — calling the role is a yield, and it is your spec edits that expose the contradiction — then comment on the issue and call on the business role. Do not decide a business rule yourself.

## Step 4 — Implement according to the app's module

**Before writing code, ask what governs the file you're about to touch.** Do not work it out from `.scrumia/config.yaml`, and do not recall it from another skill's prose:

```bash
scrumia-extends implement --path <the file you are about to edit>
```

It prints every directive the modules this project runs contribute to `implement`, for that file's app: name, type, whether it is `required`, one line of what it says, and the file to open. **Open every `required` row before writing code.** `optional` rows are offered — take the ones the change calls for.

An empty table is an answer, not a gap: no module the project runs speaks for that file, so the conventions of the neighbouring code apply.

The order the table prints is the precedence: this project's own `.scrumia/extends.json` first, then the modules the app extends, then the project-wide ones — *specific beats generic, and a project override beats both*. What the table does **not** do is arbitrate: two rows whose prose contradicts each other are both printed, and a genuine conflict is a composition problem to escalate, not a judgment call to make silently. Inside a module, that module's own routing table and `section.json` globs still decide what else to open.

Whether an implementation module is plugged in or not: if a specs module is documented, cover each criterion in `ac_id_format` from the file named by `acceptance_file` with a test that can fail; in every case, run the project's tests and linter.

Stay within the ticket's scope. What you notice in passing that exceeds it becomes an issue, not an extra line of diff. A PR that overflows is hard to validate — and human validation is the system's bottleneck.

## Step 5 — Self-review

Reread your own diff before proposing it. Look for: an uncovered `AC`, an ignored error case, a contract modified without its file, dead code, a secret, an out-of-scope file.

Fix what you find. What you can't fix here becomes an explicit note in the PR.

Commit those fixes before going further, per *Commit before you yield* above.

## Step 6 — Agent review according to the diff

**Do not spawn a role while the working tree is dirty** — spawning one is a yield, per *Commit before you yield* above. Check it:

```bash
git status --porcelain   # must print nothing before a role is spawned
```

`git diff <base>...HEAD` below reads committed history, so a role routed off it reviews the branch and nothing else.

If a team module is plugged in, route the review by what your diff actually touches. List it first — `git diff <base>...HEAD --name-only` from the worktree — then apply gate 2's table ([`docs/adr/0005-validation-gates.md`](https://github.com/tibs245/scrumia/blob/main/docs/adr/0005-validation-gates.md)), in the specs module's own vocabulary from Step 1:

| What the diff touches | Required review |
|---|---|
| 1 app, no spec | your Step 5 self-review, already done |
| Code, an App spec | the tech role |
| A business feature under `specs_root`, or a `catalog` legal/compliance file | the tech role + the business role |
| ≥2 apps, or an interface-contract file from `catalog` | the tech role, + the business role if business is at stake |

This is the same table `scrumia-review` applies at gate 2, deliberately: the two must never disagree about who owed this PR a review.

**Do not gate this on the `scope/*` label.** The label says which review to *expect*, and comparing the two is worth a line in the PR — but a wrong label is precisely the failure a review exists to catch, so it cannot be what decides whether the review runs. Where the diff's row asks for more than the label implied, and **only when the axis's own questions would have answered higher**, report that gap as a scoping signal — the questions and the reach-not-medium reading are in [`rules/gate-2-scoping-signal.md`](../../rules/gate-2-scoping-signal.md). The label reads a rule's reach; the exit grid reads the diff's paths. They disagree routinely and correctly — a specs-only diff whose rule nothing beyond its feature consumes is a correct `scope/M` that still draws a business reviewer — and calling that a mislabel fires on a whole class of correctly-labelled ticket.

**Where the signal is owed, comment it on the issue now, addressed to the manager** — the role that set the label and routes on it. Name the label the ticket carries, what the diff's row asked for, and which of the axis's questions would have answered higher:

```bash
gh issue comment <issue> --body "Scoping signal: label <label> — review routed <roles> — axis question <1|2|3> answers yes on <what>"
```

Now, not at PR time, and on the issue rather than in the PR body: the retrospective's trigger counts these gaps and a run that dies before `gh pr create` must still leave one behind — the same reason Step 0's deviation record lives there. Step 7 echoes it in the PR for a human reading the diff, and that echo is a copy.

**Apply the same role-consultation rule as refinement.** The condition is in [`rules/when-a-role-must-be-consulted.md`](../../rules/when-a-role-must-be-consulted.md). If the refinement recorded an answer on the ticket that still conditions the change, the execution references it rather than re-asking (AC-19). If the ticket's blocker is a question the execution meets first, the execution consults and records on the ticket — same condition, same reporting.

The table has no scope tier in it, `scope/XL` included: ADR-0015 sends an `XL` ticket back to scoping rather than into execution, and where Step 0's split was refused as genuinely indivisible so it executed anyway on the fallback model (`features/business/execution-policy/`), its diff routes its review like every other diff's. No tier is left without a stated review, because no tier states one.

Spawn the role by its agent type — `scrumia-teams:scrumia-tech`, `scrumia-teams:scrumia-business`. If the type does not resolve, the module that ships it was installed or updated without a restart since; say so rather than reviewing anyway, and fall back to a subprocess, prompt on stdin:

```bash
claude -p --agent scrumia-teams:scrumia-tech \
  --allowedTools "Read,Glob,Grep,Bash" < review-prompt.txt
```

Both run the actual role. [The roles' doc](https://github.com/tibs245/scrumia/blob/main/docs/agents.md) carries the restart rule and why the failure is silent.

A **Blocked** review gets fixed before opening the PR — and the fix is committed before the role is asked again, which is another yield. An **Approved with reservations** review goes out as is, with the reservations carried into the PR description and turned into issues.

**The role posts its own verdict.** The executor is the convener of the review, not its author — "the author reviews their own work" was never the defect, and the fix is not to make the executor write one. At the end of the role review, the role's agent writes its verdict on the ticket's issue, in a fixed format a later reader can find:

```
Verdict: Approved | Reservations | Blocked — #<n> — by scrumia-<role>
```

The executor does not write the verdict on the role's behalf — the role's name is the attribution, and the substitution path a structured field written by the executor's return would reopen is the one the attribution clause closes. The pull-request body echoes the verdict for a human reading the diff, but the echo is a courtesy: the record is on the issue, where a run that dies between review and PR still leaves it behind. The vocabulary and the attribution are in [`rules/role-verdict-format.md`](../../rules/role-verdict-format.md); the venue and the read-back are in [`rules/role-verdict-venue.md`](../../rules/role-verdict-venue.md). This step states only that the role posts it and the executor does not.

**If the role's agent type does not resolve**, the verdict is `not_run` with cause "agent type did not resolve" — and the PR body says the review did not run as that role. A general agent handed the role's `.md` file is not that role, and the difference is measured (`features/business/agent-team/` AC-10); a fallback that reads as the real thing is worse than a fallback that names itself.

Without a team module plugged in, your self-review from step 5 is the only review before the human. Say so explicitly in the PR: the reviewer must know what was checked and by whom.

The same holds when the role itself could not be reached. Handing your own general agent the role's `.md` file is not that role, and the difference is measured: on one sprint's five PRs, self-applied reviews returned five approvals and two reservations where the actual roles returned one blocker and nine. Report which one ran. A fallback that reads as the real thing is worse than a fallback that names itself.

## Step 7 — Open the PR

```bash
gh pr create --title "<type>(<scope>): <expected outcome>" --body "..."
```

Same `<type>` vocabulary as the branch and the commits, same mandatory scope.

The description contains: what was done, `Closes #<n>` **exactly once** — the PR body is where the close lives, and GitHub performs it; no step of this skill closes an issue, and the commits' `Refs:` trailers close nothing — the criterion-by-criterion mapping (each acceptance identifier in `ac_id_format` → its test, if a specs module is documented), the specs modified, the verdict of the agent reviews — echoing the label/diff gap Step 6 recorded, where there was one, the comment on the issue being the record and this its copy — and the open reservations with their issues.

**The description names the roles consulted during execution, their answers, and where the answer is recorded — or states that no role was needed and which condition did not apply.** A review that ran as a fallback because the agent type did not resolve is named as such, never reported as the role itself (AC-20).

If Step 0 recorded a deviation, echo it here — kind, cell, what the policy chose, what ran, why — for a human reading the diff. The echo, not the record: the comment on the issue is what a later reader queries, and the PR body is a copy of it.

Then comment on the issue with the PR link, and move the card to the `in_review` step:

```bash
scrumia-board move <n> in_review
```

If the move fails, continue anyway and say so in the final report: a dead column is not a blocked ticket.

## Step 8 — Stop

**You do not merge.** Final validation belongs to the human, except for a category explicitly listed in `autonomy.auto_merge` of `.scrumia/config.yaml` — and even then, CI must be green.

**You do not clean up the worktree.** The worktree is the calling agent's — the orchestrator
created it (or chose not to) and the orchestrator owns its lifecycle. This skill's contract
ends at the PR; the directory stays where it was until whoever handed the executor the
branch decides otherwise. Saying that here, again, because a reader following Step 8 looking
for `git worktree remove` would otherwise infer that the executor is the one to run it.

## When you're blocked

Commit what you have first: stopping hands the next move to a human, and a branch left in place with an uncommitted tree carries nothing. Then comment on the issue with: what you tried, what's blocking, and the options you see. Leave the branch in place. Do not open a half-done PR — an incomplete PR costs more to review than a clear comment.
