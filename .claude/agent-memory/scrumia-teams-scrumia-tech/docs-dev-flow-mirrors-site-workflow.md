---
name: docs-dev-flow-mirrors-site-workflow
description: docs/dev-flow.md and site/i18n/{en,fr}/workflow.json are the same content in two renderings — sweeping one step without the other is the recurring miss
metadata:
  type: project
---

`docs/dev-flow.md` and `site/i18n/{en,fr}/workflow.json` narrate the **same numbered
workflow**, sentence for sentence, in two renderings. The mapping is positional, not
by name:

| `docs/dev-flow.md` | site key |
|---|---|
| "The outline" list under step 6 | `step6_li1` … `step6_li6` |
| step 7 prose, *"The PR carries …"* | `step7_p1` |

`site/**/workflow.html` (both languages) is **generated** from that JSON by
`tools/build_site.py` — edit the JSON, rebuild, and `git diff --exit-code site/` must be
clean.

**Why:** #31 rewrote both `docs/dev-flow.md` step 6 (outline) and step 7 (what a PR
carries), but on the site swept only `step6_li4`. `step7_p1` kept the superseded sentence,
so the doc and the public page contradicted each other on the same step — the "three texts
disagreed" failure #25 already cost this project. A green `validate.py` and a clean
`git diff site/` both pass in that state: the rebuild only proves the HTML matches the
JSON, never that the JSON matches the doc.

**How to apply:** when a change touches any step of `docs/dev-flow.md`, grep the *same
step number* in both `workflow.json` files before approving — `li` items and `pN` prose
alike. Neither the validator nor the site rebuild will catch the omission. Related:
[[sweep-surface-format-rules]] for the specs-format equivalent.
