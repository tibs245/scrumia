# page-head

The opening of every page that is not the home page: a kicker naming the page's
role in the argument, the `h1`, and a lead paragraph. Introduced by #57 to carry
orbit's voice onto `workflow.html`, `reference.html` and `about.html`, which the
home page's hero does not reach.

## When to use it

Once per page, immediately inside `<main>`, on every page except `index.html` —
the home page has its own opening, `.hero`, and does not also get a `.page-head`.

Anatomy, in order:

- `.kicker` — mono, uppercase, `--text-faint`, preceded by a `--space-8`
  `--accent` dash. States the page's role in the argument, never the title
  again: "the run, in detail", not "workflow".
- `h1` — set at `--text-display`, the rung `tokens.css` reserves for exactly
  this: above the documentation `h1` size used inside a page's own sections.
  The home page's hero sets its `h1` at the same rung, so size no longer
  separates the two — the hero adds `--leading-hero` and `--tracking-hero`,
  which this block never takes.
- `.lead` — `--text-lg`, `--text-soft`, `max-width: var(--measure)`. Says what
  the page covers in one sentence a reader can skip past on purpose.

The block carries `.summon`, so it arrives the way the hero does: the page
opens on the same gesture everywhere on the site.

## When not to use it

- **On the home page.** `.hero` is index.html's own opening and is not a
  variant of this component — it carries the CTA row, the counts and Hop,
  none of which belong here.
- **Above a component's own preview**, this file included. A preview renders
  standalone; a `.page-head` on it would be a page-head pretending the preview
  is a page. Use a plain `<h1>` instead, as every other preview in this
  directory does.
- **Inside a section.** One per page, before the first `<section>`, never
  repeated lower down — a second one would compete with `section > h2::before`
  for the reader's sense of where the argument starts.

## What it refuses

- **The hero's `.eyebrow` pill.** That badge is the site's one call-out; a
  copy on three more pages spends it to nothing. `.kicker` is a different,
  quieter mark — a dash, not a pill — precisely so the two stay tellable apart.
- **`h2` at `--text-display`.** That would split the site's section rhythm in
  two: the home page's own sections sit at `--text-2xl`, and an inner page's
  sections have to match them, not the page's own opening.
- **Diluting a dense page.** `reference.html` is the hard case: its tables
  hold `--border`, `--text-faint` and mono headers at the density that makes
  them scannable, and `.page-head` is the only change that page gets — nothing
  about its tables, cards or spacing moves for this component to land.
