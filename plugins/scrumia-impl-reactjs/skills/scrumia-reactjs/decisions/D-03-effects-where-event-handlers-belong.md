# D-03: Refuse effects where event handlers belong

**Status**: Adopted
**Date**: 2026-08-13
**Impacts**: [guides/02-state-and-derivations.md](../guides/02-state-and-derivations.md)

## Context

The opening of React 19's "You Might Not Need an Effect" page states the principle
the rule rests on:

> "Effects are an escape hatch from the React paradigm. They let you 'step outside'
> of React and synchronize your components with some external system like a non-React
> widget, network, or the browser DOM. **If there is no external system involved (for
> example, if you want to update a component's state when some props or state
> change), you shouldn't need an Effect.**"
> — [You Might Not Need an Effect — React](https://react.dev/learn/you-might-not-need-an-effect)

The same page frames the question to ask directly:

> "When you're not sure whether some code should be in an Effect or in an event handler,
> ask yourself *why* this code needs to run. Use Effects only for code that should run
> *because* the component was displayed to the user."
> — [You Might Not Need an Effect — React](https://react.dev/learn/you-might-not-need-an-effect)

The page continues with the framing the rule rests on:

> "If this logic is caused by a particular interaction, keep it in the event handler. If
> it's caused by the user *seeing* the component on the screen, keep it in the Effect."
> — [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

The "Separating Events from Effects" page refines the same distinction:

> "Event handlers run in response to specific interactions."
> "Effects run whenever synchronization is needed."
> "Logic inside event handlers is not reactive."
> "Logic inside Effects is reactive."
> — [Separating Events from Effects — React](https://react.dev/learn/separating-events-from-effects)

The canonical defect: a notification that fires inside an Effect whenever the product
becomes "in cart" — fired again on every subsequent remount, including a page refresh
after a single add-to-cart. React 19's docs:

> "This Effect is unnecessary. It will also most likely cause bugs. For example, let's say
> that your app 'remembers' the shopping cart between the page reloads. If you add a
> product to the cart once and refresh the page, the notification will appear again."
> — [You Might Not Need an Effect — React](https://react.dev/learn/you-might-not-need-an-effect)

The fix moves the call into the click handler that initiated the add-to-cart.

## Arguments For

- **The bug is a re-run, not a wrong value.** The notification *is* what it should be —
  fired when the product is in the cart. It is fired again whenever the cart state
  happens to be re-read, including after a refresh, and that is what is wrong. Effects
  are reactive; the original action was not.
- **The fix is the data flow.** `addToCart(product); showNotification(...)` inside a
  click handler *is* the sequence; an Effect that observes `product.isInCart` and
  duplicates it is two sources of truth.
- **It composes with the Actions rule.** React 19's `useTransition` and `useActionState`
  are designed to run in event handlers; placing the call in the handler is what gives
  you pending state and Error Boundary integration for free.
- **It removes "did the user interact?"** reasoning from the Effect body. An effect body
  that checks "is the user clicking this button?" is one that should be a handler.

## Arguments Against (trade-offs accepted)

- For a side effect that must fire on *mount*, regardless of what the user does next,
  an Effect is correct; the rule does not refuse it.
- For a sync with an external system (chat connection, subscription, analytics), the
  "component was displayed" reason is the genuine one — these belong in Effects and
  stay there.

## Verdict

Refuse effects where event handlers answer the same question. Code that runs *because
the user did X* lives in the handler for X. Code that runs *because the component is
displayed* lives in an Effect. The two are not interchangeable.
