# ADR-0024 — There is no category of module, and no vocabulary naming one

**Status**: accepted — 2026-08-21

## Context

[ADR-0019](0019-extends-replaces-composition-and-practices.md) retired `practices` as a
config key and said so plainly. What it did not do is retire the *word* — and the word
went on naming a category the configuration no longer had.

The count, taken across the repository before this decision: 892 occurrences over roughly
130 files. Three plugin directories carried it as a prefix (`scrumia-practice-tdd`,
`-solid`, `-tanstack-query`), so it appeared in every install command, every module URL on
the site and every commit scope. `site/modules.json` still filed those three under
`"slot": "practices"`, which kept them out of the composer's additions shelf and gave the
home page a seventh slot row the configuration could not fill. `composer.js` held a
`PRACTICES` table pairing each with the app types it spoke for — a mechanism no other
module got. Each of the three documented its configuration under `settings.practices.<module>`
and read its project override from `.scrumia/practices/<module>.md`, while implementation
modules used `settings.implementation.<module>` and `.scrumia/impl/<module>.md`: two
parallel namespaces, distinguished by a category and nothing else.

Meanwhile `scrumia-zod`, `scrumia-rhf`, `scrumia-compound-design` and `scrumia-html-css`
had all shipped with no prefix, no slot and no separate namespace — and each does exactly
what a "practice module" was said to do. The vocabulary had already stopped describing the
marketplace; it survived as a distinction with nothing behind it.

Left alone, a reader reconstructs the category from the word, and the next module author
asks which of the two kinds they are writing. That question has no answer, which is the
point.

## Decision

**A module that refines what another module says is a module. There is no second kind, and
no vocabulary naming one.**

Concretely:

- **The three modules are renamed** — `scrumia-tdd`, `scrumia-solid-principles`,
  `scrumia-tanstack-query`. `solid-principles` rather than `solid` because
  `scrumia-impl-solidjs` already stands one letter away, and a name a reader has to
  disambiguate is a name that will be misread.
- **They fill no slot.** `site/modules.json` records `"slot": null`, which is what puts
  them on the composer's additions shelf beside `scrumia-zod` and the others. The slot
  index drops from seven rows to six.
- **One namespace for a module's configuration**, the one every module already uses: its
  own `params:`, resolved through `scrumia-extends --settings`. `settings.practices` joins
  `settings.implementation` as a retired nest the resolver still reconciles.
- **One project override directory**, `.scrumia/overrides/<module>.md`, replacing both
  `.scrumia/impl/` and `.scrumia/practices/`. Not `.scrumia/modules/`: that path already
  holds locally-placed modules (`features/business/local-extension/`), and a file named
  beside those directories would read as one of them.
- **A slot is a question the composition asks, not a label a module wears.** A module that
  answers no such question is not lesser for it — most of the marketplace is now in that
  position.

The word keeps its ordinary English sense. "Good practice" is a thing that exists, and
`scrumia-tdd` carries plenty; what does not exist is a *practice module*.

## Consequences

**What we gain**

- One question for a module author — *what does this refine* — instead of a taxonomy to
  place themselves in first.
- The three modules reach the composer's additions shelf, where a visitor can actually
  pick them. Under `"slot": "practices"` they were reachable only through a row that
  asked a question the config had already retired.
- The two override paths and two settings nests collapse to one each, so a module's
  documentation stops depending on which category it was filed under.

**What we accept**

- **Renaming a published module is breaking.** A project that installed
  `scrumia-practice-tdd` finds its key unresolved, and the marketplace offers no
  redirect. Each of the three carries the rename in its changelog as a breaking entry,
  per `features/business/release-versioning/`.
- **Commit scopes change** — `practice-tdd` becomes `tdd`, and so on. ADR-0017's scope
  table is updated, since it is normative rather than historical.
- **Prior ADRs keep their text.** 0010, 0011, 0019, 0020 and 0021 argue in the vocabulary
  of their date, and an accepted ADR is not rewritten. `docs/adr/README.md` no longer
  promises a housekeeping pass over 0011's citations: this is that pass, and it stops at
  the index rather than editing the record.
- **The migration shim keeps the old key's name.** `composition:`/`practices:` are still
  read with a warning, because a config that has not migrated is a config that still
  parses. Naming a retired key is not vocabulary; it is a fact about someone's file.

## Rejected alternatives

**Keeping the prefix, cleaning only the prose.** The directory name is what a visitor
types to install and what a committer types as a scope. Leaving `scrumia-practice-tdd`
standing while claiming the category is gone would put the contradiction in the one place
every user meets it.

**`.scrumia/modules/<module>.md` for the overrides.** The obvious name, and wrong: that
directory already holds `local:` modules as subdirectories. A `.md` file beside them
invites the reading that a module can be a single file.

**A `refines:` key declaring what a module sharpens.** Drafted, then dropped: it is the
category re-introduced as syntax. What a module refines is already legible from the
register it contributes to — [ADR-0020](0020-skill-extension-protocol.md)'s mechanism —
and a second declaration would be one more thing able to disagree with the first.

## To revisit

If a genuine second kind ever appears — a module the resolver must treat differently
rather than one that merely reads differently — that is a new decision with a mechanism
behind it, not a return to a word.
