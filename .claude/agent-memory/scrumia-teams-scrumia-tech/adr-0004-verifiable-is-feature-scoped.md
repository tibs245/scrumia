---
name: adr-0004-verifiable-is-feature-scoped
description: ADR-0004's "verifiable" is about feature splitting, not criterion falsifiability — and its "without subjective judgment" clashes with covering a criterion by role audit
metadata:
  type: project
---

`docs/adr/0004-feature-splitting.md` uses *verifiable* of a **feature** — "a unit of
value that can be verified independently", decided by "can you write at least one
Given/When/Then scenario that validates it, without depending on another feature under
construction?". Its Context line, *"A usable criterion must be verifiable by an agent
without subjective judgment"*, is about the **splitting criterion** the ADR is choosing,
not about an acceptance criterion.

**Why:** #31 added to `features/business/dev-flow/business.md` § *No criterion is
uncoverable* the claim that *verifiable* (§ The two paths), `qa.md` AC-1's "an
acceptance criterion that can fail" and ADR-0004's *verifiable* are "one property under
three names". They are not identical: the same feature licenses covering a criterion by
**an audit by the role that owns the judgement**, which is precisely subjective
judgement — the thing ADR-0004's sentence excludes. A reader following that pointer can
land back on the over-demanding false finding the PR exists to prevent.

**How to apply:** do not cite ADR-0004 as the definition of criterion-level
falsifiability. Cite `qa.md` AC-1. If the three-way reconciliation must stand, scope it —
"the same underlying property, applied at feature scale in ADR-0004" — and never carry
ADR-0004's *without subjective judgment* across to acceptance criteria. See
[[validate-warn-vs-error-is-the-decidability-line]] for the companion trap of defining
decidability counterfactually.
