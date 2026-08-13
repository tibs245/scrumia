# Components and Props

> How to write a React 19 component, decide whether it is a Server Component or a Client
> Component, and pass `ref` as a prop without `forwardRef`.

## Prerequisites

None — read this first, before writing a component.

## Rules

### Rule 1: Server Components by default — add `"use client"` only when the component needs it

A Server Component is rendered on the server and never sent to the browser. A Client
Component is bundled and shipped. The directive is added for *state*, an event handler,
a client-only API, or a Hook the server cannot run; React 19 docs are explicit that the
cost is paid in full:

> "Server Components can reduce the amount of code sent and run by the client. Only
> Client modules are bundled and evaluated by the client."
> ([`"use client"` — React](https://react.dev/reference/rsc/use-client))

A render-agnostic component (no state, no event handler, no client API) should stay a
Server Component; the React 19 docs note that "we don't add the `'use client'`
directive, resulting in `FancyText`'s *output* (rather than its source code) to be sent
to the browser". Full rationale: [D-04](../decisions/D-04-no-unnecessary-client-components.md).

#### Correct

```tsx
// Server Component — no directive, fetched on the server, output streamed to the client
export default async function InvoicePage({ id }: { id: string }) {
  const invoice = await db.invoices.get(id)
  return <Invoice invoice={invoice} />
}
```

```tsx
// Client Component — needs useState, justified
'use client'
import { useState } from 'react'

export function Counter({ initialValue = 0 }: { initialValue?: number }) {
  const [count, setCount] = useState(initialValue)
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Clicked {count} times
    </button>
  )
}
```

#### Incorrect

```tsx
// Marked Client unnecessarily — the entire module ships to the browser for no reason
'use client'
import { formatCurrency } from './formatters'

export function InvoiceTotal({ amount, currency }: { amount: number; currency: string }) {
  return <span>{formatCurrency(amount, currency)}</span>
}
```

---

### Rule 2: Function components — `ref` is a regular prop in React 19, no `forwardRef`

React 19 lets `ref` reach a function component through props directly. The React 19
announcement states:

> "New function components will no longer need `forwardRef`, and we will be publishing a
> codemod to automatically update your components to use the new `ref` prop. In future
> versions we will deprecate and remove `forwardRef`."
> ([React 19 release notes](https://react.dev/blog/2024/12/05/react-19))

Ref callbacks may also return a cleanup function in React 19, which is the complementary
pattern for resources a ref opens.

#### Correct

```tsx
export function MyInput({ placeholder, ref }: { placeholder: string; ref?: React.Ref<HTMLInputElement> }) {
  return <input placeholder={placeholder} ref={ref} />
}
```

#### Incorrect

```tsx
import { forwardRef } from 'react'

export const MyInput = forwardRef<HTMLInputElement, { placeholder: string }>(
  function MyInput({ placeholder }, ref) {
    return <input placeholder={placeholder} ref={ref} />
  }
)
```

---

### Rule 3: A component owns its local state or receives it as a prop — never both

Duplicated state (a prop copied into local state via `useEffect`) is React 19's version
of two sources of truth. The React docs are explicit about the principle:

> "When something can be calculated from the existing props or state, [don't put it in
> state]. Instead, calculate it during rendering."
> ([You Might Not Need an Effect — React](https://react.dev/learn/you-might-not-need-an-effect))

For resetting a child whose prop identifies "which instance this is", the React docs
prefer `key` over Effect-driven state copying:

> "By passing `userId` as a `key` to the `Profile` component, you're asking React to treat
> two `Profile` components with different `userId` as two different components that should
> not share any state. Whenever the key (which you've set to `userId`) changes, React will
> recreate the DOM and reset the state of the `Profile` component and all of its children."
> ([You Might Not Need an Effect — Resetting state with a key](https://react.dev/learn/you-might-not-need-an-effect#resetting-state-with-a-key))

#### Correct

```tsx
export function FullName({ firstName, lastName }: { firstName: string; lastName: string }) {
  // Calculated during render — no state, no effect
  return <span>{firstName} {lastName}</span>
}
```

---

### Rule 4: Compose through `children`, not wrapper hierarchies

A wrapper whose only job is to pass props down is indirection without rendering
responsibility. Composition through `children` keeps the dependency one-way and the
component legible. This is the same rule the SolidJS module states in its own context
and a recognised React idiom; React 19's ref-as-prop change makes it strictly cheaper
because the parent no longer has to forward a ref through a wrapper.

#### Correct

```tsx
export function Card({ children }: { children: React.ReactNode }) {
  return <section className="card">{children}</section>
}
```

---

> Decision rationale: [D-04 — Refuse unnecessary "use client"](../decisions/D-04-no-unnecessary-client-components.md).
