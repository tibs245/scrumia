---
name: scrumia-tanstack-query-scaffold
description: Scaffolds a complete TanStack Query feature end to end from an API schema — type, API function, mocks, MSW handlers, queryOptions factory, hook — one artifact at a time with a confirmation gate before each. Use it when a query feature is new from scratch; use scrumia-tanstack-query's guides when touching one existing piece.
---

# Scaffold a TanStack Query feature

Generates a complete feature from an API schema, one artifact at a time: type → API function → mocks → MSW handlers → query options → hook. Each step follows the rules in [`scrumia-tanstack-query`](../scrumia-tanstack-query/SKILL.md) — read that skill's guides `01-query-keys` through `08-mutations` first if this is the first time scaffolding a query in this project; this skill is the procedure, not a restatement of the rules.

**One step at a time. Never skip ahead, never generate two artifacts before showing the first.** An agent's default instinct is to produce the whole feature in one block — that defeats the point of the gates below, which exist so the user can redirect before a wrong assumption (a route param name, a mock shape) propagates through five files.

## Required inputs

Before starting, collect these from the user:

1. **API client**: which HTTP client / API version this project uses, if it has more than one (most projects have exactly one — check `/src/data/api/` before asking).
2. **Route**: e.g. `/products/{productId}/reviews` — params are in `{curly braces}`.
3. **API schema**: the response schema, pasted from the API documentation.

If any input is missing, ask for it before proceeding.

## Step 1 — TypeScript type

### Analyze

- Parse the schema to identify the entity fields, nested objects, enums, and optionality.
- Check `/src/types/` for existing types that can be reused (a shared `Resource<T>` wrapper, a common `Paginated<T>`, etc.).

### Generate

- Create or update the type file in `/src/types/<Entity>.type.ts`.
- Follow naming conventions: `PascalCase` for types, enums as union types.
- Import and reuse shared types when the schema matches a pattern already used elsewhere in the project.

### Present to user

Show the generated type and ask for confirmation before proceeding.

## Step 2 — API function

### Analyze

- Check `/src/data/api/` for existing request files in the same domain.
- Check the project's route-helpers file, if it has one (e.g. `/src/utils/apiRoutes.ts`), for existing route builders.
- Identify path params from the route (e.g. `{productId}` → `productId: string`).

### Generate

- Create or update the request file in `/src/data/api/<domain>/<domain>.requests.ts`.
- Create a typed params interface for the function arguments.
- Add a route helper in the project's route-helpers file if it has one and the route isn't already there.
- Use the project's API client — `apiClient` below is a placeholder for whatever wraps `fetch`/`axios`/`ky` in this codebase.

```tsx
// Pattern to follow:
export const get<Entity> = async ({ param1, param2 }: Get<Entity>Params) => {
  const { data } = await apiClient.get<ResponseType>(route);
  return data;
};
```

### Present to user

Show the generated API function and ask for confirmation before proceeding.

## Step 3 — Mocks

### Pause — ask for example response

Tell the user:

