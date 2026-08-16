# A compound is consumed as one symbol

*Refusal.* A consumer who reaches for a part by name instead of through the parent — the part read as a standalone, with the parent's state passed in as a prop, or rendered without the parent at all.

## What is refused

A part rendered outside the parent, with state and callbacks threaded through props as if it were a leaf. Transcribed verbatim from patterns.dev's "Cons" section — the case the pattern explicitly breaks:

```jsx
// ❌ Wrapping the parts outside the parent breaks the pattern:
// "Only direct children of the parent will have access
// to open and toggle, so wrapping components in another
// component breaks the pattern."
export default function FlyoutMenu() {
  return (
    <FlyOut>
      {/* This breaks */}
      <div>
        <FlyOut.Toggle />
        <FlyOut.List>
          <FlyOut.Item>Edit</FlyOut.Item>
          <FlyOut.Item>Delete</FlyOut.Item>
        </FlyOut.List>
      </div>
    </FlyOut>
  );
}
```

The same shape, in another form, is the part-as-standalone: a `<FlyOut.Toggle>` rendered without `<FlyOut>` above it, or with `open` and `toggle` passed in as props. In both, the parent is no longer the unit. The library now exposes the parts as knobs the consumer turns, instead of as declarations under the parent.

## What is written instead

The parent is the unit. The consumer reads one symbol; the parts are its children. Transcribed verbatim from patterns.dev:

```jsx
import React from "react";
import { FlyOut } from "./FlyOut";

export default function FlyoutMenu() {
  return (
    <FlyOut>
      <FlyOut.Toggle />
      <FlyOut.List>
        <FlyOut.Item>Edit</FlyOut.Item>
        <FlyOut.Item>Delete</FlyOut.Item>
      </FlyOut.List>
    </FlyOut>
  );
}
```

One symbol on the import line. One root element in the JSX (`<FlyOut>`). The parts are declarative children — `<FlyOut.Toggle />`, `<FlyOut.List>`, `<FlyOut.Item>` — and the parent's state (`open`, `toggle`) is hidden behind the parent's signature. The consumer names one component, not three.

## Why

Upstream documents the rule twice. The Pros section: "When importing a compound component, child components don't need to be explicitly imported." The Cons section, naming the failure mode: a part the consumer renders without the parent (or in a position the parent does not reach) silently loses its access to `open` and `toggle`. No warning, no exception, just state that no longer crosses the boundary.

The single-symbol shape is the consumer's contract. A consumer who reaches for `<FlyOut.Toggle />` standalone, or who passes `open` and `toggle` as props to a part, has stepped out of the contract and into the leaf-component shape — six props and one element, where the compound's whole point was to hide those props behind the parent.

## Sources complémentaires

- patterns.dev — [Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The single authority for this rule; no version pin.
