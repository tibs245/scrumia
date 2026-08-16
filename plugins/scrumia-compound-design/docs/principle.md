# The compound component pattern

The principle, framework-agnostic. The mechanism — the provider, the consumer — is what changes between React, Vue, Solid and Angular; the rule does not.

## What a compound is

A parent that exposes its parts through a single API. `<Tabs>` with `<Tabs.Tab>`. `<Select>` with `<Select.Option>`. `<Accordion>` with `<Accordion.Item>`. The parent is the library's public surface; the parts travel with it.

Three things follow:

1. **The parts reach the parent through context** (or `provide`/`inject`, or signals, or a service — whatever the framework offers to make a value available to descendants without prop-drilling). A consumer never has to thread the parent's state through three levels of props.
2. **The parts travel with the parent.** `<Tabs.Tab>` is reachable through `<Tabs>`. A consumer who imports `<Tab>` separately has skipped the public API.
3. **The compound is consumed as one symbol.** `<Tabs value=… onChange=…><Tabs.Tab value="a"/></Tabs>` reads as a unit. The internal state — value, onChange, the active id — is hidden behind the parent's signature.

## Why it matters

A component that takes six props and returns one element is a leaky abstraction. The consumer names every internal the parent could have hidden. The compound pattern hides the parts and exposes the parent. The consumer reads the parent, and the parent owns its internals.

The cost is one concept the consumer has to learn — the parent owns its state, not the call site. The benefit is every prop the consumer doesn't write.

## What it does not

- It is not a state management pattern. The parent owns its state because the parent owns its parts — not because the parent's state is special.
- It is not a layout pattern. A compound is free to lay its parts out however it wants; what the pattern constrains is the public surface, not the rendering.
- It is not a composition pattern. Compound is one of several ways a parent can compose with its parts; what makes it compound is the public API, not the implementation.

## Source

The single authority for this pattern is [patterns.dev — Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The principle has been stable since the pattern was first documented; a 404 on this URL is a finding, and a reworded principle is the fix.