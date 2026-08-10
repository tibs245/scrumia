# The end-to-end flow

Here is the flow as it runs with the reference composition. Another composition produces another flow — that is the point.

Each step names the module that carries it. An empty slot simplifies the corresponding step; it does not make it disappear silently.

## Overview

```
Human     │ brief, challenge, brainstorming
          ▼
discovery │ scoping → issues + branch carrying the specs
          ▼
tracker   │ refinement → Ready for dev, or sub-issues per context
   ↕      │   ↳ calls on the roles when their answer changes the ticket
team      │
          ▼
Human     │ validates dubious, critical or risky designs
          ▼
team      │ the manager prepares the sprint with the team → To dev
          ▼
team      │ dynamic workflows: implementation, review, QA
   ↕      │   ↳ implementation per the app's module
impl      │
          ▼
Human     │ PR review, test → Done
```

## 1. The human poses a brief

An idea, a problem, a hunch. Nothing formatted is required.

Scoping challenges: does the problem exist? does this solution solve it? what becomes impossible? where are the edge cases? what is assumed without being said? where is the legal side?

This is the only moment where the human's extended presence is justified — and where it costs the least, an error caught here being worth a hundred fixes later.

> **Module** — `scrumia-discovery`, skill `scrumia-brainstorm`. Without this module, the human does the scoping and creates the tickets by hand.

**Scoping is done when** the problem and the expected outcome fit in three accepted lines, at least one verifiable acceptance criterion exists, and the remaining open questions are named without being blocking. Not when everyone is tired: if it drags, the scope is too broad — scope only the first slice.

## 2. Scoping produces issues and a specs branch

Business features first, then app features — one per app, never two. Then the issues.

The specs go out on a `specs/<slug>` branch, in a PR left open. The human reviews the design in the same tool as the code, and the refinement that follows starts from something frozen rather than from the memory of a discussion.

`specs` here is a type of the project's commit vocabulary, not a prefix of its own: the same list names branches, types commits and titles PRs, and it is defined once in [ADR-0017](adr/0017-version-bump-and-commit-signal.md) § *The type vocabulary*. A `specs`-typed commit moves no module's version, because a feature carries none.

> **Modules** — `scrumia-discovery` (skill `scrumia-split`) for the splitting, `scrumia-specs` for the format, `scrumia-github-project` for the issues.

## 3. Refinement makes the ticket executable

A backlog ticket carries an intent. Refinement makes it executable, or reveals that it needs splitting.

Four conditions, all verifiable:

1. A feature to attach to exists and is up to date
2. The acceptance criteria are written, identified `AC-n`, and can fail
3. The scope is known: which apps, which anticipated files
4. No open question blocks the start

The roles with the global view are called on **when their answer changes the ticket** — not to cover the decision. The ticket can be split into sub-issues per context: one per app, because the implementation context differs.

> **Modules** — `scrumia-github-project` (skill `scrumia-refine`), which calls on `scrumia-teams` if plugged in. Without a team module, the questions go to the human.

## 4. The human validates the designs that deserve it

Escalated to the human:

- A business rule had to be invented to move forward
- The splitting changes the scope of what was asked
- The ticket is `scope/L`, or touches a contract consumed by other apps
- A role gave an opinion with reservations

Everything else goes straight to `Ready for dev`. The configured autonomy level widens or narrows this boundary: in `guided`, the human validates every transition.

## 5. The manager prepares the sprint

A sprint is a batch of tickets **that do not conflict**. The selection matters more than the launch: two tickets on the same files get serialized or merged.

The manager builds the batch with the team, according to the priorities. The human validates the batch — it is an explicit decision, never inferred from an agreement given to something else.

> **Module** — `scrumia-teams`, skill `scrumia-sprint`. By default 5 tickets maximum: beyond that, human review saturates and parallelism stops paying off.

## 6. The dynamic workflows consume the sprint

One workflow per ticket, in parallel, each in an isolated worktree. Each run receives a ticket number and nothing else: it loads its context itself.

The outline:

1. Load the context via the specs module
2. **Update the spec before the code**, if the behavior changes
3. Implement **per the app's implementation module**
4. Cover each `AC-n` with a test that can fail
5. Self-review, then review by the roles according to the diff's actual scope
6. Open the PR

> **Modules** — `scrumia-teams` orchestrates, `scrumia-impl-*` says how to code in each app, `scrumia-github-project` carries the PRs.

**Why the spec before the code**: writing the spec first surfaces the contradictions before they get encoded — where fixing them costs the least. If a contradiction with another feature appears, the run stops and calls on the business role. It never settles a rule on its own.

## 7. The human validates and merges

The PR carries the criterion-by-criterion mapping, the modified specs, the review verdicts, and the open reservations with their issues.

**Agents do not merge**, except for a category explicitly listed in `settings.autonomy.auto_merge`.

## The three gates

The cost of validation follows the risk.

| Gate | Who | Trigger |
|---|---|---|
| **1 — Automatic** | CI, linter, tests | Always. Blocking, no human. |
| **2 — Agent** | The roles | Routed by the diff's actual scope, not by the announced label. |
| **3 — Human** | You | The merge. Except for an explicitly delegated category. |

When two roles diverge, the disagreement is passed on as is — that is exactly the case that calls for human arbitration, and smoothing it into an average opinion would destroy it.

## What the human does

1. Scope and arbitrate a new idea
2. Validate dubious, critical or risky designs
3. Validate a sprint's batch
4. Settle a disagreement between roles
5. Review PRs and merge

Everywhere else, the agents move forward on their own. If the human ends up doing anything else, it is a signal about the composition — not about their discipline.

## On the "prepare the next sprint during execution" loop

It cannot be automated within one session: a subagent cannot spawn others, and agent teams are experimental with a single team per session ([ADR-0002](adr/0002-standing-roles.md)).

Two Claude Code sessions on the same repo give the same result — one consumes the current sprint, the other refines the next one. Since state lives in the tracker module and not in session memory, both stay consistent without coordinating.

It is a constraint of the current tooling, not a design choice.
