---
name: pitfall-rule-placement-in-skills
description: A rule nested under Step N of a SKILL.md binds only from Step N — the observation; the review step it implies is #205
metadata:
  type: feedback
  topic: rule-placement-in-skills
  source: agent
  stale_when: "#205 lands the check in the review skill, or a SKILL.md stops being read top to bottom"
  cites: "#205, #118"
---

**The observation.** The deliverable here is prose an agent executes top to bottom, so a
rule written as a `###` subsection inside `## Step N` binds only from Step N onward, no
matter how strongly it claims to state "the general case". An agent reaching an earlier
step has not read it yet. Found on #118: the commit-before-yield rule sat under Step 4 of
`scrumia-ticket` while the skill's earliest yield point — Step 3's spec-contradiction
escalation — sits above it.

**The rule it implies — where a cross-cutting rule belongs, and the obligation to list a
skill's yield points when reviewing one — is #205's, for the review skill.** Related:
[[pitfall-cross-skill-claims]].
