# Form management — business rules

## Value

For whoever ships a React app with user input — forms that describe
themselves through a schema, register their inputs declaratively, and read
their state through one library rather than mixing library calls with DOM
queries. It matters because a form that mixes paradigms is one that
silently drops state on re-render and double-submits on fast clicks. Not
instrumented today: nothing counts how many forms a project ships through
the library's API.

## A form has a resolver

A form using React Hook Form declares a resolver — Zod, Yup, Joi, or any
adapter `@hookform/resolvers` ships. The resolver is what connects the
form's inputs to a schema, and the schema is what makes the validation
rules one source of truth. A form without a resolver falls back to manual
`trigger` calls and per-field validation logic, which is the pattern the
plugin refuses.

## Inputs are registered, not controlled

An input managed with `register("name")` is owned by the library. An input
managed with `useState` + `onChange` is owned by the developer, and the
library has no view of it. The plugin refuses `useState` paired with an
`onChange` that could have been a `register` call, because the cost of the
state-management pattern is paid for a feature the library already provides.

## Form state is read through the library

`watch`, `getValues`, `formState`, `handleSubmit` — these are how a React
Hook Form consumer reads form state. `document.querySelector("form").value`
is how a developer reads form state when they have stopped trusting the
library. The plugin refuses the latter; the former is what the rest of the
app composes against.

## React only

The plugin scopes its contributions to `scrumia-impl-reactjs`. SolidJS
forms follow a reactive paradigm that makes the React Hook Form API a
mismatch; a SolidJS form plugin would carry its own rules. The plugin's
`extends.json` declares the scope explicitly so a SolidJS project pays no
cost.

## Sources are cited, with the version

The authoritative source is `https://react-hook-form.com`. The plugin's
README cites it and pins the major version the rules were written against,
because the API moves between majors and a rule written for v6 against a
v7 codebase is a false positive.

## What the plugin contributes

| Register | Module that opens it | Scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | `scrumia-impl-reactjs` |
| `review` | `scrumia-github-project` (via `scrumia-review`) | same |

The plugin does not depend on `scrumia-zod` to compose — a project may
adopt it with Yup or Joi as the resolver — but the pairing is documented
in `runtime-validation/`.

## Business rules

- **BR-1** — A form using React Hook Form declares a resolver; a form
  without one is refused.
- **BR-2** — Inputs are registered through `register` or `Controller`, not
  managed with `useState` + `onChange`.
- **BR-3** — Form state is read through `watch`, `getValues`, `formState`
  or `handleSubmit`; DOM-level reads are refused.
- **BR-4** — The plugin's README cites `https://react-hook-form.com` and
  pins the version the rules were written against.
- **BR-5** — The plugin contributes to the `implement` and `review`
  registers, scoped to `scrumia-impl-reactjs` only.

## Vocabulary

**"Resolver"** names the adapter that connects a schema to React Hook Form
— `@hookform/resolvers/zod` is one. **"Registered input"** names an input
the library owns, as opposed to a "controlled input" the developer owns.
