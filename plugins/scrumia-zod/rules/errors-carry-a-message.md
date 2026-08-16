# Errors carry a message where a user reads them

*Refusal.* A schema parsing user-facing input that leaves every message to the
default. At that boundary the message is part of the schema, and it is
field-targeted.

## What is refused

```ts
// ❌ a signup form; the user is told "Invalid input: expected string"
const Signup = z.object({
  email: z.email(),
  password: z.string().min(8),
});
```

The default names the type the parser was expecting — `Invalid input: expected
string, received number` — which is what the upstream docs show in the
`.parse()` failure example. The person filling in the form needs to know which
field, and what to do about it. The boundary is the schema consumer, so the
boundary is where the message lives.

## What is written instead

In Zod v4 the message is the **`error` parameter**, accepted by every schema
and every check — as a string, or as a function the docs call an *error map*.
The upstream examples verbatim:

```ts
z.string("Not a string!");

z.string("Bad!");
z.string().min(5, "Too short!");
z.uuid("Bad UUID!");
z.iso.date("Bad date!");
z.array(z.string(), "Not an array!");
z.array(z.string()).min(5, "Too few items!");
z.set(z.string(), "Bad set!");
```

The params-object form is equivalent, and is what carries the other options:

```ts
z.string({ error: "Bad!" });
z.string().min(5, { error: "Too short!" });
z.uuid({ error: "Bad UUID!" });
z.iso.date({ error: "Bad date!" });
z.array(z.string(), { error: "Not an array!" });
z.array(z.string()).min(5, { error: "Too few items!" });
z.set(z.string(), { error: "Bad set!" });
```

A function gets the issue and can branch on it — this is how "required" is
told apart from "wrong type", which a fixed string cannot do:

```ts
z.string({
  error: (iss) => iss.input === undefined ? "Field is required." : "Invalid input."
});
```

The issue object carries the discriminator (`iss.code`), the input (`iss.input`),
the originating schema (`iss.inst`), and the path (`iss.path`). Returning
`undefined` from a customizer defers to the next level of the precedence chain.

**v3 names do not apply.** `errorMap`, `invalid_type_error`, `required_error`
and the standalone `message` param are v3 vocabulary; v4 replaced all of them
with a single `error` parameter. A rule written against v3 raises false
positives here, which is why the pin is stated on every rule in this module.

### Getting the messages back out, per field

The message being on the schema is half of it — the boundary also has to hand
the UI something field-shaped. Zod ships that, so it is never hand-rolled. The
upstream examples:

```ts
const flattened = z.flattenError(result.error);
// { formErrors: string[], fieldErrors: { [key: string]: string[] } }
```

```ts
const tree = z.treeifyError(result.error);
// nested object mirroring the schema:
{
  errors: [ 'Unrecognized key: "extraKey"' ],
  properties: {
    username: { errors: [ 'Invalid input: expected string, received number' ] },
    favoriteNumbers: {
      errors: [],
      items: [
        undefined,
        { errors: [ 'Invalid input: expected number, received string' ] }
      ]
    }
  }
}
```

```ts
const pretty = z.prettifyError(result.error);
// ✖ Unrecognized key: "extraKey"
// ✖ Invalid input: expected string, received number
//   → at username
// ✖ Invalid input: expected number, received string
//   → at favoriteNumbers[1]
```

- `z.flattenError()` — `{ formErrors, fieldErrors }`, for a flat one-level form.
- `z.treeifyError()` — a nested object mirroring the schema, for nested or array
  fields: `tree.properties?.email?.errors`.
- `z.prettifyError()` — a multi-line human-readable string, for a log or CLI,
  not for a form.
- `z.formatError()` is **deprecated**; `z.treeifyError()` replaces it.

Iterating `error.issues` by hand to rebuild a per-field map is re-implementing
`flattenError`, and it is a finding for the same reason the twin type is.

### Precedence, when a message does not appear

v4 resolves four sources, highest first — a message set lower down is silently
outranked, which is what a "my custom error is ignored" report usually is:

1. schema-level — `z.string("Not a string!")`
2. per-parse — `schema.parse(v, { error: (iss) => … })`
3. global — `z.config({ customError: (iss) => … })`
4. locale — `z.config(z.locales.en())`

A global map or a locale is a legitimate way to satisfy this rule across a
whole app: the requirement is that the boundary produces field-targeted prose a
user can act on, not that every schema carries a literal string.

## Why

A user reading a form failure needs the field and the action, not the type the
parser expected. The default message — `Invalid input: expected string,
received number` — is a developer's view of the failure: it tells the reader
what shape the parser wanted, which is information the user already has by
holding the cursor on the field that failed. The schema is the only place a
field-targeted message can live, because the schema is the only place the
field name is known. Pushing the message into the parser output, the UI, or a
wrapper is re-implementing it where the field name is no longer there.

## Sources complémentaires

- `https://zod.dev/error-customization` — *The `error` parameter*, *params-object form*, *error map function*, *selective override*, *per-parse customization*, *global customization*, *internationalization*. Version pin: **Zod v4**.
- `https://zod.dev/error-formatting` — *z.flattenError*, *z.treeifyError*, *z.prettifyError*, *z.formatError* (deprecated). Version pin: **Zod v4**.
