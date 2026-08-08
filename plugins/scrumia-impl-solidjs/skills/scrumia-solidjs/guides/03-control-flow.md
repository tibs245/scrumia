# Control Flow: `<Show>`, `<Switch>`, `<For>`, `<Index>`

> How branching and list rendering work when a component body only runs once.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)

## Rules

### Rule 1: Branching on reactive state lives in JSX — no early returns before it

`if (loading) return <Spinner/>` runs once and never re-evaluates: the component froze on whatever `loading` was at mount. Branching lives in JSX — `<Show>`, `<Switch>`, `<Suspense>` — where the condition is a tracked expression, re-evaluated on every relevant signal change. Full rationale: [D-03](../decisions/D-03-no-early-returns-before-jsx.md).

#### Incorrect

```tsx
if (query.loading) return <Spinner />
```

#### Correct

```tsx
<Show when={!query.loading} fallback={<Spinner />}>
  <Cart items={query.data} />
</Show>
```

---

### Rule 2: `<For>` keys by reference, `<Index>` keys by position — never swap them

`<For>` for lists of objects, `<Index>` for lists of primitives. The wrong one "works" while recreating DOM nodes on every update — check this pairing first if a list feels slow, before reaching for any memoisation. Full rationale: [D-04](../decisions/D-04-for-vs-index.md).

#### Correct

```tsx
<For each={users()}>{u => <Row user={u} />}</For>       // objects: keyed by reference
<Index each={values()}>{v => <Cell value={v()} />}</Index> // primitives: keyed by position
```

---

> Decision rationale: [D-03 — Refuse early returns before JSX](../decisions/D-03-no-early-returns-before-jsx.md), [D-04 — `<For>` vs `<Index>`](../decisions/D-04-for-vs-index.md)
