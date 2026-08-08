# Testing

> Behaviour-first component tests, unit-tested primitives, Playwright kept outside the fast loop.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)
- [03-control-flow.md](03-control-flow.md)
- [04-data-boundary.md](04-data-boundary.md)

## Rules

### Rule 1: Test what the user observes, not component internals

Vitest plus `@solidjs/testing-library`: render, interact through roles and labels, assert on the rendered result. A test that reads a signal's value directly is coupled to an implementation detail that the next refactor will break. If the project writes acceptance criteria, the `AC-n` appears in the test name or an adjacent comment.

#### Correct

```tsx
test('disables checkout while the cart is empty', async () => {  // AC-2
  render(() => <Checkout cartId="c1" />)
  expect(await screen.findByRole('button', { name: /pay/i })).toBeDisabled()
})
```

---

### Rule 2: Signals are tested through their rendered effect

If a derived value matters, something in the UI shows it — assert on that. If nothing shows it, ask why the derivation exists.

---

### Rule 3: Reusable primitives (`createSomething`) get their own unit test, with `createRoot` for lifecycle

They are the one place where testing outside a component is the right call.

#### Correct

```tsx
test('debounces to the last value', () => {
  createRoot(dispose => {
    const [v, setV] = createSignal('a')
    const debounced = createDebounced(v, 50)
    setV('b'); vi.advanceTimersByTime(50)
    expect(debounced()).toBe('b')
    dispose()
  })
})
```

---

### Rule 4: Mock network at the `api.ts` boundary, not `fetch` globally

It is a boundary you own the contract of (see [04-data-boundary.md](04-data-boundary.md)). Mocking `fetch` globally couples every test to transport details; do it only in `api.ts`'s own tests.

```tsx
vi.mock('./api')
```

---

### Rule 5: Playwright for cross-page journeys, and only there

End-to-end tests don't take part in the fast loop; they gate the merge, not the keystroke.

---

## With the practices

**`scrumia-practice-tdd`** — the cycle runs on Vitest (`test_runner` setting). For a component: start from the acceptance criterion, write the failing Testing Library test (`getByRole`, user events — Rule 1 above), then implement. Primitives follow the classic unit cycle (Rule 3). Playwright journeys stay **outside** the red-green loop — too slow for it; they come after, as integration coverage.
