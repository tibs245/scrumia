# Compound components in Angular

The principle, in Angular's idiom. The mechanism is a service or an injection token; the rule is unchanged.

## The shape

```ts
// tabs-context.ts
import { Injectable, signal, Signal, InjectionToken, inject } from '@angular/core';

export interface TabsContext {
  value: Signal<string>;
  setValue: (next: string) => void;
}

export const TABS_CONTEXT = new InjectionToken<TabsContext>('TabsContext');

export function injectTabsContext(): TabsContext {
  const ctx = inject(TABS_CONTEXT, { optional: true });
  if (!ctx) {
    throw new Error('Tabs.* must be rendered inside <Tabs>');
  }
  return ctx;
}
```

```ts
// tabs.component.ts
import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { TABS_CONTEXT } from './tabs-context';

@Component({
  selector: 'Tabs',
  template: <ng-content></ng-content>,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TabsComponent {
  @Input() value = '';
  @Output() valueChange = new EventEmitter<string>();

  private ctx: TabsContext = {
    value: () => this.value,
    setValue: (next) => this.valueChange.emit(next),
  };
  // The provider makes the context available to descendants.
  readonly contextProvider = { provide: TABS_CONTEXT, useValue: this.ctx };
}
```

```ts
// tab.component.ts
import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { injectTabsContext } from './tabs-context';

@Component({
  selector: 'Tab',
  template: <button role="tab" [attr.aria-selected]="active" (click)="select()"><ng-content></ng-content></button>,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TabComponent {
  @Input() value = '';
  private ctx = injectTabsContext();

  get active(): boolean {
    return this.ctx.value() === this.value;
  }

  select(): void {
    this.ctx.setValue(this.value);
  }
}
```

```ts
// parts travel with the parent
TabsComponent.Tab = TabComponent;
```

The consumer reads `<Tabs>`. The state lives in `TabsComponent`, reaches `TabComponent` through the injection token, and the public API is one symbol with parts attached.

## What the rules catch, in Angular

A prop chain of three or more — `<Tabs>` → `<TabsList>` → `<Tab>` — is a finding. The threshold is the third prop level. Move `value` into the context; drop it from `<TabsList>`.

`<Tab>` imported from a separate module — `import { TabComponent } from './tab'` rather than through `TabsComponent.Tab` — is a finding. The parts travel with the parent.

`<Tab [items]="…" [value]="…" (select)="…" />` consumed without `<Tabs>` is a finding. The state the parent used to hide has leaked through the part's inputs and outputs.

## Source

The single authority for this pattern is [patterns.dev — Compound Pattern](https://www.patterns.dev/react/compound-pattern/). The Angular example above translates the principle into a service or `inject()`; the principle itself is the same.