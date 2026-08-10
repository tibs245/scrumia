---
name: sky-tokens-derivation
description: Sky tokens (#59) are color-mix() of themed tokens; per-theme strengths go through light-dark(color-mix(), color-mix()), never literals
metadata:
  type: project
  topic: site-sky-tokens
  source: agent
  stale_when: the four sky tokens stop being color-mix() derivations in design/tokens.css, or --halo-far gains its per-theme strengths
  cites: #59, design/tokens.css
---

The four sky tokens (--halo-near, --halo-far, --grid-line, --limb-glow) are single
color-mix() derivations of themed tokens (--accent, --agent, --border), replacing
orbit.html's per-theme literals. Dark #2660A8 (no-palette blue) was deliberately
re-read as --agent — "the far light is the one that labels".

**Why:** the design contract forbids inlined values; deriving from themed tokens means
the sky can never drift from the palette it claims to be made of.

**How to apply:** when a wash needs a *different strength per theme* (light usually
wants less), the sanctioned form is `light-dark(color-mix(...X%...), color-mix(...Y%...))`
— two strengths, still zero literals. Flagged in the #59 review for --halo-far, whose
single 14% is ~3× orbit's light-theme intent (5%).
