# Form management

**Status**: draft

## In brief

Declarative form management for React implementations. A form is described by
its schema, its inputs are registered through the library, and its state is
read through the library's API rather than the DOM. The plugin that carries
it (`scrumia-rhf`) targets React alone — SolidJS forms follow a different
paradigm and live elsewhere. Authoritative source:
`https://react-hook-form.com`.

## Links

- Implemented by: `plugins/scrumia-rhf/` — `extends.json` contributes refusal
  rules to the `implement` and `review` registers, scoped to
  `scrumia-impl-reactjs` only.
- Authority: `https://react-hook-form.com` — the plugin's README cites it
  and pins the version the rules were written against.
- Pairs with: `features/business/runtime-validation/` for the resolver
  pattern — Zod schemas feed `react-hook-form` through
  `@hookform/resolvers/zod`. The two plugins compose independently; the pair
  is documented but neither requires the other.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding what the plugin refuses, what it requires, and why the React-only scope |
| `qa.md` | writing or running the acceptance scenarios for the form rules |
| `tech.md` | tracing how the plugin contributes to the `implement` and `review` registers |
| `CHANGELOG.md` | history of changes to this spec |

No `ux.md`, `legal.md`, `security.md`: a form library carries no interface of
its own (the form's UX is the consuming app's), no personal data in itself,
and no privileged surface beyond what validation already covers.
