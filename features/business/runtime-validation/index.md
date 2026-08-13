# Runtime validation

**Status**: draft

## In brief

Type-safe runtime validation at trust boundaries, applicable to React and
SolidJS implementations. A schema is the source of truth — the inferred type
flows from it, error messages are part of it, and validation is applied where
untrusted data enters the application, not on every internal call. The plugin
that carries it (`scrumia-zod`) is one realisation, with
`https://zod.dev/llms.txt` as its authoritative source.

## Links

- Implemented by: `plugins/scrumia-zod/` — `extends.json` contributes
  refusal rules to the `implement` and `review` registers, scoped to
  `scrumia-impl-reactjs` and `scrumia-impl-solidjs`.
- Authority: `https://zod.dev/llms.txt` — the plugin's README cites it and
  pins the version the rules were written against.
- Defers to: `features/business/html-css-and-accessibility/` for nothing in
  particular — these are independent capabilities a project may take
  separately.
- Defers to: `features/business/form-management/` for how Zod pairs with
  React Hook Form's resolver API; the two share a usage pattern but neither
  depends on the other to compose.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding what the plugin refuses, what it requires, and which trust boundaries the rules apply to |
| `qa.md` | writing or running the acceptance scenarios for the validation rules |
| `tech.md` | tracing how the plugin contributes to the `implement` and `review` registers |
| `CHANGELOG.md` | history of changes to this spec |

No `ux.md`, `legal.md`, `security.md`: a schema library carries no interface,
no personal data in itself, and no privileged surface — though it stands at
the boundary where untrusted data enters, which `business.md` states.
