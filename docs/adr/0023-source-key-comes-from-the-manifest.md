# ADR-0023 — A module's `<owner>/<repo>` source is its manifest's claim, not the marketplace

**Status**: accepted — 2026-08-19

**Supersedes** the `<owner>/<repo>` row of [ADR-0021](0021-modules-keyed-by-source.md)'s source table.

## Context

[ADR-0021](0021-modules-keyed-by-source.md) made every module key a `<source>:<module>`
triple, and its source table rendered the marketplace row as *"a marketplace"*
(`0021-modules-keyed-by-source.md:57-61`). That worked while a marketplace served the
one repository it was named for, and stopped working the moment a marketplace could
serve a fork.

The code reads differently. `plugins/scrumia-core/bin/scrumia-extends:276-296` derives
a module's source from `.repository // .homepage` of its own `.claude-plugin/plugin.json`,
normalised to `<owner>/<repo>`, and `local-extension/tech.md:58` and
`modular-composition/tech.md:70` already say it that way. BR-13
(`modular-composition/business.md:408-417`) governs the writing side, and AC-17
(`modular-composition/qa.md:227-248`) carries the scenario. The ADR is the one artefact
still describing its own decision as being about the marketplace.

A fork exposes the gap. Fork `tibs245/scrumia` to `acme/scrumia`, install under the
alias `acme`, and `plugin.json` still claims `tibs245/scrumia` — forking does not rewrite
it. Every key sourced from the marketplace alias would have become a declared absence:
the module stops contributing, every register renders shorter, and `scrumia-extends --check`
stays green, because it inspects the modules it discovered and never the declarations.
That is the case #303 reproduced by hand and the case its migration procedure was
rewritten to pass.

## Decision

The `<owner>/<repo>` row of the source table is reworded to name what the code reads:

| Source | Where the module is |
|---|---|
| `<owner>/<repo>` | the first of `.repository` or `.homepage` the module's manifest states, normalised to `<owner>/<repo>` |
| `shared` | a directory of checkouts shared between a person's projects |
| `local` | inside the project |

A manifest claiming neither resolves the marketplace tier to nothing; that case is
reported where it occurs (BR-13, `modular-composition/tech.md:210`), and the empty
source is not silently read as a tier that matches whatever was installed.

## Arguments for

- The code, the spec, and the ADR say the same thing. The drift that led #303 to read
  the ADR's *"a marketplace"* in the marketplace sense is the drift this closes, and
  `scrumia-extends --check` will stay green on the fork case the same way it stays green
  on the resolved one.
- A fork installed under a different marketplace alias still resolves to the upstream
  the manifest claims, because forking does not rewrite `plugin.json`. This is the case
  #303 reproduced by hand and the case its migration procedure was rewritten to pass.
- The wording names the fallback the code uses (`scrumia-extends:287-289`), so the
  reader is not asked to guess which of the two fields the resolver reaches for when
  both are present.
- The marketplace tier is no longer a label the marketplace writes; it is a label the
  module's own manifest writes, and the marketplace is downstream of it. That is the
  direction the code already implements.

## Arguments against

- **The two manifest fields are read as one.** A module that declares `.homepage` when
  `.repository` is also derivable is taken at `.repository`'s word, and a module that
  declares only `.homepage` is taken at that. Renaming the row "the first of
  `.repository` or `.homepage`" admits the second is a fallback; `homepage` is rarely
  curated to that end, and a homepage that has moved to a project page can read as an
  owner the module no longer lives at. Accepted because the alternative is a field a
  module ships specifically for the binding, which is the vocabulary migration
  `modular-composition/tech.md` already decided against.
- **The empty source is not always wrong.** A repository-less module is a declared
  absence for a marketplace key, never a match — but for a `shared` or `local` key the
  source does not enter the comparison at all, and a manifest that says nothing about
  its origin is the common case there. The decision does not change that, and it is
  stated so the reader does not derive a stricter rule from the row's wording.

## Rejected alternatives

**Sourcing the `<owner>/<repo>` from the marketplace entry the project installed
through.** What #303's first draft did, and what the failing scenario it added
(`test_ac17_a_marketplace_source_is_the_manifest_not_the_alias`,
`tools/test_init_migration.py:179-211`) is written to reject. The marketplace is a
delivery channel and not a place the module comes from; a fork shares the channel
without sharing the source, and the resolver that cannot tell the two is the resolver
that was failing.

**Reading the source from the directory the module sits in.** A module's checkout
path can give a project's server program away to a contributing module — the path
*is* a project secret, and the binding that needs it is the one a manifest already
carries. The information is in the manifest, and reusing it is cheaper than asking
the file system.

**Adding a third field to `.claude-plugin/plugin.json` named `source`.** A vocabulary
addition that the kernel, every module, and every shipped marketplace would have to
take at once. The information is already in two fields the manifest already carries,
and the resolver's job is to read what is there, not to require a new one.

## Supersedes

**Replaces the `<owner>/<repo>` row of [ADR-0021](0021-modules-keyed-by-source.md)'s
source table.** The previous row read *"a marketplace"*; this ADR rewords it to
*"the first of `.repository` or `.homepage` the module's manifest states, normalised to
`<owner>/<repo>`"*. Everything else 0021 decided stands — the key, the settings
cascade, the `shared` and `local` rows — and 0021 is not modified beyond the row it
names, per `README.md:3`.

## To revisit

- If a marketplace starts rewriting `plugin.json` on fork — a behaviour nobody ships
  today, but a hook one could — the binding this ADR describes would still hold, and
  the migration procedure #303 added would simply stop needing the manifest as the
  authority. That is the case to reopen, not the case to pre-empt.
