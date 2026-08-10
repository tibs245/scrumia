---
name: vocab-yield-vs-pause
description: dev-flow names the commit-before-handoff rule two ways — "yield" (defined, normative) and "pause" (undefined shorthand); say which governs
metadata:
  type: project
  topic: commit-before-yield
  source: agent
  stale_when: features/business/dev-flow/ reconciles its pause shorthands with the yield rule, or #123's wording is rewritten
  cites: features/business/dev-flow/business.md, #123, #195
---

`features/business/dev-flow/` states the commit rule normatively as *"an execution
commits its in-flight work to the ticket's branch before the run **yields control**"*,
and defines the term inline: a yield is any pause that hands the next move to someone
else (role review, sub-agent, human verdict, wait on a check). Two older shorthands in
the same feature say **"pause"** instead — `index.md` ("committing before a pause") and
`business.md` § *The replacement test* ("commit before any pause or review"). Both
predate the rule (#123) and are list labels, not rules.

**Why:** "pause" is strictly wider than "yield" — a pause that hands control to nobody
is a pause and not a yield. A reader reaching the shorthand first can infer a broader
obligation than the feature actually states.

**How to apply:** when reviewing or writing in dev-flow, treat the *Who decides, on each
path* → **Execution** bullet as the governing statement and the two shorthands as
labels. If asked to reconcile them, that is an unwritten decision, now tracked as **#195** —
say so and point there rather than picking. Related: [[vocab-scope-label-readers]].
