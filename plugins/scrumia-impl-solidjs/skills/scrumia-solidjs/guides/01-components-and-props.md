# Components and Props

> How to access props, group them, and keep a component's state honest.

## Prerequisites

None — read this first, before writing a component.

## Rules

### Rule 1: Access props through `props.x`, never destructure

Destructuring reads once and disconnects reactivity — the bug appears at the first update, silently: the component runs once, only tracked expressions re-run. Full rationale: [D-01](../decisions/D-01-no-destructured-props.md).

#### Correct

```tsx
export function Price(props: { amount: number }) {
  return <span>{format(props.amount)}</span>
}
```

#### Incorrect

```tsx
export function Price(props: { amount: number }) {
  const { amount } = props
  return <span>{format(amount)}</span>
}
```

---

### Rule 2: Group or default props with `mergeProps` / `splitProps`, not destructuring

These helpers cover the two real reasons to destructure — defaults, grouping — while keeping the access inside a tracked read.

#### Correct

```tsx
const merged = mergeProps({ currency: 'EUR' }, props)
const [local, rest] = splitProps(props, ['amount'])
```

---

### Rule 3: A component owns its local state, or receives a signal — never both

Duplicated state (a prop copied into a local signal) desynchronises; it is the frontend's version of two sources of truth. If a value can be read from `props`, read it from `props` — don't seed a local signal from it.

---

### Rule 4: Compose through `children` and split props, not wrapper hierarchies

Deep wrapper hierarchies — components whose only job is to pass props down — add indirection without adding a rendering responsibility. Composition means `children` and split props, not enrobing.

---

## With the practices

**`scrumia-practice-solid`** — situated here:
- **S**: one component, one rendering responsibility; logic extracted into primitives ([05-project-layout](05-project-layout.md)).
- **O**: variation through composition — props, `children` — not through boolean-prop proliferation (Rule 4 above).
- **L**: a component that accepts another's props honours their contract.
- **I**: narrow props, no catch-all `config` object.

> Decision rationale: [D-01 — Refuse destructured props](../decisions/D-01-no-destructured-props.md)
