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

## Out of scope

- The hero, the slot index and the run (#60, #61, #62). This feature lands the
  ground they stand on and nothing that stands on it.
- The `site-header` rail's own behaviour (hover/focus tracking, reduced-motion
  fallback). The candidate is decided (#74, the rail) but not yet implemented
  (#112); until it lands the masthead carries no pointer behaviour at all,
  which is the only honest default in the meantime.
