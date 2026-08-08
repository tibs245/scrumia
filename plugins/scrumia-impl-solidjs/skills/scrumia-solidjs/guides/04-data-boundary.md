# Data Boundary: the `api.ts` layer

> Where network calls live, and how a component reaches them without knowing the transport.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)

## Rules

### Rule 1: No network call inside a component

Data access lives in an `api/` layer, reaching components through resources at the boundary. A component that fetches is a component you can't test without a server.

#### Correct

```tsx
// features/checkout/api.ts — the only place that knows the transport
export function fetchCart(id: string): Promise<Cart> { /* … */ }

// In the component: a resource at the boundary, nothing else
const [cart] = createResource(() => props.cartId, fetchCart)
```

The component knows `fetchCart`'s signature, not its transport. Swapping REST for anything else touches `api.ts` and its tests — nothing above.

---

### Rule 2: Route components stay thin

Composition and layout, no business logic. The boundary discipline extends to routes: a route wires features together, it does not decide how they fetch or hold state.

---

Testing this boundary — mocking `api.ts` rather than `fetch` — is covered in [06-testing.md](06-testing.md), Rule 4.

## With the practices

**`scrumia-practice-solid`** — situated here: **D** — the domain doesn't import the fetch layer; the `api/` module is the boundary and injects at the edges (Rule 1 above).
