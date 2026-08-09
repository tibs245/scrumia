---
name: pitfall-cross-skill-claims
description: In plugins/, skills assert what sibling skills do; nothing checks those claims, so a behaviour change must be swept for prose that becomes false
metadata:
  type: feedback
---

When a rule changes in `plugins/`, grep the whole tree for prose in *other* skills and
agents that asserts the old behaviour — not just the file that carried the rule.
Skills routinely state what a sibling does ("`scrumia-ticket` reads the scope to decide
who reviews it", "read by `pick-model.sh`, `scrumia-ticket` Step 6"), and a rule change
turns those from true to false.

**Why:** the deliverable is prose an agent executes, and there is no compiler.
`tools/validate.py` checks that relative links *resolve* and that scripts exist — it
never checks that a sentence is *true*. A green validate run says nothing about a stale
cross-reference. On #130 (Step 6 stopped gating the review on `scope/*`), the ticket
enumerated five restatements and the PR fixed all five, but missed
`scrumia-refine/SKILL.md` asserting the very behaviour being removed: true before the
PR, false after.

**How to apply:** on any review of a `plugins/` behaviour change, run a grep for the
*old* rule's phrasing across `plugins/`, `docs/` and `features/` before approving —
paraphrases included, not just the exact string the ticket quoted. Treat a sentence the
diff falsifies as a regression the PR introduced, not as a pre-existing wart, and
distinguish it from what a "measures vs gates" sibling ticket owns.
