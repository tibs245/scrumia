---
name: vocab-yield-vs-pause
description: dev-flow's commit rule is defined on "yield"; two older "pause" shorthands are labels, not rules — reconciling them is an unwritten decision
metadata:
  type: project
---

The governing statement is dev-flow `business.md` § *Who decides, on each path* →
**Execution**: commit before the run *yields control* (yield = any pause that hands
the next move to someone else). Two older "pause" shorthands in the same feature are
list labels; "pause" is strictly wider than "yield". The reconciliation is an open
ticket on the board — if asked to settle it, say it is unwritten rather than picking.
