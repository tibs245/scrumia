# Modular composition

**Status**: active

## In brief

A project declares which modules it runs through `extends`, a flat, unordered list in
`.scrumia/config.yaml`. Each module bids on the actions it provides for the project's
declared steps — a **decision** action has exactly one provider, a **contribution**
action may have several — and coverage is derived from those declarations rather than
asserted by a fixed slot table. `implementation` and cross-cutting practices are both
declared this way, per app; nothing forces a project to take the whole composition to
get one part of it. "Slot" survives as the word the composer's own questions use;
`business.md` § *Vocabulary* is the authority on the split between that and "action".

## Links

- Implemented by: no App feature. The mechanism this feature describes lives in
  `scrumia-core` (`plugins/scrumia-core/`), which provides no action itself — it reads
  `.scrumia/config.yaml`, writes the derived composition table into `CLAUDE.md`, and
  prints that same coverage to a terminal through
  `plugins/scrumia-core/scripts/compose-status.sh`, which both its skills end by
  running. Each module named in the table owns its own declared action's implementation.
- Defers to: `features/business/release-versioning/` for how a module evolves once
  adopted — what a version bump promises, the deprecation window, and when a project is
  told. This feature establishes that a module can be composed, not what changing it costs.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding what `extends` is, what an action is, or what a module owes to be pluggable |
| `qa.md` | Checking the composition mechanism's own acceptance criteria, including how a missing capability degrades |
| `CHANGELOG.md` | Checking history of changes to this spec |

No `ux.md` or `api-contract.md`: this feature has no interface and no API of its
own — it governs how modules declare and read configuration, not something a user
or another app calls.

