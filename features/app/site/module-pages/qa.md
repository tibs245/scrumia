# Acceptance criteria — Module pages

One scenario per rule in `tech.md`. Each scenario must be able to fail.

Covered by `tools/test_build_site.py` (`python3 tools/test_build_site.py`), run in CI
alongside `tools/validate.py` and the build itself.

## Nominal

### AC-1 — The pages generate from one template and one fact source

```gherkin
Given the marketplace manifest and the twelve modules it declares
When the site is built for English and French
Then one page per module per language exists in the published tree, each
  carrying the facts derived from the manifest — install command, source link
And there is one `site/templates/module.html`, not one template per module
And neither the module count nor the language count appears in the builder
```

### AC-3 — Exactly one file declares the emoji

```gherkin
Given a module's emoji
When the build reads it
Then `site/modules.json` is the only source that assigns it — the manifest,
  the templates and the i18n files restate none of them
And the twelve emoji are distinct

Given a plugin with no `site/modules.json` entry, or an entry naming no
  plugin, or an emoji reused across two modules
When the site is built
Then the build fails
```

### AC-4 — The sitemap covers the generated pages

```gherkin
Given the twenty-four generated module pages
When `site/sitemap.xml` is read
Then both language URLs of every module appear in it
```

### AC-8 — Every module is reachable from the site's navigation

```gherkin
Given the index page's `#modules` section, in both languages
When a reader looks at one of its twelve module cards
Then the card links to its own `modules/<name>.html`
And a reader lands on a module page without typing a URL — being listed in
  the sitemap (AC-4) is not, on its own, a way in
```

### AC-9 — The link is generated, not hand-written

```gherkin
Given the twelve module card links on the index page
When their `href` is traced to its source
Then each comes from `@modlink_<name>`, a special the builder computes from
  the same enumeration as `@emoji_<name>` — one function producing a URL per
  module name
And no literal `href="modules/…"` string is typed into the template
```

## Edge cases

### AC-2 — A gap in the prose fails the build

```gherkin
Given a string the template needs, present in one language and absent in the
  other
When the site is built
Then the build fails

Given a plugin the manifest declares with no i18n module file, in either
  language
When the site is built
Then the build fails

Given an i18n module file naming no plugin of the marketplace
When the site is built
Then the build fails

Given a page-level string a language carries that no template references
When the site is built
Then the build fails — leftover prose is a gap the same way a missing string
  is, just on the other side of the count
```

### AC-5 — Testable with a stub template

```gherkin
Given a fixture template that carries the tokens the builder expects and
  nothing else
When the builder is run against it in `tools/test_build_site.py`
Then the build succeeds independently of any design decision, proving the
  generation logic without depending on the redesign work
```

### AC-6 — A malformed page string file is reported, never raised

```gherkin
Given a `site/i18n/<lang>/<page>.json` that fails to parse
When `load_strings` reads it under its `try`, and `render_page`'s
  unused-key check reads the same file afterward
Then the failure is reported once, by `load_strings`, as a clean `error:`
  line
And no raw traceback from the unused-key check reaches the build output
```

### AC-7 — A manifest fact interpolated into markup is escaped

```gherkin
Given `@mod_tags` and `@mod_skills`, built from names sourced from
  `marketplace.json` and the skills tree
When those names are placed inside an HTML tag or attribute
Then each one is HTML-escaped before interpolation, the same way a template
  engine would escape it by default — regardless of how trustworthy today's
  fixed set of entries is
```

## Out of scope

- The site favicon's emoji is not `site/modules.json`'s concern — AC-3 governs
  a module's emoji, not the site's own mark; that it currently reuses the
  same glyph as one module is a coincidence for the designer to settle, not a
  second declaration.
- Chrome strings shared across pages (`common.json`) are out of AC-2's unused
  half: some are read programmatically rather than through a `{{token}}`
  (`mod_no_slot`, pulled from `labels` by `module_specials`), so an
  unused-key check over `common.json` would fail on a string that is in fact
  used — left open on purpose, per `tech.md`.
