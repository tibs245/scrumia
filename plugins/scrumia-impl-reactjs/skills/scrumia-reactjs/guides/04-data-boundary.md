# Data Boundary: where the fetch lives

> The Server Component / Client Component split is also where data fetching sits.
> React 19's data boundary is not the api/ folder — it is the `"use client"` line in the
> module graph.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)
- [03-control-flow.md](03-control-flow.md) (Suspense + `use`)

## Rules

### Rule 1: Data fetching lives in Server Components — `await` runs during render

React 19's Server Components reference is the source:

> "Server Components are not sent to the browser, so they cannot use interactive APIs like
> `useState`. To add interactivity to Server Components, you can compose them with Client
> Component using the `'use client'` directive."
> ([Server Components — React](https://react.dev/reference/rsc/server-components))

The same page makes the fetch case explicit — `await` runs *during render* and
contributes to streaming:

> "When you `await` in an async component, React will suspend and wait for the promise to
> resolve before resuming rendering. This works across server/client boundaries with
> streaming support for Suspense."
> ([Server Components — React](https://react.dev/reference/rsc/server-components))

The Client-side equivalent is what React 19 docs explicitly warn against: an `useEffect`
fetch produces a waterfall and is invisible to Suspense.

#### Correct — fetch in a Server Component

```tsx
// app/dashboard/page.tsx — a Server Component by default (no 'use client')
import db from './database'

export default async function Page() {
  const note = await db.notes.get('welcome')
  return (
    <div>
      <p>{note}</p>
    </div>
  )
}
```

#### Incorrect — fetch in a Client Component via `useEffect`

```tsx
'use client'
import { useState, useEffect } from 'react'

export default function Page() {
  const [note, setNote] = useState<string | null>(null)
  useEffect(() => {
    fetch('/api/notes/welcome').then(r => r.json()).then(setNote)
  }, [])
  return <div>{note ?? 'Loading…'}</div>
}
```

---

### Rule 2: Client Components do not fetch directly — they read a Promise with `use`

When the data must arrive in a Client Component (because an interactive child renders it),
React 19's answer is to start the fetch on the server and read the Promise in the
client:

> "Under the hood, a Suspense-enabled framework maintains a cache of Promises and calls
> [`use`](https://react.dev/reference/react/use) to suspend on a Promise."
> ([Suspense — React](https://react.dev/reference/react/Suspense))

```tsx
// Server Component — kicks off the fetch, passes the Promise as a prop
import { Suspense } from 'react'
import { Comments } from './Comments'

async function Page({ id }: { id: string }) {
  const commentsPromise = db.comments.get(id)
  return (
    <Suspense fallback={<p>Loading Comments…</p>}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  )
}

// Client Component — reads the Promise
'use client'
import { use } from 'react'

export function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  const comments = use(commentsPromise)
  return comments.map(c => <p key={c.id}>{c.body}</p>)
}
```

The promise has to be cached so the same instance is reused across renders; without a
framework's cache, a module-level `Map` is the documented workaround.

---

### Rule 3: A Client Component that fetches `fetch()` on its own is the pattern to avoid

The boundary `useEffect` + `setState` reaches for in a Client Component is invisible to
Suspense, produces a waterfall, and forces the client to ship whatever transport the
component imports. Reach for a Server Component, or for `use(promise)` against a Promise
created at the boundary, instead. (See Rule 2 above.)

Mocking this boundary — mocking `fetch` directly rather than the data layer — is covered
in [06-testing.md](06-testing.md), Rule 4.

---

> Decision rationale: [D-01 — Refuse `useEffect` for derived state](../decisions/D-01-no-useeffect-for-derived-state.md), [D-04 — Refuse unnecessary `"use client"`](../decisions/D-04-no-unnecessary-client-components.md).
