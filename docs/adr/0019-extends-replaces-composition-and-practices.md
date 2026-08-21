# ADR-0019 — `extends` replaces `composition:`, and folds `practices` into it

**Status**: accepted — 2026-08-11

## Context

`composition:` (ADR-0009) keys the configuration by **slot**: one named question, one
answer, project-wide.

```yaml
composition:
  specs: scrumia-specs
  tracker: scrumia-github-project
```

Two findings, independent of each other, converged on the same limit.

**A slot declared filled says nothing about what actually uses it.** An audit of the 34
skills across ScrumIA's modules, run during the scoping of issue #184, measured the
result: `scrumia-specs-find` has one provider and five prose copies, *and it is the copies
that run*; 37 of 37 skills carry a gap between what they promise and what they do. Every
one of those was invisible to `composition:`, because declaring the slot filled was the
whole test.

**`practices` is `implementation` with a different name.** ADR-0010 gave practices their
own slot, repeating per app alongside `implementation`, to answer "which cross-cutting
practices, per app?" without duplicating TDD or SOLID into every implementation module.
That reasoning holds; what does not hold is that it needed a second key. Both slots answer
one question — *which modules does this app draw on when work happens in it* — and answer
it with the same shape: a list, per app, unordered.

Three months earlier `#106` had asked, unresolved, "should a composer preset also propose
a stack?" The slot model could not answer it cleanly, because "stack" spans two slots with
no shared vocabulary between them.

## Decision

**`extends` — a flat list of the modules a project runs, replacing `composition:`,
`implementation:` and `practices:`.** ESLint-shaped, and per app where the choice is an
app's:

```yaml
extends:
  - scrumia-specs
  - scrumia-github-project
  - scrumia-teams
apps:
  - name: api
    path: apps/api
    extends: [scrumia-impl-rust, scrumia-tdd, scrumia-solid-principles]
  - name: prototype
    path: apps/prototype
    extends: [scrumia-impl-solidjs]
```

TDD applies to `api` and not to the `prototype` beside it — ADR-0010's own load case —
because each app's list is its own.

**A module installed but named in no `extends` is inert.** Presence on disk is not
participation: the harness may have twenty plugins enabled, and this project runs the ones
it names. That is what makes a module safe to install before deciding to use it.

**The list is not ordered.** Unlike ESLint's `extends`, this carries no last-wins
semantics. A reader will bring the ESLint reflex uninvited; this sentence exists to
contradict it on first read, rather than be inferred from the shape of the list. Where
precedence between two contributions is needed, it comes from **scope** — project-local,
then the app's own modules, then the project-wide ones — which is
[ADR-0020](0020-skill-extension-protocol.md)'s, and which is the same chain ADR-0010
stated in prose ("specific beats generic; the project override beats both").

**A slot stops being a label pointing at a module.** What a module offers is declared by
the module, in its own data files, and read by whoever needs it — not asserted by which
slot name it claims. ADR-0020 defines that declaration.

### `practices` is retired as a named slot

A practice module keeps every rule ADR-0010 gave it — it refines a named point of the
implementation contract, works on its own, ships reference/audit/refactor skills, and
documents the settings it reads. What it loses is a dedicated config key.

## Consequences

**What we gain**

- One question asked once — *what does this app draw on* — instead of two slots that
  happened to share a shape.
- A module can be installed and remain inert, which `composition:` could not express: a
  slot was either filled or empty.
- `#106` becomes answerable: a preset proposes a list of modules, not two unrelated slot
  choices.

**What we accept**

- **`composition:` → `extends` is a breaking config change**, consumed by every project
  that installed ScrumIA, with no installer (ADR-0001). `scrumia-init` reads the old keys
  and writes the new one; `composition:`, `implementation:` and `practices:` stay
  tolerated, with a warning, for one minor. `compose-status.sh`, `check_composition_drift()`,
  the fixture, both `site/i18n/*/index.json` and this repository's own `CLAUDE.md` need the
  migration applied, not merely documented.
- **Retiring `practices` as a slot name removes one of the seven questions the site and
  the composer narrate.** The site's account of its own composition becomes false the
  moment this ADR is accepted, until the site is updated in the same change.
- **An unordered list cannot express precedence positionally**, on purpose. A project that
  wants one rule to beat another states it in `.scrumia/extends.json`, where it is visible,
  rather than by reordering a list where a silent reorder would be a silent precedence
  change.

## Rejected alternatives

**A `practices` list kept alongside a new `extends`.** Two config keys answering
overlapping questions is the exact duplication ADR-0010 was written to prevent — this time
between two slots' worth of syntax rather than between implementation modules.

**Ordering `extends` with ESLint's last-wins semantics.** Arbitration is a decision
someone makes, not an accident of list position. Encoding it positionally makes a silent
reorder a silent behaviour change — worse than the status quo, where the one precedence
rule ADR-0010 stated is at least written down and has to be edited on purpose.

**A closed, kernel-owned vocabulary of the things a module may declare.** Drafted, and
rejected in review: a third-party module could then not declare anything the kernel had
not anticipated without a `scrumia-core` release, which contradicts what a plugin
marketplace is for. ADR-0020 keeps the vocabulary open and pays the cost in the checker
instead.

## Supersedes

This ADR **supersedes ADR-0010 in full** — the `practices` slot no longer exists.

This ADR **amends ADR-0009 on one point**: what the config declares (`extends`, flat,
instead of `composition:`, slot-keyed). ADR-0009's decision — documented composition, no
capability registry, no verb resolved to a module at call time — stands unmodified here;
where it is amended is [ADR-0020](0020-skill-extension-protocol.md), which says so
explicitly.

## To revisit

- If `practices` folded into `extends` loses addressability a project actually needed
  (override below the whole-module level), that is the "rule addressability" question #184
  named as its own, later wave — not a reason to reopen this decision.
