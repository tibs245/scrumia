# Derivations: `createMemo` vs `createEffect`

> When to derive a value from signals, and when to reach outside the reactive graph instead.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)

## Rules

### Rule 1: Fine-grained reactivity makes React reflexes wrong here

No defensive memoisation, no dependency arrays, no "lift state to force a re-render." A component runs **once**; only its reactive expressions re-run. Every pattern imported from React must survive that fact or be dropped — `createMemo` wrapping a trivial property read, a hand-rebuilt dependency array, or `untrack` used to silence a loop instead of fixing the flow are all the same reflex resurfacing.

---

### Rule 2: `createMemo` derives, `createEffect` synchronises outward

A `createEffect` that writes a signal is a derivation in disguise — it schedules an extra update and hides the data flow. Effects exist for the outside world: imperative DOM, analytics, storage. Full rationale: [D-02](../decisions/D-02-no-createeffect-as-derivation.md).

#### Incorrect

```tsx
const [total, setTotal] = createSignal(0)
createEffect(() => setTotal(price() * qty()))
```

#### Correct

```tsx
const total = createMemo(() => price() * qty())

// createEffect is for the outside world only:
createEffect(() => { document.title = `Cart (${count()})` })
```

---

> Decision rationale: [D-02 — Refuse createEffect as a derivation](../decisions/D-02-no-createeffect-as-derivation.md)
