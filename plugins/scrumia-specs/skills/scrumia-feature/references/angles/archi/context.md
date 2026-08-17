# Angle: archi

**Content-tested, Business stratum only.** The file is `archi.md`.

## What this angle answers

How the apps talk to each other **for this EPIC**, for as long as the EPIC lasts.

It is the one file of the catalog with a scheduled death. It exists because an
EPIC that spans two apps needs a place to state the coordination, and that place
must not become a permanent architecture document nobody owns.

Read by: Technical Lead, devs of the apps concerned.

## When it activates

**By context.** Both conditions, not one:

| Question | |
|---|---|
| Is this a Business feature? | if no → this angle does not apply |
| Does its implementation touch two or more apps? | if no → skip |

A Business feature implemented by a single App feature does not carry it, however
complex that app's work is — that complexity is `tech.md`'s.

**By configuration.**

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        archi: context   # always | context | never
```

`context` is the default. `always` makes little sense here — a single-app EPIC has
nothing to put in it.

## The questions to explore it

1. Which apps are involved, and what does each own in this EPIC?
2. How do they talk — which contracts are at stake? Cite the `api-contract.md`
   files rather than restating them.
3. What data crosses which boundary, and in which direction?
4. Does deployment order matter? What breaks if the pieces ship in the wrong
   order?
5. What are the degraded modes — what happens when one part of the EPIC is
   unavailable, and does the other part notice?
6. For each thing you are about to write: **if this EPIC ships and closes, does
   this still have value?** Yes → it is an ADR under `docs/adr/`, cited from here.
   No → it belongs here.

## The lifespan rule

It dies with the EPIC. When the EPIC closes — shipped **or abandoned** — the file
is deleted, not left unmaintained. Anything still worth keeping at that point was
an ADR all along, and should have been one when it was written.

## Boundary

**Holds** — cross-app communication for this EPIC; the contracts at stake, as
pointers; the cross-app data flow; the deployment order if it matters; the
degraded modes.

**May hold** — a diagram of the cross-app flow, if it says something the prose
cannot.

**Must not hold**
- a decision meant to outlive the EPIC → `docs/adr/`
- a flow internal to one app → that app's `tech.md`
- the schema itself → the `api-contract.md` that owns it, cited
- a business rule → `business.md`

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
