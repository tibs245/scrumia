# Tech — module pages

## Where each fact comes from

| Fact | Source | Why there |
|---|---|---|
| which modules exist | `.claude-plugin/marketplace.json` | the manifest is what a user installs from; a page the manifest doesn't know about would be a page nobody can install |
| name, version, tags | same entry | already declared, never retyped |
| skills | `plugins/<name>/skills/*/SKILL.md` | the directory is the list; a count would go stale, a hand-written list would lie |
| install command, source link | derived from the name | one rule, twelve pages |
| emoji, slot | `site/modules.json` | the manifest has no field for either — see below |
| what it plugs into | every `plugins/*/registers.json` and `extends.json` | derived, walked over the whole marketplace so an unrun module still shows (AC-12) |
| what it goes well with, the names | `site/modules.json`'s `pairs_with` | a name is language-neutral, validated the same way the emoji is |
| what it goes well with, the prose | `site/i18n/<lang>/modules/<name>.json`'s `pairs_with` | the *why*, and prose is the only thing that has to exist twice |
| everything else | `site/i18n/<lang>/modules/<name>.json` | prose, and prose is the only thing that has to exist twice |

The manifest is English-only, so it is the **fact** source and never the **prose**
source. That is why the module description shown on a page comes from the i18n file and
not from the manifest's own `description`: a French page carrying an English sentence
would be a divergence the build could not see.

Skill *descriptions* are left off the page for the same reason — the frontmatter that
carries them is English-only. The pages name the skills and stop there. Describing
each one would need a bilingual file of its own, and a module's `SKILL.md`
frontmatter already carries the description for whoever installs it.

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
reads fails the build too — previously a warning, which is how a leftover key
(`composer_js_strings`, now deleted) sat unnoticed.

The unused half stops at page-level keys: chrome strings are shared across pages, and
some are read programmatically rather than through a `{{token}}` — `mod_no_slot`, which
`module_specials` pulls from `labels` — so an unused-key check over `common.json` would
fail on a string that is in fact used. This is the same shape of asymmetry just closed
above, left open on purpose rather than left unnoticed.

Three more guards are added around it, specific to modules:

- a plugin the manifest declares with no i18n file, in either language, fails
- an i18n module file naming no plugin fails
- a plugin missing from `site/modules.json`, an entry naming no plugin, or an emoji used
  twice, fails

Each one turns a silent gap into a red build. None of them knows how many modules there
are.

AC-12 and AC-13 add two more, over the same shape: a `pairs_with` naming a module absent
from the marketplace, or naming the declaring module itself, fails the same way an unknown
emoji entry does; a module `pairs_with` names but whose own i18n file carries no
`pairs_with` prose, in either language, fails too — read directly rather than through a
bare `{{token}}`, since the section has to vanish entirely for a module with nothing to
say, and `render_page` gets told the key was legitimately consumed (`preused`) so its own
unused-string guard doesn't flag it as a leftover.

## What it plugs into (AC-12)

`load_extends_map`, already walking `plugins/*/registers.json` and `extends.json` for the
home page's `#extends` figure, takes the module list it walks as a parameter now: the
figure still passes its own composition (`load_project_modules()`), a module page passes
every marketplace plugin. Reading the project-scoped map here would leave the seven
modules this repository doesn't run showing no connection while their own files declare
one — the very substitution AC-12's own issue names as the one thing not to do. A register
opened with no contributor still gets a row, spelled out (`BR-1`); a module opening and
extending nothing gets no section, not a heading over an empty table.

## What it goes well with (AC-13)

`site/modules.json`'s `pairs_with` says *who* — a list of module names, validated against
the marketplace the same pass that already rejects an unknown emoji entry. Each module's
own `pairs_with` string says *why*, in prose, per language. The two meet in
`module_pairs_html`: the names become links computed from `@modlink_<name>`, never typed
into the prose by hand, so a name that doesn't resolve fails the build before it can
render a dead link.

## The `@lroot` special

Module pages are the first pages that do not sit at their language root, and the shared
chrome linked to `index.html` relatively. `@root` already meant *back to the site root*
(it is `../` on French pages, which is one level too far for a nav link), so a second
special was added: `@lroot`, *back to the language root*. It is empty on every page that
existed before, which is why their generated output is byte-for-byte unchanged.

## Reaching a module page from the index

The index page's `#modules` cards existed before `module.html` did, each one
hand-written per plugin. Their `.mod-name` had no link — the manifest enumerator gave
every fact on the card a source except that one; the link closes that gap the same
way the enumerator opened the pages: `@modlink_<name>`, one special per module,
computed alongside `@emoji_<name>` in `build()` from the same `modules` list, never a
literal `href="modules/…"` typed by hand. Twelve names still appear in `index.html` —
the card content is not itself generated (the first version's scope stopped at the
module pages) — but the URL each one points to is, which is what AC-9 asks for: the
string a template author could get wrong lives in one Python expression, not twelve.

## Reaching a module page from reference.html, and back again

`render_page` already passes `{**emoji_specials, **link_specials}` to every page in
`PAGES`, `reference.html` included — `@modlink_<name>` was reachable from its template
before this ticket, just unused there. `module.html`'s back link
(`{{@lroot}}reference.html`) points at this page's `#modules` section, so leaving a
heading unlinked broke the round trip in one direction only: a reader could reach the
section they came from but not the module page itself, one click short of where they
started. The twelve `<code>module-name</code>` headings now wrap in the same
`{{@lroot}}{{@modlink_<name>}}` pattern `index.html`'s cards use (AC-10, AC-11) — no new
special, no new build code, the same guard that keeps the index honest keeps this page
honest too.

## Escaping manifest facts

`module_specials` builds `@mod_tags` and `@mod_skills` out of names sourced from
`marketplace.json` and the skills tree. Those names are HTML-escaped before they're
folded into `<li>` markup — every entry in that manifest is authored in this repo
and gated by `tools/validate.py` in CI today, which made the raw interpolation safe in
practice, but escaping costs nothing and stops being optional the day the marketplace
takes an outside contribution.

## Deliberately not done here

The template is a stub: it carries the structure and the tokens and no design decision —
that belongs to the redesign epic. English prose shipped for all twelve modules,
reviewed against the voice the hero and the slot index settled; French followed in a
separate pass.
