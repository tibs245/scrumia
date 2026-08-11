---
name: scrumia-brainstorm
description: Scopes an idea or a brief through challenge, until it is ready to be split into features. Use it when opening a project, when a new feature arrives, or to critique an idea before committing.
---

# Brainstorming and scoping

This path exists to **turn an idea into something splittable**. It produces no document: it produces a shared understanding, then hands off to `scrumia-split`.

This is the only moment in ScrumIA where the human is engaged for a long time. Make it useful.

## The principle

You challenge, the human arbitrates. You don't write the vision for them and you don't approve out of politeness.

A successful scoping is not one where you agreed. It's one where the holes were found **before** the code.

## Flow

### 1. Listen, then rephrase

Let the human lay out their idea without interrupting. Rephrase in three lines at most: the problem, for whom, the expected outcome.

Get it validated before going any further. A disagreement here costs thirty seconds; the same disagreement after splitting costs a day.

### 2. Challenge

Attack in this order — from most expensive to least expensive if it's wrong:

1. **Does the problem exist?** Who has hit it, when, how do they cope today? An idea that answers no existing workaround is suspect.
2. **Does this solution solve this problem?** Look for the path by which it fails to solve it while working technically.
3. **What becomes impossible?** Every decision closes doors. Name the ones closing.
4. **Where are the edge cases?** Zero, duplicate, concurrency, cancellation, scaling, permissions.
5. **What is assumed without being said?** Tacit assumptions are what breaks in production.
6. **Where is the legal angle?** Personal data, payment, user content, minors, regulated sector.

One question at a time when it is structural. Group them when they are secondary — an interrogation wears people out and gets rushed answers.

When you identify a real risk, say it once, clearly, then move on. Repeating an objection already heard doesn't make it more true.

### 3. Recognize the end

Scoping is done when:

- The problem and the expected outcome fit in three accepted lines
- There is at least one verifiable acceptance criterion
- The remaining open questions are **named** and don't prevent starting
- We know which apps are affected

It is **not** done when everyone is tired. If scoping is stalling, the scope is often too broad: propose scoping only the first slice.

### 4. Hand off

Don't write the features yourself. Call `/scrumia-discovery:scrumia-split` with what has been established.

If the human wants to stop before splitting, create a `scope/XL` issue that captures the scoping and the open questions. Nothing gets lost, nothing rots in a notes file.

## What this project scopes against

```bash
scrumia-extends scope-idea
```

A module the project runs may carry a constraint an idea has to survive before it is worth
splitting — a regulatory boundary, a platform limit, a cost ceiling. It arrives here from
the module that owns it. An empty table means the challenge below is the whole bar.

## Bringing in Business and Tech

You can delegate during scoping:

- `scrumia-business` — when the idea touches existing rules, or to check it doesn't contradict any
- `scrumia-tech` — when feasibility or architecture cost is the blocking point

Do it when the answer **changes the rest of the discussion**, not to cover the decision. An opinion requested after the fact is useless.

## What you don't do

- No PRD, no vision document, no session notes file.
- No implementation plan: that's path 2.
- No numeric estimate at this stage. An estimate before splitting is an invention.
