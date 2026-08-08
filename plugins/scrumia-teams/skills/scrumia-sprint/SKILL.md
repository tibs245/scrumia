---
name: scrumia-sprint
description: Prepares a sprint with the team then consumes it as dynamic workflows, one isolated worktree per ticket. Use it to launch a batch of tickets ready for development.
---

# Preparing and consuming a sprint

A sprint is a batch of tickets that can move forward **in parallel without stepping on each other**. Selection matters more than launching.

## Step 1 — Build the batch

Take the tickets ready for development from the tracker module: acceptance criteria written, scope set, dependencies resolved. When the tracker is `scrumia-github-project`:

```bash
${CLAUDE_SKILL_DIR}/../../../scrumia-github-project/scripts/board.sh ready --milestone "<sprint>"
```

A milestone is the sprint's boundary. Without it you are reading the whole ready column and calling it a sprint. Check `filter_suspect` in the answer before concluding a milestone is empty — an unknown milestone name and an empty one look identical.

Another tracker module fills the slot differently, and that path may not resolve at all: ask it for what's ready in its own terms rather than assuming this one's layout.

Then discard the conflicts. Two tickets touching the same files get serialized or merged; they don't go out together. The most reliable signal is the scope declared in the ticket; failing that, two tickets on the same app feature almost always overlap.

Then ask the execution policy about each surviving ticket:

```bash
${CLAUDE_SKILL_DIR}/../../scripts/pick-model.sh <n>
```

A ticket answering `split_or_model` doesn't enter the sprint as-is: try to split it first, and only carry it in on its fallback model if the work proves indivisible. A ticket answering `split` goes back to refinement. Keep each ticket's returned model — Step 3 needs it.

`settings.team.sprint.max_tickets` caps the batch — 5 by default. It's not a technical limit: beyond that, human review saturates and parallelism stops paying off.

## Step 2 — Get the batch validated

Present the batch before launching: number, title, scope, risk, the model each will run on, apps touched, and the reason for excluding the discarded tickets. Showing the model matters — it is where an unrated risk becomes visible as a cost, and where the human can object before anything runs.

**Launching is a human decision.** Don't infer it from an agreement given to something else.

## Step 3 — Consume the sprint

One dynamic workflow per ticket, in parallel, each with `isolation: worktree`. Each worktree lands at `.worktrees/<branch>` inside the project directory, never `../<repo>-<n>` — same convention as `scrumia-ticket` Step 2: Claude Code's permissions are scoped to the project directory, and a path outside it triggers extra prompts or fails outright in restricted modes.

Give each execution the ticket number and the model `pick-model.sh` returned for it in Step 1 — nothing else. It loads its own context via the plugged-in modules; passing it your summary of the ticket would add a distortion.

The model is per ticket, not per sprint. A batch of five routinely runs on three different models, and that is the point: a `scope/S risk/critical` ticket gets the strong model while a `scope/M risk/low` one next to it does not.

Each execution follows the same outline:

1. Load the context via the specs module
2. Update the spec if the behavior changes — before the code
3. Implement per the implementation module of the app concerned
4. Cover each acceptance criterion with a test
5. Self-review, then review by the roles according to scope
6. Open the PR

The modules carrying these steps are those declared in `CLAUDE.md`. If a slot is empty, the corresponding step is simplified, not silently skipped: say so in the PR.

## Step 4 — Gather

For each ticket: PR opened, blocked and why, or sent back to refinement and what was missing.

Flag what needs human attention: review reservations, business contradictions raised, tickets sent back.

Merge nothing. Don't automatically relaunch a ticket that failed — a failure has a cause, and relaunching it unchanged reproduces it.

## Preparing the next sprint during execution

This can't be automated within one session: a subagent can't spawn others, and agent teams are experimental with a single team per session.

In practice, two Claude Code sessions on the same repo give the same result — one consumes the current sprint, the other refines the next one with the manager. Since the living state is in the tracker module and not in session memory, the two stay consistent without coordinating.

It's a constraint of the current tooling, not a design choice. See `docs/adr/0002-standing-roles.md`.
