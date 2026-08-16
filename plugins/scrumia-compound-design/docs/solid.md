# Compound components in Solid

The principle, in Solid's idiom. The mechanism is `createContext` plus `useContext`; the rule is unchanged.

## The shape

```tsx
import { createContext, useContext, JSX as SolidJSX, ParentComponent } from 'solid-js';
import { createSignal, Accessor } from 'solid-js';

interface TabsContextValue {
  value: Accessor<string>;
  setValue: (next: string) => void;
}

const TabsContext = createContext<TabsContextValue>();

function useTabsContext(): TabsContextValue {
  const ctx = useContext(TabsContext);
  if (!ctx) {
    throw new Error('Tabs.* must be rendered inside <Tabs>');
  }
  return ctx;
}

export const Tabs: ParentComponent<{ initialValue?: string }> = (props) => {
  const [value, setValue] = createSignal(props.initialValue ?? '');
  return (
    <TabsContext.Provider value={{ value, setValue }}>
      {props.children}
    </TabsContext.Provider>
  );
};

export const Tab: ParentComponent<{ value: string }> = (props) => {
  const ctx = useTabsContext();
  const active = () => ctx.value() === props.value;
  return (
    <button
      role="tab"
      aria-selected={active()}
      onClick={() => ctx.setValue(props.value)}
    >
      {props.children}
    </button>
  );
};

// The parts travel with the parent.
Object.assign(Tabs, { Tab });
```

The consumer reads `<Tabs>`. The state lives in `Tabs`, reaches `Tab` through `useContext`, and the public API is one symbol with parts attached.

## What the rules catch, in Solid

A prop chain of three or more — `<Tabs>` → `<TabsList>` → `<Tab>` — is a finding. The threshold is the third prop level. Move `value` into the context; drop it from `<TabsList>`.

`<Tab>` imported from a separate module path — `import { Tab } from './Tab'` rather than through `Tabs.Tab` — is a finding. The parts travel with the parent.

`<Tab items={…} value={…} onSelect={…} />` consumed without `<Tabs>` is a finding. The state the parent used to hide has leaked through the part's props.

## Source

The single authority for this pattern is [patterns.dev — Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The Solid example above translates the principle into `createContext`; the principle itself is the same.