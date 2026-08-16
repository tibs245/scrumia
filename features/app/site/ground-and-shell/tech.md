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

## Token discipline this feature answers to

`design/tokens.css` already states two of this feature's governing rules, so they
are cited here rather than repeated: a theme is a token redefinition, written once
per token as a `light-dark()` pair (top-of-file comment); the sky is scenery, not
an actor, so `--halo-far` is mixed from `--sky` rather than from `--human` or
`--agent` (the `--sky` comment). `design/identity.md` states the third: `--human`
sits at least 35° of OKLab hue and ΔE 8 from `--accent`, enforced by
`tools/check_contrast.py` — the corollary to identity decision 4, because the one
thing marking a person's decision must never be read as the thing that points.

This feature adds one more, not yet stated elsewhere: **no value is a literal
restatement of another token.** A wash, a glow or a rim light derived from the
accent is written as a `color-mix()` of `--accent` (`--glow-accent`, `--halo-near`,
`--limb-glow`), never as that accent's hex spelled out again. A derivation copied
by hand stops being a derivation the moment the source token moves — `--glow-accent`'s
own comment names this as the reason it exists.

## The theme is resolved before first paint

The saved choice is applied by an inline script in `<head>`, not by `theme.js` —
the deferred file only owns the toggle control afterward. `<head>` is the only
point in the load before anything has painted, so it is the only point where the
saved theme can be applied without a flash of the wrong one. `theme.js` documents
the same split at the point where a reader could otherwise expect the deferred
file to do this.

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

**Nothing is hidden by CSS that JavaScript has to un-hide.** Every rule that hides
something is gated on `.js`, a class the inline `<head>` script sets before first
paint — the same script that can also un-hide, and only when the reader has not
asked for reduced motion (`style.css`'s "Motion" comment). No JavaScript, a failed
script, an old browser, or `prefers-reduced-motion`: the class is absent, nothing
matches, and the page renders complete rather than blank.

The `.js` gate proves that a script capable of un-hiding is running. It does not
prove that `motion.js` will ever arrive — the HTML can be delivered and the
connection drop before the deferred fetch completes, and a timeout living inside
that file would then never run. So the stylesheet that hides also un-hides: the
hidden state carries a delayed `unhide` animation as the un-hiding of last
resort. Any future rule that hides content must carry the same expiry.

## No browser script is executed by CI, and what closes that gap instead

Nothing in `.github/workflows/validate.yml` runs `composer.js`, `header.js`,
`motion.js`, `theme.js`, or the inline `<script>` that `partials/head.html`
ships into every built page — every gate reads them as text
(`tools/test_composer.py` lifts table literals with a regex) or not at all. What CI does guarantee is the
no-JS floor: `qa.md` AC-4 here, and the composer's own `qa.md` AC-3 last line —
each page and each pre-rendered artifact is complete without a script running.
Above that floor, a change to `configParts()`, to the inline theme/`.js`-gate
script, or to any other script's runtime behaviour ships green even when
broken.

The gap is accepted, not closed, and bounded to one check, itself only over
`site/assets/*.js` — the inline `<head>` script is not covered either: `node
--check` on every file in `site/assets/*.js`, run one file at a time — a single
glob argument makes `--check` silently stop after the first file and still
exit 0, which would be the false-green this step exists to remove. That buys
"the file parses," nothing about what it does when it runs, and Node parses a
syntax superset of the browser floor above (Chrome/Edge 123, Firefox 120,
Safari 17.5), so a passing check is not a promise the file runs in Safari.

A DOM stub or a `node --test` suite executing `configParts()` was considered and
rejected: the DOM surface these scripts touch (`querySelector`, `:checked`,
`closest`, `dataset`, the `createElement`/`appendChild` tree `composer.js`
builds) is enough that a no-dependency stub becomes a small selector engine —
an artifact more likely to mis-report a passing script than the code it tests.
Generating the composer's pre-rendered blocks from the same source
`composer.js` reads was considered too, and rejected for the same reason from
the other direction: it would collapse two independently-maintained statements
into one, turning `tools/test_composer.py`'s AC-3 checks into tautologies.

**Reopening trigger.** A second app shipping browser JavaScript, or the composer
coming to own something a no-JS reader cannot get either way: at that point the
answer is a real browser (Playwright), never a hand-rolled DOM stub.
