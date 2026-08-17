# Angle: business

**Mandatory in every feature, both strata.** The file is `business.md`.

## What this angle answers

Why this feature is worth building, and what it promises — stated so that a reader
who knows nothing about the implementation can agree or disagree with it.

It is the only angle that can make a feature be abandoned. That is its job: a
feature whose value cannot be stated is a splitting or deletion candidate, not a
feature missing a paragraph.

Read by: business, QA, devs. Written before any other file of the feature.

## When it activates

Always — this angle has no condition. What varies is which variant you write:

| Situation | Variant |
|---|---|
| `features/business/<feature>/` | Business stratum: the reference — value, personas, use cases, journey as intent, rules, vocabulary |
| `features/app/<app>/<feature>/` with a Business parent | App stratum: this app's share of the value, a reference to the parent, and only what is specific to this app |
| `features/app/<app>/<feature>/` with no Business parent | App stratum, and `index.md` states why the feature is purely technical |

No `.scrumia/config.yaml` key can switch this angle off. A project that wants
features without a value statement wants a different specs module.

## The questions to explore it

Answer them in this order. The first four are the `## Value` section and are not
optional; the rest produce a section only if they have an answer.

**Value — who, what, why, measured**

1. Who is this for? Name a role, a persona, a caller — not "the user" in general.
   If two audiences want opposite things from it, that is a splitting signal.
2. What does it bring them that they do not have today? State the gain, not the
   mechanism that produces it.
3. Why does it matter? What goes wrong, or stays wrong, if this is never built?
4. Can that contribution be measured? Name the measure — or say plainly it is not
   instrumented today. An invented metric is worse than an admitted absence.

**Personas**

5. Who acts in this feature, and what do they come for?
6. Is there an actor who is affected without acting — someone the feature decides
   something about? They belong here too.

**Use cases**

7. What situations make this feature worth building? One line each.
8. Which situation is the most frequent, and which is the most costly when it fails?

**The journey, as intent**

9. What are the steps, stated as actor intent and value delivered?
10. At each step, what would make the actor stop or give up? That is where the
    rules usually hide.

**The rules**

11. What must always be true, whatever the interface? Those are the invariants.
12. What is forbidden, and what happens when someone tries anyway?
13. Which rules do you not know the answer to yet? Write them as open questions —
    an uncertain rule resolved by assertion is the defect this format costs the
    most to undo.

**Vocabulary**

14. Which domain terms does this feature rely on, and does any of them already
    mean something else in a neighbouring feature? A term that collides is a
    finding, not a paragraph.

## Boundary

**Holds** — the value statement, the business rules, the invariants, the domain
vocabulary, the personas, the use cases, and the user journey as intent.

**May hold** — an open business question, clearly marked as open rather than
resolved by assertion.

**Must not hold**
- a screen, a control, a navigation path → `ux.md`
- a technology choice, or a constraint of the implementation → `tech.md`
- a test scenario → `qa.md`
- a schema another feature consumes → `api-contract.md`
- the history of how a rule came to be → the issue
- a ticket, issue or PR number → the tracker

The membership tests that settle the contested edges — business vs ux on the
journey, business vs tech on mechanisms — are stated once in
[`../../catalog.md`](../../catalog.md) § *The membership tests*. Read them there;
they are not repeated here, because a second copy is how they drift.

## What sources it

`business.md` is sourced from business rules and needs alone — persona, scenario,
need — and nothing else. What flows out of it differs by reader: `qa.md`'s
acceptance criteria are downstream of these rules, one way only. `business.md`
never reads `qa.md` back to justify a rule.

Its relationship with an ADR is a **pointer, not a narration**: it names which ADR
is the current authority on something it states, and stops there. It never
restates what the ADR decided, quotes its former wording, or explains how the
decision was reached.

## Duplication

Duplicating a business rule in two files guarantees they will diverge. A single
reference, a single place that has authority. An App feature **never** copies a
rule from its Business parent — it references it.

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
