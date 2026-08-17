# Angle: legal

**Content-tested, both strata.** The file is `legal.md`.

## What this angle answers

Which obligations this feature is subject to, on what data, for how long, and what
the people concerned may demand.

It records obligations. It does not invent them: an obligation nobody has verified
is written as an open question, never resolved by assertion. A confident wrong
answer here is worse than an admitted gap, because it stops anyone from asking.

Read by: legal, business, devs.

## When it activates

**By context.** One yes is enough.

| Question | Default when unsure |
|---|---|
| Does it process personal data — anything that identifies a person, directly or not? | yes → write it |
| Does it handle payment, or anything with a monetary flow? | yes → write it |
| Does it store or publish content produced by users? | yes → write it |
| Could a minor be a user of it? | yes → write it |
| Does it touch health, finance, or another regulated sector? | yes → write it |
| Does it carry a named legal risk of its own — a trademark question, a licence obligation, a third-party terms-of-service constraint? | yes → write it |

Every default is "yes → write it". That is deliberate: on this angle, the cost of a
file that turns out unnecessary is a paragraph, and the cost of an absent one is a
liability nobody looked at.

**By configuration.**

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        legal: context   # always | context | never
```

`context` is the default. `always` suits a regulated project where every feature
must record a compliance judgement even when the answer is "nothing applies".

## The questions to explore it

1. Which obligations apply, **named**? Not "GDPR" as a word — the article, the
   principle, or the specific requirement.
2. What data is processed, and on what legal basis for each category?
3. How long is it kept, and what happens at the end of that period — deletion,
   anonymisation, archival?
4. What rights do the people concerned have here, and how are they exercised in
   practice? A right nobody can exercise is not granted.
5. What notices and consents are required, when are they shown, and what does the
   user see?
6. Is anything uncertain? Write it as an open question with what would settle it —
   not as a conclusion.
7. Is there a residual legal risk the project accepts rather than resolves? Record
   it with the acceptance record defined in the security angle — stated once
   there, referenced from here, so the two cannot drift.

## Boundary

**Holds** — the applicable obligations, named; the data processed and its legal
basis; the retention period; the rights of the individuals; the required notices
and consents.

**May hold** — an open question about an obligation, with what would settle it.

**Must not hold**
- made-up legal advice — an uncertain obligation is an open question, not a ruling
- an engineering risk with no legal trigger → `security.md`
- a second format for accepting residual risk → the security angle's acceptance
  record, referenced
- the implementation of a right → `tech.md` or `ux.md`; here it is required, not
  designed

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
