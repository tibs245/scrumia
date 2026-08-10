---
name: pitfall-rule-placement-in-skills
description: A cross-cutting rule nested under a numbered Step in a SKILL.md only binds from that step onward — earlier yield points stay uncovered even when the prose says "general case"
metadata:
  type: feedback
---

In this repo the deliverable is prose an agent executes top to bottom. A rule written as a
`###` subsection inside `## Step N` binds only from Step N onward, no matter how strongly the
prose claims to state "the general case". An agent reaching an earlier step has not read it yet.

**Why:** found reviewing #118 (commit-before-yield). The rule was placed under Step 4 of
`scrumia-ticket`, but the skill's earliest yield point — Step 3's "call on the business role"
on a spec contradiction — sits above it. The general-case wording could not reach backwards.

**How to apply:** when reviewing a SKILL.md change that introduces a cross-cutting rule, list
every point in the file where the run hands control to someone else (role spawn, human
escalation, `When you're blocked`, a wait on a check) and check each one is *after* the rule's
heading. A cross-cutting rule belongs at its own `##` level, placed at the earliest step where
it becomes applicable — not inside the step that motivated it.

Related: [[pitfall-cross-skill-claims]] — same family, prose that reads true and is not.
