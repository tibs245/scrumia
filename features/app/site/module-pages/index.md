# Module pages

**Status**: active
**Stratum**: app — `site`

## In brief

One page per marketplace module, in every language the site ships, generated rather
than written. The marketplace manifest is the enumerator and the fact source: a module
appears on the site because it exists in `.claude-plugin/marketplace.json`, and no page
restates a fact the manifest already carries. Prose is the only thing written by hand,
one file per module per language, loaded through the same path as every other page —
which is what keeps the anti-divergence guard working instead of being reimplemented.

Twelve modules and two languages make twenty-four pages today. Nothing in the build
knows either number.

## Links

- Parent (business): `features/business/modular-composition` — what a module is and
  what it owes. This feature only decides how one gets shown.
- Implemented by: `tools/build_site.py` (the site app's build step), with
  `tools/test_build_site.py` covering the criteria below.
- Sibling ticket: #66 writes the English prose in the site's voice, #58 the French.

## Files present

| File | Why it exists |
|---|---|
| `tech.md` | the fact-source split, the two guards, and where the emoji lives |
| `qa.md` | acceptance criteria for the generation and its failure modes |
| `CHANGELOG.md` | history of changes to this spec |

No `business.md`: the parent feature is named above and this feature adds no rule of
its own. No `ux.md` or `a11y.md`: the page's design is #66's and the redesign epic's,
not this feature's — the template here is deliberately a stub. No `api-contract.md`,
`legal.md`, `devx.md`: no exposed interface, no personal data, no published library.

## Open issues

- #65 — Enumerate modules from the manifests and generate their pages
- #66 — Write the twelve module micro-identities in English
- #58 — French copy pass over the redesigned site
- #70 — Nothing links to the module pages: they exist only in the sitemap
- #71 — An unreadable page JSON tracebacks, and manifest facts reach the HTML unescaped
