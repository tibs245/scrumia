# Business rules — <feature>

<Business feature: the reference — value, personas, use cases, the journey as
intent, the rules, the vocabulary. App feature: this app's value, plus a
reference to the parent — never a copy of its rules — and only what is
specific to this app. Omit any section with nothing to say, except Value,
which every feature states.>

## Value

<Four answers, in order: who this is for; what it brings them; why it
matters; whether that contribution can be measured — name the measure, or
say plainly it is not instrumented today. Business stratum: the feature's
value. App stratum: this app's share of the value, then a reference to the
parent Business feature — never a copy of its rules.

Write what changes for a person, not what the system does. "So that <who>
stops <losing what>" is the shape; "the system does X" is the defect this
section exists to prevent.>

## Personas

<Who acts in this feature, and what they come for. Include an actor the
feature decides something about without them acting.>

## Use cases

<The situations that make this feature worth building.>

## The journey, as intent

<The steps as actor intent and the value delivered — no screen, no control,
no click path. The moment a step names one, it belongs to `ux.md` instead
(membership test, catalog.md).>

## The rules

<The business rules and invariants. A rule constrains what the product
promises, whatever tool enacts it; how a tool achieves it belongs to
`tech.md`. An uncertain rule is written as an open question, not resolved by
assertion.>

## Vocabulary

<The domain terms this feature relies on, defined once. A term a neighbouring
feature already defines differently is a finding, not a paragraph.>
