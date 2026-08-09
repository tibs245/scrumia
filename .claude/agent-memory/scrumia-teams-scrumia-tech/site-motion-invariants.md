---
name: site-motion-invariants
description: The site's .js pre-paint motion gate, the reduced-motion blanket rule's animation-delay blind spot, and the fact that .summon fades every direct child including decoration
metadata:
  type: project
---

Three invariants of `site/assets/style.css` motion system that reviews keep needing:

1. **The `.js` gate is the reduced-motion story.** The inline script in
   `site/templates/partials/head.html` adds `.js` to the root only when
   `prefers-reduced-motion` is NOT set and IntersectionObserver exists. Every
   hiding/arrival rule is gated on `.js`, so no-JS and reduced-motion readers get
   the complete page on first paint. Explicit `animation: none` overrides inside
   `@media (prefers-reduced-motion: reduce)` are NOT dead weight: they cover the
   mid-session OS toggle (`.js` is never removed once set), and the blanket rule
   zeroes `animation-duration` but **not `animation-delay`** - so any `both`-fill
   animation with a delay would show its from-state during the delay. House
   pattern: each animated subsystem adds its own `animation: none` in that media
   query (see `.js .summon > *` and `.hop-seg, .hop-eye`). Watch specificity when
   adding the override: `.js .run-track.summon.is-in > .step > .step-mark` (0,6,0)
   outranks the reduced-motion reset `... > .step > *` (0,5,0), so the reset does
   not actually neutralise it.

2. **Arrival order is per-container.** `.hero` and `.slots` assign `--i` with
   `nth-child` selectors, so adding/removing a direct child silently shifts the
   stagger; `.run-track` instead carries `style="--c:n; --i:n"` inline on each
   `.step` (#62) and is immune. Prefer the inline form when adding a container.

3. **`.js .summon > *` fades EVERY direct child, decoration included.** A
   container that mixes content children with a drawn element (a rule, a line, a
   spine) animates the decoration with the full `summon` keyframe -
   `translateY(10px) scale(0.985)` - while any child given a fade-only override
   stays put, and the two visibly desync. Found on `.run-horizon` reviewing #62.
   Fix pattern: exempt the decoration in the same rule that exempts the
   pass-through wrapper, or give it `animation-name: land` (fade only).

Layout note from the same review: `.run`'s `@media (min-width: 1440px)` breakout
(`width: var(--page-wide); margin-inline: calc((100% - var(--page-wide)) / 2)`)
reduces algebraically to `left = (viewport - --page-wide) / 2` - independent of
`--page-max` and of `main`'s padding, but it depends on `main { margin: 0 auto }`
and on the media threshold staying >= `--page-wide` + 2 gutters. Verified in
headless Chrome at 1439/1440/1441/1920.

**Why:** points 1-2 established reviewing #60 (hero), point 3 reviewing #62 (run
horizon); all three look like redundancy or free-to-change DOM until you know the
gate's semantics.
**How to apply:** when reviewing any `site/` change that adds children to a
`.summon` container or touches animations, check what the generic
`.js .summon > *` pair at ~line 900 sweeps up, and require the per-subsystem
reduced-motion override for delayed animations.
