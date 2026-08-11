# ADR-0019 — `extends` replaces `composition:`, and folds `practices` into it

**Status**: accepted — 2026-08-11

## Context

Two findings, independent of each other, converged on the same mechanism.

An audit of the 34 skills across ScrumIA's modules (37 actions, 8 agents), run during
the scoping of issue #184, measured what the `composition:` model of ADR-0009 could not
see: 18 of 34 actions serve none of the project's seven declared steps; `Build` alone
carries 14 of 20 flow couplings while three steps carry exactly one action each;
`scrumia-specs-find` has one provider and five prose copies, and it is the copies that
run; 37 of 37 skills carry a gap between what they promise and what they do. `composition:`
answers "which module fills which slot" — a question with one answer per slot, project-wide.
It cannot express "which module provides which action, and how many provide it, and for
which app" — the question this audit needed to ask to find any of the above.

Separately, ADR-0010 gave `practices` its own slot, repeating per app alongside
`implementation`, to answer "which cross-cutting practices, per app?" without duplicating
TDD or SOLID into every implementation module. That decision holds up mechanically three
years later — nothing about *why* a practice should live in one place and be cited by
name has changed. What changed is the vocabulary above it: once `implementation` and
`practices` are both understood as **contributions to the `Build` step** (§ *Two kinds of
action*, below), `practices` answers a question `extends` already asks — "who contributes
to Build, for this app" — through a second, redundant key.

Three months earlier `#106` had asked, unresolved, "should a composer preset also propose
a stack?" — a question the slot model could not answer cleanly because "stack" spans two
slots (`implementation`, `practices`) with no shared vocabulary between them. Naming both
as contributions to the same step is what makes that question answerable at all: a preset
proposes a step's contributors, not two unrelated slots.

## Decision

**`extends` — a flat list of plugged modules, replacing `composition:`.** A project's
`.scrumia/config.yaml` declares which modules it runs, ESLint-shaped:

```yaml
extends:
  - scrumia-specs
  - scrumia-github-project
  - scrumia-teams
  - scrumia-discovery
  - scrumia-design
apps:
  - name: api
    path: apps/api
    extends: [scrumia-impl-rust, scrumia-practice-tdd, scrumia-practice-solid]
```

**The list is not ordered.** Unlike ESLint's `extends`, this carries no last-wins
semantics — arbitration between two modules bidding on the same decision action is
explicit (§ *Two kinds of action*), never positional. A reader will bring the ESLint
reflex uninvited; this sentence exists to contradict it on first read, not to be inferred
from the shape of the list.

**A slot stops being a label pointing at a module. It becomes a named set of required
actions.** Coverage is **derived** from what modules declare providing, not asserted by
which slot a module claims. A module that declares an action with no caller is a hole
the mechanism can now see — it could not be seen under `composition:`, where declaring
was the whole test.

**Two kinds of action.** A **decision** has exactly one provider: who moves a card, which
model runs a ticket, who settles a business rule. A **contribution** legitimately has
several: reviewing a PR, applying a practice to a Build. `implementation` and `practices`
were always contributions to `Build` — ADR-0010 said as much without the word: "the
choice stays per app", multiple modules, one step. `extends` states that directly instead
of routing it through two slots that happened to repeat the same way.

**Three absence states.** A key absent from the config means nobody decided — warn once.
`not-applicable` means the step does not exist for this project — removed from the
coverage denominator. `human` means the step exists and a person covers it, no tool —
counted as covered. This is what makes "seven steps, three of them are you" a computed
sentence instead of copy that can go stale.

**Four recipient sets**, named so `extends` is scoped to the one it actually configures:
**run** (the project's own steps — what `extends` configures), **kernel** (`init`,
`compose`; non-configurable by construction), **adoption** (the five `*-setup` skills
plus the two contract audits), **authoring** (`rules`, outside the product). Coverage is
measured against **run** only; the other three are named so the denominator in any
"N of M covered" claim is never silently half the system.

### `practices` is retired as a named slot

The `practices` slot (ADR-0010) is folded into `extends`, declared **per app** — the
axis ADR-0010 exists to preserve, and the one a flat, project-level list cannot express
on its own:

```yaml
apps:
  - name: api
    path: apps/api
    extends: [scrumia-impl-rust, scrumia-practice-tdd]
  - name: prototype
    path: apps/prototype
    extends: [scrumia-impl-solidjs]
```

TDD applies to `api` and not to the `prototype` next to it — ADR-0010's own load case —
because each app's `extends` list is its own. A practice module keeps every rule ADR-0010
gave it (refines a named point of the implementation contract, works on its own, ships
reference/audit/refactor skills, documents `settings.practices.<module>`) unchanged; what
it loses is a dedicated config key. **The one precedence rule ADR-0010 stated — specific
beats generic, the project override (`.scrumia/impl/<module>.md`) beats both — is
unchanged and is restated here because ADR-0010's own text is the only place that carried
it.** An unordered `extends` list has no positional way to express it; this ADR keeps it
in prose, on purpose, rather than trying to encode a 3-level precedence chain into list
order (see § *The list is not ordered*, above).

