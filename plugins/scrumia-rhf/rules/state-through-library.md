# state-through-library

*A form whose values are read through `document.querySelector`, `formRef.current.elements`, `new FormData(form)`, or `event.target.elements[...].value` is a form that has stepped out of the library's API. The DOM has no view of the validation, the blur tracking, the dirty tracking, or the submission lifecycle the library is maintaining alongside.*

## What is refused

A React component that calls `useForm` reads the form's state — current values, errors, submission status, touched and dirty state — through the API the library exposes, not through the DOM:

- `watch(name)` / `watch(["a","b"])` / `watch()` — read values and subscribe to changes, re-rendering the calling component when the subscribed fields change.
- `getValues(name)` / `getValues()` / `getValues(["a","b"])` — read values on demand, without subscribing (no re-render). Use in event handlers, in callbacks passed outside React, in submit handlers that need the latest snapshot.
- `formState` from `useForm`'s return — for `errors`, `isSubmitting`, `isSubmitSuccessful`, `isSubmitted`, `isDirty`, `isValid`, `isValidating`, `touchedFields`, `dirtyFields`, `submitCount`, `disabled`, `isLoading`, `isReady`.
- `handleSubmit(handler)` for the submission entry point. The handler receives the validated values the library has — not `FormData(form)`, not `event.target.elements`, not anything the DOM offered.

A form that reads its state through any other channel — `document.querySelector("form").elements`, `formRef.current` reaching into the DOM, `event.target.elements[i].value`, `new FormData(form)` — is the finding.

## What is written instead

**Refused.** A form whose values are read off the DOM at submit time. The handler takes the DOM event, walks the form's elements, and assembles the values by hand. The library's `handleSubmit` is bypassed entirely; the schema (if there is one) has not run.

```tsx
import { useRef } from "react"
import { useForm } from "react-hook-form"

export function OrderForm() {
  const formRef = useRef<HTMLFormElement>(null)
  const { register } = useForm()

  function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    // Reading the DOM — validation never ran, blur never tracked, dirty never tracked.
    const data = new FormData(formRef.current!)
    console.log(Object.fromEntries(data.entries()))
  }

  return (
    <form ref={formRef} onSubmit={onSubmit}>
      <input {...register("product")} />
      <input {...register("quantity")} type="number" />
      <button type="submit">Order</button>
    </form>
  )
}
```

The handler reads what the DOM happens to show — last-typed strings, no coercion, no validation, no touched or dirty tracking. A field with a `register` validation rule the user bypassed will still reach the handler; a field whose value the schema would have transformed (`valueAsNumber`, `valueAsDate`) is whatever the input attribute showed.

**Written instead.** `handleSubmit(handler)`. The library owns the entry point, runs the schema, and calls the handler with the validated values the resolver returned — typed as the schema, not as the DOM:

```tsx
import { useForm, SubmitHandler } from "react-hook-form"

type FormValues = {
  firstName: string
  lastName: string
  email: string
}

export default function App() {
  const { register, handleSubmit } = useForm<FormValues>()
  const onSubmit: SubmitHandler<FormValues> = (data) => console.log(data)
  const onError = (errors) => console.log(errors)

  return (
    <form onSubmit={handleSubmit(onSubmit, onError)}>
      <input {...register("firstName")} />
      <input {...register("lastName")} />
      <input type="email" {...register("email")} />
      <input type="submit" />
    </form>
  )
}
```

The handler runs only after validation succeeds. The data parameter is the validated, coerced shape — the same shape the resolver returned. The `onError` callback receives the errors when validation fails.

For reads inside the component — conditional UI, derived values, "show this field when that one is set" — `watch` is the call:

```tsx
import { useForm } from "react-hook-form"

interface IFormInputs {
  name: string
  showAge: boolean
  age: number
}

function App() {
  const {
    register,
    watch,
    formState: { errors },
    handleSubmit,
  } = useForm<IFormInputs>()
  const watchShowAge = watch("showAge", false)
  const watchAllFields = watch()
  const watchFields = watch(["showAge", "age"])

  const onSubmit = (data: IFormInputs) => console.log(data)

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("name", { required: true, maxLength: 50 })} />
      <input type="checkbox" {...register("showAge")} />
      {watchShowAge && (
        <input type="number" {...register("age", { min: 50 })} />
      )}
      <input type="submit" />
    </form>
  )
}
```

`watch("showAge", false)` subscribes the component to one field and gives a fallback while the form's `defaultValues` haven't loaded. `watch()` subscribes to the whole form. `watch(["a","b"])` subscribes to a slice.

For reads in event handlers, callbacks outside React, or any place that should *not* subscribe and re-render — `getValues`:

