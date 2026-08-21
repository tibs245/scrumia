# scrumia-tanstack-query

For apps that hold server state in a
[TanStack Query](https://tanstack.com/query) cache — `@tanstack/react-query`,
`@tanstack/solid-query`, or any other adapter of the same core library. Plugs in app by
app, alongside an implementation module or without one.

## What it answers

How server state gets fetched, cached and mutated without duplicating it into local
state, losing a cache entry to a hand-typed key, or hand-rolling loading and error
handling per component — nine guides, read on demand, from a query key to a tested
component. A second skill scaffolds a new feature through the same nine guides' worth of
decisions, one artifact at a time.

## What it refuses

- No hand-typed query key or query function bypassing `queryOptions()` — the guides make
  it the mandatory factory, not a convenience.
- No cache entry duplicated into local state. What TanStack Query owns, a component reads
  from it — never copies into `useState`, or a signal, alongside it.
- No React-only reading of a stack-agnostic rule. Every guide's code is
  `@tanstack/react-query` because it has the richest surface to illustrate, but the query
  key hierarchy, `queryOptions()`, broad-invalidation-by-default and the mock boundary all
  come from `@tanstack/query-core` and apply to every adapter; a guide that touches a hook
  carries a one-line note on where Solid's primitives differ.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-tanstack-query` | The reference — nine guides, query keys through testing, loaded on demand. |
| `scrumia-tanstack-query-scaffold` | Scaffolds a new query feature step by step: type → API function → mocks → handlers → query options → hook, with a confirmation gate between each. |

## Settings it reads

Under this module's own `params:` in `.scrumia/config.yaml`:
`data_root` and `adapter` (`react` or `solid`).

## What it expects to find

An app that lists `scrumia-tanstack-query` in its own `extends`. This
marketplace ships `scrumia-impl-solidjs` and no `scrumia-impl-react`; a SolidJS app gets
the React-first reference with the Solid deltas called out, a React app gets it at face
value. An optional `.scrumia/overrides/scrumia-tanstack-query.md` records house
exceptions without forking the module.

## Decisions

Thirteen, `D-01` through `D-13` — every guide closes on the one behind its rule, for
developers who want to understand, challenge or evolve a rule via PR rather than take
it on faith. See [`skills/scrumia-tanstack-query/SKILL.md`](skills/scrumia-tanstack-query/SKILL.md)
for the full index.

## Not shipped yet

`scrumia-tdd` and `scrumia-solid-principles` each ship a reference, an `-audit` and
a `-refactor`. This module ships the reference and a scaffold only — no
`scrumia-tanstack-query-audit`, no `scrumia-tanstack-query-refactor`. On a codebase that
predates this module, there is no automated pass to find inline `queryKey`/`queryFn`,
query data copied into local state, or mutations that never invalidate; an agent applies
the reference by hand instead. Porting the reference first, ahead of audit and refactor,
is deliberate — the next milestone, not a maybe.
