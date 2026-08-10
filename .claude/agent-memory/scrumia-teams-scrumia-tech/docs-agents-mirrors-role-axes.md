---
name: docs-agents-mirrors-role-axes
description: docs/agents.md line ~42 enumerates the tech role's six review axes by name only — renaming an axis in scrumia-tech.md leaves it stale, and no grep for the rule text finds it
metadata:
  type: project
---

`docs/agents.md` carries a one-line enumeration of `scrumia-teams/agents/scrumia-tech.md`'s
numbered review order — *"correctness, contract, coupling, testability, consistency,
debt"* — and the equivalent prose for the business role. It reproduces the **axis names
only**, never the axis text.

**Why:** #31 renamed tech's item 4 from **Testability** to **Coverage** and rewrote it
across four surfaces; the sweep grepped the rule's phrasing, which `docs/agents.md` does
not contain, so the enumeration stayed on the old name. `validate.py` cannot see it —
nothing links, nothing generates.

**How to apply:** whenever a role agent's numbered list is renamed or reordered, grep
`docs/agents.md` for the old axis word before opening the PR. Sibling surfaces to check
in the same pass: `site/i18n/{en,fr}/modules/scrumia-teams.json` (currently carries no
axis list, but it is the natural second home). Companion to
[[sweep-surface-format-rules]] and [[docs-dev-flow-mirrors-site-workflow]].
