# Tech — module pages

## Where each fact comes from

| Fact | Source | Why there |
|---|---|---|
| which modules exist | `.claude-plugin/marketplace.json` | the manifest is what a user installs from; a page the manifest doesn't know about would be a page nobody can install |
| name, version, tags | same entry | already declared, never retyped |
| skills | `plugins/<name>/skills/*/SKILL.md` | the directory is the list; a count would go stale, a hand-written list would lie |
| install command, source link | derived from the name | one rule, twelve pages |
| emoji, slot | `site/modules.json` | the manifest has no field for either — see below |
| everything else | `site/i18n/<lang>/modules/<name>.json` | prose, and prose is the only thing that has to exist twice |

The manifest is English-only, so it is the **fact** source and never the **prose**
source. That is why the module description shown on a page comes from the i18n file and
not from the manifest's own `description`: a French page carrying an English sentence
would be a divergence the build could not see.

Skill *descriptions* are left off the page for the same reason — the frontmatter that
carries them is English-only. #66 settled the call: the pages name the skills and stop
there. Describing each one would need a bilingual file of its own, and a module's
`SKILL.md` frontmatter already carries the description for whoever installs it.

## Why `site/modules.json` and not the manifest

The emoji and the slot are language-neutral facts about a module that the marketplace
schema has no field for. Putting them in `marketplace.json` was the preferred option and
was tested rather than assumed:

```
$ claude plugin validate --strict .claude-plugin/marketplace.json
  ❯ plugins[0].emoji: Unknown field 'emoji'. Claude Code ignores it at load time.
✘ Validation failed (--strict treats warnings as errors)
```

The runtime tolerates the field by ignoring it; the vendor's own validator classifies it
as unknown and `--strict` — the mode a marketplace author is told to run in CI — rejects
it. A repository whose product *is* a marketplace should not ship a manifest that fails
that check, so the two facts live in one file of our own instead, keyed by plugin name
and reconciled against the manifest at build time. Single-source is preserved by the
guard, not by the location.

`site/modules.json` is build input that sits inside the published tree, because Pages
serves `site/` alone and the build has no staging step. It is data, not a page.

## The guards

The existing anti-divergence guard is reused, not reimplemented: module pages go through
the same `load_strings` / `render` path as every other page, so a key present in English
and absent in French fails the build exactly as it always has. That guard now covers both
directions of the same gap: a page-level string an i18n file carries that no template
reads fails the build too (#114) — previously a warning, which is how a leftover key
(`composer_js_strings`, deleted by #114) sat unnoticed.

The unused half stops at page-level keys: chrome strings are shared across pages, and
some are read programmatically rather than through a `{{token}}` — `mod_no_slot`, which
`module_specials` pulls from `labels` — so an unused-key check over `common.json` would
fail on a string that is in fact used. This is the same shape of asymmetry #114 just
closed, left open on purpose rather than left unnoticed.

Three more guards are added around it, specific to modules:

- a plugin the manifest declares with no i18n file, in either language, fails
- an i18n module file naming no plugin fails
- a plugin missing from `site/modules.json`, an entry naming no plugin, or an emoji used
  twice, fails

Each one turns a silent gap into a red build. None of them knows how many modules there
are.

## The `@lroot` special

Module pages are the first pages that do not sit at their language root, and the shared
chrome linked to `index.html` relatively. `@root` already meant *back to the site root*
(it is `../` on French pages, which is one level too far for a nav link), so a second
special was added: `@lroot`, *back to the language root*. It is empty on every page that
existed before, which is why their generated output is byte-for-byte unchanged.

## Reaching a module page from the index

The index page's `#modules` cards existed before `module.html` did (#65), each one
hand-written per plugin. Their `.mod-name` had no link — the manifest enumerator gave
every fact on the card a source except that one, so #70 closes it the same way #65
opened the pages: `@modlink_<name>`, one special per module, computed alongside
`@emoji_<name>` in `build()` from the same `modules` list, never a literal
`href="modules/…"` typed by hand. Twelve names still appear in `index.html` — the
card content is not itself generated (#65's scope stopped at the module pages) — but
the URL each one points to is, which is what AC-9 asks for: the string a template
author could get wrong lives in one Python expression, not twelve.

## Escaping manifest facts

`module_specials` builds `@mod_tags` and `@mod_skills` out of names sourced from
`marketplace.json` and the skills tree. Those names are HTML-escaped before they're
folded into `<li>` markup (#71) — every entry in that manifest is authored in this repo
and gated by `tools/validate.py` in CI today, which made the raw interpolation safe in
practice, but escaping costs nothing and stops being optional the day the marketplace
takes an outside contribution.

## Deliberately not done here

The template is a stub: it carries the structure and the tokens and no design decision —
that belongs to the redesign epic. English prose is real as of #66, reviewed against the
voice the hero (#60) and the slot index (#61) settled; French is #58's.
