# QA — module pages

Covered by `tools/test_build_site.py` (`python3 tools/test_build_site.py`), run in CI
alongside `tools/validate.py` and the build itself.

## AC-1 — the pages generate from one template and one fact source

One page per module per language exists in the published tree, and every one of them
carries the facts derived from the manifest (install command, source link). There is one
`site/templates/module.html`, not one template per module. Twelve modules × two
languages = twenty-four pages today; neither number appears in the builder.

## AC-2 — a gap in the prose fails the build

Three failures, each verified on a throwaway fixture rather than asserted:

- a string the template needs, present in one language and absent in the other
- a plugin the manifest declares with no i18n module file, in either language
- an i18n module file naming no plugin of the marketplace

## AC-3 — exactly one file declares the emoji

`site/modules.json` is the only source that assigns an emoji to a module: the manifest,
the templates and the i18n files restate none of them. The twelve are distinct, and the
build fails on a reused emoji, on a plugin with no entry, and on an entry naming no
plugin.

The site favicon is out of this rule's scope — it is the site's own mark, and that it
currently reuses the same glyph as one module is a coincidence for the designer to
settle, not a second declaration.

## AC-4 — the sitemap covers the generated pages

Both language URLs of every module appear in `site/sitemap.xml`.

## AC-5 — testable with a stub template

The builder is proven against a fixture whose template carries the tokens and nothing
else, which is what makes this feature independent of the design work.

## AC-6 — a malformed page string file is reported, never raised

`render_page`'s unused-key check reads the same `site/i18n/<lang>/<page>.json` that
`load_strings` already parsed under a `try`. An invalid file is reported once, by
`load_strings`, as a clean `error:` line — never as a raw traceback from the check.

## AC-7 — a manifest fact interpolated into markup is escaped

`@mod_tags` and `@mod_skills` build markup out of names sourced from
`marketplace.json` and the skills tree. Every fact placed inside an HTML tag or
attribute is HTML-escaped before interpolation, the same way a template engine would
escape it by default — regardless of how trustworthy today's fixed set of entries is.
