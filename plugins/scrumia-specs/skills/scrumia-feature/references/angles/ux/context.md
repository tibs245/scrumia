# Angle: ux

**Content-tested, App stratum only.** The file is `ux.md`.

## What this angle answers

What the user sees, in what order, and what the screen refuses to do. It is the
interface half of a journey whose intent half lives in `business.md`.

Read by: UX, frontend devs.

## When it activates

**By context.** One yes is enough.

| Question | Default when unsure |
|---|---|
| Does this feature put something on a screen a person looks at? | yes → write it |
| Does it change what an existing screen shows, or when? | yes → write it |
| Does it produce output a person reads directly — a CLI's output, an email, a generated page? | yes → write it |
| Is it a backend feature whose result is only ever consumed by another program? | no → skip |

A Business feature never carries this file: a journey stated as intent is
`business.md`'s, and the moment it names a screen it is an App feature's subject.

**By configuration.**

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        ux: context   # always | context | never
```

`context` is the default. `always` suits a product where every feature is
user-facing and an absent file would be an oversight rather than an assertion.

## The questions to explore it

1. Where does the user enter this screen or flow from, and where do they leave to?
2. Which components does it use? Each is a pointer to its
   `design/components/<name>/spec.md` with its role here — never a copy of the
   component's anatomy.
3. What are the states — empty, loading, error, success — and what is the exact
   copy in each? Empty and error are the two that get skipped and then invented at
   implementation time.
4. What is the reading order, and does it match the visual order?
5. What moves focus, and what announces itself when it changes?
6. What are the text alternatives for anything non-textual?
7. Which accessibility properties does this journey have to hold? State them in
   prose here; anything that can pass or fail against a named technical criterion
   is a tagged `qa.md` criterion instead.
8. What must this screen never do — an action it must not offer, a state it must
   not enter — that is not already a component-level refusal?
9. Does this screen need a value — a colour, a spacing, a duration — that no token
   and no component supplies? That is a finding for `design/`, not a number
   written here.

## Boundary

**Holds** — the screen or flow with its entry and exit points; the composition, as
pointers to component specs; the states with their copy; the navigation, reading
order and focus flow; the text alternatives; the accessibility properties stated
in prose; the interface constraints.

**May hold** — a markdown or ASCII mockup, **only as a seed** for a layout that
has no `design/` counterpart yet. It converts into an exploration or a component
spec; it does not stay a permanent second drawing. A link to an external design
tool serves the same purpose.

**Must not hold**
- a literal colour, spacing or duration → `design/tokens.css`
- a component's anatomy or behaviour → its `design/components/` spec, cited
- a business rule, or the intent behind the journey → `business.md`
- a WCAG target that can pass or fail → a tagged `qa.md` criterion

When prose here touches something a criterion tests, it cites the criterion and
names the constraint — it does not restate the criterion's mechanism. Identity-level
rules (contrast minimums, the accent hue-distance rule) live in `design/` and are
cited, never restated.

The membership tests — business vs ux on the journey, ux vs qa on accessibility —
are stated once in [`../../catalog.md`](../../catalog.md) § *The membership tests*.

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
