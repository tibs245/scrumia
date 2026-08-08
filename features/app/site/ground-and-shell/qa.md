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
- Which of the three `site-header` candidates wins. Until that is decided the
  masthead carries no scroll behaviour at all, which is the only honest default.
