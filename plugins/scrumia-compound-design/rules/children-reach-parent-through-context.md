# Children reach the parent through context

*Refusal.* A compound's parts reading parent state through three or more prop levels instead of through context (or its framework equivalent — `provide`/`inject` in Vue, signals in Solid, a service or `inject()` in Angular).

## What is refused

A consumer who reaches the parent through anything other than a provider boundary. patterns.dev documents the failure mode on the `React.Children.map` alternative: component nesting is limited, and wrapping the parts in another component breaks the pattern.

```jsx
// ❌ Wrapping breaks the React.Children.map alternative:
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

The chain has crossed a provider boundary without a provider — the parts reach the parent only as deep as the cloneElement recursion walks. One extra `<div>`, and the rule's signature appears.

## What is written instead

The provider is the parent; the parts reach it through `useContext`. Transcribed verbatim from patterns.dev:

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
```

The reach is one level: provider to consumer. The `<div>` wrapper above no longer breaks anything, because the lookup is by context, not by recursion depth. Every part reads the parent's state through `useContext(FlyOutContext)` regardless of where in the tree it sits.

## Why

The `React.Children.map` alternative fails silently: `React.cloneElement` walks `props.children` once and clones each one with the new props. A wrapper component is not in `props.children`; the parts inside it get nothing. The bug presents as "the parts don't update" — no warning, no exception, just state that never reaches the consumer. Context solves it by separating the reach from the position: the provider is the root, the consumer is whoever calls `useContext`, and the tree between them is irrelevant.

The same principle is what `provide`/`inject` (Vue), signals (Solid), and `inject()` (Angular) all implement. The medium changes; the rule — that the parts reach the parent through the framework's provider, not through prop drilling — does not.

## Sources complémentaires

- patterns.dev — [Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The single authority for this rule; no version pin.
