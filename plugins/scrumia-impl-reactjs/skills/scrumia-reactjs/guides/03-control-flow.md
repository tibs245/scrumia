# Control Flow: Suspense, `<form action>`, Conditional Rendering

> Branching, list rendering and form submission as React 19 describes them — declarative
> primitives instead of imperative `if`s, `useEffect` chains and `onSubmit` handlers.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)

## Rules

### Rule 1: Suspense is the readiness primitive — `useEffect` is invisible to it

React 19's Suspense reference is explicit:

> "Suspense does not detect when data is fetched inside an Effect or event handler. It only
> activates in the [cases listed below.]"
> ([Suspense — React](https://react.dev/reference/react/Suspense))

What activates Suspense is reading a Promise with `use`, lazy-loading, streaming server
content, or stylesheet/font/image loading — not a `useEffect` `setState` chain. The
Effect-based equivalent is shown in the docs with the comment: *"Suspense can't see this
fetch, so its fallback never shows. The list stays empty until the data arrives."*

Suspense and `useTransition` are designed to compose: a Suspense boundary inside a
Transition keeps the *already revealed* content on screen instead of replacing it with a
fallback. React 19's docs:

> "Replacing visible UI with a fallback creates a jarring user experience. To prevent this
> from happening, mark the update as non-urgent using `startTransition`."
> ([Suspense — Preventing already-revealed content from hiding](https://react.dev/reference/react/Suspense#preventing-already-revealed-content-from-hiding))

#### Correct — `use(promise)` with Suspense

```tsx
import { use, Suspense } from 'react'

function Albums({ albumsPromise }: { albumsPromise: Promise<Album[]> }) {
  const albums = use(albumsPromise)
  return (
    <ul>{albums.map(a => <li key={a.id}>{a.title}</li>)}</ul>
  )
}

export default function Page() {
  const albumsPromise = fetchAlbums() // cached at module scope
  return (
    <Suspense fallback={<AlbumsGlimmer />}>
      <Albums albumsPromise={albumsPromise} />
    </Suspense>
  )
}
```

#### Incorrect — `useEffect` setState

```tsx
function EffectAlbums({ artistId }: { artistId: string }) {
  const [albums, setAlbums] = useState<Album[]>([])
  useEffect(() => {
    let active = true
    fetchData(`/${artistId}/albums`).then(result => {
      if (active) setAlbums(result)
    })
    return () => { active = false }
  }, [artistId])
  // Suspense can't see this fetch — its fallback never shows.
  return <ul>{albums.map(a => <li key={a.id}>{a.title}</li>)}</ul>
}
```

---

### Rule 2: `<form action>` replaces `onSubmit` for the submission itself

React 19's `<form>` docs state the case for `action` directly:

> "Reading form data with `onSubmit` works in every version of React and gives you direct
> access to the submit event, so you can call `e.preventDefault()` and read the data
> yourself. Passing the function to the `action` prop instead runs the submission in a
> Transition. React then tracks the pending state, sends thrown errors to the nearest error
> boundary, and lets the form work with `useActionState` and `useOptimistic`. An `action`
> can also be a Server Function, which `onSubmit` does not support."
> ([`<form>` — React](https://react.dev/reference/react-dom/components/form))

A Server Function in `action` also gives progressive enhancement — the form submits
without JavaScript:

> "When `<form>` is rendered by a Server Component, and a Server Function is passed to
> the `<form>`'s `action` prop, the form is progressively enhanced."
> ([`<form>` — React](https://react.dev/reference/react-dom/components/form))

#### Correct

```tsx
async function search(formData: FormData) {
  'use server'
  const query = formData.get('query')
  await db.search.run(query)
  redirect(`/results?q=${encodeURIComponent(query)}`)
}

export default function SearchForm() {
  return (
    <form action={search}>
      <input name="query" />
      <button>Search</button>
    </form>
  )
}
```

#### Incorrect — `onSubmit` for what `action` already does

```tsx
function SearchForm() {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = e.currentTarget
    const formData = new FormData(form)
    const query = formData.get('query')
    await db.search.run(query)
    redirect(`/results?q=${encodeURIComponent(query as string)}`)
  }
  return (
    <form onSubmit={handleSubmit}>
      <input name="query" />
      <button>Search</button>
    </form>
  )
}
```

---

### Rule 3: Conditional rendering during render — not in a `useEffect` `setState`

Branching on a flag inside JSX is a tracked expression evaluated during render; setting
state from an `useEffect` to "derive" the same condition is the same defect React 19's
"You Might Not Need an Effect" page is written to prevent. React's docs frame the
principle as:

> "If you can calculate something during render, you don't need an Effect."
> ([You Might Not Need an Effect — React](https://react.dev/learn/you-might-not-need-an-effect))

`if (loading) return <Spinner />` is a related pattern that is acceptable in React 19
because the function body re-runs on every render — unlike SolidJS where this rule's
defect is silent. The SolidJS module states the refusal against its own model; React 19
states no equivalent rule. What remains is the broader principle: do not push the
branching into an `useEffect`.

#### Correct

```tsx
function Albums({ albumsPromise }: { albumsPromise: Promise<Album[]> }) {
  const albums = use(albumsPromise)
  return (
    <ul>{albums.map(a => <li key={a.id}>{a.title}</li>)}</ul>
  )
}

export default function Page() {
  return (
    <Suspense fallback={<AlbumsGlimmer />}>
      <Albums albumsPromise={fetchAlbums()} />
    </Suspense>
  )
}
```

#### Incorrect

```tsx
function Albums({ artistId }: { artistId: string }) {
  const [albums, setAlbums] = useState<Album[] | null>(null)
  if (albums === null) return <Spinner />
  useEffect(() => {
    fetchData(`/${artistId}/albums`).then(setAlbums)
  }, [artistId])
  return <ul>{albums.map(a => <li key={a.id}>{a.title}</li>)}</ul>
}
```

---

> Decision rationale: [D-01 — Refuse `useEffect` for derived state](../decisions/D-01-no-useeffect-for-derived-state.md), [D-02 — Refuse imperative DOM](../decisions/D-02-no-imperative-dom.md).
