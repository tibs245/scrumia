# Ground and shell — the static site

**Status**: active
**Stratum**: app (`site`)

## In brief

Everything on the site that is not a section: the token vocabulary the pages are
written in, the lit ground they sit on, and the chrome that wraps them — masthead,
footer, skip link, theme toggle, arrival gate.

**No Business parent, on purpose.** This feature is purely presentational: it
carries no business rule, only the rules that keep an interface honest across two
themes, two languages and a reader with JavaScript switched off. What the site
*says* belongs to the business features it renders; what it *looks like* belongs to
`design/identity.md`, which this feature implements rather than restates.

## Where the authority sits

| Question | Answered by |
|---|---|
| What should someone feel? | `design/identity.md` |
| Which values may be used? | `design/tokens.css` — the vocabulary |
| What does the top bar do? | `design/components/site-header/spec.md` |
| Which direction is the site being built in? | `design/explorations/orbit.html`, adopted by #53 |

`site/assets/tokens.css` is generated from `design/tokens.css` by
`tools/build_site.py` and is never edited. `site/assets/style.css` consumes those
tokens and holds no literal colour, spacing or duration of its own.

## The rules this feature owns

**A theme is a token redefinition, and each theme's values are written once.** The
palette is expressed with `light-dark()` under `color-scheme`, so the system
preference and the toggle read the same single definition. A palette written twice
drifts the first time someone adjusts one copy — the toggle then contradicts the
system preference, and nothing in the file shows it.

**No value is a literal restatement of another token.** A wash, a glow or a rim
light derived from the accent is written as a `color-mix()` of `--accent`, never as
that accent's own hex spelled out again. Derivations recomputed by hand stop being
derivations the moment the accent moves.

**Nothing is hidden by CSS that JavaScript has to un-hide.** The hiding is gated on
a class set by an inline script before first paint — the same script that can
un-hide. A reader with no JavaScript, a failed script, or `prefers-reduced-motion`
gets a complete page, never a blank one.

**The theme is resolved before first paint.** The saved choice is applied by an
inline script in `<head>`, not by an external file, so no reader sees the wrong
theme flash to the right one.

**The ground is lit, not filled.** A fixed two-wash halo and a masked grid stand for
one cold light source behind the page; the page scrolls past the light rather than
carrying it. The grid belongs to peripheral vision and is masked away wherever text
sits.

## Files present

| File | Why it exists |
|---|---|
| `qa.md` | The criteria the shell must keep passing — both themes, both directions, no-JS |
| `tech.md` | The browser floor this bet needs, and the two mechanisms that look like tricks |
| `legal.md` | The trademark / affiliation risk the redesign's palette and mascot carry, its mitigations, and the owner's acceptance of what's left over |
| `CHANGELOG.md` | History of changes to this spec |

No `business.md`: there is no business rule here, and no Business parent to
reference. No `api-contract.md`, no `archi.md`: the site is one app that calls
nothing. No `ux.md`: the sections own their own interaction, and none of them is
this feature.

## Open issues

- #60, #61, #62 — the hero, the slot index and the run. Each consumes the tokens
  this feature lands and is out of its scope.
- The `site-header` component still ships three candidates and no verdict; the
  shell renders none of the three scroll behaviours until that is settled.
