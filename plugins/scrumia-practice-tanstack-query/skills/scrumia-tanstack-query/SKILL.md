---
name: scrumia-tanstack-query
description: The ScrumIA TanStack Query reference — query keys, the queryOptions() factory, useQuery, select, useSuspenseQuery, useQueries, dependent queries, mutations, and testing, as nine guides loaded on demand. Load it before writing or reviewing data-fetching code in an app where the TanStack Query practice is plugged in.
---

# Coding with TanStack Query

This practice refines one point of the implementation contract: **how server state is fetched, cached, and mutated.** It applies to apps that list it in their own `extends` in `.scrumia/config.yaml`, with or without an implementation module — nothing here assumes `scrumia-impl-solidjs`, `scrumia-impl-rust`, or any other module is present. When an implementation module for the app's framework does situate TanStack Query for its stack, its tooling takes precedence over the generic examples here; today none of this marketplace's implementation modules does, so the guides below are the whole answer.

> Entry point for an agent. Read this file first, then open only the guide(s) the task needs — loading all nine for a one-line fix defeats the point of splitting them.

## The single rule

**Every query goes through a `queryOptions()` factory built on a key from a centralized `queryKeys.ts` — never an inline `queryKey`/`queryFn` pair.**

Everything else follows from it: one factory reused by `useQuery`, `useSuspenseQuery`, `useQueries`, prefetching and tests alike; invalidation that targets a key nobody hand-typed twice; a cache that never silently forks into two entries for what was meant to be one query.

## Guides (for code generation)

| File | Use when you need to... |
|------|------------------------|
| [01-query-keys](guides/01-query-keys.md) | Define query keys in a centralized `queryKeys.ts` (foundation) |
| [02-query-options](guides/02-query-options.md) | Declare query options, create a `*.queries.ts` factory file |
| [03-use-query](guides/03-use-query.md) | Fetch and display data with `useQuery` |
| [04-select](guides/04-select.md) | Transform or filter fetched data for a component |
| [05-use-suspense-query](guides/05-use-suspense-query.md) | Load data with Suspense boundaries |
| [06-use-queries](guides/06-use-queries.md) | Run multiple queries in parallel (dynamic list) |
| [07-dependent-queries](guides/07-dependent-queries.md) | Chain queries where B depends on A's result |
| [08-mutations](guides/08-mutations.md) | Create, update, or delete server data |
| [09-testing](guides/09-testing.md) | Unit test select functions and page components |
| [10-migrating-an-existing-codebase](guides/10-migrating-an-existing-codebase.md) | Bring a codebase written against the older key vocabulary up to these guides |

## Routing table

```
"I need to define query keys for a feature"
  → 01-query-keys

"I need to create a queries file for a feature"
  → 01-query-keys + 02-query-options

"I need to fetch data and display it"
  → 01-query-keys + 02-query-options + 03-use-query

"I need to transform/filter the data I fetched"
  → 04-select (assumes 01 + 02 + 03)

"I need query B to wait for query A"
  → 07-dependent-queries (assumes 01 + 02)

"I need to load data with Suspense"
  → 05-use-suspense-query (assumes 01 + 02)

"I need to run N queries in parallel"
  → 06-use-queries (assumes 01 + 02)

"I need to create/update/delete a resource"
  → 08-mutations (assumes 01 + 02)

"I need to unit test my queries or page components"
  → 09-testing (assumes 02 + 04)

"I have an existing codebase on the older key vocabulary (byUser, lists(), listByCategory)"
  → 10-migrating-an-existing-codebase

"I need to scaffold a whole new query feature from an API schema"
  → the sibling skill scrumia-tanstack-query-scaffold, which walks all of the above
    in order, one artifact at a time
```

## Dependencies between guides

