# Modular composition

**Status**: active

## In brief

A project declares which modules it runs through `extends`, a flat, unordered list in
`.scrumia/config.yaml`; a module installed and named nowhere is inert. A main skill
declares what it is for and stops — what it must apply is contributed by other modules as
**data**, keyed by a **register** (a named extension point), and rendered into one table
at the moment the skill asks for it. A contribution names no consumer, which is what lets
one fragment serve implementation, review and audit without being written three times.
`implementation` and cross-cutting practices are both declared through `extends`, per app;
nothing forces a project to take the whole composition to get one part of it, and nothing
is stored, so nothing can go stale. `business.md` § *Vocabulary* is the authority on
"slot", "register", "directive" and "fragment".

## Links

- Implemented by: no App feature. The mechanism this feature describes lives in
  `scrumia-core` (`plugins/scrumia-core/`) — it reads `.scrumia/config.yaml`, writes the
  composition table into `CLAUDE.md`, renders a register's directives through the
  `scrumia-extends` name it publishes, and prints the composition to a terminal through
  `plugins/scrumia-core/scripts/compose-status.sh`, which both its skills end by running.
  Each module declares what it opens, contributes and consumes in its own
  `registers.json`, `extends.json` and `dependencies.json`.
- Defers to: `features/business/release-versioning/` for how a module evolves once
  adopted — what a version bump promises, the deprecation window, and when a project is
  told. This feature establishes that a module can be composed, not what changing it costs.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding what `extends` is, what a register or a directive is, or what a module owes to be pluggable and to contribute |
| `tech.md` | Understanding how the mechanism resolves — the pipeline, where the order comes from, what fails and what reports it, and the practices for writing an extension |
| `qa.md` | Checking the composition mechanism's own acceptance criteria, including how a missing capability degrades |
| `CHANGELOG.md` | Checking history of changes to this spec |

No `ux.md`: this feature has no interface of its own. No `api-contract.md` either,
although the three data files are a schema several modules produce and one tool parses:
the field-by-field reference ships inside `scrumia-core`'s `scrumia-extend` skill, so a
project reads the version matching the tooling it installed rather than this repository's
`main`. Restating it here would guarantee the two diverge.
