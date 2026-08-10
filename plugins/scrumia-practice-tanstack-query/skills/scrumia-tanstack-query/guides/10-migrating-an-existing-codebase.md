# Migrating an existing codebase

A codebase written against the older query-key vocabulary — `lists()` / `details()` scope
functions, per-line `as const`, names like `byUser` or `listByCategory` — reaches the current
guides through the four steps below. Each is mechanical and each ends in `tsc --noEmit`, which
is what turns a rename into a checked one.

The decisions behind them are [D-12](../decisions/D-12-as-const-simplification.md) and
[D-13](../decisions/D-13-query-key-naming-conventions.md).

## 1. Simplify `as const` in `queryKeys.ts`

**Effort**: Low — mechanical find-and-replace.

```diff
 export const queryKeys = {
   products: {
-    all: ['products'] as const,
-    lists: () => [...queryKeys.products.all, 'list'] as const,
-    detail: (id: string) => [...queryKeys.products.details(), id] as const,
+    all: ['products'],
+    list: (filters: ProductFilters) => [...queryKeys.products.all, 'list', { filters }],
+    detail: (id: string) => [...queryKeys.products.all, 'detail', id],
   },
 } as const;
```

- Remove `as const` from every line inside the object.
- Keep the **single** `as const` at the end of the object declaration.
- Verify `strict: true` is set in your `tsconfig.json`.
- Run `tsc --noEmit` to confirm no type regressions.

## 2. Remove `lists()` / `details()` scope functions

**Effort**: Low to Medium — remove scope functions and update consumers.

```diff
 export const queryKeys = {
   products: {
     all: ['products'],
-    lists: () => [...queryKeys.products.all, 'list'],
-    list: (filters) => [...queryKeys.products.lists(), { filters }],
-    details: () => [...queryKeys.products.all, 'detail'],
-    detail: (id) => [...queryKeys.products.details(), id],
+    list: (filters) => [...queryKeys.products.all, 'list', { filters }],
+    detail: (id) => [...queryKeys.products.all, 'detail', id],
   },
 } as const;
```

- Replace `queryKeys.*.lists()` invalidation calls with `queryKeys.*.all`.
- `list` and `detail` now spread from `all` directly.
- Run `tsc --noEmit` to catch all broken references.

## 3. Rename non-standard query key methods

**Effort**: Medium — requires renaming + updating all consumers.

| Find | Replace with | Notes |
|------|-------------|-------|
| `byId(id)` | `detail(id)` | Single entity lookup |
| `byUser(userId)` | `detail(userId)` or `list({ userId })` | Use `detail` if result is a single entity/view, `list` if it's a filtered collection |
| `byResource(resourceId)` | `detail(resourceId)` | Single resource lookup |
| `listByCategory(cat)` | `list({ category: cat })` | Filtered collection |
| `getAll()` / `fetchAll()` | `all()` | Full collection, no pagination |

**Steps:**
1. Update `queryKeys.ts` — rename methods.
2. Update `*.queries.ts` — update references to renamed keys.
3. Update components/hooks — update `invalidateQueries`, `getQueryData`, etc.
4. Run `tsc --noEmit` to catch all broken references.
5. Run tests to verify behavior is unchanged.

## 4. Replace hardcoded key strings

**Effort**: Low — search for string array patterns in `invalidateQueries`, `setQueryData`, `getQueryData`.

```diff
- queryClient.invalidateQueries({ queryKey: ['products', 'list'] });
+ queryClient.invalidateQueries({ queryKey: queryKeys.products.all });
```

**Search pattern**: Look for `queryKey: [` in your codebase outside of `queryKeys.ts`. Every hit is a candidate for replacement.
