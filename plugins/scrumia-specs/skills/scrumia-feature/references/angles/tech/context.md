# Angle: tech

**Content-tested, App stratum.** The file is `tech.md`.

## What this angle answers

Why this implementation is shaped the way it is — the part the code cannot say
about itself.

It does not document what the code already states. A file that lists the modules
of a directory is a stale copy of `ls`; a file that says why the directory is split
that way, and what was rejected, is worth reading a year later.

Read by: devs, Technical Lead.

## When it activates

**By context.** One yes is enough.

| Question | Default when unsure |
|---|---|
| Does this feature add a dependency? | yes → write it |
| Was a structural choice made where another was plausible? | yes → write it |
| Is debt being assumed knowingly? | yes → write it |
| Does the implementation live under a constraint a reader would not guess — a platform limit, a performance budget, a compatibility floor? | yes → write it |
| Does data flow inside this app in a way the code does not make obvious? | no |
| Is it a Business feature? | no → this angle is App-only |

**By configuration.**

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        tech: context   # always | context | never
```

`context` is the default.

## The questions to explore it

1. What dependency does this add, and what did it replace or avoid writing? A
   dependency with no stated reason is one nobody can remove later.
2. What structure was chosen, and which plausible alternative was rejected? Name
   the alternative — "we chose X" without a rejected Y records nothing.
3. What debt is being assumed? State it with its date and its **exit condition** —
   the event that makes it worth paying off. Debt with no exit condition is not
   debt, it is a decision nobody will revisit.
4. What constraint does the implementation live under that a reader would not
   guess from the code?
5. How does information move inside this app for this feature? Only the parts the
   code does not make obvious. Anything crossing an app boundary is `archi.md`'s.
6. Is any of the above actually a decision meant to outlive this feature? Then it
   is an ADR, cited from here, not written here.

## Boundary

**Holds** — dependencies added and their reason; structure chosen and alternative
rejected; debt assumed with its date and exit condition; the constraints the
implementation lives under; the flow of information and data **within this app**.

**May hold** — a pointer to the ADR that owns a decision this feature applies.

**Must not hold**
- flow that crosses an app boundary → `archi.md`
- a rule the business owns → `business.md`
- a schema another feature consumes → `api-contract.md`
- how a criterion is tested → `qa.md` states what must hold; here, only what the
  code cannot say
- a restatement of what the code already says

The membership tests — tech vs archi on data flow, business vs tech on mechanisms
— are stated once in [`../../catalog.md`](../../catalog.md) § *The membership
tests*.

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
