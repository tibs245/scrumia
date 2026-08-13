# D-01: Refuse `useEffect` for derived state

**Status**: Adopted
**Date**: 2026-08-13
**Impacts**: [guides/02-state-and-derivations.md](../guides/02-state-and-derivations.md), [guides/03-control-flow.md](../guides/03-control-flow.md), [guides/04-data-boundary.md](../guides/04-data-boundary.md)

## Context

The canonical defect, in React 19's own words:

> "**When something can be calculated from the existing props or state, [don't put it in
> state]. Instead, calculate it during rendering.** This makes your code faster (you avoid
> the extra 'cascading' updates), simpler (you remove some code), and less error-prone (you
> avoid bugs caused by different state variables getting out of sync with each other)."
> — [You Might Not Need an Effect — Updating state based on props or state](https://react.dev/learn/you-might-not-need-an-effect#updating-state-based-on-props-or-state)

```tsx
const [fullName, setFullName] = useState('')
useEffect(() => { setFullName(firstName + ' ' + lastName) }, [firstName, lastName])
```

The page-level summary is the rule to keep:

> "**If you can calculate something during render, you don't need an Effect.**"
> — [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

React 19's docs also recommend `useMemo` for expensive calculations and `key` for
resetting a child when an identity prop changes:

> "By passing `userId` as a `key` to the `Profile` component, you're asking React to treat
> two `Profile` components with different `userId` as two different components that should
> not share any state. Whenever the key (which you've set to `userId`) changes, React will
> recreate the DOM and reset the state of the `Profile` component and all of its
> children."
> — [You Might Not Need an Effect — Resetting state with a key](https://react.dev/learn/you-might-not-need-an-effect#resetting-state-with-a-key)

## Arguments For

- **The defect is invisible at the second render.** `setFullName` schedules an update; the
  first render uses a stale value, then the next render commits the right one. The bug
  rarely shows up in screenshots taken by hand and shows up only in the test that races
  the timing.
- **The fix is the right shape anyway.** `const fullName = firstName + ' ' + lastName`
  *is* the data flow; writing it twice (once into state, once into an Effect that
  mirrors it) hides it.
- **It is the principle behind a chain of patterns.** The same page goes on to derive
  `useMemo` (caching), `key` (resetting), and the "store the id, not the item" pattern
  from the same observation. Refusing the root makes the rest legible.
- **The cost is zero.** `fullName` is exactly as readable as `firstName + ' ' + lastName`
  inlined; there is no ergonomic case for the duplicate state.

## Arguments Against (trade-offs accepted)

- For genuinely expensive computations, inlining without `useMemo` recomputes on every
  render. React 19's answer is `useMemo` — also covered by this rule, which keeps the
  computation in render and caches it explicitly.
- React Compiler removes the need for manual `useMemo` in many cases. The module's
  `react_compiler` setting names this; the rule stays, the ergonomics get better.

## Verdict

Refuse `useEffect` for derived state. Calculate during render. Reach for `useMemo` when
the computation is expensive, for `key` when an identity prop changes, and for storing
the *id* of the selection rather than the *item* when state has to be reflected back into
props.
