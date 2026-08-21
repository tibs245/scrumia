# Ground and shell — the static site

**Status**: active

## In brief

Everything on the site that is not a section: the token vocabulary the pages are
written in, the lit ground they sit on, and the chrome that wraps them — masthead,
footer, skip link, theme toggle, arrival gate.

## Links

- No Business parent — purely technical, per `business.md`'s App rule.
- Authority:
  - `design/identity.md` — what someone should feel, and the accent-hue-distance
    rule for actor colours (the corollary to decision 4)
  - `design/tokens.css` — the vocabulary; owns "a theme is a token redefinition",
    "the sky is scenery, not an actor", and the ground's two-wash light
  - `design/components/site-header/spec.md` — what the top bar does, rail included
  - `design/components/label-register/spec.md` — the mono, uppercase, faint
    register that names what the nearby controls are for; its five call sites
    consume it rather than restate it
  - `design/explorations/orbit.html` — the direction adopted during the redesign
  - `tools/check_contrast.py` — the runnable form of `qa.md` AC-6; lives at the
    repo root, outside this feature

## Files present

| File | Read it when |
|---|---|
| `qa.md` | The criteria the shell must keep passing — both themes, both directions, no-JS |
| `tech.md` | The browser floor this bet needs, and the mechanisms that look like tricks |
| `ux.md` | What the ground looks like as scenery, not as tokens |
| `legal.md` | The trademark / affiliation risk the redesign's palette and mascot carry, its mitigations, and the owner's acceptance of what's left over |
| `business.md` | Checking the value this feature brings, and why it carries no business rule of its own |
| `CHANGELOG.md` | History of changes to this spec |

No `api-contract.md`, no `archi.md`: the site is one app that calls
nothing.
