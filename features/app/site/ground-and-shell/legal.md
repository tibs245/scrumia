# Legal — Ground and shell

No personal data, no payment, no user content, no regulated sector: the trigger
here is different from the catalog's usual list. ScrumIA is a marketplace that
distributes Claude Code plugins, uses a palette inspired by — but, after
mitigation 1 below, distinct from — Claude Code's, and ships an original
mascot. That combination sits close enough to the edge of nominative fair use
that the residual risk needs a name and an owner, not a shrug.

## The constraint

Claude Code and Anthropic are third-party marks. ScrumIA may name them —
"a Claude Code plugin marketplace" is accurate, necessary, and protected as
nominative fair use — but it may not imply sponsorship, endorsement, or
affiliation that does not exist.

A single element read alone is ordinary: naming the platform in prose, or using a
warm accent colour of ScrumIA's own choosing, each sit well inside fair use. The
risk in this feature is the **stack**: a Claude-adjacent warm accent, on the
site's mascot, on a marketplace that distributes Claude Code plugins. Read
together, that combination signals "official" more than any one part does on its
own — the exact affiliation implication the redesign epic (#40) already flagged
about itself.

`design/identity.md` and `design/components/hop/spec.md` are the files that carry
this decision day to day; this file is where the residual risk and its acceptance
are recorded, since neither of those is a legal file.

## The mitigations

Required by the business role's review of #52 ("compliant with reservations" —
the role declined to sign the residual risk alone):

1. **The accent is ScrumIA's own token value, not Anthropic's identifiable brand
   hex.** `design/tokens.css`'s `--human` / `--agent` pair is not
   `#D97757` (Claude Code's own coral). Verified at the time of writing:
   `design/tokens.css` on this branch already carries distinct values
   (`#9E4517` / `#F0996F`). One remaining loose end is not this feature's to fix:
   `design/identity.md` still quotes `#D97757` in prose, as the *inspiration*
   for the palette rather than its value — out of this ticket's scope (owned by
   #52, which is already rewriting that exact paragraph). Flagged in the PR, not
   edited here.
2. **A plain non-affiliation statement on the site.** Delivered by this feature:
   the footer, present on every page in both languages — `qa.md` AC-5 verifies
   it. The string lives in `site/i18n/{en,fr}/common.json` as
   `footer_non_affiliation`.
3. **No Anthropic marks, wordmarks, or mascot likeness.** Already settled in #40
   and reaffirmed by `design/components/hop/spec.md`'s "What it refuses" — Hop
   carries no anthropomorphism and belongs to the Claude Code ecosystem through
   colour only. Verified at the time of writing: no Anthropic-branded asset, logo
   or wordmark exists anywhere in the repository.

## What is not covered here

This file records a trademark / nominative-fair-use risk, not a data-protection
one. There is no personal data processed by this feature, so the retention,
rights and consent fields the catalog's `legal.md` template expects for that case
do not apply — asserted, not omitted.

## Acceptance of the residual risk

Under the three mitigations above, the residual risk is acceptable. The
acceptance itself belongs to the project owner (tibs245), not to whoever writes
this file — recorded here on **2026-08-09** as the mechanism by which it takes
effect: **merging the PR that carries this file, if done by tibs245 himself, is
that acceptance.** If a PR in this flow is ever merged by an agent instead, an
explicit sign-off comment from tibs245 on the closing issue is required in its
place — a merge alone would not carry it.

The acceptance is conditional on mitigation 1's loose end — the hex still quoted
in `design/identity.md` — being resolved. The tracker, not this file, is where
that dependency between tickets is recorded. If either that item, or a future
change that adds a fourth stacking element (a claim of endorsement, a shared
name, an Anthropic asset), goes unresolved, this acceptance does not carry
forward automatically and the business role should be asked again.
