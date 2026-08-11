---
name: docs-agents-mirrors-role-axes
description: docs/agents.md enumerates each role's review axes by name only — renaming or reordering an axis in the agent file leaves it stale, and grepping the rule's phrasing never finds it
metadata:
  type: project
---

`docs/agents.md` carries a one-line enumeration of `scrumia-teams/agents/scrumia-tech.md`'s
numbered review order — currently *"correctness, contract, coupling, testability,
consistency, debt"* — and the equivalent prose for the business role. It reproduces the
**axis names only**, never the axis text. `validate.py` cannot see either surface drift
from the other — nothing links, nothing generates.

**How to apply:** whenever a role agent's numbered list is renamed or reordered, grep
`docs/agents.md` for the old axis word before opening the PR. Sibling surface to check in
the same pass: `site/i18n/{en,fr}/modules/scrumia-teams.json` (currently carries no axis
list, but it is the natural second home). Companion to [[sweep-surface-format-rules]] and
[[docs-dev-flow-mirrors-site-workflow]].
