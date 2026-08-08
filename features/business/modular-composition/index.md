# Modular composition

**Status**: active
**Stratum**: business

## In brief

ScrumIA answers a fixed set of project-steering questions — specs, tracking, team,
discovery, implementation, practices, design — through **slots**. A slot is one
question; a module plugged into it is one replaceable answer. A project picks a
module per slot, or leaves the slot empty on purpose. Nothing forces a project to
take the whole composition to get one part of it.

## The slots

A slot is a question a project-steering method has to answer, named so a module can
claim it instead of the project inventing its own. Seven exist today:

| Slot | The question | Reference module |
|---|---|---|
| `specs` | Where do specs live, in what shape? | `scrumia-specs` |
| `tracker` | Where does state live: tickets, columns, PRs? | `scrumia-github-project` |
| `team` | Which standing roles, with what scope? | `scrumia-teams` |
| `discovery` | How does an idea become framed work? | `scrumia-discovery` |
| `implementation` | How we code — per app | `scrumia-impl-rust`, `scrumia-impl-solidjs` |
| `practices` | Which cross-cutting practices — per app | `scrumia-practice-tdd`, `scrumia-practice-solid` |
| `design` | Where does the design system live? | `scrumia-design` |

`implementation` and `practices` are the two slots that repeat: they apply per app,
not once for the whole project.

A module may also ship the **standing role** that guards its slot's capability, rather
than that role living in the `team` slot's module. `scrumia-design` is the first to do
so: a design role in a project with no design system would have nothing to judge but
taste. The role registers in the same `settings.team.roles` list, so routing stays
single-sourced — see `docs/adr/0014-roles-ship-with-their-capability.md` and the
`agent-team` feature.

An **empty slot is a declared absence, not an oversight**. `.scrumia/config.yaml`
sets it to `null` explicitly — never omits the key — so a reader can tell "this
project hasn't chosen yet" apart from "this project deliberately has no discovery
step". Agents adapt what they propose accordingly instead of assuming a capability
that isn't there.

## Links

- Implemented by: no App feature. The mechanism this feature describes lives in
  `scrumia-core` (`plugins/scrumia-core/`), which fills no slot itself — it reads
  `.scrumia/config.yaml` and writes the composition table into `CLAUDE.md`. Each
  module named in the table owns its own slot's implementation.

## Files present

| File | Why it exists |
|---|---|
| `business.md` | What a module owes to be pluggable, and the rule it must never break |
| `qa.md` | The composition mechanism's own acceptance criteria, including how a missing capability degrades |
| `CHANGELOG.md` | History of changes to this spec |

No `ux.md`, `a11y.md` or `api-contract.md`: this feature has no interface and no
API of its own — it governs how modules declare and read configuration, not
something a user or another app calls.

## Open issues

- #7 — module versioning and breaking-change migration: left open by this feature,
  deliberately. See "Out of scope" in `qa.md`.
