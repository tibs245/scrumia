# Project Layout

> Where Server Components, Client Components, route segments, primitives and shared state
> sit; what may import what.

## Prerequisites

None — structural, read anytime; not sequenced with the other guides.

## Rules

### Rule 1: Server-first, by feature, App Router as the default

Server Components are the default in React 19, and the App Router is the framework
surface that ships them. The module does **not** dictate a directory layout — every
React app settles its own tree and writes it down. The rules this module stands behind
are the principles, not the names of the folders:

- **Server-first**: route segments are Server Components by default. A `"use client"`
  directive is opted into at the leaf that actually needs interactivity, not propagated
  up from a layout.
- **By feature, not by kind**: the unit of ownership is the feature, not the file
  category. A feature owns its components, its tests, its primitives and its data
  access together, so a change to one is a change to all of one.
- **Data access is named and singular**: each feature has one module the network
  reaches. Other features import its functions and types, not its components' internals
  (see [04-data-boundary](04-data-boundary.md)).
- **Cross-feature UI is dumb**: a component that several features need is Server-first,
  accepts its data through props, and lives somewhere the features all reach.

The Pages Router is supported for legacy projects only. A new project picks the App
Router; a project on the Pages Router records the exception in its project override
without forking the module.

---

### Rule 2: `"use client"` lives at the leaf, not at the shell

Marking a shell or layout as `"use client"` propagates the directive through the module
dependency tree and ships the layout's transitive imports to the browser. The leaf-first
pattern keeps the bundle as small as the interactivity actually requires:

> "Server Components can reduce the amount of code sent and run by the client. Only Client
> modules are bundled and evaluated by the client."
> ([`"use client"` — React](https://react.dev/reference/rsc/use-client))

#### Correct — Server layout, Client child

```tsx
// app/layout.tsx — Server Component
import { CartButton } from '@/features/cart/CartButton'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header>
          <CartButton /> {/* Client Component */}
        </header>
        {children}
      </body>
    </html>
  )
}
```

#### Incorrect — Client layout for the whole shell

```tsx
'use client'
import { CartButton } from '@/features/cart/CartButton'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  // The whole layout, its providers, every imported module — bundled and shipped.
  // …
}
```

---

### Rule 3: Dependencies flow one way — Server may import Client; Client must not import Server-only

A Client Component cannot import a Server Component because the Server Component may use
server-only APIs. The Server Component imports Client Components and passes the rendered
output as `children` or props. React 19's docs state the boundary:

> "When a file marked with `'use client'` is imported from a Server Component, compatible
> bundlers will treat the module import as a boundary between server-run and client-run
> code."
> ([`"use client"` — React](https://react.dev/reference/rsc/use-client))

---

### Rule 4: Cross-feature reach goes through `api.ts` and the contract, not internals

`features/checkout/api.ts` is the only place that knows the transport; other features
import its functions and types, not its components' internals. This is the same
discipline the SolidJS module states for its own data boundary — the difference is which
line marks the boundary (a `"use client"` directive vs a module name).

---

> These rules are structural defaults; `.scrumia/impl/scrumia-impl-reactjs.md`, if
> present, may record a project's exceptions (see the skill's [Project override](../SKILL.md#project-override)
> section).
