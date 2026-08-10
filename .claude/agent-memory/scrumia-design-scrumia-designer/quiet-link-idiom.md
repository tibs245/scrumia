---
name: quiet-link-idiom
description: The quiet-link rule has no home in the design system yet — that is #208; this holds only what a reader cannot get from it
metadata:
  type: project
  topic: site-link-styling
  source: agent
  stale_when: "#208 states the quiet-link rule in design/identity.md or a component spec"
  cites: "#208, #70, design/components/module-card/spec.md"
---

The idiom, its general form and the incomplete exception list are in **#208**. Read it
there; this entry does not carry the rule.

**What #208 does not give you, and a review of `site/` needs:** the reason
`a.mod-name` is allowed to decline the accent is identity decision 4 — *"one accent — if
two things on a screen are pointing, neither is"* — and on the module card the accent is
already spent on `.mod-slot`, directly below it in the same `.mod-id` stack. The
justification is recorded at `design/components/module-card/spec.md:18`, which names
`.mod-slot` correctly.

Until #208 lands, treat a second text-coloured link as unresolved rather than as
precedent: say the rule has no home and point at #208.
