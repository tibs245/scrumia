---
name: rule-vs-rationale-duplication
description: The drift test for "the rule is written twice" is owned by agent-team/business.md — this entry says when it comes up and what a review keeps getting wrong
metadata:
  type: project
  topic: rule-restated-in-two-places
  source: agent
  stale_when: features/business/agent-team/business.md § Four channels, one home each states the drift test differently
  cites: features/business/agent-team/business.md, #118
---

The rule lives in `features/business/agent-team/business.md` § *Four channels, one home
each* — second bullet. Read it there; this entry does not carry it.

**When it comes up:** any criterion phrased "the rule is stated once in X and the skill
cites it rather than restating it". Established on #118 / PR #173, where the skill kept a
spec's rationale sentence and explicitly disclaimed holding the trigger, and passed.

**What a review keeps getting wrong:** judging by textual overlap. Ask instead which
sentences are normative, and object only to those. See [[vocab-yield-vs-pause]] for the
vocabulary this sits on.
