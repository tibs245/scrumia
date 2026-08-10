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

## Links

- No Business parent — purely technical, per `business.md`'s App rule.
- Authority:
  - `design/identity.md` — what someone should feel, and the accent-hue-distance
    rule for actor colours (the corollary to decision 4)
  - `design/tokens.css` — the vocabulary; owns "a theme is a token redefinition",
    "the sky is scenery, not an actor", and the ground's two-wash light
  - `design/components/site-header/spec.md` — what the top bar does, rail included
  - `design/explorations/orbit.html` — the direction adopted by #53
  - `tools/check_contrast.py` — the runnable form of `qa.md` AC-6; lives at the
    repo root, outside this feature

## Files present

| File | Read it when |
|---|---|
| `qa.md` | The criteria the shell must keep passing — both themes, both directions, no-JS |
| `tech.md` | The browser floor this bet needs, and the mechanisms that look like tricks |
| `ux.md` | What the ground looks like as scenery, not as tokens |
| `legal.md` | The trademark / affiliation risk the redesign's palette and mascot carry, its mitigations, and the owner's acceptance of what's left over |
| `CHANGELOG.md` | History of changes to this spec |

No `business.md`: there is no business rule here, and no Business parent to
reference. No `api-contract.md`, no `archi.md`: the site is one app that calls
nothing.

## Open issues

None currently open.
