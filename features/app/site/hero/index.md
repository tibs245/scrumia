# Hero — the static site

**Status**: active
**Stratum**: app (`site`)

## In brief

The first thing a reader sees: an eyebrow, a three-line architecture-scale headline,
one sentence of lead copy, one filled control, Hop's first appearance on the site, and
three counts that state the shape of the composition. Everything below the fold is a
different feature's scope.

## Links

- Business parent: none beyond the epic. The copy decision itself is recorded in
  `ux.md` and the ticket, not a dedicated `business.md`.
- Authority: `design/identity.md` — what someone should feel in the first three
  seconds, and decision 2 ("motion means causality") for the ring's arrival order.
- Authority: `design/tokens.css` — the vocabulary; the hero holds no literal colour,
  spacing or duration of its own.
- Authority: `design/components/hop/spec.md` — Hop's states, sizes and what it
  refuses.
- Authority: `design/components/button/spec.md` — the one-primary rule: one
  `.btn-primary` per screen, not per section.
- Authority: `design/explorations/orbit.html` — the direction the hero is built in,
  adopted by #53.

## Files present

| File | Read it when |
|---|---|
| `qa.md` | Checking or writing a test for the hero — both languages, every width |
| `ux.md` | Touching what the hero shows, its reading order, or its arrival motion |
| `tech.md` | Touching the Hop arrival gate or the counts' derivation/debt |
| `CHANGELOG.md` | Checking what changed in this feature and when |

No `business.md`: nothing here is specific to this app beyond what Links already
states — there is no business parent beyond the epic. No `api-contract.md`,
`archi.md`, `legal.md`, `devx.md`, `security.md`: nothing here exposes an interface,
crosses an app boundary, touches personal data, is consumable by another app, or
carries a rated risk.

## Open issues

None currently open.
