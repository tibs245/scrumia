# API contract — Composer

## Produced contract

**The emitted YAML matches init's schema.** The composer is a producer of
`.scrumia/config.yaml`, and the shape it emits is the one
`plugins/scrumia-core/skills/scrumia-init/SKILL.md` (Step 3) defines for a
project written by hand: a `project:` block with `name` and `repo`, a
`modules:` mapping declaring the modules the project runs, and one `apps[]`
entry per chosen stack carrying `name`, `path`, `type` and its own `modules:`
mapping.

**Every key is `<source>:<module>`**, per
[ADR-0021](../../../../docs/adr/0021-modules-keyed-by-source.md) — one grammar,
no bare name and no exception. For a module this site ships, the source half is
`tibs245/scrumia`, the same marketplace the install block adds; a bare name is
not a shorter spelling of it but a key nothing resolves. Each value is an empty
mapping: `params:` belongs to whoever configures the module, and the composer
knows no value to put there.

**An absent capability has no key to spell.** The mapping names what is present,
so a slot the visitor leaves empty is emitted as a comment standing where its
module would have gone, carrying the same consequence the row stated. The order
of the seven rows is the order of the mapping, which is what lets an absence be
read in place rather than inferred from what is missing.

The composer never fabricates a `settings:` block, and never a `params:` under a
key: those are each module's setup skill to write, and `scrumia-init` filling
them in later is not drift.
