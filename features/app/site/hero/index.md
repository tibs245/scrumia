# Hero — the static site

**Status**: active
**Stratum**: app (`site`)

## In brief

The first thing a reader sees: an eyebrow, a three-line architecture-scale headline,
one sentence of lead copy, one filled control, Hop's first appearance on the site, and
three counts that state the shape of the composition. Everything below the fold is a
different feature's scope.

## Where the authority sits

| Question | Answered by |
|---|---|
| What should someone feel? | `design/identity.md` |
| Which values may be used? | `design/tokens.css` — the vocabulary |
| What does Hop look like, and when may it move? | `design/components/hop/spec.md` |
| Which direction is the hero built in? | `design/explorations/orbit.html`, adopted by #53 |

`site/assets/tokens.css` is generated from `design/tokens.css` by `tools/build_site.py`
and is never edited by hand. `site/assets/style.css` consumes those tokens; the hero
section holds no literal colour, spacing or duration of its own.

## The rules this feature owns

**The headline breaks are authored, not computed.** At `--text-hero` scale a line
break is a composition decision: `hero_title` carries `<br>` where the line should
end, in both languages, and no CSS `text-wrap: balance` substitutes for that choice.

**Exactly one filled control shows in the hero.** `.btn-primary` marks the one thing
the page wants a reader to do; every other control in the hero is `.btn-ghost` or
carries no fill at all.

**The hero never spends `--human` or `--agent`.** Only `--accent`, `--text` and the
surfaces — the human/agent colour rule is a different feature's decision (#52) and the
hero does not anticipate it either way.

**Hop arrives once, and does not loop.** `.hop-arrive` plays on the `.js` class alone —
the same pre-paint gate the rest of the shell uses — so Hop is assembled and lit on
the first frame for a reader with no JavaScript, a script that failed, or
`prefers-reduced-motion`.

**A count in the hero is derived, or its debt is dated.** Today's three counts (slots,
modules shipped, human touchpoints) are literals because #65 (the manifest enumerator)
has not landed; the debt is written as a comment in `site/templates/index.html` next
to the numbers, dated, and names the issue that resolves it.

## Files present

| File | Why it exists |
|---|---|
| `qa.md` | The criteria the hero must keep passing — both languages, every width |
| `CHANGELOG.md` | History of changes to this spec |

No `business.md`: the copy decision is recorded here and in the ticket, and there is
no business parent beyond the epic. No `ux.md`: `design/explorations/orbit.html` and
`design/identity.md` already carry the interaction intent, and duplicating it here
would drift the day one of them changes. No `api-contract.md`, `archi.md`, `legal.md`,
`devx.md`: nothing here exposes an interface, touches personal data or changes how the
project is built.

## Open issues

- #65 — Enumerate modules from the manifests and generate their pages. When it lands,
  the hero's three counts stop being literals.
