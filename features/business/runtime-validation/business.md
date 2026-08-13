# Runtime validation — business rules

## Value

For whoever builds a web app that touches untrusted data — the type a
function expects at its boundary is the type it actually receives at
runtime, with errors that mean something to the caller. It matters
because TypeScript's compile-time guarantees stop at the trust boundary:
an API response typed as `User` is typed as `User` only because the
developer trusts the server. The schema is what makes that trust
explicit. Not instrumented today: nothing counts how many trust
boundaries a project actually validates.

## Sources

This module's authority is the schema library's own documentation, not
community advice. Every rule the plugin ships cites the source below; a
rule without a citation is not shipped, and a citation that drifts is
rewritten against the version the rules were pinned against.

| Source | URL | What it provides |
|---|---|---|
| Zod documentation | `https://zod.dev/llms.txt` | The complete schema-library reference: schema construction, type inference, error messages, transforms, refinements, async parsing. The plugin pins to the major version the rules were written against; the citation is the link, the pin is the contract. |

The plugin does not draw from blog posts, conference talks, or
third-party tutorials. The schema library's own documentation is the
single source — a rule not stated there is not in the plugin.

## The module's role

The module's business rules are statements about *what this module is and
what it does for the project that adopts it*. They are not a list of good
practices — those live in the plugin's `rules/` directory, one file per
behavioural rule, each citing the source above.

- **BR-1** — The module extends the implementation modules that ship with
  ScrumIA: `scrumia-impl-reactjs` and `scrumia-impl-solidjs`. A project
  running either gains the module's validation directives; a project
  running neither pays no cost.

- **BR-2** — The module can be taken directly as an implementation module
  by a project that does not run React or SolidJS — a Node service, a
  CLI, a server-rendered app. Schema validation is not a UI concern; the
  framework-specific scoping is a default, not a requirement.

- **BR-3** — Every rule the module ships cites the schema library's own
  documentation — never a blog post, never a tutorial, never a community
  pattern. A rule whose citation has drifted from the pinned version is
  rewritten; a rule the documentation no longer states is removed, not
  paraphrased.

- **BR-4** — The module helps web development carry solid notions of
  runtime validation. "Solid" means grounded in the library's documented
  API, applied at the seam between trusted and untrusted code, and
  reasoned about in terms of the type system the schema produces — not
  fashionable, not "defensive", not framework-specific.

- **BR-5** — The module anchors validation in the application's DNA, not
  in an ad-hoc defensive layer. Schemas describe trust boundaries
  (network, file, user input, message queue), not internal function
  arguments; the type the function receives is the type the schema
  produces, derived once, not re-declared.

- **BR-6** — The module provides patterns for the recurring validation
  problems a web app meets: form input, API response shape, query-string
  parsing, environment variables, message-payload contracts. Each
  pattern carries its source citation, its trade-offs (e.g. parsing cost
  vs. trust gain), and the failure mode it prevents.

- **BR-7** — The module teaches how to design and audit validation — not
  only *what* to validate. The audit skill answers "is this boundary
  actually validated?" the way an implementation module answers "is this
  code correct?" — by refusing the shape that would otherwise pass. A
  reader of the module's docs finishes with both the patterns and the
  practice of catching a missing parse.

## What the plugin contributes

The plugin (`scrumia-zod`) carries refusal rules to two registers,
scoped to two implementation modules by default:

| Register | Module that opens it | Default scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | `scrumia-impl-reactjs`, `scrumia-impl-solidjs` |
| `review` | `scrumia-github-project` (via `scrumia-review`) | same |

The plugin does not depend on `scrumia-rhf` to compose. A project that
adopts Zod without forms pays the cost of Zod alone; a project that
adopts both reaches the resolver pattern documented in
`features/business/form-management/`.

## Vocabulary

**"Trust boundary"** names the seam between code that produced a value
and code that consumes it across a boundary the type system cannot reach:
network, file, user input, message queue. **"Inferred type"** names the
TypeScript type a schema produces through the schema library's inference
API — what makes BR-5's "derive, do not re-declare" possible. **"Solid"**
in BR-4 means grounded in the library's documented API, not in a
community convention.
