---
name: pitfall-cross-skill-claims
description: validate.py checks that links resolve, never that a sentence is true — the gap; the sweep obligation it implies is #205
metadata:
  type: feedback
  topic: stale-cross-references
  source: agent
  stale_when: "#205 lands the sweep in the review skill, or validate.py gains a check that a cross-skill claim is true"
  cites: "#205, #130"
---

**The gap, which no document owns.** Skills routinely assert what sibling skills do
("`scrumia-ticket` reads the scope to decide who reviews it"), and there is no compiler.
`tools/validate.py` checks that relative links *resolve* and that scripts exist — it never
checks that a sentence is *true*. A green run says nothing about a stale cross-reference.
On #130 the ticket enumerated five restatements and the PR fixed all five, but missed
`scrumia-refine/SKILL.md` asserting the very behaviour being removed: true before, false
after.

**The sweep obligation this implies — grep the old rule's phrasing across `plugins/`,
`docs/` and `features/` before approving a behaviour change — belongs in the review skill
and is #205.**