### How modules connect to each other — unchanged from ADR-0009

Resolution still happens at composition, not at call time. `scrumia-init` still reads the
config and writes, between markers in `CLAUDE.md`, what an agent needs — now a table
**derived** from declared actions rather than retyped from named slots. A module still
cites another by name in prose, never through a runtime lookup. **This is a change to
what gets produced — a derived table instead of a retyped one — not to when resolution
happens or where an agent looks.** ADR-0009's own rejection of the capability registry
stands: "the agent must keep in mind that 'creating a ticket' goes through a verb
pointing to a module it cannot see" is exactly as true of an action name as it was of a
slot name. Nothing here resolves an action to a module in the hot path.

A module still reaches another **by a name the harness resolves, never by a path** — the
constraint measuring coverage now depends on (a plugin reaching another by a relative
path cannot be counted as a real edge; see #185). This was implicit under ADR-0009; this
ADR makes it load-bearing, because the coverage calculation in `tools/` cannot function
without it.

## Consequences

**What we gain**

- Coverage answers a question `composition:` structurally could not ask: not "is the slot
  filled" but "does anything call what was declared". The audit that motivated this ADR
  is the proof — it needed the action vocabulary to be askable at all.
- `implementation` and `practices` stop being two slots that happen to share a shape
  (multiple, per-app) and become one question asked once: what does this app's `Build`
  draw on.
- A closed, kernel-owned action vocabulary keeps the customisation promise bounded: a
  project chooses which steps and who covers what, never what the actions are called.
- `#106` ("should a composer preset also propose a stack?") becomes answerable: a preset
  proposes a step's contributors, not two unrelated slot choices.

**What we accept**

- **`composition:` → `extends` is a breaking config change**, consumed by every project
  that installed ScrumIA, with no installer (ADR-0001). `scrumia-init` reads the old key
  and writes the new one; `composition:` stays tolerated, with a warning, for the
  deprecation window `features/business/release-versioning/` defines — counted in
  **releases**, not in version levels: readable at the release that deprecates it and the
  one after, removable no earlier than the one after that. This ADR does not set that
  window and an earlier draft's "one minor" did not survive contact with it:
  `features/business/modular-composition/` defers the question to `release-versioning` by
  name, and `scrumia-core` sits below `1.0.0`, where a rename-level change ships *as* a
  minor — so "one minor" would remove the key in the very release that deprecated it.
  `compose-status.sh`, `check_composition_drift()`, the fixture, both `site/i18n/*/index.json`
  and this repo's own `CLAUDE.md` table all need the migration applied to them, not just
  documented — tracked as implementation tickets from this scoping's split.
- **The action vocabulary is closed by the kernel.** A third-party module cannot bid on
  an action name it does not know without a `scrumia-core` release. An `x-<module>/<action>`
  opaque-prefix escape hatch is reserved as a mitigation, not adopted — a decision this
  ADR defers rather than makes.
- **"Coverage is derived" still means "derived from declaration", not "measured by
  execution".** A module that declares an action with no caller is now visible as a hole;
  a module that declares an action and is never actually invoked in a live session still
  reads as covered until something walks real call graphs. Derivation narrows the blind
  spot `composition:` had; it does not close it.
- **`practices` retiring as a slot name removes one of the seven questions the site and
  the composer narrate ("two of the seven are empty").** The site's account of its own
  composition (`site/i18n/{en,fr}/index.json`) becomes false the moment this ADR is
  accepted, until the implementation tickets this scoping files land. That window is
  accepted as the cost of shipping the spec and the site update as separate, reviewable
  units rather than one unreviewable one.

## Rejected alternatives

**A `practices` list kept alongside a new `extends`.** Two config keys answering
overlapping questions is the exact duplication ADR-0010 itself was written to prevent —
this time between two slots' worth of syntax rather than between implementation modules.

**Ordering `extends` and using ESLint's last-wins semantics for precedence.** Considered
and rejected during the scoping: arbitration between two decision-action providers, or
between an implementation module and a practice module, is a business call ("who is
allowed to make this decision"), not an accident of list position. Encoding it positionally
makes a silent reorder a silent precedence change — worse than the status quo, where the
one precedence rule ADR-0010 stated is at least written down and has to be edited on
purpose to change.

## Supersedes

This ADR **supersedes ADR-0010 in full** — the `practices` slot no longer exists, folded
into `extends` as described above.

This ADR **amends ADR-0009 on one point**: what `scrumia-init` derives (an actions-based
table instead of a slot table) and what the config declares (`extends`, flat, instead of
`composition:`, slot-keyed). ADR-0009's decision — documented composition, resolved once
at composition time, never at call time, no capability registry — stands unmodified; that
is confirmed, not revisited, by § *How modules connect to each other* above.

## To revisit

- If the action vocabulary's closedness becomes a recurring friction for third-party
  modules, revisit the `x-<module>/<action>` escape hatch reserved but not adopted here.
- If `practices` folded into `extends` turns out to lose addressability that a project
  actually needed (fine-grained override below the whole-module level), that is the
  "rule addressability" open question #184 already named as its own, later wave — not a
  reason to reopen this decision.
