# scrumia-practice-tanstack-query

The `practices` slot, for apps that hold server state in a [TanStack Query](https://tanstack.com/query) cache — `@tanstack/react-query`, `@tanstack/solid-query`, or any other adapter of the same core library. Plugs in app by app, alongside an implementation module or without one.

## What it answers

One cross-cutting question: **how does server state get fetched, cached, and mutated without duplicating it into local state, losing a cache entry to a hand-typed key, or hand-rolling loading and error handling per component.** Nine guides, read on demand rather than all at once, cover the path from a query key to a tested component. A second skill scaffolds a brand-new feature through the same nine guides' worth of decisions, one artifact at a time.

## Skills

| Skill | Role |
|---|---|
| `scrumia-tanstack-query` | The reference — nine guides, query keys through testing, loaded on demand |
| `scrumia-tanstack-query-scaffold` | Scaffolds a new query feature step by step: type → API function → mocks → handlers → query options → hook, with a confirmation gate between each |

## React-first examples, stack-agnostic rules

Every guide's code uses `@tanstack/react-query` — it has the richest surface to illustrate (Suspense boundaries, `useQueries`, the destructuring habit worth warning about). The rules don't come from React, though: the query key hierarchy, `queryOptions()` as the mandatory factory, broad-invalidation-by-default, the mock boundary in tests — all of it is defined by `@tanstack/query-core` and shared across every adapter. Each guide that touches a hook carries a one-line framework note on where the Solid primitive actually differs (mainly: `create*` naming instead of `use*`, and no destructuring the reactive result).

This marketplace ships `scrumia-impl-solidjs` as an implementation module and no `scrumia-impl-react`. This practice module does not assume either is present — a SolidJS app plugging in `scrumia-impl-solidjs` and this practice gets a reference written React-first with the Solid deltas called out; a React app gets the reference at face value with no implementation module situating it further, because none exists yet.

## Not shipped yet

`scrumia-practice-tdd` and `scrumia-practice-solid` each ship three skills: a reference, an `-audit` that measures an existing codebase against it, and a `-refactor` that closes the gap in safe steps. This module ships the reference and a scaffold only — no `scrumia-tanstack-query-audit`, no `scrumia-tanstack-query-refactor`.

**What that costs**: on a codebase that predates this module, there is no automated pass to find the queries still using inline `queryKey`/`queryFn`, the components copying query data into `useState`, or the mutations that never invalidate. An agent applying the reference by hand, guide by guide, is the only option today — slower, and it relies on the agent noticing the gap rather than a dedicated pass surfacing it.

Porting the reference first, ahead of audit and refactor, is deliberate: those two skills are worth writing against a settled set of guides, not one still being adapted from its source. They're the next milestone for this module, not a maybe.

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

If `.scrumia/practices/scrumia-practice-tanstack-query.md` exists, its content takes precedence over the skills in this module. A project records its house exceptions there without forking the module.

## Decisions

Every guide closes on a link into `decisions/` — the ADR behind that guide's rule, for developers who want to understand, challenge, or evolve a practice via PR rather than take it on faith. Thirteen decisions, `D-01` through `D-13`, cover everything from why `queryOptions()` is mandatory to why query keys follow a fixed vocabulary. See [`skills/scrumia-tanstack-query/SKILL.md`](skills/scrumia-tanstack-query/SKILL.md) for the full index.
