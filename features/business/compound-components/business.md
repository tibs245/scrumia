# Compound components — business rules

## Value

For whoever ships a component library — reusable parts that compose at the
call site without leaking their internal state. It matters because a
component that takes six props and returns one element is a leaky
abstraction: the consumer names every internal the parent could have
hidden. The compound pattern hides the parts and exposes the parent. Not
instrumented today: nothing counts how many components a library exposes as
a unit versus as scattered imports.

## Children reach the parent through context

A compound component's children communicate with the parent through context
(React, Solid), provide/inject (Vue), or the framework's equivalent. Props
drilling through three levels is the smell: the parent is a compound, the
implementation is not. The plugin refuses a compound whose children receive
parent state through prop chains of three or more.

## Sub-components are co-located

A compound's parts live with the parent — same file, or a directory the
parent exports from. A consumer of `<Tabs>` does not import `<Tab>` from
`@acme/ui/tab`; they import it from `<Tabs.Tab>`. The plugin refuses an
export that exposes a compound's children separately, because the public
API is the parent.

## Documentation is framework-agnostic

The pattern is the same across React, Vue, Solid and Angular — the
mechanism differs. The plugin's documentation covers at least three of
those four side by side, with the same principle stated in each framework's
idiom. A doc that translates a React example alone is a doc for one
framework, not a doc for the pattern.

## What the plugin contributes

| Register | Module that opens it | Scope |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | any implementation module |

The plugin does not contribute to `review`: the pattern's review is the
same review any component passes — props shape, accessibility, performance
— and adding it to `review` would duplicate what an implementation module's
own rules already cover.

## Business rules

- **BR-1** — A compound component's children reach the parent through
  context or its framework equivalent; a prop chain of three or more
  levels is refused.
- **BR-2** — Sub-components are co-located with the parent; exporting
  them separately from the parent's module is refused.
- **BR-3** — The compound is consumed as a unit (`Parent.Child` syntax or
  its framework equivalent); the public API is the parent.
- **BR-4** — The plugin's documentation covers React, Vue, Solid and
  Angular side by side, with examples in each framework's idiom; a doc
  covering fewer than three is refused.
- **BR-5** — The plugin contributes to the `implement` register only;
  `review` is the implementation module's own concern.

## Vocabulary

**"Compound component"** names a parent that exposes its parts through a
single API: `<Tabs>` with `<Tabs.Tab>` rather than `<Tabs>` with
`<Tab items={...}>`. **"Context equivalent"** names whatever mechanism a
framework offers to make a value available to descendants without props —
`provide`/`inject` in Vue, signals in Solid, services in Angular.
