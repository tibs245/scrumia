# Technical notes — Ground and shell

## The browser floor, and what happens below it

The palette is written with `light-dark()`, and the washes with `color-mix()`.
Both have been in every engine since 2024 — Chrome and Edge 123, Firefox 120,
Safari 17.5 — which is the floor this app targets. It is a deliberate bet, and
this is what it buys and what it costs.

**Below the floor, the page renders as unstyled default text**: an unsupported
`light-dark()` makes every `var(--token)` that carries it invalid at
computed-value time, so the property falls back to inherited or initial. Content,
layout, navigation and the no-JavaScript behaviour all survive; the identity does
not. Legible and complete, off-brand.

**There is no cheap fallback.** The invalidation happens where the `var()` is
substituted, not where the token is declared, so a `@supports` guard would have
to carry a second full palette — which is the duplication `qa.md` AC-1 exists to
prevent. Paying for a 2024 browser floor with the exact defect the ticket removed
is the wrong trade. If the floor ever has to drop, the answer is a build step
that expands the pairs, not a hand-maintained second copy.

## Why a theme change freezes every transition

`theme.js` sets `data-theme-switching` on the root, flips the theme, reads a
computed style to force the recalc, and clears the attribute on the next task.

The second reason is the load-bearing one. A theme flip changes only the used
`color-scheme`; the custom properties' text never changes. A transition already
running on a property whose value resolves through `light-dark()` is not
re-resolved by that flip, and the element keeps the previous theme's colour
permanently — observed on `.btn-primary`, whose `background` is transitioned.
Freezing transitions for the frame of the flip is what makes the toggle correct.

The synchronous style read is not dead code. Without it the attribute would be
removed before the new values were ever computed, and the freeze would do
nothing. If a build step is ever introduced, that statement has to be protected
from minification.

## Why nothing is hidden without an expiry

The `.js` gate proves that a script capable of un-hiding is running. It does not
prove that `motion.js` will ever arrive — the HTML can be delivered and the
connection drop before the deferred fetch completes, and a timeout living inside
that file would then never run. So the stylesheet that hides also un-hides: the
hidden state carries a delayed `unhide` animation as the un-hiding of last
resort. Any future rule that hides content must carry the same expiry.
