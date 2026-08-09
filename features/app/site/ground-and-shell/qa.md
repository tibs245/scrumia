# Acceptance criteria — Ground and shell

One scenario per rule in `index.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — Each theme's palette is written once

```gherkin
Given `design/tokens.css`
When a palette token's value is looked for
Then it appears exactly once per theme — as one `light-dark()` pair — and no
  `[data-theme]` block or `prefers-color-scheme` block restates it
```

### AC-2 — No literal value outside the vocabulary

```gherkin
Given `site/assets/style.css`
When it is read for colours, spacing rungs and durations
Then every one of them is a `var(--token)`, and the only literals left are the
  geometry of a single control that appears once
And every token `design/tokens.css` gained for this direction carries a comment
  saying what it is for, or it is not in the file
```

### AC-3 — Both themes are correct both ways

```gherkin
Given a reader whose system preference is dark, and one whose preference is light
When each of them loads the site and then presses the theme toggle
Then the page shows the theme they asked for in all four combinations, the choice
  survives a reload, and the toggle wins over the system preference in both
  directions
```

### AC-5 — The non-affiliation statement reaches every page, in both languages

```gherkin
Given `site/i18n/en/common.json` and `site/i18n/fr/common.json`
When the site is built by `tools/build_site.py`
Then both carry a `footer_non_affiliation` key — the build's anti-divergence
  guard fails otherwise — and the footer partial renders it on every built page,
  in the language of that page
```

### AC-6 — Every real pair is measured, and the two actors stay tellable apart

```gherkin
Given `design/tokens.css`
When `python3 tools/check_contrast.py` resolves both themes from its `light-dark()`
  pairs
Then every pair a page actually lays on another meets its WCAG 2.1 minimum — 4.5:1
  for body text, 3:1 for a boundary that carries meaning — in light and in dark
And `--human` sits at least 35° of OKLab hue and ΔE 8 away from `--accent`, so the
  colour that marks a person's decision can never be read as the colour that points
And the run exits non-zero when either fails
```

The hue floor is the half a contrast ratio cannot see: it is a luminance
measurement, and two colours a reader cannot tell apart can sit at 7:1.

AC-6 is enforced, not just stated: `python3 tools/check_contrast.py` runs as its own
step in the `validate` CI workflow, so a failing pair or hue floor goes red under its
own name, not under a generic marketplace check. The tool only measures the pairs it
is told about — it cannot see a consumer that lays one token on another for the first
time. Whoever introduces a new token-on-token pair in `site/assets/style.css` adds the
matching row to `PAIRS` in `tools/check_contrast.py`, in the same PR that introduces
the pair.

### AC-7 — The rail is the header's one accent mark

```gherkin
Given a reader with a hover-capable pointer, on any page with a current nav link
When they hover or focus a different nav link, then stop pointing at anything
Then the rail moves under the pointed-at or focused link, and slides back to the
  current page's link when they stop
And at no point are the rail and the static current-page underline both showing
  an accent mark at once
```

### AC-8 — Touch and no-JS keep the static underline

```gherkin
Given a reader on a touch device, or one whose script never ran
When they load a page with a current nav link
Then the header renders the current page with a static accent underline,
  exactly as #59 shipped it, and no rail element ever activates
```

## Edge cases

### AC-4 — The page is complete without JavaScript

```gherkin
Given a reader with JavaScript disabled, or whose script failed to run, or whose
  system asks for `prefers-reduced-motion: reduce`
When the page loads
Then every element is visible — nothing is left hidden waiting for a script that
  will never run
And no reader sees one theme painted and then replaced by another
```

### AC-9 — Reduced motion keeps the rail, not its travel

```gherkin
Given a reader whose system asks for `prefers-reduced-motion: reduce`, on a
  hover-capable pointer
When the page loads, and they hover or focus a nav link
Then the rail is at the correct position at every point — home on load, under
  the pointed-at link while pointing — with no animated transition between them
```

## Out of scope

- The hero, the slot index and the run (#60, #61, #62). This feature lands the
  ground they stand on and nothing that stands on it.
