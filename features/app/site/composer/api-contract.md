# API contract — Composer

## Produced contract

**The emitted YAML matches init's schema.** The composer is a producer of
`.scrumia/config.yaml`, and the shape it emits is the one
`plugins/scrumia-core/skills/scrumia-init/SKILL.md` (Step 3) defines for a
project written by hand: a `project:` block with `name` and `repo`, one
project-level `extends:` list naming the five chosen non-empty modules
(`specs`, `tracker`, `team`, `discovery`, `design` slots — an unchosen one is
simply absent from the list, per
`docs/adr/0019-extends-replaces-composition-and-practices.md`; `extends` carries
no `null` placeholders the way `composition:` did, since a flat list has no
per-slot key to leave empty), and one `apps[]` entry per chosen stack carrying
`name`, `path`, `type` and its own `extends:` list — the app's implementation
module and any practice modules together, in the order the visitor picked
them, since the list carries no precedence meaning of its own. The composer
never fabricates a `settings:` block: those are each module's setup skill to
write, and `scrumia-init` filling them in later is not drift.

**Migration note, not this contract's concern to implement:** `scrumia-init`
reading a project's pre-existing `composition:` key and converting it is
`scrumia-core`'s job, tracked as its own implementation ticket. This contract
states what the composer emits for a new project today, on the current schema.
