# Compound components in Vue

The principle, in Vue's idiom. The mechanism is `provide` / `inject`; the rule is unchanged.

## The shape

```vue
<script setup lang="ts">
import { provide, inject, ref, Ref } from 'vue';

interface TabsContext {
  value: Ref<string>;
  onChange: (next: string) => void;
}

const TabsSymbol = Symbol('TabsContext');

export function useTabsContext(): TabsContext {
  const ctx = inject<TabsContext>(TabsSymbol);
  if (!ctx) {
    throw new Error('Tabs.* must be rendered inside <Tabs>');
  }
  return ctx;
}
</script>

<script setup lang="ts">
const props = defineProps<{ value: string }>();
const emit = defineEmits<{ (e: 'change', next: string): void }>();

provide(TabsSymbol, { value: toRef(props, 'value'), onChange: emit });
</script>

<template>
  <div class="tabs">
    <slot />
  </div>
</template>

<!-- Tab.vue -->
<script setup lang="ts">
const props = defineProps<{ value: string }>();
const ctx = useTabsContext();
const active = computed(() => ctx.value.value === props.value);
</script>

<template>
  <button
    role="tab"
    :aria-selected="active"
    @click="ctx.onChange(props.value)"
  >
    <slot />
  </button>
</template>
```

```ts
// parts travel with the parent
Tabs.Tab = Tab;
```

The consumer reads `<Tabs>`. The state lives in `Tabs`, reaches `Tab` through `inject(TabsSymbol)`, and the public API is one symbol with parts attached.

## What the rules catch, in Vue

A prop chain of three or more — `<Tabs>` → `<TabsList>` → `<Tab>` — is a finding. The threshold is the third prop level. Move `value` into the provided context; drop it from `<TabsList>`.

`<Tab>` imported from a separate module path — `import Tab from './Tab.vue'` rather than through `Tabs.Tab` — is a finding. The parts travel with the parent.

`<Tab :items="…" :value="…" @select="…" />` consumed without `<Tabs>` is a finding. The state the parent used to hide has leaked through the part's props.

## Source

The single authority for this pattern is [patterns.dev — Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The Vue example above translates the principle into `provide` / `inject`; the principle itself is the same.