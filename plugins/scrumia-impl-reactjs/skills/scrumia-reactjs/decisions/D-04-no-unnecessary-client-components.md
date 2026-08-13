# D-04: Refuse unnecessary `"use client"`

**Status**: Adopted
**Date**: 2026-08-13
**Impacts**: [guides/01-components-and-props.md](../guides/01-components-and-props.md), [guides/05-project-layout.md](../guides/05-project-layout.md)

## Context

React 19's docs list the two advantages of keeping a component a Server Component, and
both are about what does *not* ship:

> "Server Components can reduce the amount of code sent and run by the client. Only
> Client modules are bundled and evaluated by the client."
> — [`"use client"` — React](https://react.dev/reference/rsc/use-client)

> "Server Components benefit from running on the server. They can access the local
> filesystem and may experience low latency for data fetches and network requests."
> — [`"use client"` — React](https://react.dev/reference/rsc/use-client)

The same page gives the test for when a component may stay render-agnostic:

> "we don't add the `'use client'` directive, resulting in `FancyText`'s *output* (rather
> than its source code) to be sent to the browser when referenced from a Server
> Component."
> — [`"use client"` — React](https://react.dev/reference/rsc/use-client)

The directive propagates through the **module dependency tree**, not the render tree:

> "When a file marked with `'use client'` is imported from a Server Component, compatible
> bundlers will treat the module import as a boundary between server-run and client-run
> code."
> — [`"use client"` — React](https://react.dev/reference/rsc/use-client)

A component added to the tree at the top carries its whole transitive dependency graph
to the browser. That is the cost being refused.

## Arguments For

- **The directive is paid in full, every request.** A `"use client"` at the layout
  ships the layout, its providers, every imported module, and every transitive
  dependency the bundler can reach, on every page that uses it.
- **It is unnecessary for most components.** A render-agnostic component stays a
  Server Component by default. The Server Component's *output* is what the browser
  receives; the source code does not.
- **It is what blocks Server-side fetching.** A Client Component cannot `await db.get()`
  during render. Marking a component a Client when it could have been a Server moves the
  fetch into a `useEffect` on the client, which is the data boundary violation
  [04-data-boundary](../guides/04-data-boundary.md) is written to prevent.
- **It is decided at the leaf, not at the root.** Marking the shell `"use client"` is
  the worst case; a single interactive button at the leaf is enough. The project layout
  states this and the rule depends on it.

## Arguments Against (trade-offs accepted)

- For a component whose HTML output is much larger than its source, the React 19 docs
  note that forcing it Client-side may be cheaper:

  > "But if `FancyText`'s HTML output was large relative to its source code (including
  > dependencies), it might be more efficient to force it to always be a Client
  > Component. Components that return a long SVG path string are one case where it may
  > be more efficient to force a component to be a Client Component."
  > — [`"use client"` — React](https://react.dev/reference/rsc/use-client)

  The exception is named, not silently granted; record it in the project override.
- A third-party client library that uses `useState` or `useEffect` forces a `"use
  client"` at the boundary that imports it. The rule does not refuse this — the
  boundary is named in a comment.

## Verdict

Refuse unnecessary `"use client"`. Add the directive only when the component or one of
its imports needs state, an event handler, a client API or a Hook the server cannot run.
Place it at the leaf, name the exception in a comment when a third-party library forces
the boundary, and keep the rest Server-first.
