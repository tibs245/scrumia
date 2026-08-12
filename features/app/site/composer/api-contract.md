# API contract — Composer

## Produced contract

**The emitted YAML carries the shape ADR-0021 defines.** The composer is a
producer of `.scrumia/config.yaml`, and its authority on that file's shape is
[ADR-0021](../../../../docs/adr/0021-modules-keyed-by-source.md) with
`features/business/modular-composition/business.md`, not a consuming module's
own template. It emits a `project:` block with `name` and `repo`, a `modules:`
mapping declaring the modules the project runs, and one `apps[]` entry per
chosen stack carrying `name`, `path`, `type` and its own `modules:` mapping.

**Every key is `<source>:<module>`** — one grammar, no bare name and no
exception. For a module this site ships, the source half is `tibs245/scrumia`,
the same marketplace the install block adds; a bare name is not a shorter
spelling of it but a key nothing resolves. Each value is an empty mapping:
`params:` belongs to whoever configures the module, and the composer knows no
value to put there.

**An absent capability has no key to spell.** The mapping names what is
present, so a slot the visitor leaves empty is emitted as a comment carrying
the consequence its row stated, and an app left with no module of its own
carries that consequence on its empty mapping. The composer emits in row order
as a producer's courtesy; no reader may take meaning from a key's position,
which an unordered mapping does not carry.

**A composition with nothing in it is still emitted.** A visitor who empties
every project-level slot gets a `modules:` key carrying its five comments and
no entry — which reads as empty rather than as a mapping, and is the empty
composition said in the same words the rows used, not a file that failed to
generate.

The composer never fabricates a `settings:` block, and never a `params:` under
a key: those are each module's setup skill to write, and `scrumia-init` filling
them in later is not drift.
