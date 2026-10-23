# An opposition the person can make, and that lasts

*Refusal.* An opt-out that is missing, hidden outside the privacy policy, that expires
before the measurement it refuses, or that cannot be read and is then ignored.

## What is refused

- No way to refuse, because "the data is anonymous".
- A refusal stored in a cookie shorter than the measurement cookie: it lapses, the
  measurement resumes, and the person never chose that.
- A control that says nothing about its state.
- A refusal marker the tool does not recognise, so that the tool's own tracker (or a
  second one) goes on counting.
- Measuring when the marker cannot be read.

## What is written instead

- **The control lives in the privacy policy**, in the section that describes cookies
  and other trackers, rendered by the module and only when a site identifier is set.
  With no JavaScript it renders nothing, and the text says that then nothing is
  measured.
- **The refusal is a marker the tool respects.** Umami excludes a browser that holds
  `umami.disabled` in local storage; Matomo's `optUserOut` writes a cookie. The module
  writes the marker the tool documents, and removes it to opt back in. A marker of the
  module's own invention is a finding.
- **States, shown as text.** Measured (a button to stop). Opted out (a button to be
  measured again). Refused by the browser (a signal is set; no button, the text says
  the signal is what is in force). Storage unreadable (no button; the text says
  nothing is measured because the choice cannot be read).
- **Unreadable storage means not measured.** If reading the marker throws, no send
  happens: not being able to read an opposition is not a licence to ignore it.
- **The state shown is re-read after each write.** A write that fails leaves the state
  as it was, and an alert under the button says the choice was not kept.
- **The refusal outlasts the measurement.** A cookie marker lasts longer than the
  measurement cookie, by a stated duration (Matomo's default is thirty years; about
  thirteen months is a common measurement lifetime). A storage marker has no expiry
  and lasts until the visitor clears it; the policy says so, and that it holds for
  that browser only.
- **Accessible state**: a status region present from the first render, so a screen
  reader announces the change; no pressed-state attribute on a button whose label
  already changes.
- **Same look as the application's other secondary buttons.** No new component for
  a one-off.
- **What the browser keeps is a constant in the module.** The policy's list of what is
  kept (cookies, a storage key, or nothing for those who did not object) is generated
  from it or checked against it, so the page cannot announce what the code does not
  set, or the reverse.

## Why

The exemption rests on the person being told and able to object without friction.
An opposition that quietly expires, that the tool does not read, or that is dropped
when it cannot be read, is the same as none.
