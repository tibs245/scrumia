---
name: vocab-scope-label-readers
description: scope/* has entry readers and no exit reader — when counting its readers, say whether you count programmatic readers or readings
metadata:
  type: project
---

The axis is owned by `features/business/execution-policy/business.md` § *The scope
axis measures reach, not medium* (ADR-0015); entry-vs-exit routing is specified there
and in `agent-team`/`dev-flow`. "One reader" (programmatic: `pick-model.sh`) and "two
readers" (plus the manager's entry reading) are both true — a spec stating a bare
count without saying which it counts creates a contradiction with the other feature.

**How to apply:** on any change touching label routing, check the wording says "asked
at entry" / "routed to" for entry and reserves "required review" for gate 2, and that
no prose implies a higher tier buys a reviewer.
