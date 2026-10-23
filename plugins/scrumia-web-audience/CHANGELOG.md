# Changelog — scrumia-web-audience

All notable changes to this module, on [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- `send-to-the-collection-directly` — the module posts a closed body to the tool's
  collection on the site's own domain instead of loading the tool's script.
- `the-proxy-opens-one-route` — one relayed route with its conditions, the client
  address written by the proxy, no access log; the unfiltered body named as a risk.
- `measurement-after-the-page` — starts when the page is idle; a failure never shows,
  and a test proves it.
- `tool-and-database-apart` — the tool's own database, no outgoing call, administration
  off the Internet, a purge where the tool has no retention.
- `exemption-conditions` — a section on "no cookie is not no tracker" and on
  pseudonymous against anonymous; Umami as the first worked example.

### Changed
- `opt-out-that-lasts` — the refusal is a marker the tool respects (a storage key or a
  cookie), a fourth state for unreadable storage, nothing sent when the marker cannot
  be read.
- `production-only-and-browser-signals` — the identifier format follows the tool; the
  signals are read before every send.
- `cleaned-addresses`, `one-module-declarative-markup` — a body built by the module, and
  the collection path as what the ownership test searches for.
- `web-audience-audit` — ten questions instead of six.
- Umami is the example of reference; Matomo stays as another.

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
