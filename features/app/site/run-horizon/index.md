# Run horizon — the home page's run section

**Status**: active
**Stratum**: app (`site`)

## In brief

The `#flow` section of the home page: one reference run, seven steps, drawn as a
single hairline with human steps standing above it and agent steps hanging
below. It is the only section that encodes the human/agent colour rule and the
only one that spends `--page-wide`. Under it sit the legend and the three
moments — the same three human steps, named in prose.

Orbit replaced seven boxed columns with this line; the case for that is in #53.

## Links

- Business parent: none beyond the epic — the section renders content that
  belongs to `dev-flow` (see Authority below) but is not that feature's
  implementation.
- Authority: `design/identity.md`, decision 1 — inverted by #52 — which hue
  marks which actor.
- Authority: `design/components/run-horizon/spec.md` — how a step is drawn,
  and everything it refuses.
- Authority: `design/tokens.css` — the vocabulary.
- Authority: `features/business/dev-flow/index.md` — the seven steps rendered
  here.
- Authority: `design/explorations/orbit.html` — the direction this is built
  in, adopted by #53.

## Files present

| File | Read it when |
|---|---|
| `qa.md` | Checking the two-line budget, the ratio, the greyscale read, or the flare — before touching layout, copy or colour |
| `ux.md` | Touching the run's composition on the page, the legend, or the accessibility read without colour |
| `CHANGELOG.md` | Checking what changed in this feature and when |

No `business.md`: nothing here is specific to this app beyond what Links
already states — there is no business parent beyond the epic. No
`api-contract.md`, `archi.md`, `legal.md`, `devx.md`, `security.md`, `tech.md`:
nothing here exposes an interface, crosses an app boundary, touches personal
data, is consumable by another app, carries a rated risk, or holds a technical
choice specific to this feature beyond what the component spec already states.

## Open issues

- #186 — run-horizon names dev-flow as the authority for the seven steps,
  which it does not carry.
- #160 — The seven steps have no spec: three files point at dev-flow, which
  does not carry them.
- #103 — Judge the run's rail, now that it is what most screens see.
