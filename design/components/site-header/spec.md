# site-header

The bar at the top of every page: the mark, the wordmark, the navigation, the
language pair and the theme toggle.

**Status: shipped — the rail (#74, implemented in #112).** #59 shipped the
static bar described below; the rail is its one pointer treatment. The
rejected candidates, and the reasons they lost, live in ticket #74 — not in
this file.

## What ships

The baseline is the bar #59 delivered — `site/templates/partials/header.html`
and the Header section of `site/assets/style.css`. One line, sticky, and
translucent: the ground at 82% over the page, saturated and blurred behind it,
so the page visibly runs underneath. It is not a solid band and must not
become one.

- **Masthead** — `mark.svg` at 22px left of the wordmark, display face, the
  "IA" in accent cyan. The mark, not Hop: Hop is one per screen
  ([hop](../hop/spec.md)), and #60 gave its one arrival to the hero — a
  sticky header would drag a second lit eye over it on every scroll past the
  fold. The masthead also sits below Hop's 28px floor, which is exactly the
  case hop/spec.md names the mark's fallback for.
- **Bottom edge** — a 1px gradient lit from the wordmark outward: accent at
  55%, fading through the border colour to transparent inside the first
  third. It reads as light spilling from the brand, not as the lid of a
  container. This edge is also why there is no scroll-progress rule — see
  "What it refuses".
- **Navigation** — mono at `--text-sm`, resting at `--text-faint`, rising to
  `--text` when pointed at and on `aria-current="page"`. `--text-faint` is
  the floor: ~5.2:1 (light) / ~6.3:1 (dark) on the solid ground, and about
  4.9:1 at worst over the translucent bar — passing, without margin. Nothing
  in this header may render text dimmer than `--text-faint`.
- **Language pair and theme toggle** — mono at `--text-xs`, the current
  language in accent, the toggle a 30px pill. Both live inside the single
  line.
- Below 640px the navigation scrolls horizontally, scrollbar hidden, rather
  than wrapping — see "What it refuses".

## The rail

The one motion this header owns, and it is caused motion: a single cyan rail
under the navigation that slides to the link you point at or focus, and
slides home to the current page when you stop. It replaces the shipped
per-link underline for pointer users, because the shipped treatment
double-points — hover any link and the `aria-current` underline stays lit
beside the hovered one, two cyan marks in one bar, which is what identity
decision 4 forbids. The rail is one mark with one position, and its travel
shows the relation between where the reader is and where they are pointing.

Rules the implementation must keep — the component preview holds a working
reference for each:

- The rail serves the page links, GitHub included. It never chases the
  language pair or the theme toggle; those keep their own treatments.
- It takes its first position without a transition, and only then earns one.
  Animating in from zero width would say something arrived, and nothing did —
  the current page was already the current page.
- Placement waits for fonts to load, and must not depend on
  `requestAnimationFrame` firing (it never does in a background tab).
- Degradation is the baseline above, and the baseline is not a lesser
  header: no JS and touch render the static current-page underline exactly
  as #59 shipped it; `prefers-reduced-motion` keeps the rail but removes the
  travel — a position change is a state report, the easing is not.

## When not to use it

- **On a preview or a component page.** These render standalone, with no chrome;
  a header on them is a header pretending the component is a page.

## What it refuses

- **A second row.** Everything fits one line down to 640px, where the navigation
  scrolls horizontally rather than wrapping. A header that wraps has become a
  menu and should say so.
- **A call-to-action button.** The header routes; it does not sell. The hero owns
  the next step — see [button](../button/spec.md).
- **Hiding on scroll-down.** A header that disappears when you scroll is a header
  whose motion stands for nothing the reader asked for.
- **A scroll-progress rule.** Settled in #74: the lit bottom edge already
  owns that pixel row and its meaning, and the site's pages are too short
  for scroll position to be a state worth reporting. One line cannot say
  "where the light comes from" and "how far you have read" at once.
- **Motion the reader did not cause.** Also settled in #74: the looping
  scanline lost to identity decision 2. If a page should feel alive before
  the reader acts, that belongs to Hop in the hero — never to chrome
  repeated on every page.
