# inputs-are-registered

*A `<input>` whose value and change handling are owned by a `useState` paired with an `onChange` to the same field has rebuilt, by hand, what `register("name")` already provides — and the library no longer sees the field as one of its own.*

## What is refused

A `<input>`, `<select>` or `<textarea>` element rendered inside a form (any component that calls `useForm`) must be one of:

1. **Owned by the library.** Its props are the spread of `register("name")` — `{...register("name")}` — or it is wrapped by `<Controller>` from `react-hook-form`, which wires the same `name`, `onChange`, `onBlur`, `value`, and `ref` through the library's API. The library owns the field's value, blur, dirty and validation state.
2. **Genuinely controlled from outside the form.** Its `value` comes from outside the form's data — a third-party editor with rich internal state, a piece of UI whose source of truth is not the form. This is not subject to this rule; a reviewer judges whether the case is genuine.
3. **Managed by `useState` + `onChange` to the same field, with no library call in sight.** This is the refusal. The `useState` declares a value the library does not know; the `onChange` writes to it; the library's `register` is missing. The form's data, as the library sees it, is undefined or stale; the form's validation, as the schema sees it, never runs on the field.

## What is written instead

**Refused.** A form whose input owns its own state with `useState`, with `onChange` writing back to it. The library sees nothing — there is no `register`, no `<Controller>`, no spread. The form's "data" is the React state, the schema (if there is one) cannot reach it.

```tsx
import { useState } from "react"
import { useForm } from "react-hook-form"

export function ProfileForm() {
  const { handleSubmit, formState: { errors } } = useForm()
  const [name, setName] = useState("")

  return (
    <form onSubmit={handleSubmit((data) => {
      // data has no "name" — the library never saw it
      console.log(data)
    })}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      {errors.name && <span>Required</span>}
      <button type="submit">Save</button>
    </form>
  )
}
```

The library returns `data` with no `name` field — `useState` never wrote through it. The `errors.name` check is unreachable, because the schema (or the library's per-field rules, if any) has no field named `name` to put an error on.

**Written instead.** The spread of `register("name")`. The library owns `ref`, `onChange`, `onBlur`, `name`, and (in v7) the validation rules registered alongside. The form's data on submit is exactly what the library tracked; `formState.errors` is keyed by the same `name`.

```tsx
import { useForm } from "react-hook-form"

export function ProfileForm() {
  const { register, handleSubmit, formState: { errors } } = useForm()

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register("name")} placeholder="Name" />
      {errors.name && <span>Required</span>}
      <button type="submit">Save</button>
    </form>
  )
}
```

The same call covers selects and textareas — the library's API is the constant across input types. With a `<select>`:

```tsx
import { useForm } from "react-hook-form"

export default function App() {
  const { register, handleSubmit } = useForm({
    defaultValues: {
      firstName: "",
      lastName: "",
      category: "",
      checkbox: [],
      radio: "",
    },
  })

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input {...register("firstName", { required: true })} placeholder="First name" />
      <input {...register("lastName", { minLength: 2 })} placeholder="Last name" />
      <select {...register("category")}>
        <option value="">Select...</option>
        <option value="A">Category A</option>
        <option value="B">Category B</option>
      </select>

      <input {...register("checkbox")} type="checkbox" value="A" />
      <input {...register("checkbox")} type="checkbox" value="B" />

      <input {...register("radio")} type="radio" value="A" />
      <input {...register("radio")} type="radio" value="B" />

      <input type="submit" />
    </form>
  )
}
```

When a third-party controlled component is the right answer — React-Select, MUI, a date picker — the library's wrapper is `<Controller>`, which carries the same `field` props (`onChange`, `onBlur`, `value`, `name`, `ref`) through to the wrapped component:

```tsx
import { useForm, Controller } from "react-hook-form"
import ReactDatePicker from "react-datepicker"

type FormValues = { ReactDatepicker: string }

export function App() {
  const { handleSubmit, control } = useForm<FormValues>()

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <Controller
        control={control}
        name="ReactDatepicker"
        render={({ field: { onChange, onBlur, value, ref } }) => (
          <ReactDatePicker
            onChange={onChange}
            onBlur={onBlur}
            selected={value}
          />
        )}
      />
      <input type="submit" />
    </form>
  )
}
```

The `render` callback receives the same wiring `register` would have returned, expressed for components that do not accept a `ref` in the standard slot.

## Why

The library's API is built around `register` as the place where the form's data, blur tracking, dirty tracking, and validation meet. The library documents this directly: "`register` ... allows you to register an input or select element and apply validation rules in React Hook Form. Validation rules are all based on the HTML standard and also allow for custom validation methods." When a field bypasses `register`, every one of those four contracts breaks at once:

- **Data**: the value the form submits is whatever `useState` last wrote, not what the library's `handleSubmit` returns. A field the user never blurred, never validated, is indistinguishable from a field the library never knew existed.
- **Validation**: with no resolver and no `register`-attached rules, the schema has no field to check, and the library's per-field rules are absent. The form either has no validation or has duplicated it in the `useState` setter — two sources of truth, neither reachable from `formState.errors`.
- **Blur and dirty**: `formState.touchedFields` and `formState.dirtyFields` track the fields the library registered. An input the library does not see is neither touched nor dirty by the library's reckoning; a UI that gates "Submit" on `formState.isDirty` will misreport.
- **Submit**: `handleSubmit` reads from the library's internal store. A field the store never received is `undefined` on submit. A reviewer who assumes "all inputs are tracked" is looking at a form where one of them is not.

The library's `register` rules — transcribed from the `useForm/register` documentation — make the cost of a `useState` parallel explicit: a registered input is the one the library sees, on every channel the form depends on.

## Sources complémentaires

- `https://react-hook-form.com/docs/useform/register` — anchor `#props` for the return table (`ref`, `name`, `onChange`, `onBlur`, plus v7.21.0+ progressive `min`/`max`/`minLength`/`maxLength`/`pattern`/`required`/`disabled`); anchor `#options` for the rules object (validation rules, value coercion, `disabled`, `deps`); the "Register input or select" example block is the source of the multi-input example above. The "Destructuring assignment" tip is also from this page.
- `https://react-hook-form.com/docs/usecontroller/controller` — the Props and Return tables; the "Rules" admonition on `name` being unique. The "Web" examples block is the source of the React DatePicker example transcribed above.
- Version pin: **v7**. `register`'s return value (`ref`, `name`, `onChange`, `onBlur`) is v7's stable shape; the progressive options table was added in v7.21.0 and is documented as such. `<Controller>`'s `field` object (`onChange`, `onBlur`, `value`, `name`, `ref`) and `fieldState` (`invalid`, `isTouched`, `isDirty`, `error`) are v7's contract; a v8 that renames or reshapes them is a breaking change for this rule.
