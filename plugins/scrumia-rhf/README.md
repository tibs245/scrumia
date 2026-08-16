# scrumia-rhf

The implementation slot, for React apps that carry their forms through
[React Hook Form](https://react-hook-form.com) — a form declares a
resolver, its inputs are registered through the library, and its state
is read through the library's API rather than the DOM. Plugs in app by
app, scoped to `scrumia-impl-reactjs` only.

## What it answers

How React Hook Form gets written in an app that plugs this module in:
schema-driven validation as one source of truth, declarative input
registration, library-aligned state access — as three refusal rules
read on demand, plus an audit skill that measures an existing app
against them.

## What it refuses

- No form without a resolver — validation is one schema, not per-field
  logic.
- No `useState` + `onChange` pair where `register("name")` already
  provides the same — the library owns registered inputs.
- No state read through `document.querySelector`, `formRef.current`,
  `FormData(form)` or `event.target.elements` — the library's API is
  the source of truth.

Each is a `rules/<name>.md` file, citing
[`https://react-hook-form.com`](https://react-hook-form.com) (pinned to
**v7**, the major version the rules were written against).

## What it ships

| Skill | Role |
|---|---|
| `rhf-audit` | Measures an existing React app against the three refusals — resolver coverage, input classification, state channel. Reports; fixes nothing itself. |

## Settings it reads

None. The plugin is dependency-free and reads no configuration. A
project that needs an exemption (a genuinely-controlled input the
audit cannot prove is justified) records it in
`.scrumia/impl/scrumia-rhf.md`, and the audit honours the exemption on
its next pass.

## What it expects to find

An app that lists `scrumia-impl-reactjs` in its own `extends`; within
it, `src/**/*.tsx` and `src/**/*.ts` are what the rules apply to. A
project running `scrumia-impl-solidjs` (and no React impl) pays no
cost — the contributions are filtered out by the composition's
per-module scope, and `scrumia-extends`'s table omits the rows.

## Source

The rules cite [`https://react-hook-form.com`](https://react-hook-form.com),
pinned to **v7**. The library's reference for `useForm`, `register`,
`Controller`, `formState`, `watch`, `getValues` and `handleSubmit` is
the single source — a rule not stated there is not in the plugin. A
rule whose citation has drifted from v7 is rewritten; a rule the v7
documentation no longer states is removed, not paraphrased.

The plugin does not draw from blog posts, conference talks, or
third-party tutorials. The library's own documentation is the single
source — a rule the documentation does not state is not in the plugin.

## Resolvers supported

The plugin is resolver-agnostic. Any adapter `@hookform/resolvers`
ships — Zod, Yup, Joi, Vest, TypeBox, Superstruct — works without a
plugin change. A project adopting Zod as its schema library pairs this
plugin with `scrumia-zod` (the runtime-validation plugin) for the
resolver-side wiring; the pairing is documented, neither plugin
requires the other.

## Versioning

The plugin's version tracks the form library's major. A rule written
for v7 against a v6 codebase raises false positives (`useForm`
signature, `Controller` props, `formState` keys). The pin is the
statement the rules are current as of that version. Bumping the major
version the rules are pinned to is a breaking change for the plugin.
