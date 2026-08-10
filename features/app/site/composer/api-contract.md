# API contract — Composer

## Produced contract

**The emitted YAML matches init's schema.** The composer is a producer of
`.scrumia/config.yaml`, and the shape it emits is the one
`plugins/scrumia-core/skills/scrumia-init/SKILL.md` (Step 3) already defines
for a project written by hand: a `project:` block with `name` and `repo`,
all five `composition:` keys spelled even when `null` (`specs`, `tracker`,
`team`, `discovery`, `design`), and one `apps[]` entry per chosen stack
carrying `name`, `path`, `type`, `implementation` and `practices`. The
composer never fabricates a `settings:` block: those are each module's setup
skill to write, and `scrumia-init` filling them in later is not drift.
