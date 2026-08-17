# Angle: devx

**Content-tested, App stratum.** The file is `devx.md`.

## What this angle answers

How someone outside this feature uses what it exposes, and what will trip them up.

Its reader is a developer in another app or another team who will never read this
feature's code. Everything here is written for them; the internal *why* stays in
`tech.md`.

Read by: devs of the other apps.

## When it activates

**By context.** One yes is enough.

| Question | Default when unsure |
|---|---|
| Does this feature expose a library, an SDK, or a package others import? | yes → write it |
| Does it expose reusable components, hooks or helpers? | yes → write it |
| Does it publish a command, a script or a binary others run? | yes → write it |
| Is what it exposes consumed only by this feature's own code? | no → skip |

The distinction with `api-contract.md`: a contract states the **shape** of data
crossing a boundary; this angle states how to **use** what is exposed. A published
library usually needs both — the contract for what it returns, this for how to
call it.

**By configuration.**

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        devx: context   # always | context | never
```

`context` is the default.

## The questions to explore it

1. What is exposed, exactly — which names, imported or invoked how?
2. What is the smallest example that actually works? Not a sketch: something a
   reader can paste and run.
3. What trips up a first-time consumer? The argument that looks optional and is
   not, the order that matters, the silent no-op. If you cannot name one, you have
   not watched anyone use it.
4. What is stable, and what may change without notice?
5. What is deliberately not supported, so nobody files a bug about it?

## Boundary

**Holds** — how to use it; minimal working examples; the pitfalls; what is stable
and what is not.

**May hold** — a note on what is deliberately unsupported.

**Must not hold**
- the internal why of the implementation → `tech.md`
- the schema of data crossing a boundary → `api-contract.md`
- a business rule about what the thing means → `business.md`

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
