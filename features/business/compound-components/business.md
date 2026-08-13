# Compound components — business rules

## Value

For whoever ships a component library — reusable parts that compose at
the call site without leaking their internal state. It matters because
a component that takes six props and returns one element is a leaky
abstraction: the consumer names every internal the parent could have
hidden. The compound pattern hides the parts and exposes the parent.
Not instrumented today: nothing counts how many components a library
exposes as a unit versus as scattered imports.

## Sources

This module's authority is a single pattern reference, not a list of
opinion pieces. The principle has been stable since the pattern was
first documented; the URL is the citation, and a 404 is the failure
mode the audit catches.

| Source | URL | What it provides |
|---|---|---|
| patterns.dev — Compound Pattern | `https://www.patterns.dev/react/compound-pattern/` | The canonical write-up of the compound component pattern: parent exposes its parts through a single API, children reach the parent through context (or framework equivalent), parts are co-located. The reference uses React; the plugin's documentation translates the principle into Vue, Solid, and Angular idioms side by side. |

The plugin does not draw from blog posts, conference talks, or
ad-hoc community conventions. The pattern reference is the single
source — a principle not stated there is not in the plugin.

## The module's role

The module's business rules are statements about *what this module is
and what it does for the project that adopts it*. They are not a list
of good practices — those live in the plugin's `rules/` directory,
one file per behavioural rule, each citing the source above.

- **BR-1** — The module extends the implementation modules that ship
  with ScrumIA whose framework supports context or its equivalent:
  `scrumia-impl-reactjs`, `scrumia-impl-vue`, `scrumia-impl-solidjs`,
  `scrumia-impl-angular`. The pattern transfers across frameworks; the
  mechanism differs. A project running any of them gains the module's
  composition directives; a project running none pays no cost.

- **BR-2** — The module can be taken directly as an implementation module
  by a project that does not run any framework covered above — a
  static site, a documentation tool, an HTML-only prototype. The pattern
  is the deliverable; the framework-specific scoping is a convenience.

- **BR-3** — Every rule the module ships cites the pattern reference —
  never a blog post, never a tutorial, never a community convention. A
  rule whose citation has rotted is rewritten against the patterns.dev
  page that still resolves; a rule the reference no longer states is
  removed, not paraphrased.

- **BR-4** — The module helps component-library authors carry solid
  notions of composition. "Solid" means the parent owns the parts (not
  the consumer), the communication goes through context or its framework
  equivalent (not props drilling), and the public API is one symbol
  (not a constellation of imports). Not fashionable, not minimal,
  framework-agnostic in principle, framework-specific in mechanism.

- **BR-5** — The module anchors compound composition in the library's
  DNA, not in a separate audit pass. Sub-components travel with the
  parent (`Tabs.Tab`, not `Tab` imported separately); exports expose
  the parent as the unit; a consumer who reaches for `<Tab items={…}>`
  is reading the wrong shape, and the audit skill catches it.

- **BR-6** — The module provides patterns for the recurring compound
  problems a component library meets: tabs with controlled state,
  accordions with exclusive open sections, menus with keyboard
  navigation, listboxes with selection state, comboboxes with async
  data. Each pattern carries its source citation, its trade-offs
  (e.g. flexibility vs. surface area), and the failure mode it prevents.

- **BR-7** — The module teaches how to design and audit component
  composition — not only *what* a compound should expose. The audit
  skill answers "is this compound composed correctly?" the way an
  implementation module answers "is this code correct?" — by refusing
  the shape that would otherwise pass. A reader of the module's docs
  finishes with both the principle and the practice of catching a
  leaked internal.

## What the plugin contributes

The plugin (`scrumia-compound-design`) carries refusal rules to one
register only:

| Register | Module that opens it | Scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | any implementation module whose framework supports context or its equivalent |

The plugin does **not** contribute to `review`. A compound component's
review is the same review any component passes — props shape,
accessibility, performance — and adding it to `review` would duplicate
what an implementation module's own rules already cover.

## Vocabulary

**"Compound component"** names a parent that exposes its parts through
a single API — `<Tabs>` with `<Tabs.Tab>`, not `<Tabs>` with `<Tab
items={…}>`. **"Context equivalent"** names whatever mechanism a
framework offers to make a value available to descendants without
props — `provide`/`inject` in Vue, signals in Solid, services or
`inject()` in Angular. **"Solid"** in BR-4 means grounded in the
pattern's documented principle, not in a community convention.
**"DNA"** in BR-5 names the library's public surface: what the
library exposes as a unit is what its consumers import.
