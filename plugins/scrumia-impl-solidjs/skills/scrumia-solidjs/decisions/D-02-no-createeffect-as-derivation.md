# D-02: Refuse `createEffect` as a derivation

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/02-derivations.md](../guides/02-derivations.md)

## Context

Two SolidJS primitives can both "produce a value from other signals":

```tsx
// Effect-as-derivation
const [total, setTotal] = createSignal(0)
createEffect(() => setTotal(price() * qty()))

// Memo
const total = createMemo(() => price() * qty())
```

Both end with a `total` that reflects `price()` and `qty()`. They are not equivalent underneath: `createEffect` schedules its callback as a side effect after the reactive graph settles, while `createMemo` is itself part of the graph — computed synchronously as a dependency, cached, and re-read like a signal.

## Arguments For

- **Extra scheduling.** The effect-as-derivation path is: signal changes → effect scheduled → effect runs → `setTotal` → dependents of `total` re-run. `createMemo` collapses this to one hop. In a chain of several such effects, each adds a scheduling round-trip.
- **Hidden data flow.** `createMemo` is legible at the declaration site: "`total` is `price() * qty()`." An effect that writes `setTotal` inside its body only reveals that relationship by reading the effect's implementation — the signal declaration alone lies about where the value comes from.
- **It's the same class of bug as duplicated state** (see `01-components-and-props.md`, Rule 3): a value that could be computed is instead stored and kept manually in sync — one more place for the sync to drift.
- **`createEffect` has a real job it should stay legible for**: driving the outside world (DOM writes, `document.title`, storage, analytics). Every effect in a codebase should name an outside-world target; if grep finds one that doesn't, it's a derivation in disguise.

## Arguments Against (trade-offs accepted)

- For a derivation with an expensive side branch (e.g., debouncing before setting), an effect reads more naturally step by step than a single memo expression.
- Some derivations are cheap enough that neither form matters for correctness — the argument is purely about legibility, not behavior.

## Verdict

Refuse `createEffect` as a derivation. Any effect body that calls a signal setter is treated as a finding: rewrite as `createMemo`, or a plain derived function when memoisation isn't needed. Reserve `createEffect` for effects that touch something outside the reactive graph — DOM, storage, analytics, third-party APIs.
