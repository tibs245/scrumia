# Module pages

**Status**: active

## In brief

One page per marketplace module, in every language the site ships, generated rather
than written. The marketplace manifest is the enumerator: a module appears on the site
because it exists in `.claude-plugin/marketplace.json`. Prose is the only thing written
by hand, one file per module per language, loaded through the same path as every other
page — which is what keeps the anti-divergence guard working instead of being
reimplemented.

Twelve modules and two languages make twenty-four pages today. Nothing in the build
knows either number.

## Links

- Business parent: `features/business/modular-composition` — what a module is and
  what it owes. This feature only decides how one gets shown.

## Files present

| File | Read it when |
|---|---|
| `tech.md` | tracing where a fact comes from, how the guards catch a missing string or a manifest mismatch, or where the emoji lives |
| `qa.md` | writing or running the acceptance criteria for the generation and its failure modes |
| `business.md` | checking the value a module page brings, or what this app's share of `modular-composition` covers |
| `CHANGELOG.md` | checking history of changes to this spec |

No `ux.md`: the page's design is the redesign epic's, not this feature's — the
template here is deliberately a stub. No `api-contract.md`, `legal.md`, `devx.md`: no
exposed interface, no personal data, no published library.
