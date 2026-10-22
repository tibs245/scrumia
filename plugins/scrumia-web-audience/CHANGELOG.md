# Changelog — scrumia-web-audience

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-10-22
### Added
- The module: audience measurement on a web app kept inside the consent exemption, six
  rules contributed to the `implement` and `review` registers.
- `closed-event-catalogue`, `one-module-declarative-markup`, `cleaned-addresses`,
  `production-only-and-browser-signals`, `opt-out-that-lasts` — the five refusals.
- `exemption-conditions` — the fifteen conditions as closed questions, the refusal of
  campaign attribution, and a Matomo worked example. A paraphrase: the regulator's
  current text prevails.
- `web-audience-audit` — a skill that checks an existing app against the six rules.
- `scripts/detect-direct-tracker-calls.sh` — lists files outside the measurement module
  that mention the tracker queue; exits `3` on a finding.
