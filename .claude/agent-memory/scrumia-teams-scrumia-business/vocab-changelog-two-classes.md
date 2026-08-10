---
name: vocab-changelog-two-classes
description: Changelog vocabulary — spec changelogs take four categories, plugin changelogs six; the catalogue is the authority and the PR field is gone
metadata:
  type: project
---

Two changelog classes, two vocabularies, decided in #213:

- `features/*/CHANGELOG.md` — no versions, four categories (`Added`, `Changed`,
  `Deprecated`, `Removed`). Entry = `## YYYY-MM-DD — <title>` + `- Issue:`,
  `- Category:`, `- Breaking:`. **No `PR:` field**: the entry ships inside the PR,
  so a PR number is a thing that does not exist when the entry is written.
- `plugins/*/CHANGELOG.md` — Keep a Changelog whole, six categories, versions.

**Where each is stated.** The spec half's authority is `scrumia-feature`'s
`references/catalog.md` § `CHANGELOG.md`; the plugin half's is
`docs/format-changelog.md`. `feature-format/business.md` § *Absolute rule — no
inline history* states the **rule** (name only what exists; one entry, one
category) and delegates the enumeration. Do not let a third file enumerate the
categories — see [[rule-vs-rationale-duplication]].

**Why:** the repo's failed first attempt left 65 unfilled `#NN` PR placeholders
across 83 entries; the fix was to stop carrying a field nobody can fill.

**How to apply:** when reviewing a spec that mentions the changelog, check it does
not still promise a PR number (`feature-format/qa.md` AC-14's exemption and
`github-tracking/index.md` both did after #213), and check the class before
judging a category — `Fixed` and `Security` are legal in a plugin changelog and
not in a spec one.
