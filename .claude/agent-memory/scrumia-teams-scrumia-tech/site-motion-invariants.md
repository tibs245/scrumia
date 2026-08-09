---
name: site-motion-invariants
description: The site's .js pre-paint motion gate and the reduced-motion blanket rule's blind spot (animation-delay), plus the arrival-stagger nth-child coupling
metadata:
  type: project
---

Two invariants of `site/assets/style.css` motion system that reviews keep needing:

1. **The `.js` gate is the reduced-motion story.** The inline script in
   `site/templates/partials/head.html` adds `.js` to the root only when
   `prefers-reduced-motion` is NOT set and IntersectionObserver exists. Every
   hiding/arrival rule is gated on `.js`, so no-JS and reduced-motion readers get
   the complete page on first paint. Explicit `animation: none` overrides inside
   `@media (prefers-reduced-motion: reduce)` are NOT dead weight: they cover the
   mid-session OS toggle (`.js` is never removed once set), and the blanket rule
   zeroes `animation-duration` but **not `animation-delay`** — so any `both`-fill
   animation with a delay would show its from-state during the delay. House
   pattern: each animated subsystem adds its own `animation: none` in that media
   query (see `.js .summon > *` and `.hop-seg, .hop-eye`).

2. **Arrival stagger is coupled to DOM child count.** `.js .hero.is-in > *:nth-child(n)`
   selectors assign `--i` per child; adding/removing a direct child of `.hero`
   (or `.flowmap`/`.slots`) silently shifts the stagger. Decoration goes in
   `::before`/`::after` precisely to avoid becoming a counted child — the
   `.hero::after` limb comment says so.

**Why:** established reviewing #60 (hero); both points look like redundancy or
free-to-change DOM until you know the gate's semantics.
**How to apply:** when reviewing any `site/` change that adds children to a
`.summon` container or touches animations, check the nth-child block (~line 765)
and require the per-subsystem reduced-motion override for delayed animations.
