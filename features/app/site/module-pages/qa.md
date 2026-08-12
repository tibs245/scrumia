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

### AC-10 — The reference page's module sections are reachable too

```gherkin
Given the reference page's `#modules` section, in both languages
When a reader looks at one of its twelve `<code>module-name</code>` headings
Then the heading links to its own `modules/<name>.html`
And a reader who followed `module.html`'s back link (`{{@lroot}}reference.html`)
  can complete the round trip back to the module they left, not just to the
  section they landed on
```

### AC-11 — The reference page's link is generated too

```gherkin
Given the twelve module heading links on the reference page
When their `href` is traced to its source
Then each comes from `@modlink_<name>`, the same special AC-9 already covers
And no literal `href="modules/…"` string is typed into the reference template
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

### AC-8 — A module page shows what it plugs into, derived and never declared

```gherkin
Given a module that opens registers, and modules that declare contributions to
  them
When that module's page is built, in every language
Then it names the registers it opens and the modules contributing to each, and
  the registers it contributes to and the module opening each — every row linked
  to its own page
And all of it is derived from what each module declares in its own
  `registers.json` and `extends.json`, with no field anywhere naming a relation
And a module declaring neither shows this section not at all, with no empty
  heading standing where the list would be
```

**Derived from the modules' own declarations, not from this repository's
composition.** `scrumia-extends` answers for the modules a project runs; this
repository runs five of the twelve, so reading it would leave the implementation
and practice modules showing nothing while they in fact declare contributions to
`implement`, `review` and `audit`.

This section says what is mechanically true and stops there. On today's twelve
modules it is empty for `scrumia-core`, `scrumia-rules` and `scrumia-discovery`,
which is a correct answer and not a gap — AC-9 is what a reader of those pages
needs.

### AC-9 — A module page says what it goes well with, and cannot invent one

```gherkin
Given a module whose usefulness alongside another is not expressed by any
  register — the kernel every composition needs, or a format written for
  implementation modules that declares no contribution
When its page is built
Then it carries a short editorial line naming those modules and the situation
  that calls for them, each linked to its own page
And a module naming one that does not exist fails the build rather than
  rendering a dead link
And a module with nothing to say carries no such section, with no empty heading
  standing where it would be
```

The two sections answer different questions and neither is a rendering of the
other: AC-8 says who this module mechanically connects to, AC-9 says what to
install beside it. Only the second is what a reader arriving at
`scrumia-rules` — which declares nothing and exists precisely for implementation
modules — came to find out.

The editorial line lives with the other language-neutral module facts, keyed by
plugin name, where the builder already fails on an unknown name.

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
