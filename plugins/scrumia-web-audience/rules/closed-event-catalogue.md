# Events come from a closed catalogue

*Refusal.* An event name written at a call site that the specification does not list.
Measurement without consent is exempt only for a small, stated purpose, so what is
measured is a closed list, not whatever a page finds convenient to send.

## What is refused

```ts
// ❌ a name invented where the button is
tracker.push(['trackEvent', 'hero-cta-hover', 'blue-variant']);
```

A new event name arrives with its own purpose, and each purpose is something the
regulator's exemption has to cover. A name typed freely at a call site is a purpose
nobody decided.

## What is written instead

1. The specification holds the catalogue as a table: the event name, what it answers,
   and the values it may carry. Three or fewer kinds of event is the shape the
   exemption conditions describe (page presence, use of a feature, load or reading
   time); the table says which kind each one is.
2. The code holds the same list once, as a typed constant the compiler enforces:

```ts
export const eventNames = ['page-view', 'signup-confirmed', 'store-click'] as const;
export type EventName = (typeof eventNames)[number];
```

3. A value an event carries is a closed list too (`store-click` carries one of two
   store names), never free text taken from the page.
4. Adding an event is a specification change first: the table gains a row, the
   catalogue constant follows. A name that is in the code and not in the table is a
   finding.
5. What is refused is written in the same section, so the next person does not
   reopen it: linking an event to an account or an address, passing the visitor
   identifier to another system, A/B testing, heatmaps, session recording,
   measurement inside a native app, automatic link tracking.

## Why

The exemption is granted to a defined measurement, and the catalogue is that
definition made executable. Without it, the list drifts one reasonable event at a
time until the processing is no longer the one the privacy policy announced.
