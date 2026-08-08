# D-03: Refuse early returns before JSX

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/03-control-flow.md](../guides/03-control-flow.md)

## Context

A React reflex for conditional rendering:

```tsx
if (query.loading) return <Spinner />
return <Cart items={query.data} />
```

In React, the whole function body re-runs on every render, so the early return is re-evaluated every time and genuinely branches. In SolidJS, the component function body runs **once**. The `if` is evaluated once, at mount, against whatever `query.loading` was at that instant — and never again. If the component happened to mount while loading, it returns `<Spinner />` forever; the `<Cart>` branch is unreachable no matter what `query.loading` becomes later.

## Arguments For

- **The bug is invisible in the common case.** A component that mounts already-loaded, or a manual smoke test performed after data resolves, never triggers the frozen branch — it ships and fails for whichever user's timing hits the loading state at mount.
- **JSX control-flow components (`<Show>`, `<Switch>`, `<Suspense>`) exist precisely to be reactive.** They re-evaluate their `when` condition as a tracked expression on every relevant signal change — the exact behavior an early return can't provide. There is no capability lost by refusing the early return.
- **Consistency with the rest of the reactive model.** This is the same "runs once" fact behind the props-destructuring refusal (D-01) and the effect-as-derivation refusal (D-02) — one mental model, three rules.

## Arguments Against (trade-offs accepted)

- For a condition that is truly static for the component's lifetime (e.g., a feature flag resolved at build time, not a signal), an early return is harmless and arguably clearer than a `<Show>`.
- Early returns are a familiar, low-ceremony idiom; `<Show>`/`<Switch>` add JSX nesting.

## Verdict

Refuse early returns before JSX whenever the condition reads a signal, a resource, or anything reactive — which covers the overwhelming majority of real cases (`loading`, `error`, feature toggles driven by a store). Branching on reactive state lives in JSX: `<Show>`, `<Switch>`, `<Suspense>`.
