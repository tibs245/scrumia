# Changelog — feature format

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

## 2026-08-22 — Nesting depth is bounded by structure, not by a numeric limit
- Issue: #456
- Category: Changed
- Breaking: no — no existing feature was nested past the previous one-level bound, and the change loosens a restriction rather than adds one; the structural tests still apply

## 2026-08-19 — The referential set gains `Cited by`, for the inverse-asymmetry case a consumer raises
- Issue: #310
- Category: Added
- Breaking: no — an additive key, no existing index fails to conform

## 2026-08-17 — Disposition on disk, a fixed link vocabulary, and a content test that is answered
- Issue: #429
- Category: Added
- Breaking: yes — an index using a link key outside the fixed set no longer conforms

## 2026-08-10 — An entry names only what exists when it is written, and classifies one change
- Issue: #213
- Category: Added
- Breaking: no

## 2026-08-10 — Changelog rebuilt on Keep a Changelog's categories
- Issue: #213
- Category: Changed
- Breaking: no
