# Changelog — Slot index

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

## 2026-08-21 — The intro states the rule, not the count
- Issue: #244
- Category: Changed
- Breaking: no
- Detail: `slots_intro` no longer hard-asserts how many of the seven slots are
  empty today. It states the rule the cards beneath carry (a slot is a question;
  a module is one answer; empty on purpose is a real answer) and preserves the
  "nothing is faked in their place" / "rien n'y est simulé" clause verbatim.
  Pinning the prose to the composition's current contents had it break the day
  a module filled `implementation` or `practices`; the same shape #165 caught in
  `install_composition_intro`.

## 2026-08-16 — The untranslated-"slot" rule moves here from the hero
- Issue: #304
- Category: Added
- Breaking: no

## 2026-08-10 — Changelog rebuilt on Keep a Changelog's categories
- Issue: #213
- Category: Changed
- Breaking: no
