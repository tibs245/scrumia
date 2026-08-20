---
name: scrumia-sprint
description: Prepares a sprint with the team then consumes it as dynamic workflows, one isolated worktree per ticket. Use it to launch a batch of tickets ready for development.
---

# Preparing and consuming a sprint

A sprint is a batch of tickets that can move forward **in parallel without stepping on each other**. Selection matters more than launching.

## Step 1 — Build the batch

Take the tickets ready for development from the tracker module: acceptance criteria written, scope set, dependencies resolved. When the tracker is `scrumia-github-project`:

```bash
scrumia-board ready --milestone "<sprint>"
```

A milestone is the sprint's boundary. Without it you are reading the whole ready column and calling it a sprint. Check `filter_suspect` in the answer before concluding a milestone is empty — an unknown milestone name and an empty one look identical.

`scrumia-board` is the name that module publishes on the session's PATH; this skill holds no path to it and must not construct one, because where that module is installed is not knowable from here. Another tracker module fills the slot differently, and the name will not be found at all: ask it for what's ready in its own terms rather than assuming this one's layout. A name that is not found is a slot answered differently, never a cue to read the board by hand — an unfiltered `gh project` read is silently truncated at 30 items.

Then discard the conflicts. Two tickets touching the same files get serialized or merged; they don't go out together. The most reliable signal is the scope declared in the ticket; failing that, two tickets on the same app feature almost always overlap.

Then ask the execution policy about each surviving ticket:

```bash
scrumia-pick-model <n>
```

A ticket answering `split_or_model` doesn't enter the sprint as-is: try to split it first, and only carry it in on its fallback model if the work proves indivisible. A refusal decided here is a **deviation**: keep the reason the work could not be divided, and pass it to the execution in Step 4 so it lands on the ticket's own record. A ticket answering `split` goes back to refinement. Keep each ticket's returned model — Step 4 needs it.

`settings.team.sprint.max_tickets` caps the batch — 5 by default. It's not a technical limit: beyond that, human review saturates and parallelism stops paying off.

## Step 2 — Load what this project batches against

```bash
scrumia-extends sprint
```

A module the project runs may constrain what may share a sprint — a migration that must
run alone, a contract change that blocks everything consuming it. It arrives here from the
module that owns the rule, rather than being remembered. An empty table means the conflict
matrix above is the whole constraint.

## Step 3 — Get the batch validated

Present the batch before launching: number, title, scope, risk, the model each will run on, apps touched, and the reason for excluding the discarded tickets. Showing the model matters — it is where an unrated risk becomes visible as a cost, and where the human can object before anything runs.

**A human objecting to a model is an override**, and this is the only moment its reason exists. Keep it in the batch, in the human's own words, against the ticket it applies to — Step 4 hands it to the execution, which is what records it. Don't record it yourself here: a deviation is a property of a run, and the batch you are presenting may not launch. Reconstructed a day later the reason is a guess, and a deviation whose reason is a guess is worth nothing to the reader it was recorded for.

**Launching is a human decision.** Don't infer it from an agreement given to something else.

## Step 4 — Consume the sprint

