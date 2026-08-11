---
name: scrumia-solidjs
description: ScrumIA's SolidJS practices — behaviour-first component tests, fine-grained reactivity without React reflexes, feature-based structure, and what we refuse. Load it before writing code in an app whose implementation module is scrumia-impl-solidjs.
---

# Coding in SolidJS

This module contributes to `build/apply-implementation` for every app that lists it in its own `extends` in `.scrumia/config.yaml`. It has authority over the "how" in those apps — including over your own preferences. It is one choice among several defensible ones; each rule comes with its reason, given with each rule below.

## The contract

- **How we test** — behaviour-first component tests, unit-tested primitives, Playwright kept outside the fast loop. → [06-testing](guides/06-testing.md)
- **Which design principles** — fine-grained reactivity without React reflexes: `createMemo` derives, `createEffect` synchronises outward; a component owns its state or receives it, never both. → [02-derivations](guides/02-derivations.md), [01-components-and-props](guides/01-components-and-props.md)
- **How the code is structured** — by feature, not by kind; data access at the `api/` boundary; primitives and shared state have a named home. → [05-project-layout](guides/05-project-layout.md), [04-data-boundary](guides/04-data-boundary.md)
- **What we refuse** — destructured props, early returns before JSX, effects used as derivations, swapped `<For>`/`<Index>`, deep wrapper hierarchies, default global state. → [D-01](decisions/D-01-no-destructured-props.md), [D-02](decisions/D-02-no-createeffect-as-derivation.md), [D-03](decisions/D-03-no-early-returns-before-jsx.md), [D-04](decisions/D-04-for-vs-index.md)

## Guides

| File | Use when you need to... |
|------|--------------------------|
| [01-components-and-props](guides/01-components-and-props.md) | Write or review a component's props access and local state |
| [02-derivations](guides/02-derivations.md) | Derive a value from signals, or decide between `createMemo` and `createEffect` |
| [03-control-flow](guides/03-control-flow.md) | Branch UI (`<Show>`, `<Switch>`) or render a list (`<For>`, `<Index>`) |
| [04-data-boundary](guides/04-data-boundary.md) | Fetch data from a component, or place a route |
| [05-project-layout](guides/05-project-layout.md) | Place a new file: feature, primitive, or shared state |
| [06-testing](guides/06-testing.md) | Write a test for a component, a primitive, or an end-to-end journey |

## Routing table

```
"I need to write a new component"
  → 01-components-and-props + 03-control-flow

"I need to access or group props inside a component"
  → 01-components-and-props

"I need to derive a value from one or more signals"
  → 02-derivations

"I need to synchronise with the outside world (DOM, storage, analytics)"
  → 02-derivations

"I need to branch UI on a loading/error/empty state"
  → 03-control-flow

"I need to render a list"
  → 03-control-flow

"I need to fetch data for a component"
  → 04-data-boundary (assumes 01)

"I need to place a new file — component, primitive, or shared state"
  → 05-project-layout

"I need to decide if state should be global"
  → 05-project-layout

"I need to write a component test"
  → 06-testing (assumes 01, 03, 04)

"I need to write a primitive's unit test"
  → 06-testing

"I need an end-to-end / cross-page test"
  → 06-testing (Playwright, outside the red-green loop)

"I need the full contract before writing code in a covered app"
  → 01-components-and-props + 02-derivations + 03-control-flow + 04-data-boundary + 05-project-layout + 06-testing
```

## Dependencies between guides

```
01-components-and-props  ← foundation, no dependencies — read first
02-derivations            ← requires 01
03-control-flow           ← requires 01
04-data-boundary          ← requires 01
05-project-layout         ← structural, no dependencies — read anytime
06-testing                ← requires 01, 03, 04 — tests what the earlier guides produce
```

## Decisions

The `decisions/` folder explains **why** each refusal was adopted — not needed to write code, useful to challenge or evolve the rule via PR.

| D-NN | Decision | Related guide |
|------|----------|----------------|
| [D-01](decisions/D-01-no-destructured-props.md) | Refuse destructured props | [01-components-and-props](guides/01-components-and-props.md) |
| [D-02](decisions/D-02-no-createeffect-as-derivation.md) | Refuse `createEffect` as a derivation | [02-derivations](guides/02-derivations.md) |
| [D-03](decisions/D-03-no-early-returns-before-jsx.md) | Refuse early returns before JSX | [03-control-flow](guides/03-control-flow.md) |
| [D-04](decisions/D-04-for-vs-index.md) | `<For>` vs `<Index>` — never swapped | [03-control-flow](guides/03-control-flow.md) |

## Settings

Under `settings.implementation.scrumia-impl-solidjs` in `.scrumia/config.yaml`:

```yaml
settings:
  implementation:
    scrumia-impl-solidjs:
      test_runner: vitest       # the only supported value today; declared for replaceability
      e2e: playwright           # playwright | null (no journey tests)
      coverage_threshold: null  # number, or null: no enforced threshold
      strict_mode: true         # TypeScript strict — turning it off is a project decision
```

## Project override

If `.scrumia/impl/scrumia-impl-solidjs.md` exists, its content takes precedence over this skill and its guides. A project records its house exceptions there — a legacy state library, a different data layer — without forking the module.

## The module's other skill

`scrumia-solidjs-audit` — measures the gap between an existing app and these rules, finding by finding, citing the guide or decision each finding violates.

## Scope

This module applies to apps whose `.scrumia/config.yaml` lists `scrumia-impl-solidjs` in the app's own `extends`. Within such an app, `section.json`'s globs (`src/**/*.tsx`, `src/**/*.ts`) pick which files trigger the guides above.
