# form-has-resolver

*A form whose validation lives in code next to each field — `required: true`, `pattern: /.../`, `validate: (v) => ...` — has reinvented per-field logic that one schema was supposed to replace.*

## What is refused

A React component that calls `useForm` from `react-hook-form` must pass a `resolver` to it. The resolver is the bridge between a schema (Zod, Yup, Joi, Vest, Ajv, TypeBox, Superstruct, or a hand-rolled adapter) and the form's validation step — the contract through which the library's `formState.errors` becomes a single, schema-shaped source of truth instead of a collection of per-field decisions.

A form without a resolver is the narrow finding this rule names: validation rules attached to individual inputs, each living next to its JSX, with no schema for any of them to reconcile against.

## What is written instead

**Refused.** A form that asks `useForm` to validate each field by the rules the JSX passes to `register`. The rules live next to each field; the schema that should hold them is nowhere in sight.

```tsx
import { useForm } from "react-hook-form"

export function SignupForm() {
  const { register, handleSubmit, formState: { errors } } = useForm()

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input
        {...register("name", { required: true })}
        placeholder="Name"
      />
      <input
        type="number"
        {...register("age", { required: true, min: 18, max: 120 })}
      />
      <input type="submit" />
    </form>
  )
}
```

Each `register` call carries its own rules. There is no object the form can point at and say "this is the contract." A field added later carries its own rules in its own JSX. A field removed leaves a stale object the auditor can no longer trace.

**Written instead.** The form imports a schema from `@hookform/resolvers/zod` (or `yup`, `joi`, `ajv`, `vest`, ...) and passes it as `resolver`. The `register` calls carry no rules — the schema owns them.

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const schema = z.object({
  name: z.string().min(1),
  age: z.number().min(18).max(120),
})

type Schema = z.infer<typeof schema>

export function SignupForm() {
  const { register, handleSubmit } = useForm<Schema>({
    resolver: zodResolver(schema),
  })

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register("name")} />
      <input type="number" {...register("age", { valueAsNumber: true })} />
      <input type="submit" />
    </form>
  )
}
```

The schema is one object, declared once, that the resolver passes to the library on every change. `register("age", { valueAsNumber: true })` is a *type coercion*, not a validation rule — it tells the library to read the input as a number so the schema sees one. The form's `formState.errors` is what the resolver returns, nothing else.

The same shape holds for any schema library the resolver adapter covers. With Yup:

```tsx
import { useForm } from "react-hook-form"
import { yupResolver } from "@hookform/resolvers/yup"
import * as yup from "yup"

const schema = yup
  .object()
  .shape({
    name: yup.string().required(),
    age: yup.number().required(),
  })
  .required()

export function App() {
  const { register, handleSubmit } = useForm({
    resolver: yupResolver(schema),
  })

  return (
    <form onSubmit={handleSubmit((d) => console.log(d))}>
      <input {...register("name")} />
      <input type="number" {...register("age")} />
      <input type="submit" />
    </form>
  )
}
```

With Joi:

```tsx
import { useForm } from "react-hook-form"
import { joiResolver } from "@hookform/resolvers/joi"
import Joi from "joi"

interface IFormInput {
  name: string
  age: number
}

const schema = Joi.object({
  name: Joi.string().required(),
  age: Joi.number().required(),
})

export function App() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<IFormInput>({
    resolver: joiResolver(schema),
  })

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input {...register("name")} />
      <input type="number" {...register("age")} />
      <input type="submit" />
    </form>
  )
}
```

## Why

The library's contract is that `formState.errors` is whatever the resolver returned. Without a resolver, the contract breaks at three boundaries at once:

1. **Per-field rules can disagree.** Two fields the user reads as "the same check" (the password and the confirm-password) carry the rule twice, in two JSX sites, written by two hands. The schema would have given them one rule, defined once.
2. **The `errors` object is per-field, not per-form.** The library only returns what each `register` call's rules produced. A cross-field rule — "the password and the confirmation match" — has nowhere to live. The resolver carries it because the schema carries it.
3. **A rule the JSX omits is silently absent.** A field added with `{...register("name")}` and no `required` is, to the library, an optional field. The schema would have said whether it was; the JSX has said nothing.

The library documents this directly: the resolver's contract is "Integrates with your preferred schema validation library" — it is the option through which a single source of truth enters the form. The schema-validation rules in the same section make the consequences explicit: "Schema validation focuses on field-level error reporting. Parent-level error checking is limited to the direct parent level, which is applicable for components such as group checkboxes" — without a schema there is no parent-level checking at all.

The regression a form without a resolver invites is silent: every field still validates, just inconsistently, just not in the place that makes the schema the source of truth. The audit treats the absence as a refusal because the inconsistency accumulates over the form's life, not at the moment the form is written.

## Sources complémentaires

- `https://react-hook-form.com/docs/useform` — section `useForm: UseFormProps`, anchor `#resolver`. The resolver contract: "Integrates with your preferred schema validation library." Supported adapters named: Yup, Zod, Joi, Vest, Ajv, and "many others." Code examples transcribed above (Yup, Zod, Joi) come from the same page, anchor `#resolver`, tabs of the Examples block.
- `https://react-hook-form.com/docs/useform` — section `useForm: UseFormProps`, anchor `#resolver`, the "Rules" admonition. The clauses quoted in *Why* above: schema-validation focus is field-level, parent-level checking is limited, the resolver function is cached, re-validation runs one field at a time, and a resolver cannot be combined with the built-in validators (`required`, `min`, etc.). The hierarchical-errors note ("`❌ { "participants.1.name": someErr }` will not set or clear properly — instead, use `✅ { participants: [null, { name: someErr } ] }`") is from the same admonition.
- Version pin: **v7**. The resolver API and the `@hookform/resolvers/*` adapter names quoted above are from `react-hook-form` v7 documentation; a future major bump that changes the resolver signature is a breaking change for this rule.
