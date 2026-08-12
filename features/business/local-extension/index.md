# Local extension

**Status**: draft

## In brief

The places a module may live besides a marketplace, and the material a project may add
without a module at all. Three locations — published, checked out in a directory shared
between a person's projects, or inside the project — resolved by one mechanism, holding
the same artefact to the same standard. Alongside them, local material that is
deliberately not a module: a directive, a rules section, a skill. What a project's own
`CLAUDE.md` claims has to stay true for someone who clones it without any of this.

## Links

- Implemented by: no App feature. Resolution is `scrumia-core`'s, through the name it
  publishes for rendering a register's directives.
- Defers to: `features/business/modular-composition/` for what `extends` is, what a
  directive is, and the order in which contributions are rendered — a project-local
  contribution's precedence is stated there and not restated here.
- Defers to: `features/business/module-anatomy/` for what any module must look like. A
  module resolved outside a marketplace is held to it unchanged.
- Consumed beyond this feature: `features/business/module-authoring/` decides *when* a
  module moves between the locations this feature defines;
  `features/business/knowledge-placement/` routes toward them.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding where a module may live, what local material is legitimate without being one, and what a clone without it must still see |
| `qa.md` | Checking this feature's acceptance criteria |
| `CHANGELOG.md` | History of changes to this spec |

