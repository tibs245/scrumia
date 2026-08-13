# State and Derivations

> When to derive a value during render, when to reach for a Hook, and when a mutation
> is an Action — the new shape React 19 gives to user-initiated state changes.

## Prerequisites

- [01-components-and-props.md](01-components-and-props.md)

## Rules

### Rule 1: Derive during render — `useEffect` is not for state that can be calculated

React 19's docs state the principle twice, and the second statement is the one to keep:

> "**If you can calculate something during render, you don't need an Effect.**"
> ([You Might Not Need an Effect — React](https://react.dev/learn/you-might-not-need-an-effect))

> "**When something can be calculated from the existing props or state, [don't put it in
> state.] Instead, calculate it during rendering.** This makes your code faster (you avoid
> the extra 'cascading' updates), simpler (you remove some code), and less error-prone (you
> avoid bugs caused by different state variables getting out of sync with each other)."
> ([You Might Not Need an Effect — Updating state based on props or state](https://react.dev/learn/you-might-not-need-an-effect#updating-state-based-on-props-or-state))

For expensive calculations, `useMemo` is the React 19 idiom; React Compiler may remove
the need for manual `useMemo` entirely on projects that opt in. Full rationale: [D-01](../decisions/D-01-no-useeffect-for-derived-state.md).

#### Correct

```tsx
function Form() {
  const [firstName, setFirstName] = useState('Taylor')
  const [lastName, setLastName] = useState('Swift')
  // Calculated during render
  const fullName = firstName + ' ' + lastName
  return <p>{fullName}</p>
}
```

#### Incorrect

```tsx
function Form() {
  const [firstName, setFirstName] = useState('Taylor')
  const [lastName, setLastName] = useState('Swift')
  const [fullName, setFullName] = useState('')
  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])
  // …
}
```

---

### Rule 2: Mutations go through Actions — `useActionState`, `useTransition`, `useOptimistic`

React 19 introduces Actions as the unit of mutation. The React 19 announcement:

> "In React 19, we're adding support for using async functions in transitions to handle
> pending states, errors, forms, and optimistic updates automatically."
> ([React 19 release notes — Actions](https://react.dev/blog/2024/12/05/react-19))

Actions give the component pending state, error routing to the nearest Error Boundary,
and optimistic updates for free. The four primitives are layered:

| Primitive | Role | Source of truth |
|---|---|---|
| `useTransition` | marks state updates as non-urgent; returns `isPending` | [useTransition](https://react.dev/reference/react/useTransition) |
| `useActionState` | wraps a reducer-style Action for `<form action>` or manual dispatch | [useActionState](https://react.dev/reference/react/useActionState) |
| `useOptimistic` | temporary value rendered while an Action is in flight | [useOptimistic](https://react.dev/reference/react/useOptimistic) |
| `use(promise)` | read a Promise during render — for data, not for mutations | [use](https://react.dev/reference/react/use) |

`useActionState` is described by React 19 as:

> "You can think of `useActionState` as `useReducer` for side effects from user Actions.
> Since it computes the next Action to take based on the previous Action, it has to order
> the calls sequentially. If you want to perform Actions in parallel, use `useState` and
> `useTransition` directly."
> ([useActionState — React](https://react.dev/reference/react/useActionState))

#### Correct — submit a form, optimistic update, pending state

```tsx
'use client'
import { useActionState, useOptimistic } from 'react'

async function updateName(previousName: string, formData: FormData) {
  const next = formData.get('name') as string
  await db.users.setName(next)
  return next
}

export function ChangeName({ currentName }: { currentName: string }) {
  const [optimistic, setOptimistic] = useOptimistic(currentName)
  const [, action, isPending] = useActionState(
    async (prev: string, formData: FormData) => {
      const next = await updateName(prev, formData)
      return next
    },
    currentName
  )

  return (
    <form action={async (formData) => {
      setOptimistic(formData.get('name') as string)
      await action(formData)
    }}>
      <input name="name" defaultValue={currentName} />
      <button disabled={isPending}>Update</button>
      <p>Your name is: {optimistic}</p>
    </form>
  )
}
```

#### Incorrect — manual pending/error bookkeeping

```tsx
'use client'
function ChangeName({ initialName }: { initialName: string }) {
  const [name, setName] = useState(initialName)
  const [error, setError] = useState<string | null>(null)
  const [isPending, setIsPending] = useState(false)

  const handleSubmit = async () => {
    setIsPending(true)
    const err = await updateName(name)
    setIsPending(false)
    if (err) { setError(err); return }
    // …
  }
  // …
}
```

---

### Rule 3: A Transition marks an update non-urgent — never a controlled input

React 19's `useTransition` reference is explicit about the limit:

> "You can't use a Transition for a state variable that controls an input."
> ([useTransition — React](https://react.dev/reference/react/useTransition))

The reason follows: input changes must stay synchronous. A controlled `<input>` is
updated from the change event, not from a Transition.

A Transition is also what enables *interruptibility* — a state update inside a
Transition is interrupted by more urgent updates, so the UI stays responsive while the
non-urgent work re-runs:

> "A state update marked as a Transition will be interrupted by other state updates."
> ([useTransition — React](https://react.dev/reference/react/useTransition))

#### Correct

```tsx
const [isPending, startTransition] = useTransition()
const [query, setQuery] = useState('')
const deferred = useDeferredValue(query)

return (
  <>
    <input value={query} onChange={e => setQuery(e.target.value)} />
    {isPending && <span>Searching…</span>}
    <div style={{ opacity: query !== deferred ? 0.6 : 1 }}>
      <SearchResults query={deferred} />
    </div>
  </>
)
```

#### Incorrect

```tsx
const [isPending, startTransition] = useTransition()
const [text, setText] = useState('')

function handleChange(e) {
  startTransition(() => {
    setText(e.target.value) // ❌ Transitions don't gate controlled input updates
  })
}
```

---

> Decision rationale: [D-01 — Refuse `useEffect` for derived state](../decisions/D-01-no-useeffect-for-derived-state.md), [D-03 — Refuse effects where event handlers belong](../decisions/D-03-effects-where-event-handlers-belong.md).
