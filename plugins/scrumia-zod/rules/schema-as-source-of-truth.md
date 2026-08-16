# The schema is the source of truth

*Refusal.* A TypeScript type or interface declared next to a schema that restates
the schema's shape. The type is derived from the schema, never written twice.

## What is refused

```ts
const User = z.object({ username: z.string(), xp: z.number() });

// ❌ the schema says one shape, the interface says another, nothing links them
interface User { username: string; xp: number }
```

The upstream example shows the *derived* form: `Player` carries the same two
fields the schema declares, and `z.infer` extracts the type. The inverse above
— the schema on one line, the interface on the next, no link between them —
compiles today and is the failure mode this rule names. Add `email` to the
schema and the interface keeps its old shape; nothing fails at compile time;
the drift is found at runtime, in whichever consumer trusted the interface.

## What is written instead

Derive the type from the schema with `z.infer`. This is the upstream example
verbatim, with our note attached:

```ts
const Player = z.object({
  username: z.string(),
  xp: z.number()
});

// extract the inferred type
type Player = z.infer<typeof Player>;

// use it in your code
const player: Player = { username: "billie", xp: 100 };
```

One declaration, one shape. When the schema gains a field, every consumer of
`Player` is updated by the compiler, with no separate file to keep in step.

When a `.transform()` makes the input and output types diverge, the upstream
docs give two extractors rather than one. The pattern is:

```ts
const mySchema = z.string().transform((val) => val.length);

type MySchemaIn  = z.input<typeof mySchema>;   // string
type MySchemaOut = z.output<typeof mySchema>;  // number — same as z.infer
```

`z.infer` is `z.output`. A consumer holding pre-transform data wants
`z.input`; reaching for `z.infer` there is the same duplication bug with a
different symptom: a type that compiles and describes the wrong side of the
boundary.

## Why

The compiler cannot propagate a schema change to a hand-written interface,
because the interface is the thing the compiler is reading. The two
declarations are equal at first, then drift by one field, and the parser stops
producing what the type claims. The failure is silent — no type error, no test
that fires by default — and surfaces only when a downstream consumer trips on a
property that is no longer there. `z.infer` exists so the schema is the only
declaration worth keeping in step, and the compiler does the rest.

## Sources complémentaires

- `https://zod.dev/basics` — *Inferring types*, *Type inference*. Version pin: **Zod v4**.
- `https://zod.dev/api` — `z.infer`, `z.input`, `z.output` entries. Version pin: **Zod v4**.
