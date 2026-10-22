# An opposition the person can make, and that lasts

*Refusal.* An opt-out that is missing, hidden outside the privacy policy, or that
expires before the measurement it refuses.

## What is refused

- No way to refuse, because "the data is anonymous".
- A refusal stored in a cookie shorter than the measurement cookie: it lapses, the
  measurement resumes, and the person never chose that.
- A control that says nothing about its state.

## What is written instead

- **The control lives in the privacy policy**, in the section that describes the
  cookies, rendered by the module and only when a site identifier is set.
- **Three states, shown as text:** measured (a button to stop), opted out (a button
  to be measured again), and refused by the browser (a signal is set; no button,
  and the text says the signal is what is in force).
- **The refusal cookie outlasts the measurement cookie** by a good margin, and its
  duration is stated. Matomo's default is thirty years; choose a stated duration
  longer than the measurement cookie (about thirteen months is a common choice) and
  apply it with `optUserOut`.
- **Accessible state**: a status region present from the first render, so a screen
  reader announces the change; no pressed-state attribute on a button whose label
  already changes.
- **Same look as the application's other secondary buttons.** No new component for
  a one-off.
- **The cookies the module sets are a constant in the module.** The policy's cookie
  table is generated from it or checked against it, so the page cannot announce a
  cookie the code does not set, or the reverse.

## Why

The exemption rests on the person being told and able to object without friction.
An opposition that quietly expires is the same as none.
