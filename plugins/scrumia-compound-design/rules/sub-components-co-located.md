# Sub-components are co-located with the parent

*Refusal.* A part exported from a separate file, a separate directory, or a separate top-level symbol of the package — the consumer reaching the part without going through the parent.

## What is refused

A library whose parts are importable on their own. patterns.dev names the cure for this — "only `FlyOut` needs to be imported in any file" — which is only meaningful if a part imported on its own is the violation. The bad shape, in upstream's idiom:

```jsx
// ❌ The parts reached through a path the parent does not own.
// This is what patterns.dev warns against by saying
// "only FlyOut needs to be imported in any file":
import { Toggle } from "./FlyOut/Toggle";
import { List } from "./FlyOut/List";
import { Item } from "./FlyOut/Item";

export default function FlyoutMenu() {
  return <Toggle />;
}
```

The consumer reads three symbols where it should read one. The library now exposes `<Toggle>`, `<List>`, and `<Item>` as top-level paths alongside `<FlyOut>`; the public surface is four names where it should be one. A consumer who imports `<Toggle>` directly has skipped the parent, and the audit names the skipped symbol.

## What is written instead

The parts travel with the parent. Transcribed verbatim from patterns.dev:

```jsx
const FlyOutContext = createContext();

function FlyOut(props) {
  const [open, toggle] = useState(false);

  return (
    <FlyOutContext.Provider value={{ open, toggle }}>
      {props.children}
    </FlyOutContext.Provider>
  );
}

function Toggle() {
  const { open, toggle } = useContext(FlyOutContext);

  return (
    <div onClick={() => toggle(!open)}>
      <Icon />
    </div>
  );
}

function List({ children }) {
  const { open } = React.useContext(FlyOutContext);
  return open && <ul>{children}</ul>;
}

function Item({ children }) {
  return <li>{children}</li>;
}

// The parts travel with the parent.
FlyOut.Toggle = Toggle;
FlyOut.List = List;
FlyOut.Item = Item;
```

The export reads `<FlyOut>`, and `<FlyOut.Toggle>`, `<FlyOut.List>`, `<FlyOut.Item>` travel with it. Upstream's consumer code — also transcribed verbatim — proves the shape: only the parent is imported, and every part is read through it.

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

One import, one symbol on the public surface, four parts attached to it. The library's contract is `FlyOut`, not `FlyOut` plus its parts as siblings.

## Why

A library with two public names where one would do has two contracts to maintain. A change to `Toggle` ripples to every consumer who imported it directly, but the change is invisible to consumers who use `<FlyOut.Toggle />` — they saw the same symbol, but reached it through the parent. The audit catches the divergence at the import line: a `<Toggle>` import is a finding because the library never named it. Co-location makes the divergence impossible: there is no separate path, because the only path goes through the parent.

## Sources complémentaires

- patterns.dev — [Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The single authority for this rule; no version pin.
