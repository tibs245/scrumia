# Angle: qa

**Mandatory in every feature, both strata.** The file is `qa.md`.

## What this angle answers

What has to be true for this feature to be accepted — written so that each answer
can pass or fail, before the code that satisfies it exists.

This module treats `qa.md` as the central document, not as an appendix. A criterion
carries a stable identifier (`AC-<n>`) that tickets cite and test code references.
When a behaviour changes, this file changes first: the contradiction then surfaces
before it is encoded in code, where fixing it costs the least.

Read by: QA, devs, execution and review agents.

## When it activates

Always. What varies is the altitude:

| Stratum | What the criteria cover |
|---|---|
| Business | the business criteria, independent of any interface |
| App | the criteria of this implementation, including technical cases — timeout, network error, concurrent state — and the accessibility targets that can fail, tagged as such |

No configuration key can switch this angle off. A feature nobody can test is not a
feature.

## The questions to explore it

**The nominal case first**

1. What is the one path that has to work? Write it before any edge case — a file
   that opens on an edge case usually has no agreed nominal.

**Then, systematically, the cases that produce bug tickets**

2. Zero / empty — nothing exists yet, the list is empty, the input is blank.
3. Boundary — the first, the last, the maximum, the value just past it.
4. Duplicate — the same thing twice, or the same request replayed.
5. Concurrency — two actors on the same object at the same moment.
6. Cancellation — the actor stops midway; what is left behind?
7. Expiration / timeout — the thing was valid and no longer is.
8. Insufficient permissions — the actor may not do this; what do they see?

Not every case applies. The ones that do not are deleted, not written as "N/A".

**Then the boundary of the promise**

9. What will someone reasonably expect this feature to do that it does not? That
   is the *Out of scope* section, and it is what prevents bug tickets on behaviour
   never promised.

**Finally, per criterion**

10. Can this criterion fail? If no state of the world makes it false, it tests
    nothing and must be rewritten or deleted.
11. Is its Given a state you can actually set up, and its Then a result you can
    actually observe?
12. Does it restate a business rule rather than test it? A criterion is an
    observation, not a repetition.

## Falsifiability, and the other "verifiable"

A criterion must be able to fail. That is a property of **one written criterion**,
and it is this angle's own test.

It is not the same property as ADR-0004's *verifiable*, which is a
**feature-splitting** criterion — "can you write at least one Given/When/Then
scenario that validates this unit of value without referencing another in-progress
feature". Two different properties under one shared word: cite this section for
whether a criterion can fail, ADR-0004 for whether a unit of value is small enough
to split on.

## Boundary

**Holds** — the acceptance criteria, Given/When/Then, one scenario per case, each
under a `### AC-<n>` heading; the out-of-scope section.

**May hold** — an accessibility target that can fail, tagged; a criterion marked
as covering a case that is deliberately not implemented yet, if the *Out of scope*
section says so.

**Must not hold**
- the persona or the value the criteria protect → `business.md`
- why a rule exists → the issue
- how the implementation satisfies a criterion → `tech.md`
- a ticket, issue or PR number → the tracker

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
