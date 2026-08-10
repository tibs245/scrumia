---
name: scope-rubric-vs-site-tools-coupling
description: site/ and tools/ are declared peer apps while build_site.py is the site's builder, so app-count scoping mislabels site-prose tickets — open on the board
metadata:
  type: project
---

`tools/build_site.py` is the site's builder: a site-prose ticket touches both declared
apps by construction, so any "≥2 apps" reading over-grades it. Judge by blast radius
(ADR-0015), say which rule you applied, and do not silently approve the label. The
structural fix (model tools as the site's builder, or carve out build tooling) is an
open ticket on the board.
