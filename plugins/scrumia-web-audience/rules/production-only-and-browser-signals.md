# Measured in production only, and only if the browser has not said no

*Refusal.* A measurement that runs in development, preview or test builds, or that
loads after the browser has sent a do-not-track signal.

## What is refused

- A site identifier written into the source, so every build, including a developer's
  machine, reports to the production statistics.
- A tracker loaded unconditionally, with the opt-out left to the server.

## What is written instead

- **The site identifier is a build-time setting**, read at one place from the
  environment and declared in the environment type. The inventory of the production
  deployment sets it; every other environment leaves it empty.
- **Empty means nothing is rendered**: no script, no configuration, no opt-out
  control. A value that is present and is not a positive integer stops the build and
  names the variable, rather than measuring the wrong site.
- **No banner.** If the measurement stays inside the exemption, nothing asks for
  consent, and a banner would announce a choice that does not exist. A banner is
  what the application needs the day it leaves the exemption, and that is a
  specification change.
- **The module reads the browser's signals itself**: Global Privacy Control
  (`navigator.globalPrivacyControl`) and Do Not Track (`navigator.doNotTrack`,
  `window.doNotTrack`, values `1` or `yes`). If either is set, the tracker is not
  loaded. Configuring the tracker to respect it is not enough: a tracker never
  loaded sends nothing and sets no cookie.
- **Pages that must not be measured at all** (the ones that read a token, an
  administration area) are a list in the module, tested.

## Why

The statistics answer a question about the public site. Anything else in them is
noise, and a developer's traffic is the cheapest way to make the figures wrong.
Respecting the signal costs nothing and is part of what the exemption assumes.