> I need an example API response to generate realistic mocks. Please paste a real response (I'll anonymize it) or describe what a typical response looks like.

### Generate

Once the user provides the example:

- Anonymize all sensitive data (IDs → UUIDs `a1b2c3d4-...`, names → generic names, IPs → `192.168.x.x`, dates → recent dates).
- Create the mock file in `/src/mocks/<domain>/<domain>.ts` (or `.mock.ts`, depending on the project's convention).
- Export a typed array of mock data.
- Ensure the mock matches the TypeScript type from Step 1.

```tsx
// Pattern to follow:
export const mock<Entities>: <Type>[] = [
  {
    // anonymized data matching the type
  },
];
```

### Present to user

Show the generated mock and ask for confirmation before proceeding.

## Step 4 — MSW Handlers

### Analyze

- Check `/src/mocks/` for existing handler files to match the project's handler pattern — some projects wrap raw MSW `http.get`/`http.post` handlers in a small project-specific helper (a typed params object, a shared delay/error toggle); follow whatever is already there rather than introducing a second style.
- Check the test setup file (`setupMsw.ts` or equivalent) to understand how handlers are aggregated.

### Generate

- Create or update the handler file in `/src/mocks/<domain>/<domain>.handler.ts`.
- Follow the existing handler pattern in the project. If there is no existing pattern, plain MSW is the default:

```tsx
// Pattern to follow — plain MSW, adapt to the project's wrapper if it has one:
import { http, HttpResponse } from 'msw';

export type T<Entity>MockParams = {
  is<Entity>Error?: boolean;
};

export const get<Entity>Mocks = ({
  is<Entity>Error = false,
}: T<Entity>MockParams = {}) => [
  http.get('<route with :params>', () =>
    is<Entity>Error
      ? new HttpResponse(null, { status: 500 })
      : HttpResponse.json(mock<Entities>),
  ),
];
```

- Update the test setup file to include the new handlers and their params type.

### Present to user

Show the generated handler and the setup update, ask for confirmation.

## Step 5 — Hook

### Analyze

- Check `/src/data/hooks/` (or wherever hooks live in this project) for existing hooks to match naming and patterns.
- Determine if this query depends on another (e.g. needs an ID from a parent query) → use the `ensureQueryData` pattern from [`07-dependent-queries`](../scrumia-tanstack-query/guides/07-dependent-queries.md).
- Determine the query key hierarchy based on existing keys in `queryKeys.ts` (see [`01-query-keys`](../scrumia-tanstack-query/guides/01-query-keys.md)) — add a new entry there rather than inventing a standalone key constant.

### Generate

- Add the query key to `queryKeys.ts` (or create it if this is the first query in the project).
- Add the query options to the feature's `*.queries.ts` factory (see [`02-query-options`](../scrumia-tanstack-query/guides/02-query-options.md)) — create the file if this is the first query for this feature.
- Export a hook wrapping `useQuery` (or `useSuspenseQuery` if the user asked for Suspense — see [`05-use-suspense-query`](../scrumia-tanstack-query/guides/05-use-suspense-query.md)) with the factory method.
- If the query has nullable external params, add `enabled: !!param` (see [`03-use-query`](../scrumia-tanstack-query/guides/03-use-query.md), Rule 3).
- If the query depends on another query's result, use `ensureQueryData` in the `queryFn` instead of `enabled` (see [`07-dependent-queries`](../scrumia-tanstack-query/guides/07-dependent-queries.md), Rule 2).

```tsx
// Pattern to follow:
// queryKeys.ts
export const queryKeys = {
  // ...existing entries
  <entity>: {
    all: ['<entity>'],
    detail: (id: string) => [...queryKeys.<entity>.all, 'detail', id],
  },
} as const;

// <domain>.queries.ts
const detail = (id: string) =>
  queryOptions({
    queryKey: queryKeys.<entity>.detail(id),
    queryFn: () => get<Entity>({ id }),
  });

export const <entity>Queries = { detail };

// In a component
const { data } = useQuery(<entity>Queries.detail(id));
```

### Present to user

Show the complete hook and ask for confirmation.

## Summary

After all steps are confirmed, show a recap:

```
✓ Type:     src/types/<Entity>.type.ts
✓ API:      src/data/api/<domain>/<domain>.requests.ts
✓ Mock:     src/mocks/<domain>/<domain>.ts
✓ Handler:  src/mocks/<domain>/<domain>.handler.ts
✓ Keys:     src/data/queryKeys.ts (updated)
✓ Queries:  src/features/<domain>/<domain>.queries.ts
```

## Important rules

- **Always check existing files first** — never duplicate types, routes, or mocks that already exist.
- **Follow the project's existing conventions** — naming, file structure, import paths. This skill's code patterns are illustrative defaults, not a house style to impose over an established one.
- **Ask before writing** — show each generated file and get user confirmation before moving to the next step.
- **One step at a time** — don't skip ahead, don't generate two artifacts before a gate.
- **Anonymize mocks** — never include real data in mock files.
