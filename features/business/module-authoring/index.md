# Module authoring

**Status**: draft

## In brief

How a ScrumIA module comes into existence, changes, and moves — from nothing to a module
that already meets the anatomy standard, and from a module used in one project to one a
marketplace publishes. A module is created where it is first used and moves only once
reuse is demonstrated; promotion changes its location and never its shape. Authoring
refuses the two cheapest mistakes it could make: a module built for a need below the
threshold, and a new slot no project would fill differently.

## Links

- Implemented by: no App feature. What this feature describes is a skill in
  `scrumia-core` and the checker `module-anatomy` owns.
- Defers to: `features/business/module-anatomy/` for what a well-formed module contains.
  Authoring produces modules against that standard and states none of it.
- Defers to: `features/business/release-versioning/` for what a version bump promises an
  adopting project and what moves the number. Authoring names the bump a change calls
  for; it does not define what the bump is worth.
- Defers to: `features/business/local-extension/` for where a module may live and how it
  is found there. Authoring says *when* a module moves; that feature says *what the
  places are*.
- Defers to: `features/business/knowledge-placement/` for where something goes when it is
  below the threshold a module deserves. The refusal to create a module below it is only
  usable because that feature names the alternative.
- Defers to: `features/business/modular-composition/` for what a slot is and when a new
  one is justified.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding when a module is created, where, what editing one costs, and when it is promoted |
| `qa.md` | Checking this feature's acceptance criteria |
| `CHANGELOG.md` | History of changes to this spec |

No `tech.md`: the mechanics an author touches — the checker, the resolution of a module
outside the marketplace — belong to the two features that own them, and restating them
here would guarantee they diverge.

