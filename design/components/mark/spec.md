# mark

A frozen swatch of the dark theme, not a themed graphic. `site/assets/mark.svg`
draws three slots — two filled, one deliberately empty and outlined — on the
navy ground. Navy is the product's true ground; the light theme is the same
page seen in daylight, and the mark is the piece of the page that remembers
what it's built on. On the cream masthead it therefore reads as a navy tile.
That is the signature, chosen rather than inherited (#76).

The four shapes are the dark-theme `light-dark()` values of three tokens,
spelled as literal hex because the mark does not consult `tokens.css` at
render time:

| Shape | Hex | Token (dark value) |
|---|---|---|
| Ground tile | `#000B1C` | `--ground` |
| Filled slot ×1, empty-slot outline | `#3B7CAD` | `--border-strong` |
| Filled slot ×1 | `#73E3FF` | `--accent` |

## Why it does not theme

Both places the mark appears load the SVG as an external document — the
favicon `<link>` and the masthead's `<img src>` — and an externally loaded
SVG sees the reader's OS-level `prefers-color-scheme`, never the page's own
`data-theme` toggle. If the mark repainted with `light-dark()`, it would
follow the OS setting while the rest of the page follows the toggle: one
mark, two behaviours, visibly disagreeing with itself for exactly the reader
who reaches for our own switch. The favicon can never be fixed this way — a
`<link rel="icon">` has no path into the main document's cascade, data URI
or external file. A static mark can't disagree with itself, in either place.

Contrast is theme-independent for the same reason the mark is: the tile
carries its own ground. `#3B7CAD` on `#000B1C` is ≈4:1, `#73E3FF` well above
— both clear the 3:1 graphics-object minimum in either theme, at 22px and in
a tab.

## Where it appears

Exactly two places, same file both times:

| Placement | Class / attribute | Size |
|---|---|---|
| Masthead, inline | `.brand-mark` | 22px |
| Favicon | `<link rel="icon">` | browser chrome size |

## What it refuses

- **Theming.** No `light-dark()`, no `currentColor`, no light/dark variant.
  These four shapes are the one sanctioned freeze of token values in the
  whole system — everywhere else, a literal colour outside `tokens.css` is a
  finding. Repainting the mark is a design decision taken in this file, not
  a find-and-replace against a token rename.
- **The actor colours.** `--human` and `--agent` never enter the mark. The
  three slots are composition — two modules filled, one open — not a duel
  between the two actors, and coral in a logo crosses the line
  `identity.md` § "What coral costs" exists to hold.
- **New placements without review.** A third usage cites this file first.
  Below 16px the dashed empty-slot outline closes up and the mark stops
  making its argument — the outlined slot is the point, not a gap in the
  drawing.
