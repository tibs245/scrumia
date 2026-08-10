---
name: pitfall-gh-search-in-qualifier
description: gh mangles a leading in: qualifier and silently returns every issue — the environment fact; the review step it implies is #205
metadata:
  type: feedback
  topic: gh-search-filtering
  source: agent
  stale_when: gh stops swallowing a leading in: qualifier — re-verify on any upgrade past 2.96.0
  cites: "#205, #32"
---

**The environment fact, which no document owns.** `gh search issues --repo <r>
'in:comments "foo" "bar"'` does not filter. `gh` parses the leading `in:` as a qualifier
and swallows the rest of the string as its value, so GitHub ignores it and returns **every
issue in the repo**, exit 0, no warning. Verified on gh 2.96.0 against tibs245/scrumia:
123 rows filtered, 123 unfiltered, 0 for a nonsense bare term.

Working forms: `--match comments 'foo' 'bar'`, or
`gh api -X GET search/issues -f q='repo:<r> in:comments "foo" "bar"'` for exact phrases.
A colon is stripped, so `"Deviation:"` and `"Deviation"` match identically; a slash
separates but adjacency survives, so `"L/low"` and `"XL/low"` do not collide. `gh` always
sends `advanced_search=true`, so never validate a documented query against the raw API
alone.

**The review obligation this implies — execute any documented `gh search` before approving
it, against a negative control — belongs in the review skill and is #205.** Do not act on
it from here.
