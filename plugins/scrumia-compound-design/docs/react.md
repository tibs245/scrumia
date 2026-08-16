# Compound components in React

The principle, in React's idiom. The mechanism is `createContext` plus `useContext`; the rule is unchanged.

## The shape

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface TabsContextValue {
  value: string;
  onChange: (next: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext(): TabsContextValue {
  const ctx = useContext(TabsContext);
  if (ctx === null) {
    throw new Error('Tabs.* must be rendered inside <Tabs>');
  }
  return ctx;
}

export function Tabs({ value, onChange, children }: {
  value: string;
  onChange: (next: string) => void;
  children: ReactNode;
}) {
  return (
    <TabsContext.Provider value={{ value, onChange }}>
      {children}
    </TabsContext.Provider>
  );
}

function Tab({ value, children }: { value: string; children: ReactNode }) {
  const ctx = useTabsContext();
  const active = ctx.value === value;
  return (
    <button
      role="tab"
      aria-selected={active}
      onClick={() => ctx.onChange(value)}
    >
      {children}
    </button>
  );
}

// The parts travel with the parent.
Tabs.Tab = Tab;
```

The consumer reads the parent. The state lives in `Tabs`, reaches `Tab` through `useContext`, and the public API is one symbol with parts attached.

## What the rules catch, in React

A prop chain of three or more — `<Tabs>` → `<Tabs.List>` → `<Tabs.Trigger>` — is a finding. Two levels is fine: `Tabs` to `Tabs.List` is internal composition. The third is the consumer-implied shape: `Tabs.List` passing `value` through to `Tabs.Trigger`. Move `value` into the context, drop the prop from `Tabs.List`.

`<Tab>` imported from a separate module path — `import { Tab } from './components/Tab'` rather than through `Tabs.Tab` — is a finding. The parts travel with the parent; a separate path breaks the public API.

`<Tab items={…} value={…} onSelect={…} />` consumed without `<Tabs>` is a finding. The state the parent used to hide — value, onSelect — has leaked through the part's signature. The audit names the part, the leak, and the fix.

## Source

The single authority for this pattern is [patterns.dev — Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The React example above is the same example, in the same idiom.