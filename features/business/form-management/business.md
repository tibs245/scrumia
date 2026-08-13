# Form management — business rules

## Value

For whoever ships a web app with user input — forms that describe
themselves through a schema, register their inputs declaratively, and
read their state through one library rather than mixing library calls
with DOM queries. It matters because a form that mixes paradigms is
one that silently drops state on re-render and double-submits on fast
clicks. Not instrumented today: nothing counts how many forms a project
ships through the library's API.

## Sources

This module's authority is the form library's own documentation, not
community advice. Every rule the plugin ships cites the source below;
a rule without a citation is not shipped, and a citation that drifts
is rewritten against the version the rules were pinned against.

| Source | URL | What it provides |
|---|---|---|
| React Hook Form documentation | `https://react-hook-form.com` | The form library's reference: hook signatures (`useForm`, `useController`, `useFormContext`), resolver contract, field registration, validation modes, error state, performance model. The plugin pins to the major version the rules were written against. |

The plugin does not draw from blog posts, conference talks, or
third-party tutorials. The library's own documentation is the single
source — a rule not stated there is not in the plugin.

## The module's role

The module's business rules are statements about *what this module is
and what it does for the project that adopts it*. They are not a list
of good practices — those live in the plugin's `rules/` directory,
one file per behavioural rule, each citing the source above.

- **BR-1** — The module extends `scrumia-impl-reactjs`. A React project
  gains the module's form directives; a project running SolidJS (and
  not React) pays no cost. The framework scope is a constraint, not a
  preference: form libraries are not interchangeable across frameworks,
  and pretending otherwise produces rules that do not transfer.

- **BR-2** — The module can be taken directly as an implementation module
  by a React project that does not run the broader ScrumIA composition.
  The form library's API stands on its own; the framework-specific
  scoping is the default, not a requirement.

- **BR-3** — Every rule the module ships cites the form library's own
  documentation — never a blog post, never a tutorial, never a community
  pattern. A rule whose citation has drifted from the pinned version is
  rewritten; a rule the documentation no longer states is removed, not
  paraphrased.

- **BR-4** — The module helps web development carry solid notions of
  form design. "Solid" means schema-driven (validation is one source),
  declarative (inputs are registered, not managed), and library-aligned
  (state is read through the library's API, not the DOM). Not
  fashionable, not minimal, not framework-agnostic — form design has
  React-shaped answers because React Hook Form is React-shaped.

- **BR-5** — The module anchors forms in the application's DNA, not in
  a separate audit pass. Every form declares a resolver; every input is
  registered through the library; every state read goes through the
  library's API. A form that mixes paradigms is the regression the
  test catches, not a thing a documentation page warns about.

- **BR-6** — The module provides patterns for the recurring form problems
  a web app meets: dynamic field arrays, conditional fields, multi-step
  wizards, async validation, server-side errors surfaced into the form,
  focus management between fields, submission state. Each pattern carries
  its source citation, its trade-offs (e.g. controlled vs. uncontrolled
  cost), and the failure mode it prevents.

- **BR-7** — The module teaches how to design and audit forms — not
  only *what* a form should look like. The audit skill answers "is this
  form using the library's API end-to-end?" the way an implementation
  module answers "is this code correct?" — by refusing the shape that
  would otherwise pass. A reader of the module's docs finishes with
  both the patterns and the practice of catching a mixed paradigm.

## What the plugin contributes

The plugin (`scrumia-rhf`) carries refusal rules to two registers,
scoped to one implementation module by default:

| Register | Module that opens it | Default scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | `scrumia-impl-reactjs` |
| `review` | `scrumia-github-project` (via `scrumia-review`) | same |

The plugin does not depend on `scrumia-zod` to compose. A project may
adopt React Hook Form with Yup, Joi, or any other adapter the resolver
package ships — the Zod pairing is documented but neither plugin
requires the other.

## Vocabulary

**"Resolver"** names the adapter that connects a schema to the form
library — `@hookform/resolvers/zod` is one. **"Registered input"** names
an input the library owns; a "controlled input" is one the developer
owns, and the module considers the latter a regression unless it is
genuinely necessary. **"Solid"** in BR-4 means grounded in the library's
documented API, not in a community convention. **"DNA"** in BR-5 names
the project's forms: every form's structure is what its code asserts.
