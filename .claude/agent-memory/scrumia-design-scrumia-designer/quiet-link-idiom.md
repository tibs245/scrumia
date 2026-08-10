---
name: quiet-link-idiom
description: Site links are accent+underline by default; .mod-name is the one deliberate exception (text-coloured, underline only) because .mod-slot already carries the card's accent
metadata:
  type: project
  topic: site-link-styling
  source: agent
  stale_when: a second instance appears and the idiom is promoted to design/identity.md, or .mod-name stops being the only text-coloured link in site/assets/style.css
  cites: #70, #197, design/components/module-card/spec.md
---

`site/assets/style.css` styles every link as `a { color: var(--accent) }` plus the UA
underline (no `text-decoration: none` reset except on nav, `.btn`, `.skip-link`,
`footer a`). `a.mod-name` (#70) is the first link that keeps `color: var(--text)` at
rest and takes `--accent` only on `:hover`/`:focus-visible`.

**Why:** identity decision 4, "one accent — if two things on a screen are pointing,
neither is". On the module card the accent is already spent on `.mod-slot`, which sits
directly under `.mod-name` in the same `.mod-id` stack. Accenting the name would put
two cyans two lines apart and the slot label would stop pointing.

Note the reasoning recorded in `design/components/module-card/spec.md` and the CSS
comment both credit `.mod-cmd` with the accent — `.mod-cmd` is `--text-soft` on
`--surface-sunken`, it carries none. The conclusion is right, the element named is wrong — **#197**.

**How to apply:** a text-coloured underlined link is a legitimate ScrumIA idiom, but only
where an adjacent element already holds the accent. Anywhere else, links are accent.
If a second instance appears, promote it from a per-component comment to a rule in
`design/identity.md` or a `link-quiet` entry in the components dir — right now the
pattern has one instance and no home in the system. See [[sky-tokens-derivation]] for the
other case where a rule lives in a derivation rather than a token.
