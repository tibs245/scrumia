# Tech — Hero

## Structure

Hop arrives once, and does not loop: `.hop-arrive` (the arrival animation) plays only
on the `.js` class, and that class is set by the inline pre-paint script in
`site/templates/partials/head.html` — the only code that runs before first paint. The
script adds `.js` only when `IntersectionObserver` exists and `prefers-reduced-motion`
is not set. What a reader sees when the class is withheld — no JavaScript, a failed
script, or reduced motion — is `ux.md`'s States, tested by `qa.md` AC-4 (a11y); this
file stops at the gate's mechanism. This is the site-wide gate applied to Hop
specifically; the gate's own mechanism, and its use for the rest of the hero's
`.summon` elements, is `ground-and-shell`'s concern. The general "no loop on a real
page" rule is `design/components/hop/spec.md`'s (`.hop-loop` is preview-only), cited
rather than restated here.

## Debt

The three counts in `.counts` (slots, modules shipped, human touchpoints) are
literals, not values computed from `.claude-plugin/marketplace.json` and
`.scrumia/config.yaml`. Debt assumed 2026-08-09, exit condition: until the
counts are computed from the manifests (`site/templates/index.html`, inline
comment next to the numbers).

The manifest enumerator has since landed, along with the per-module pages —
not a recount of the hero's own counts. The debt is unpaid: the numbers are
still literals, and no open issue currently tracks migrating them. This is a
gap, not a resolved item — the comment in `site/templates/index.html` needs
a live issue number in place of the closed one, or the derivation done
outright.
