# Validation sits at the trust boundary

*Refusal.* A `.parse()` on a value the type system already proved. Runtime
validation is the seam between trusted and untrusted code, not a layer applied
everywhere in the hope of catching something.

## What a trust boundary is

The seam where a value arrives from somewhere the compiler cannot see:

- **network** — `fetch`, `axios`, an RPC client, a webhook body
- **file** — `fs.readFile`, `readFileSync`, a config or fixture on disk
- **user input** — a form submission, a query string, a CLI argument
- **message queue** — a subscriber payload, an event bus handler
- **process environment** — `process.env`, which is `string | undefined` and
  nothing more, whatever the deployment claims

What these share is that the TypeScript type is an *assertion by the
developer*, not a fact. `const user: User = await res.json()` compiles because
`json()` returns `any`. The schema is what turns that assertion into a check.

## What is refused

```ts
// ❌ the argument was built two lines up, in this file, by this module
function computeTotal(order: Order) {
  const validated = OrderSchema.parse(order);   // proves nothing
  return validated.items.reduce((n, i) => n + i.price, 0);
}

const order = buildOrder(cart);   // typed Order, constructed here
computeTotal(order);
```

The upstream docs are explicit: *"`Zod` returns a strongly-typed deep clone of
the input."* `.parse()` is a clone operation. On a value the type system
already proved, the clone is the entire cost and there is no guarantee to
buy — the parse cannot fail unless the constructor is broken, and if the
constructor is broken the parse is not where that gets fixed. What it actually
does:

- every call pays a deep clone (the `valid` return value is a fresh object),
- the schema becomes a second declaration of a shape the compiler already
  enforces, which is the same twin [`schema-as-source-of-truth`](schema-as-source-of-truth.md)
  refuses,
- a reader can no longer tell which parses in the file are load-bearing.

## What is written instead

Parse once, at the seam, and let the inferred type carry the guarantee inward.
The upstream pattern is:

```ts
Player.parse({ username: "billie", xp: 100 });
// => returns { username: "billie", xp: 100 }
```

That is the seam form: an untyped input enters, the parser produces a typed
result, and the result is what the rest of the code consumes. The inward
trust is sound because the return type is `z.infer<typeof OrderSchema>` — the
single declaration
[`schema-as-source-of-truth`](schema-as-source-of-truth.md) requires.

```ts
async function loadOrder(id: string): Promise<Order> {
  const res = await fetch(`/api/orders/${id}`);
  return OrderSchema.parse(await res.json());   // the boundary
}

function computeTotal(order: Order) {           // trusts its type
  return order.items.reduce((n, i) => n + i.price, 0);
}
```

`Order` being `z.infer<typeof OrderSchema>` is what makes the inward trust
sound. Where the type is a hand-written twin, the boundary proves the
schema's shape and the callee trusts a different one.

### `.parse` or `.safeParse` at that boundary

Both belong at the seam; they differ in who handles the failure. The upstream
docs:

```ts
try {
  Player.parse({ username: 42, xp: "100" });
} catch(error){
  if(error instanceof z.ZodError){
    error.issues;
    /* [
      {
        expected: 'string',
        code: 'invalid_type',
        path: [ 'username' ],
        message: 'Invalid input: expected string'
      },
      {
        expected: 'number',
        code: 'invalid_type',
        path: [ 'xp' ],
        message: 'Invalid input: expected number'
      }
    ] */
  }
}
```

```ts
const result = Player.safeParse({ username: 42, xp: "100" });
if (!result.success) {
  result.error;   // ZodError instance
} else {
  result.data;    // { username: string; xp: number }
}
```

- `.parse()` **throws** a `ZodError`. Right where a failure is exceptional and
  an error boundary or a middleware above already handles it.
- `.safeParse()` returns `{ success: true, data }` or `{ success: false, error }`
  — no `try`/`catch`. Right where the failure is an expected outcome to render,
  which is every user-facing boundary, and pairs with the field-targeted
  messages [`errors-carry-a-message`](errors-carry-a-message.md) asks for.

A `.parse()` wrapped in a `try`/`catch` that only converts the throw into a
returned value is `.safeParse()` written the long way.

## Why

The compiler's guarantee stops at the seam. Inside a module, the code is
already proving its own invariants by construction — a value built here is
typed as what was built here, and a parse on it adds cost without adding
trust. At the seam, the situation inverts: the value has crossed a boundary
the compiler cannot see, and the parse is the only thing that recovers the
guarantee the type claims. Validation is the seam, not the body — applying
it everywhere inverts the cost and the benefit, and the calls that matter
become indistinguishable from the calls that don't.

## Sources complémentaires

- `https://zod.dev/basics` — *Parsing data*, *Handling errors*, *`.parse` / `.safeParse`*. Version pin: **Zod v4**.
- `https://zod.dev/api` — `parse`, `safeParse`, `parseAsync`, `safeParseAsync` entries. Version pin: **Zod v4**.