One dynamic workflow per ticket, in parallel, each with `isolation: worktree`. This
skill — the sprint orchestrator — is the one and only layer that creates the worktree
for that ticket. The execution skill (`scrumia-github-project:scrumia-ticket`) cites
the rule from [`features/business/dev-flow/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/dev-flow/business.md) § *Isolation: the
orchestrator decides the execution mode, the executor does not isolate itself* and
neither calls `git worktree add` nor cleans up afterwards: a second layer doing so is
the drift the rule exists to refuse.

Each worktree path is `.worktrees/<branch>` — **resolved against the orchestrator's own
cwd**, never as an absolute path. Claude Code's project-scoped permissions and
harness-owned working trees mean that cwd is a directory the harness may tear down on
session end or on a sibling's return; what carries an execution's output is the branch,
not the directory, so an executor that commits before any yield is durable across that.
The convention that puts `.worktrees/` inside the project directory (not `../<repo>-<n>`)
is a permission-scope choice: a worktree outside the project triggers extra prompts or
fails outright in restricted modes. Both rules apply to whatever cwd this skill runs in.

Create one worktree per ticket:

```bash
git worktree add .worktrees/<branch> -b <branch>
```

The branch name follows the project's commit-type vocabulary from
[`docs/adr/0017-version-bump-and-commit-signal.md`](https://github.com/tibs245/scrumia/blob/main/docs/adr/0017-version-bump-and-commit-signal.md) § *The type vocabulary*
— `<type>/<n>-<slug>`.

If the command fails with a `.lock: File exists` error, a sibling holds it briefly:
retry, up to three times, a few seconds apart. If it still fails after that, the lock is
stale — its owner died holding it. Report the lock file's path and stop; never delete a
lock file in a shared `.git` yourself: four siblings may be live inside it.

The number of siblings is `sprint.max_tickets`, a human-review cap — git is not the
limiting factor. Raising it is a review-bandwidth decision, never a git one.

When the worktree is in place, dispatch the execution in it. Give each execution the
ticket number and the model it runs on — nothing else. It loads its own context via the
plugged-in modules; passing it your summary of the ticket would add a distortion.

The one exception is a **deviation**: where the model you pass is not the one `scrumia-pick-model` answered — a human overrode it in Step 3, or Step 1 refused a split — say so, and pass the reason with it. It cannot reconstruct a reason it was never told, and a model handed over with no explanation reads exactly like a policy answer. Tell it not to re-derive the choice either: the decision was made here.

Recording it is the tracker module's business, not this one's: `scrumia-github-project` writes it on the issue at its ticket flow's Step 0. Another module fills the slot differently — pass it the deviation all the same, and if it turns out to record nothing, that is a gap to report rather than a reason to keep the reason to yourself.

The model is per ticket, not per sprint. A batch of five routinely runs on three different models, and that is the point: a `scope/S risk/critical` ticket gets the strong model while a `scope/M risk/low` one next to it does not.

Each execution follows the same outline:

1. Load the context via the specs module
2. Update the spec if the behavior changes — before the code
3. Implement per the implementation module of the app concerned
4. Cover each acceptance criterion with a test
5. Self-review, then review by the roles according to scope
6. Open the PR

The modules carrying these steps are the ones the project's `extends` names. Where nothing covers a step, it is simplified, not silently skipped: say so in the PR.

Step 5's role review spawns the role by its agent type — the execution is itself a subagent spawned by the orchestrator, so the orchestrator (the session that runs the sprint) is the agent that may spawn subagents. If the type does not resolve, the module was installed or updated without a restart since ([`rules/agent-restart-after-install.md`](../../rules/agent-restart-after-install.md)); fall back to a subprocess, prompt on stdin:

```bash
claude -p --agent scrumia-teams:scrumia-business \
  --allowedTools "Read,Glob,Grep,Bash" < review-prompt.txt
```

If a role cannot be reached either way, the PR says the review did not run as that role. It never substitutes a general agent for it in silence.

## Step 5 — Gather

For each ticket, in this order, the gather reads the ticket's issue and the rules
named by `features/business/dev-flow/`:

1. **The verdict.** Read the ticket's issue comments for a `Verdict: … by scrumia-*`
   token, attributable to a role. The role's verdict is the record; the executor's
   report is not. The verdict is one of three states:
   - `run` — the role review ran as the role, with a verdict attached (`Approved`,
     `Reservations`, `Blocked`).
   - `not_required` — the ticket's scope is `scope/S`. This is derived from the
     scope label, not asserted by the executor — an executor that declares
     `not_required` on a `scope/M` or `scope/L` produces a non-compliant record.
   - `not_run` — a required review did not run as its role. **Cause is mandatory**:
     `skipped`, `unreachable`, `agent type did not resolve`, `self-applied`,
     whatever the case is. A `not_run` without a cause is non-compliant.
2. **The PR opened, blocked, or sent back to refinement.** The PR exists, or it does
   not — and the verdict is the role's, not the executor's word for it. A **Blocked**
   verdict lands on an open PR: the PR stays open, the card returns to `in_progress`,
   and the gather flags the ticket. Gate 3 keeps the merge regardless.
3. **The net.** If the ticket's issue carries no role-signed verdict at gate 3, the
   orchestrator runs the role review on that absence — a checkable fact, not a
   declaration by the executor. The net is the immune system to the executor's
   report failing twice.

The gather's report carries, per ticket: the verdict state, the role (or `not_required`),
and the cause for `not_run` — never silence. A ticket whose verdict is absent is
reported as `not_run` with cause "no role-signed comment on the issue", so the
absence is named and the substitution path is closed.

Flag what needs human attention: any `not_run` outcome, review reservations, business
contradictions raised, tickets sent back, and any ticket that deviated from the
policy's answer.

A deviation reported here is a **second copy for the human in front of you**, not the record — the record is on the ticket, written when the deviation was decided, and it is the copy that survives this session.

Merge nothing. Don't automatically relaunch a ticket that failed — a failure has a cause, and relaunching it unchanged reproduces it.

## Preparing the next sprint during execution

This can't be automated within one session: a subagent can't spawn others, and agent teams are experimental with a single team per session.

In practice, two Claude Code sessions on the same repo give the same result — one consumes the current sprint, the other refines the next one with the manager. Since the living state is in the tracker module and not in session memory, the two stay consistent without coordinating.

It's a constraint of the current tooling, not a design choice. See `docs/adr/0002-standing-roles.md`.
