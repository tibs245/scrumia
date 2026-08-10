---
name: validate-warn-vs-error-is-the-decidability-line
description: validate.py's warn()/error() split is the repo's real boundary between an approximate check and one that decides a property
metadata:
  type: project
---

`tools/validate.py` ships two verdict channels — `warn()` (advisory, exit 0) and
`error()` (gate, exit 1) — and the choice between them encodes whether a check
*decides* its property or merely approximates it. `check_french_leftovers()` counts
accented characters past a threshold, false-positives on proper nouns, and is
therefore `warn()`. `check_doc_links()` runs clean on this repo's real content and is
therefore `error()`.

**Why:** `features/business/dev-flow/dev-flow` § *Covering a criterion* (#31) tried to
define decidability counterfactually — "returns the verdict a careful reader would, on
every case the criterion covers" — which no regex-based check survives, including
`check_doc_links()` itself, whose link regex misses reference-style links and matches
inside fenced code blocks. The warn/error split is the operable version of the same
distinction, and it is decidable by running the check rather than by imagining inputs.

**How to apply:** when a spec or review needs to say whether an automated check covers
a criterion, ask whether it runs clean over this repo's actual content — that is the
question `error()` vs `warn()` already answers. Do not ask whether an adversarial input
exists; one always does. See [[review-head-vs-origin-vs-brief]] for the companion
check-before-you-judge habit.
