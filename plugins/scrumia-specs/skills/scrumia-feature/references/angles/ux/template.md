# UX — <feature>

<The interface half of the journey: what the user sees, in what order, and
what the screen refuses to do. Omit any section with nothing to say.>

## Screen / flow

<Entry point, exit point.>

## Composition

<The components this screen uses, each a pointer to its
`design/components/<name>/spec.md`, with its role on this screen — never a
copy, no literal colour, spacing or duration (those live in
`design/tokens.css`). A value this screen needs that no token or component
supplies is a finding for `design/`, not a number written here.>

## States

<Empty, loading, error, success — with the exact copy per state.>

## Navigation

<Reading order, focus flow, what changes announce themselves.>

## Interface constraints

<What this screen must never do, when it is not already a component-level
refusal.>

<A markdown or ASCII mockup, if present, is only a seed for a layout that has
no `design/` counterpart yet — it converts into an exploration or a
component spec, it does not stay a permanent second drawing. A WCAG target
that can pass or fail is a tagged `qa.md` criterion, not written here.>
