# Changelog — Composer

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

## 2026-08-12 — The emitted config is a `modules:` mapping keyed by source (AC-2, AC-3, AC-6)
- Issue: #301
- Category: Changed
- Breaking: yes — a composition the composer emitted before this reads under the
  retired `composition:` keys, which `scrumia-extends` reports and migrates away from

## 2026-08-12 — Additions past the seven slots, ours and the visitor's own (AC-9, AC-10)
- Issue: #298
- Category: Added
- Breaking: no

## 2026-08-10 — Changelog rebuilt on Keep a Changelog's categories
- Issue: #213
- Category: Changed
- Breaking: no
