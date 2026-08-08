---
name: scrumia-rules-update
description: Evolves an existing rule — locates its governing decision, challenges it in writing against the new context, updates decision and guides together, and logs the change in the section's CHANGELOG. Use whenever a rule needs to change, not just its guide.
---

# Evolving a rule

Requires `scrumia-rules` — the format this skill operates on. Works on any section, module-shipped or project-local; a module-shipped section still evolves through its own repository, this skill just documents how the change is shaped once you're there.

## The hard rule

**Never change a guide without updating its decision.** A guide with no decision behind it is an opinion, not a rule — and an opinion an agent enforces as if it were a rule is worse than no rule at all, because nothing invites it to be questioned.

The rule runs both ways: a decision changed without its guide is dead weight — the agent reading the guide keeps following the old rule while the record of *why* has already moved on.

## Step 1 — Locate the governing decision

Follow the guide's `> Decision rationale: D-NN — decisions/D-NN-slug.md` pointer, or the index's decisions table if you're starting from the decision side.

**If neither exists**, the guide has no decision behind it. Don't evolve it yet — write the missing decision first, reconstructed from the best available evidence (`git blame` on the guide, the original author if reachable, the codebase pattern it was clearly describing), and say plainly in its `## History` that it was reconstructed after the fact. Only then proceed to Step 2.

## Step 2 — Challenge it with the new context, in writing

Not a rubber stamp. Before touching anything, write out — in the decision itself, or a note that becomes part of it:

- **What changed** since the decision was made — the concrete new context driving this update (a new library version, a case the original decision didn't anticipate, a pattern that turned out costlier than expected).
- **Arguments for keeping** the current verdict despite the new context.
- **Arguments for changing** it.

A challenge that only lists arguments for the change is not a challenge, it's a decision already made looking for cover. Restate the case for the status quo even if you'll end up rejecting it — that's what proves it was considered, not skipped. This mirrors the Arguments For / Arguments Against split the decision already carries; you're re-running it with the new context added to the table.

## Step 3 — Refine or supersede

Two shapes, decided by whether the **verdict** itself changes:

- **Refine** — same verdict, a nuance added, an example corrected, wording tightened. Edit the decision in place; append a dated line to its `## History`.
- **Supersede** — the verdict changes. Write a **new** decision file, `D-NN` at the next free number in the section, with its own `Status` (`Adopted` or `Proposed`, per the same criteria `scrumia-rules-setup` uses). Set the old decision's `Status: Superseded by D-NN`. **Never rewrite an old verdict in place** — this project's own ADRs follow the identical rule, for the identical reason: it must stay possible to see what was actually believed at the time, not just what's believed now.

## Step 4 — Update the impacted guide(s), same change

Every guide the decision's `Impacts` line names gets updated together with the decision, not in a follow-up:

- New rule content, Correct/Incorrect examples, if the rule itself changed.
- A corrected `Decision rationale` link, if Step 3 superseded rather than refined.

## Step 5 — Append the section's `CHANGELOG.md`

```markdown
## YYYY-MM-DD — <short description>
- Decision: D-NN (superseded by D-MM, if applicable)
- Guides: guides/NN-topic.md, ...
- Why: one line — the decision carries the full argument, don't restate it here
```

Same discipline as a spec's changelog: history lives here in one line pointing at the decision; the reasoning itself lives in exactly one place, the decision file, not duplicated.

## Step 6 — Report back

What changed, refine or supersede, which guides were touched, the `CHANGELOG.md` entry added. If Step 1 had to reconstruct a missing decision, say so explicitly — that's a gap in the section worth the user's attention beyond this one update.

## What you don't do

- No editing a guide's rule without touching its decision in the same change.
- No rewriting an `Adopted` decision's verdict in place — supersede it.
- No decision — new or refined — that skips Arguments Against.
- No commit — the user reviews.

## The module's two other skills

- `scrumia-rules` — the format this skill operates on; read it first.
- `scrumia-rules-setup` — scaffold a project-local section before it has anything to evolve.
