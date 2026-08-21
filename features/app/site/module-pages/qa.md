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

### AC-14 — `load_extends_map`'s default root tracks `ROOT`, and the deliberate asymmetry is named

```gherkin
Given `tools/build_site.py`'s `ROOT` reassigned at test time to a fixture tree
When `load_extends_map()` is called with no explicit `plugins_root`
Then it resolves against the reassigned `ROOT`, not against the value the
  module saw at import — every read of `ROOT` is computed at call time, the
  same way `skill_names()` already does

Given `extends_map_specials()`, which deliberately reads the real
  repository's `plugins/` regardless of any fixture context (to avoid
  regressing `tools/test_extends_map.py`)
When the function is read
Then it passes the root explicitly, and the "real repo" intent is named —
  a separately-named constant or parameter that says so, rather than
  relying on an import-time default to happen to still be correct

Given a single fixture build that exercises both call paths under one
  `run_fixture()`
When `tools/test_build_site.py` runs
Then the call that wants the fixture's `plugins/` reads the fixture, and
  the call that wants the real repo reads the real repo — both observable
  through the output, not by inspecting which module-level constant the
  call happened to bind
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

### AC-12 — A module page shows what it plugs into, derived and never declared

```gherkin
Given a module that opens registers, and modules that declare contributions to
  them
When that module's page is built, in every language
Then it names the registers it opens and the modules contributing to each, and
  the registers it contributes to and the module opening each — every row linked
  to its own page
And all of it is derived from what each module declares in its own
  `registers.json` and `extends.json`, with no field anywhere naming a relation
And a register a module opens that nobody contributes to is shown with `no
  contribution` in words, never omitted
And a module declaring neither file shows this section not at all, with no empty
  heading standing where the list would be
```

**A register with no contributor is shown.** Three of the twelve modules open one
today — `scrumia-discovery` (`scope-idea`, `split`), `scrumia-teams` (`sprint`),
`scrumia-design` (`design`) — and each teaches the mechanism for free.
`extends-map` AC-3 requires exactly this on the home page; two specs on one branch
must not rule opposite ways on the same fact. `modular-composition` BR-1 is the
authority: an empty register is an answer, not a failure.

Draw the absence with `slot-index`'s state machinery rather than a new one — dashed
leader, `--text-faint`, spelled out in words. Its spec gives the reason verbatim: a
missing row says *we forgot*, a dashed leader says *we decided*. Not the gap idiom,
which is reserved for a degradation; an unfilled register is not a loss.

**Derived from the modules' own declarations, not from this repository's
composition.** `scrumia-extends` answers for the modules a project runs; this
repository runs five of the twelve, so reading it would leave the modules an app
draws on showing nothing while they in fact declare contributions to
`implement`, `review` and `audit`.

This section says what is mechanically true and stops there. On today's twelve
modules it is absent only for `scrumia-core` and `scrumia-rules`, which declare
neither file — a correct answer and not a gap, and AC-13 is what a reader of those
two pages needs.

### AC-13 — A module page says what it goes well with, and cannot invent one

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

**The two sections take different forms, not different headings.** The derived half
is a table — register, direction, module — because the data is genuinely tabular and
runs from one row to seven, and `.table-wrap` already exists. The editorial half is
one prose sentence with inline links and no list at all. Two adjacent `<ul>`s
differing only in wording would hide the very distinction these two criteria spend
two paragraphs defending; prose against a table is legible at a glance, and each may
vanish alone without the page looking cut.

Module names in both sections are `--text` at rest and `--accent` on
`:hover`/`:focus-visible`, never accent at rest: seven links in one block, under a
section that already spends an accent rule, is the pointing-inflation
`design/identity.md` refuses. And neither section draws a module as `module-card` —
a reference to a module drawn heavier than the module the page is about.

The two sections answer different questions and neither is a rendering of the
other: AC-12 says who this module mechanically connects to, AC-13 says what to
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
