# Runtime validation — business rules

## Value

For whoever builds a React or SolidJS app — the type a function expects at
its boundary is the type it actually receives at runtime, with errors that
mean something to the caller. It matters because TypeScript's compile-time
guarantees stop at the trust boundary: an API response typed as `User` is
typed as `User` only because the developer trusts the server. The schema is
what makes that trust explicit. Not instrumented today: nothing counts how
many trust boundaries a project actually validates.

## The schema is the source of truth

When a Zod schema exists for a value, the TypeScript type that represents
the same value is derived from the schema — `z.infer<typeof Schema>`, never a
hand-written `interface`. A hand-written twin drifts the moment the schema
moves; a derived type cannot. The plugin refuses a separate declaration
that could have been inferred.

## Validation is at the boundary

Runtime validation earns its cost at the boundary between trusted and
untrusted code: an API response, a form submission, a parsed URL, a message
from another process. A function that takes an `User` it constructed itself
two lines up is not a candidate for validation — the cost is paid for an
answer the type system already gave. The plugin refuses validation in
internal call paths as over-engineered.

## Errors carry a message

A schema used at a trust boundary declares its error messages. A generic
`"Invalid input"` is a debugging floor, not a user experience; a
field-targeted message is what a caller can act on. The plugin refuses a
schema at a user-facing boundary without `errorMap` or per-field messages.

## Sources are cited, with the version

The authoritative source is `https://zod.dev/llms.txt`. The plugin's README
cites it and pins the major version the refusal rules were written against,
because Zod's API moves between majors and a rule written for v3 against a
v4 codebase is a false positive.

## What the plugin contributes

| Register | Module that opens it | Scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | `scrumia-impl-reactjs`, `scrumia-impl-solidjs` |
| `review` | `scrumia-github-project` (via `scrumia-review`) | same |

The plugin does not depend on `scrumia-rhf` to compose — it ships and applies
without forms in the picture.

## Business rules

- **BR-1** — A Zod schema's inferred type is the source of truth; a
  hand-written twin that could have been derived is refused.
- **BR-2** — A schema at a trust boundary carries error messages targeted at
  the field they describe; a generic `"Invalid input"` is refused at a
  user-facing boundary.
- **BR-3** — Runtime validation is applied at trust boundaries only;
  validation in internal call paths is refused as over-engineered.
- **BR-4** — The plugin's README cites `https://zod.dev/llms.txt` and pins
  the version the rules were written against.
- **BR-5** — The plugin contributes to the `implement` and `review`
  registers, scoped to `scrumia-impl-reactjs` and `scrumia-impl-solidjs`.

## Vocabulary

**"Trust boundary"** names the seam between code that produced a value and
code that consumes it across a boundary the type system cannot reach:
network, file, user input, message queue. **"Inferred type"** names the
TypeScript type a schema produces through `z.infer<>` or its equivalent,
which is what makes BR-1's refusal possible.
