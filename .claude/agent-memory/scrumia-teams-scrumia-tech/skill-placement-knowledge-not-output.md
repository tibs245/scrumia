---
name: skill-placement-knowledge-not-output
description: Where a new skill belongs in the composition — with the knowledge the finding needs, not with the tool that files its output; the five shipped audit skills are the proof
metadata:
  type: project
---

`docs/modules.md`'s "Adding a module" rule ends at *"otherwise, it's one more skill in an
existing module"* and deliberately does not say **which** module. The composition answers
that by placement, not by prose: every audit skill sits in the module that owns the
knowledge its finding needs — `scrumia-tdd-audit`, `scrumia-solid-audit`,
`scrumia-rust-audit`, `scrumia-solidjs-audit`, `scrumia-design-audit`, spread across the
`practices`, `implementation` and `design` slots. None sits in the `tracker`, even though
every one of them ends in issues. `scrumia-tdd-audit` states the split outright: *"An audit
observes, it does not fix"*, and it hands findings to the tracker only as issues.

**Why:** a spec proposed the opposite heuristic — "the module that already owns its
output" — and used it to place a future debt-audit skill in the `tracker` slot. Applied,
that skill would have to carry Rust ownership signals, SOLID over-application signals and
design mutedness signals, or reduce to a wrapper over five skills that already exist.

**How to apply:** when any spec or ADR proposes where a not-yet-written skill lands, check
it against the shipped placements before accepting the reasoning. "Owns the output" is not
this composition's rule. Also: a spec that describes a capability generically (an audit, a
review, a refactor) must be checked against `ls plugins/*/skills/` — the capability is
often already shipped several times over, and the spec that fails to name them argues its
case from a weaker position than it has. Related: [[pitfall-cross-skill-claims]].