```
01-query-keys     ← foundation, no dependencies — define keys first
02-query-options  ← requires 01
03-use-query      ← requires 01, 02
04-select         ← requires 01, 02, 03
05-use-suspense   ← requires 01, 02
06-use-queries    ← requires 01, 02
07-dependent      ← requires 01, 02
08-mutations      ← requires 01, 02
09-testing        ← requires 02, 04
```

## Decisions (for humans challenging practices)

The `decisions/` folder contains Architecture Decision Records (ADRs) explaining **why** each practice was chosen. Not needed for code generation — they exist for developers who want to understand, challenge, or evolve the practices via PR.

| ADR | Decision | Related guide |
|-----|----------|---------------|
| [D-01](decisions/D-01-query-options-mandatory.md) | queryOptions() mandatory vs inline | 02-query-options |
| [D-02](decisions/D-02-query-keys-colocation.md) | Centralized queryKeys.ts vs co-located keys | 01-query-keys |
| [D-03](decisions/D-03-no-state-duplication.md) | Never copy query data into useState | 03-use-query |
| [D-04](decisions/D-04-select-vs-queryfn.md) | select vs queryFn transformation | 04-select |
| [D-05](decisions/D-05-suspense-vs-usequery.md) | useSuspenseQuery vs useQuery default | 05-use-suspense-query |
| [D-06](decisions/D-06-use-queries-vs-multiple.md) | useQueries vs multiple useQuery | 06-use-queries |
| [D-07](decisions/D-07-dependent-queries-pattern.md) | Separate chained queries vs single queryFn | 07-dependent-queries |
| [D-08](decisions/D-08-invalidation-vs-setquerydata.md) | Invalidation vs setQueryData after mutation | 08-mutations |
| [D-09](decisions/D-09-optimistic-updates-when.md) | When optimistic updates are worth it | 08-mutations |
| [D-10](decisions/D-10-staletime-strategy.md) | staleTime default and cache strategy | 02-query-options |
| [D-11](decisions/D-11-error-handling-strategy.md) | Error handling — Boundaries vs local vs global | 03-use-query |
| [D-12](decisions/D-12-as-const-simplification.md) | `as const` on outer object only (not per-line) | 01-query-keys |
| [D-13](decisions/D-13-query-key-naming-conventions.md) | Standardized query key naming (`all`, `list`, `detail`) | 01-query-keys |

## Framework notes

Every guide's code examples use `@tanstack/react-query` — the richest surface to illustrate (Suspense boundaries, `useQueries`, hook destructuring). The rules themselves — the query key hierarchy, `queryOptions()` as the mandatory factory, the invalidation strategy, the mock boundary in tests — hold unchanged for `@tanstack/solid-query` and any other TanStack Query adapter. Each guide that touches a hook carries a one-line note on where the Solid primitive differs (mainly: `create*` instead of `use*`, and no destructuring the result). This marketplace currently ships `scrumia-impl-solidjs` as an implementation module and no `scrumia-impl-react` — this practice module does not assume either is present, and does not need one to apply.

## Settings

Under `settings.practices.scrumia-practice-tanstack-query` in `.scrumia/config.yaml`:

```yaml
settings:
  practices:
    scrumia-practice-tanstack-query:
      data_root: src/data      # where queryKeys.ts and *.queries.ts live
      adapter: react            # react | solid — which TanStack Query package this app imports
```

## Project override

If `.scrumia/practices/scrumia-practice-tanstack-query.md` exists, its content takes precedence over this skill. A project records its house exceptions there without forking the module.

## Scaffolding a new feature

`scrumia-tanstack-query-scaffold` walks an agent through generating a complete feature — type → API function → mocks → handlers → query options → hook — one artifact at a time, with a confirmation gate between each. Reach for it when the feature is new end to end; reach for the guides above when you're touching one piece of an existing one.

## What's not here yet

No `scrumia-tanstack-query-audit` or `scrumia-tanstack-query-refactor` skill ships in this module yet — see the [module README](../../README.md) for what that costs today and why it's next on the roadmap rather than shipped now.
