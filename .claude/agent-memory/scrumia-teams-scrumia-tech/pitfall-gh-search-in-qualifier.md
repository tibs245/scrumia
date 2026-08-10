---
name: pitfall-gh-search-in-qualifier
description: gh search issues mangles an in: qualifier inside the query string and silently returns every issue; specs that document such a command are false
metadata:
  type: feedback
  topic: gh-search-filtering
  source: agent
  stale_when: gh stops swallowing a leading in: qualifier — re-verify against a negative control on any gh upgrade past 2.96.0
  cites: #32
---

`gh search issues --repo <r> 'in:comments "foo" "bar"'` does **not** filter. `gh` parses
the leading `in:` as a qualifier and swallows the rest of the string as its value —
it sends `q=( in:"comments \"foo\" \"bar\"" ) repo:… type:issue`. GitHub ignores the
unrecognised `in:` value and returns **every issue in the repo**, exit 0, no warning.
Verified on gh 2.96.0 against tibs245/scrumia: 123 rows for the filtered query, 123 for
the unfiltered one, 0 for a nonsense bare term.

Working forms:
- `gh search issues --repo <r> --match comments 'foo' 'bar'` — gh auto-quotes a
  multi-word positional as a phrase; single-word args stay bare.
- `gh api -X GET search/issues -f q='repo:<r> in:comments "foo" "bar"'` — the only form
  with exact phrase control.

Tokenisation facts checked at the same time: a colon is stripped, so `"Deviation:"` and
`"Deviation"` match identically — a trailing colon buys no precision. A slash is a
separator but adjacency survives, so `"L/low"` and `"XL/low"` do **not** collide.
`gh` always sends `advanced_search=true`; the legacy engine gives different (looser)
counts, so never validate a documented query against the raw API alone.

**Why:** the failure is full recall, not an error — a reviewer who eyeballs the output
sees rows and concludes the query works. Found on #32, where a spec's whole queryability
criterion rested on the broken command.

**How to apply:** any `gh search` command written into a spec, skill or script must be
executed before approval, and checked against a *negative control* (a term that should
return nothing) — not just "did it return rows". Related: [[pitfall-cross-skill-claims]].
