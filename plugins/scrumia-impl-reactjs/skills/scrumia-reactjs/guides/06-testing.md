# Testing

> Behaviour-first component tests, Server Components tested through their rendered output,
> Playwright kept outside the fast loop.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)
- [03-control-flow.md](03-control-flow.md)
- [04-data-boundary.md](04-data-boundary.md)

## Rules

### Rule 1: Test what the user observes — through rendered output, not internals

React Testing Library plus Vitest: render, interact through roles and labels, assert on
the rendered result. A test that reads a `useState` cell directly is coupled to an
implementation detail the next refactor will break. If the project writes acceptance
criteria, the `AC-n` appears in the test name or an adjacent comment.

#### Correct

```tsx
test('disables checkout while the cart is empty', async () => { // AC-2
  render(<Checkout cartId="c1" />)
  expect(await screen.findByRole('button', { name: /pay/i })).toBeDisabled()
})
```

---

### Rule 2: Server Components are tested as their rendered output, not by importing them

A Server Component cannot be rendered in a Jest/Vitest environment that has no RSC
runtime. The test reads the rendered HTML (snapshot or partial-match) or imports a
purely-presentational child of the Server Component instead. Server-side test
infrastructure belongs to the framework (Next.js, Remix, …) — this module's role is
to refuse the pattern of importing a `'use server'` module into a client test and
running it there.

#### Correct

```tsx
// Test the presentational child the Server Component composes
test('renders the invoice total when given an invoice', () => {
  render(<InvoiceTotal invoice={fixtureInvoice} />)
  expect(screen.getByText(/€42\.00/)).toBeInTheDocument()
})
```

#### Incorrect

```tsx
// Imports the Server Component into a unit test
import InvoicePage from '@/app/dashboard/page' // 'use server' inside — fails on import
```

---

### Rule 3: Reusable primitives (`useSomething`, `createSomething`) get their own unit test

A Hook or a small factory is the one place where testing outside a component is the
right call — render it inside a tiny harness, assert on its rendered effect.

#### Correct

```tsx
import { useState } from 'react'

test('debounces to the last value', async () => {
  function Harness() {
    const [v, setV] = useState('a')
    const debounced = useDebounced(v, 50)
    return (
      <>
        <button onClick={() => setV('b')}>b</button>
        <span>{debounced}</span>
      </>
    )
  }
  render(<Harness />)
  await userEvent.click(screen.getByRole('button'))
  vi.advanceTimersByTime(50)
  expect(screen.getByText('b')).toBeInTheDocument()
})
```

---

### Rule 4: Mock at the data boundary, not at `fetch` globally

The data boundary in React 19 is the feature's `api.ts` (Server-side) or the Promise
the Server Component creates (Client-side `use(promise)`). Mocking `fetch` globally
couples every test to transport details; do it only in the api layer's own tests.

```tsx
vi.mock('./api')
```

---

### Rule 5: Playwright for cross-page journeys, and only there

End-to-end tests don't take part in the fast loop; they gate the merge, not the
keystroke. The Playwright test invokes a Server Component the same way the browser
does — through a built app — and asserts on the rendered DOM.

---

## With the practices

**`scrumia-practice-tdd`** — the cycle runs on Vitest (`test_runner` setting). For a
component: start from the acceptance criterion, write the failing Testing Library test
(`getByRole`, user events — Rule 1 above), then implement. Hooks follow the classic
unit cycle (Rule 3). Playwright journeys stay **outside** the red-green loop — too slow
for it; they come after, as integration coverage.

Server Components in React 19 are tested with the framework's recommended approach (Next.js
App Router's testing helpers, etc.). This module does not duplicate what the framework
documents — it refuses the patterns that no framework supports (importing a Server
Component into a client unit test).
