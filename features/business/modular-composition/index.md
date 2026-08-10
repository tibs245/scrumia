# Modular composition

**Status**: active
**Stratum**: business

## In brief

ScrumIA answers a fixed set of project-steering questions — specs, tracking, team,
discovery, implementation, practices, design — through **slots**. A slot is one
question; a module plugged into it is one replaceable answer. A project picks a
module per slot, or leaves the slot empty on purpose. Nothing forces a project to
take the whole composition to get one part of it.

## Links

- Implemented by: no App feature. The mechanism this feature describes lives in
  `scrumia-core` (`plugins/scrumia-core/`), which fills no slot itself — it reads
  `.scrumia/config.yaml`, writes the composition table into `CLAUDE.md`, and
  prints that same composition to a terminal through
  `plugins/scrumia-core/scripts/compose-status.sh`, which both its skills end by
  running. Each module named in the table owns its own slot's implementation.

## Files present

| File | Read it when |
|---|---|
| `business.md` | Deciding what a slot is, which seven exist, or what a module owes to be pluggable |
| `qa.md` | Checking the composition mechanism's own acceptance criteria, including how a missing capability degrades |
| `CHANGELOG.md` | Checking history of changes to this spec |

No `ux.md` or `api-contract.md`: this feature has no interface and no API of its
own — it governs how modules declare and read configuration, not something a user
or another app calls.

