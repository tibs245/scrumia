# The measurement waits for the page, and never touches it

*Refusal.* A measurement that delays rendering, or whose failure shows on the page.

## What is refused

- The tracker or the first send in the page's critical path: before first paint, in a
  blocking script, inside a handler the page's own behaviour depends on.
- A send whose rejection, a collection that is down, a blocked request, a thrown
  exception from the module, surfaces as a console error loop, a broken button or a
  half-rendered page.

## What is written instead

- **The module starts after the page has loaded, when the browser is idle**:
  `requestIdleCallback` with a timeout once `readyState` is `complete` (otherwise on
  `load`), and a zero-delay timer where idle callbacks do not exist. Nothing of the
  rendering depends on it.
- **Every entry point swallows what goes wrong.** The send ignores a rejected promise
  and a thrown error; the scheduled task runs inside a guard that returns without a
  message. The page is never told.
- **A test proves it.** One test makes the send throw, one makes it reject, one makes
  the collection unreachable, and each asserts the page's behaviour is unchanged and
  nothing is thrown. A test that only covers the happy path does not prove this rule.
- **Delegated listeners do the same**: a click on a declared element sends in the
  guard and then lets the click go on.

## Why

Audience figures are worth less than the page. A measurement that can break rendering,
or that delays it for people who did not consent to being counted, costs more than it
returns.
