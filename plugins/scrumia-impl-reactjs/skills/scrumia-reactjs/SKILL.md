---
name: scrumia-reactjs
description: ScrumIA's React 19 practices — Server Components by default, Actions and useActionState for mutations and forms, derived state calculated during render, behaviour-first component tests, feature-based structure, and what we refuse. Load it before writing code in an app whose implementation module is scrumia-impl-reactjs.
---

# Coding in React 19

## The contract

- **How we test** — behaviour-first component tests with React Testing Library; Server Components tested through their rendered output, never by importing the server-only module; route-level journey tests outside the fast loop. → [06-testing](guides/06-testing.md)
- **Which design principles** — Server Components by default, the `"use client"` boundary added only when state, an event handler or a client API demands it. Derived state is calculated during render, not duplicated into an Effect. Mutations go through Actions (`useActionState`, `useTransition`, `useOptimistic`) so pending, error and ordering are React's problem, not the component's. → [02-state-and-derivations](guides/02-state-and-derivations.md), [01-components-and-props](guides/01-components-and-props.md), [03-control-flow](guides/03-control-flow.md)
- **How the code is structured** — by feature, not by kind; Server Components own data fetching, Client Components live at the leaves; primitives and shared state have a named home. → [05-project-layout](guides/05-project-layout.md), [04-data-boundary](guides/04-data-boundary.md)
- **What we refuse** — `useEffect` for derived state, imperative DOM escape hatches, effects where event handlers answer the same question, unnecessary `"use client"`. → [D-01](decisions/D-01-no-useeffect-for-derived-state.md), [D-02](decisions/D-02-no-imperative-dom.md), [D-03](decisions/D-03-effects-where-event-handlers-belong.md), [D-04](decisions/D-04-no-unnecessary-client-components.md)

## Guides

| File | Use when you need to... |
|------|--------------------------|
| [01-components-and-props](guides/01-components-and-props.md) | Write or review a component's signature, decide Server vs Client, pass `ref` as a prop |
| [02-state-and-derivations](guides/02-state-and-derivations.md) | Decide between `useState`, a derived value, `useActionState`, `useTransition`, `useOptimistic`, `use(promise)` |
| [03-control-flow](guides/03-control-flow.md) | Branch UI on a loading/error/empty state, render a list, handle a `<form>` submission |
| [04-data-boundary](guides/04-data-boundary.md) | Fetch data, place a route segment, decide where the network call lives |
| [05-project-layout](guides/05-project-layout.md) | Place a new file — feature folder, Server-first route, primitive, shared state |
| [06-testing](guides/06-testing.md) | Write a test for a component or a primitive, test a Server Component, plan a route-level journey |

## Routing table

```
"I need to write a new component"
  → 01-components-and-props + 03-control-flow

"I need to decide Server Component vs Client Component"
  → 01-components-and-props (and 04-data-boundary for what to fetch)

"I need to expose a ref from a function component"
  → 01-components-and-props (ref as a prop, no forwardRef)

"I need to derive a value from props or state"
  → 02-state-and-derivations (calculate during render — D-01)

"I need to handle a user mutation (submit, save, add)"
  → 02-state-and-derivations + 03-control-flow (Actions: useActionState, useTransition, useOptimistic)

"I need to show an immediate UI before an async action settles"
  → 02-state-and-derivations (useOptimistic)

"I need to keep the UI responsive while a non-urgent update runs"
  → 02-state-and-derivations (useTransition)

"I need to branch UI on a loading/error/empty state"
  → 03-control-flow (Suspense + ErrorBoundary + conditional render)

"I need to read a Promise in a render"
  → 03-control-flow + 02-state-and-derivations (use(promise))

"I need to render a list"
  → 03-control-flow (key stability; primitives get the same key prop)

"I need to fetch data for a route"
  → 04-data-boundary (Server Component, async/await, no useEffect)

"I need to fetch data inside a Client Component"
  → 04-data-boundary (Suspense-enabled cache + use(promise), never useEffect)

"I need to place a new file — component, primitive, or shared state"
  → 05-project-layout

"I need to decide between the App Router and the Pages Router"
  → 05-project-layout

"I need to write a component test"
  → 06-testing (assumes 01, 03, 04)

"I need to test a Server Component"
  → 06-testing (import the rendered output, not the server-only module)

"I need to write a primitive's unit test"
  → 06-testing

"I need an end-to-end / cross-page test"
  → 06-testing (Playwright, outside the red-green loop)

"I need the full contract before writing code in a covered app"
  → 01-components-and-props + 02-state-and-derivations + 03-control-flow + 04-data-boundary + 05-project-layout + 06-testing
```

## Dependencies between guides

```
01-components-and-props  ← foundation, no dependencies — read first
02-state-and-derivations ← requires 01
03-control-flow           ← requires 01
04-data-boundary          ← requires 01, 03 (Suspense)
05-project-layout         ← structural, no dependencies — read anytime
06-testing                ← requires 01, 03, 04 — tests what the earlier guides produce
```

## Decisions

The `decisions/` folder explains **why** each refusal was adopted — not needed to write
code, useful to challenge or evolve the rule via PR. Each cites the React 19 docs passage
the rule rests on (the `read` link in `extends.json` points at the React docs section).

| D-NN | Decision | Related guide |
|------|----------|----------------|
| [D-01](decisions/D-01-no-useeffect-for-derived-state.md) | Refuse `useEffect` for derived state | [02-state-and-derivations](guides/02-state-and-derivations.md) |
| [D-02](decisions/D-02-no-imperative-dom.md) | Refuse imperative DOM escape hatches | [01-components-and-props](guides/01-components-and-props.md), [03-control-flow](guides/03-control-flow.md) |
| [D-03](decisions/D-03-effects-where-event-handlers-belong.md) | Refuse effects where event handlers belong | [02-state-and-derivations](guides/02-state-and-derivations.md) |
| [D-04](decisions/D-04-no-unnecessary-client-components.md) | Refuse unnecessary `"use client"` | [01-components-and-props](guides/01-components-and-props.md), [05-project-layout](guides/05-project-layout.md) |

## Settings

Under `settings.implementation.scrumia-impl-reactjs` in `.scrumia/config.yaml`:

```yaml
settings:
  implementation:
    scrumia-impl-reactjs:
      test_runner: vitest       # the only supported value today; declared for replaceability
      e2e: playwright           # playwright | null (no journey tests)
      coverage_threshold: null  # number, or null: no enforced threshold
      react_compiler: false     # true when the project uses the React Compiler — see 02-state-and-derivations
```

## Project override

If `.scrumia/impl/scrumia-impl-reactjs.md` exists, its content takes precedence over this
skill and its guides. A project records its house exceptions there — a legacy state
library, a different data layer, a framework choice that pre-dates Server Components —
without forking the module.

## The module's other skill

`scrumia-reactjs-audit` — measures the gap between an existing app and these rules,
finding by finding, citing the guide or decision each finding violates.

## Scope

This module applies to apps whose `.scrumia/config.yaml` lists `scrumia-impl-reactjs` in
the app's own `extends`. Within such an app, `section.json`'s globs (`src/**/*.tsx`,
`src/**/*.ts`) pick which files trigger the guides above.
