---
name: pitfall-gh-search-in-qualifier
description: gh search with an in: qualifier inside the query string silently returns everything — the mechanics are specified in github-tracking/tech.md; the craft rule is the negative control
metadata:
  type: feedback
---

The failure mode and the working forms are specified in
`features/business/github-tracking/tech.md` (moved there from this entry). What no
spec carries: **any `gh search` command written into a spec, skill or script must be
executed before approval, against a negative control** — a term that should return
nothing — because this failure's shape is full recall with exit 0, and eyeballing
rows proves nothing. Related: [[pitfall-cross-skill-claims]].