```tsx
import { useForm } from "react-hook-form"

type FormInputs = {
  test: string
  test1: string
}

export default function App() {
  const { register, getValues } = useForm<FormInputs>()

  return (
    <form>
      <input {...register("test")} />
      <input {...register("test1")} />
      <button
        type="button"
        onClick={() => {
          const values = getValues()
          const singleValue = getValues("test")
          const multipleValues = getValues(["test", "test1"])
        }}
      >
        Get Values
      </button>
    </form>
  )
}
```

The library documents the contrast directly: "`getValues` **will not** trigger re-renders or subscribe to input changes."

For form-level state — errors, isSubmitting, isDirty — destructure from `formState`:

```tsx
import { useForm } from "react-hook-form"

const { formState: { errors, isSubmitting, isDirty, isValid, touchedFields } } = useForm()
```

`formState` is wrapped in a `Proxy` to improve render performance and skip extra logic when a specific state is not subscribed to — read it before a render in order to enable the state update, and read all the keys you want to subscribe to (do not gate a subscription behind a conditional that may be false on first render).

## Why

The library's contract is that the DOM is the *input* layer, not the *state* layer. The values are tracked inside the library; the errors are whatever the resolver returned; the submission state is whatever `handleSubmit` produces; the touched and dirty sets are tracked on the registered fields. Reaching past the API for any of these reaches past all of them at once:

1. **Validation.** A DOM read sees the last value the user typed. It does not see the validated value, the coerced value, or the resolver's verdict. `event.target.elements["age"].value` is the string in the input, not the number the schema coerced it to.
2. **Touched and dirty.** The DOM cannot tell whether the field has been blurred, only whether the input has a `value`. A form that gates "Submit" on a DOM-derived "all fields filled" check passes when the user pasted everything in at once without ever focusing a field — `touchedFields` would have caught that; the DOM did not.
3. **Submission state.** `isSubmitting`, `isSubmitSuccessful`, `submitCount`, and the `disabled` flag are library-level concepts with no DOM counterpart. The DOM only knows whether the form has been submitted; it does not know whether the submit succeeded.
4. **Errors.** `event.target.elements` carries no error. A handler that wants the field errors reads `formState.errors`; the DOM has nothing to offer.

The library documents the API above as the contract for state access — `watch` for subscribed reads, `getValues` for on-demand reads, `formState` for form-level state, `handleSubmit` for the submission entry point. Reaching the DOM bypasses all four at once, and the bypass is silent: the form still submits, the values still arrive, and the audit cannot prove they are wrong without re-running the validation by hand.

## Sources complémentaires

- `https://react-hook-form.com/docs/useform/watch` — the four overloads (`watch(name)`, `watch(names[])`, `watch()`, deprecated `watch(callback)`), the "Rules" admonition on `defaultValue` vs `defaultValues` precedence and re-render scope, and the "Watch in a Form" example block. The conditional-`showAge` example transcribed above is from this page's TS tab.
- `https://react-hook-form.com/docs/useform/getvalues` — the contract line "will not trigger re-renders or subscribe to input changes," the field-name resolution table (`getValues()`, `getValues("root")`, `getValues("root.test1")`, `getValues(["a","b"])`), the `dirtyFields` / `touchedFields` filter options (v7.63.0+), and the JS example block. The button-click example above is the JS example, lightly trimmed.
- `https://react-hook-form.com/docs/useform/formstate` — the full Return table (`isDirty`, `dirtyFields`, `touchedFields`, `defaultValues` (v7.37.0+), `isSubmitted`, `isSubmitSuccessful`, `isSubmitting`, `isLoading` (v7.41.0+), `submitCount`, `isValid`, `isValidating`, `validatingFields` (v7.51.0+), `errors`, `disabled` (v7.48.0+), `isReady` (v7.56.0+)), and the "Rules" admonition on the `Proxy` wrapping and the `[formState]` vs `[formState.errors]` `useEffect` dependency rule.
- `https://react-hook-form.com/docs/useform/handlesubmit` — the props table (`SubmitHandler`, `SubmitErrorHandler`), the "Rules" admonition (the `disabled`-as-`undefined` clause; the `setError` recommendation in the `try/catch` block), and the Sync example block. The two-handler example above (`onSubmit` + `onError`) is the TS tab of that block.
- Version pin: **v7**. The `formState` keys listed in the Return table are v7's contract; `defaultValues` (v7.37.0+), `isLoading` (v7.41.0+), `disabled` (v7.48.0+), `isReady` (v7.56.0+), `validatingFields` (v7.51.0+), and the `dirtyFields` / `touchedFields` `getValues` filter (v7.63.0+) are version-tagged in the upstream documentation. `getValues`'s "will not trigger re-renders" line and the four `watch` overloads are part of v7's stable surface; a v8 change to any of them is a breaking change for this rule.
