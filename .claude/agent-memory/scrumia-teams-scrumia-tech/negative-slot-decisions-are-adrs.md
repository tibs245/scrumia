---
name: negative-slot-decisions-are-adrs
description: A "we will not build this module / will not split this slot" decision is recorded as an ADR with reopen conditions and a stated cost — ADR-0013 is the precedent
metadata:
  type: project
---

Composition-shape decisions that are **negative** — no new slot, no split, no module —
are recorded in `docs/adr/`, not only in `docs/modules.md` or `docs/roadmap.md`.
`docs/adr/0013-tracker-stays-one-slot.md` is the pattern: the decision, an explicit
*"Reopen this when…"* list, a *"What we accept"* section naming who is blocked by it, and
*"Rejected alternatives"*.

**Why:** `docs/adr/README.md` says an accepted ADR is never modified and that *"the 'what
we accept' section is not optional — a decision without a stated cost has not been
examined."* A feature spec carries only its current version (`CLAUDE.md`, Shared rules),
so a rejection argued inside `features/**/business.md` is erased by the next edit to that
file, with nothing recording that the alternative was ever weighed.

**How to apply:** when a change decides *not* to fill a slot or not to build a candidate
module, ask for the ADR — or at minimum for the two things an ADR would have forced: the
reopen condition, and the cost accepted. `docs/modules.md`'s candidate list is a register
of intent, not a venue for reasoning. Related: [[skill-placement-knowledge-not-output]].
