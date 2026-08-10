---
name: scope-rubric-vs-site-tools-coupling
description: site/ and tools/ are declared as two apps, so scrumia-refine's "≥2 apps → scope/L" rule mislabels every site-prose ticket; the coupling is structural, not accidental
metadata:
  type: project
  topic: site-tools-app-split
  source: agent
  stale_when: .scrumia/config.yaml stops declaring site and tools as peer apps, or scrumia-refine's scope rubric gains a carve-out for an app and its build tooling
  cites: #114, .scrumia/config.yaml
---

`.scrumia/config.yaml` declares `site` and `tools` as two peer apps, but
`tools/build_site.py` **is** the site's builder: the i18n data in `site/i18n/`
and the guard that reads it in `tools/` cannot be changed independently. Any
ticket that touches the site's prose contract therefore touches two apps by the
config's own table.

`scrumia-github-project/skills/scrumia-refine/SKILL.md:85-87` grades scope as:
`S` = 1 app **and no spec modified**; `M` = 1 app but a spec changes;
`L` = ≥2 apps. So these tickets mechanically grade `L`, which the model matrix
(`config.yaml`, `L/low`) routes to **opus** rather than sonnet.

Observed on #114 / PR #189: labelled `scope/S risk/low` (→ sonnet) while the
diff touched `site/i18n/{en,fr}/index.json`, `tools/build_site.py`,
`tools/test_build_site.py` and three spec files. The work was correct anyway,
but the label was wrong on both clauses of `S`, and the refinement that set it
had itself planned the spec edits.

**Why:** the gap is not a one-off mislabel — it recurs for every site-prose
ticket, because the two-app split does not match the real unit of change. Two
honest fixes exist: model `tools` as the site's builder rather than a peer app,
or give the scope rubric a carve-out for an app and its build tooling.
**How to apply:** when refining or reviewing a ticket that touches site prose,
expect the `scope/S` vs `≥2 apps` contradiction and judge by blast radius, not
by app count — then say which rule you applied. Do not silently approve the
label. Related: [[contract-block-carries-names-not-status]].
