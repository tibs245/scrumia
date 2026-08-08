# D-04: `<For>` vs `<Index>` — never swapped

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/03-control-flow.md](../guides/03-control-flow.md)

## Context

```tsx
<For each={users()}>{u => <Row user={u} />}</For>
<Index each={values()}>{v => <Cell value={v()} />}</Index>
```

`<For>` keys its rendered rows **by reference** (or by an explicit key you provide): if `users()` returns the same object at the same logical position, the DOM node for that row is reused. `<Index>` keys **by position**: the DOM node at index `i` is reused regardless of what value now lives there, and the item itself is passed down as a signal.

Both compile and both render correct output when swapped — that is exactly what makes the mistake hard to notice: `<Index>` over a list of freshly-created objects (a `.map()` result, a page of API data) sees a "new" reference at every position on every update and recreates every row's DOM; `<For>` over a list of primitives compares primitive equality per element and behaves acceptably by luck for simple cases, but loses `<Index>`'s per-item signal granularity where it would have helped.

## Arguments For

- **Wrong choice degrades silently to "still works, just slower."** There's no error — only DOM nodes being torn down and rebuilt on every update instead of patched, invisible without a profiler.
- **The rule of thumb is cheap to apply and matches the primitive/object split already used elsewhere** (D-01's `props.x`, memo vs effect): objects → `<For>` (reference identity is meaningful), primitives → `<Index>` (position is what's stable, and `<Index>` gives each cell its own signal for the value).
- **"Just always use `<For>`" is not a safe default.** It's the more common component in examples, which is precisely why the swap into primitive lists goes unnoticed.

## Arguments Against (trade-offs accepted)

- `<For>` alone would simplify the rule to memorize — one component, no branch.
- For short, rarely-updated lists, the DOM-churn cost of the wrong choice is negligible; enforcing the distinction everywhere is more rigor than the situation needs.

## Verdict

Keep both, matched to what the list contains: `<For>` for lists of objects (keyed by reference/explicit key), `<Index>` for lists of primitives (keyed by position). If a list feels slow, check this pairing first — before reaching for memoisation.
