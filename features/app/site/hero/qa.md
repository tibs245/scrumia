# Acceptance criteria — Hero

One scenario per rule in `ux.md` and `tech.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — The hero renders from the build, in both languages, with the breaks holding at every width

```gherkin
Given the site built by `tools/build_site.py`
When the English and French home pages are read
Then the hero renders with no unresolved template token
And the headline's authored `<br>` breaks land in the same place regardless of
  viewport width — nothing is re-wrapped by `text-wrap: balance`
```

### AC-2 — Exactly one filled control shows in the hero

```gherkin
Given the rendered hero
When every control inside it is inspected
Then exactly one carries `.btn-primary`, and no other element in the hero's
  viewport is filled with the accent colour
```

### AC-5 — The hero spends only `--accent`, `--text` and the surfaces

```gherkin
Given the rendered hero
When every element inside it is inspected for the colour it spends
Then no element uses `--human`, `--human-surface`, `--agent` or `--agent-surface`
And only `--accent`, `--text`, `--ground` and the surface tokens appear
```

## Edge cases

### AC-3 — A count is derived, or its debt is dated

```gherkin
Given the three numbers in `.counts`
When their source is checked
Then either they are computed from `.claude-plugin/marketplace.json` and
  `.scrumia/config.yaml`, or a dated comment naming the issue that will compute
  them sits next to the numbers in `site/templates/index.html`
```

### AC-4 — Hop arrives once and respects reduced motion (a11y)

```gherkin
Given a reader with JavaScript enabled and no reduced-motion preference
When the hero loads
Then the ring (`.hero-figure`) is visible from the first frame, not faded in with
  the rest of the hero
And Hop's segments and eye animate in once inside it, gated by the same `.js`
  class the shell's pre-paint script sets, and never repeat
And the eyebrow, headline and lead fade in after the ring, never before it

Given a reader with JavaScript disabled, or `prefers-reduced-motion: reduce`
When the hero loads
Then Hop is already assembled and its eye is already lit — nothing travels
```

### AC-6 — The headline's claim matches the composition the page goes on to describe

```gherkin
Given the rendered headline and the sections that follow it on the same home page
When the model the headline states is compared against the model `#slots` and
  `#extends` (or whichever sections describe the composition at the time) actually
  show
Then the headline names no capability, count or relationship that those sections
  contradict
And a headline that still reads "every capability is a slot" fails this criterion
  once any section on the same page describes a capability filling no slot
```

## Out of scope

- The slot index and the run, and everything below the hero — owned by
  `features/app/site/slot-index/` and `features/app/site/run-horizon/`. This
  feature lands only the hero.
- Which of the three `site-header` candidates wins, and the human/agent colour
  rule — owned by `features/app/site/ground-and-shell/` — the hero uses
  neither `--human` nor `--agent`.
