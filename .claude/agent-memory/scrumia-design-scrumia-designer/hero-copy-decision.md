---
name: hero-copy-decision
description: The hero's copy rules are owned by the hero feature — this entry holds only the FR term the spec does not carry, and points at the rest
metadata:
  type: project
  topic: site-hero-copy
  source: agent
  stale_when: features/app/site/hero/index.md states that "slot" stays untranslated in the FR copy
  cites: features/app/site/hero/index.md, features/app/site/hero/qa.md, #60
---

The hero's rules live in `features/app/site/hero/` — *"A count in the hero is derived, or
its debt is dated"* and the authored-line-break rule, both gated by that feature's `qa.md`.
Read them there; this entry does not carry them.

**The one thing no document owns:** "Slot" is the FR site's own term and is kept
untranslated (`site/i18n/fr/index.json`). Nothing in the hero spec or in `design/` says so,
so a translation pass would "fix" it. That belongs in the hero spec — until it is there,
it is here.

**What to watch:** the three counts are still literals in `site/templates/index.html`
under a dated debt note, not derived. #65 closed without making them derivable, so
`features/app/site/hero/index.md`'s "Open issues" entry for #65 is past due.
