---
name: quiet-link-idiom
description: A text-coloured underlined link is legitimate only where an adjacent element already holds the accent; one instance exists and its promotion into the design system is on the board
metadata:
  type: project
---

`a.mod-name` keeps `color: var(--text)` at rest and takes `--accent` only on
`:hover`/`:focus-visible` — legitimate because `.mod-slot`, directly under it, already
spends the card's accent (identity decision 4: "if two things on a screen are pointing,
neither is").

**How to apply:** anywhere else, links are accent. If a second instance appears, the
idiom must first be promoted from a per-component comment into `design/identity.md` or
a components entry — that promotion is an open ticket on the board; until it lands the
pattern has one instance and no home.
