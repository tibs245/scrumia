# Changelog — Modular composition

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

## 2026-08-12 — Each layer is normalised to the current shape before the layers combine (AC-20, AC-21)
- Issue: #328
- Category: Changed
- Breaking: no

## 2026-08-12 — `settings.tracker` and `settings.team.execution` are deprecated in favour of their modules' `params:`
- Issue: #315
- Category: Deprecated
- Breaking: no

## 2026-08-12 — A module reads its configuration through the cascade, and stops when it cannot (BR-15, BR-16, AC-19)
- Issue: #315
- Category: Added
- Breaking: no

## 2026-08-12 — AC-18 also requires the layers to reach the module, and the criteria leave the out-of-scope section
- Issue: #315
- Category: Changed
- Breaking: no

## 2026-08-12 — Discovery is three tiers in one pass, and binding is stated per tier (tech.md)
- Issue: #291
- Category: Changed
- Breaking: no

## 2026-08-12 — `tech.md` names the debt a `local:` or `shared:` key carries until it resolves
- Issue: #302
- Category: Added
- Breaking: no

## 2026-08-12 — `extends:`, `composition:` and `practices:` are deprecated
- Issue: #302
- Category: Deprecated
- Breaking: no — all three are still read; removal comes two releases after this one

## 2026-08-12 — `modules` keyed by source replaces `extends`, with a settings cascade (BR-13, BR-14, AC-17, AC-18)
- Issue: #302
- Category: Changed
- Breaking: yes — every project on `extends:` migrates; see ADR-0021

## 2026-08-11 — A dependency names the source it comes from (BR-11, AC-12)
- Issue: #281
- Category: Changed
- Breaking: no

## 2026-08-11 — `tech.md` states how the extension mechanism resolves
- Issue: #281
- Category: Added
- Breaking: no

## 2026-08-11 — A skill is extended by data, and the table is computed when asked (BR-1, BR-2, BR-8..BR-12)
- Issue: #281
- Category: Added
- Breaking: no

## 2026-08-11 — `extends` replaces `composition:`, folding `practices` in
- Issue: #184
- Category: Changed
- Breaking: yes — `composition:` and the `practices` slot are retired; see
  `docs/adr/0019-extends-replaces-composition-and-practices.md` for the migration note

## 2026-08-11 — A module's references have to resolve inside it (BR-7, AC-9)
- Issue: #185
- Category: Added
- Breaking: no

## 2026-08-10 — Versioning is redirected to the feature that now owns it
- Issue: #7
- Category: Changed
- Breaking: no

## 2026-08-10 — Changelog rebuilt on Keep a Changelog's categories
- Issue: #213
- Category: Changed
- Breaking: no
