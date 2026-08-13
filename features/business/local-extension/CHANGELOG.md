# Changelog — Local extension

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

## 2026-08-13 — What `CLAUDE.md` claims is reconciled against what resolves, not asserted (BR-8, AC-7, tech.md)
- Issue: #292
- Category: Added
- Breaking: no

## 2026-08-13 — A rules section is a document a directive names, and a project holding no module is handed to no checker (BR-3, BR-4, AC-8)
- Issue: #292
- Category: Changed
- Breaking: no

## 2026-08-12 — A shadow, a conflict and an honest reader are three rules of their own (BR-5, BR-6, BR-7, BR-9, AC-11)
- Issue: #291
- Category: Added
- Breaking: no

## 2026-08-12 — Each source resolves from its own location, not from whatever carries the name (BR-1, AC-1..AC-5, tech.md)
- Issue: #291
- Category: Changed
- Breaking: yes — a `local:` or `shared:` key stops binding a marketplace module of that
  name; a project relying on that binding declares the marketplace source instead

## 2026-08-12 — A module's location is its declaration's source, not a field beside it (BR-6, AC-9)
- Issue: #302
- Category: Changed
- Breaking: no

## 2026-08-12 — Three locations for a module, and material a project adds without one (BR-1..BR-7)
- Issue: #285
- Category: Added
- Breaking: no
