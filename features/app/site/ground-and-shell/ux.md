# UX — Ground and shell

## Interface constraints

**The ground is lit, not filled.** The page sits on a fixed two-wash halo — near
and far — standing for one cold light source behind it, plus a masked grid that
belongs to peripheral vision and disappears wherever text sits. The page scrolls
past the light rather than carrying it: the halo does not move with the content.
Both washes are `color-mix()` derivations of themed tokens, never a flat fill — the
values themselves are `design/tokens.css`'s (`--halo-near`, `--halo-far`,
`--grid-line`), not restated here.
