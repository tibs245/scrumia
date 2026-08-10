---
name: pluggability-vs-evolution
description: The "three things a module owes to be pluggable" list has a membership test and a second home in qa.md AC-6 — versioning/changelog obligations fail the test and belong to the deferred evolution question
metadata:
  type: project
---

`features/business/modular-composition/business.md` § *What a module owes to be pluggable*
("Three things, no more": `SKILL.md`, a scope, the never-assume rule) is **not** an open list
of good practices. It carries its own membership test, stated right under it: an item belongs
only if skipping it *"breaks silently the day a project composes the module with a different
set of modules than the one it was written against"*.

Two consequences, both easy to miss:

- **The list is restated in `qa.md` AC-6**, which promises a third-party module "only needs to
  satisfy the three things any module owes ... to be composable". Adding a fourth item changes
  what every external module owes, not just ScrumIA's twelve.
- **Everything about versions, changelogs, bumps and migration is already deferred** by
  `qa.md` § *Out of scope* to #7 — *"how a module evolves once adopted"*, explicitly including
  "how that project finds out about a breaking change". A changelog is that mechanism, so it is
  an evolution obligation, not a pluggability one. Its home is the `release` slot epic (#86,
  AC-1 = the ADR, AC-3 = the per-plugin changelog), not this list.

**Why:** the two families read alike ("what a module owes") and refinement passes keep proposing
the first as a home for the second — it happened on #87.

**How to apply:** before accepting any addition to the three, run the membership test out loud.
A module with no changelog composes fine; one with no `SKILL.md` does not. If the `release` ADR
concludes there is no slot, the fallback home is a *separate section* of this business.md
("what a published module owes its consumers"), never a fourth item in the pluggable list.
Related: [[vocab-mandatory-vs-optional]].
