---
name: scrumia-standup
description: Convenes the project's standing roles so they can be asked something — reads the composition, brings up the enabled roles, reports what each owns. Use it when someone asks to start the team, to take stock, or to route a question to a role. It launches no sprint.
---

# Convening the team

Someone asked for the team. Give them the team — not a sprint. Executing tickets is `scrumia-sprint`, and starting one here is the failure this skill exists to prevent.

## Step 1 — Read who is on it

`settings.team.roles` in `.scrumia/config.yaml` lists the roles and which are `enabled`. Only enabled roles get convened; a disabled one is a capability the project decided not to have, and you say so rather than routing to it anyway.

An entry carrying `from:` belongs to another module — `scrumia-design` ships `designer` this way. Convene it like the others, and read its definition from that module.

**Check that each role's module is actually installed**, not merely declared:

```bash
claude plugin list
```

A role declared `enabled: true` whose module is absent is the worst of the three states: the composition says the reviewer exists, and nothing reaches it. Report the gap and name the install command — don't quietly convene two roles out of four.

## Step 2 — Bring them up

The roles are not processes waiting to be attached to. Each convocation is a fresh one that rebuilds its context from the tracker, which is exactly why two sessions stay consistent without coordinating.

Convene each enabled role as a subprocess, prompt on stdin:

```bash
claude -p --agent scrumia-teams:scrumia-manager \
  --allowedTools "Read,Glob,Grep,Bash" < prompt-manager.txt
```

`--allowedTools` is variadic: it swallows a positional prompt, so pass the prompt on stdin. The Agent tool does not resolve these agent types from a standard session — [the roles' doc](../../../../docs/agents.md) records what was measured and what is still open.

Convene them in parallel; they don't talk to each other, and a role that waits on another produces the averaged synthesis this team is built to avoid.

Tell each one the same three things: it is being convened, nothing is to be executed, and it must not write — no file, no commit, no `board.sh move`. Then ask for what that role owns and nothing else. Give the manager its startup sequence (config, slots, memory, board); ask the others for their read of the current state through their own lens.

Pass on the facts already established in the session so they don't re-derive them, and only those you actually verified.

## Step 3 — Report

Per role: what it owns here, its read of the current state, and what it refuses to rule on with where that goes instead.

Then the decisions waiting on the human, which is the point of convening at all.

**Where two roles disagree, hand both positions over unchanged.** A disagreement between roles is the most useful thing this team produces; averaging it destroys it. Add your recommendation after, marked as yours.

Report any drift between what the composition declares and what you found — a role enabled but not installed, a slot filled by an absent module, a contract naming a file that isn't there.

## What this skill does not do

It does not launch a sprint, move a card, or refine a ticket. It brings the roles up and hands the floor to the human.

If what was actually wanted is a batch of tickets executed, that's `scrumia-sprint` — and launching it stays a human decision, taken with the batch in front of them.

## On "standing"

The word means persistent memory and externalised state, not a live process. A role remembers across sessions through `memory: project` and rebuilds everything else from the tracker. Nothing keeps running between two convocations, and nothing needs to — see [ADR-0002](../../../../docs/adr/0002-standing-roles.md).
