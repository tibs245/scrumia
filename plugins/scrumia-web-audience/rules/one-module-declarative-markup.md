# One module owns the tracker; pages declare

*Refusal.* A page, component or script outside the measurement module that calls the
tracker's queue or names the analytics product.

## What is refused

```tsx
// ❌ a component reaching the tracker itself
onClick={() => window._paq.push(['trackEvent', 'store-click', 'app-store'])}
```

Every direct call is a place where a name, a value or a URL escapes the catalogue and
the cleaning, and a place that has to be found again when the product is replaced.

## What is written instead

One feature directory holds everything: loading the tracker, its configuration, the
address cleaning, the catalogue, the opt-out control. The rest of the application
neither imports it for the queue nor mentions the product.

- **A page declares an event with attributes.** An element carries
  `data-audience-event="store-click"` and, where the catalogue allows a value,
  `data-audience-store="app-store"`. One delegated listener in the module reads them.
  A helper in the module builds the attribute set from the typed catalogue, so a
  wrong name does not compile.
- **An event with no element to carry it** (a confirmation shown after an
  asynchronous step) is a function exported by the module, named after the event.
- **The tracker is loaded by the module** from a same-origin path, so the content
  security policy stays as it was. A configuration script the build processes keeps
  its fingerprint out of the policy; an inline one does not.
- **A test makes the rule fail.** It lists the source files outside the module and
  fails if any contains the queue's name (`_paq` for Matomo). The bundled script
  `scripts/detect-direct-tracker-calls.sh` is the same check for a codebase with no
  such test yet.

## Why

One owner is what makes the other rules enforceable: the catalogue, the cleaned
addresses and the signals are applied in one place or not at all.
