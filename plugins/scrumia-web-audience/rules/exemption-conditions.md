# The exemption conditions, asked one at a time

*Method.* France's data-protection authority (CNIL) lets a site measure its audience
without asking for consent when the measurement stays inside a set of conditions.
This file paraphrases them as closed questions so a change can be checked against
each. **The regulator's current text prevails over this paraphrase**: read the
documents below on the regulator's site before relying on an answer, and say in the
specification which date they were read.

Documents the conditions are drawn from, by title: the guidelines on cookies and
other trackers (deliberation 2020-091); the recommendation on cookies and other
trackers; the self-assessment tool for an audience measurement solution exempt from
consent (July 2025); and the vendor-specific configuration guide the regulator
publishes for the solution in use.

## The questions

Each is answered yes or no from the code, the configuration or the specification.
A no is a finding, or a decision to leave the exemption and ask for consent.

| # | Question |
|---|---|
| 1 | Is there a single purpose, the audience measurement of the publisher's own site, and no other use of the data? |
| 2 | Is the set of events closed, and limited to page presence, use of a feature, and load or reading time? (`closed-event-catalogue.md`) |
| 3 | Are the results statistics only: no visit log, no per-person profile, no raw export? |
| 4 | Is the IP address never stored, or truncated before anything is stored by at least its last byte, and is the address the tool reads the one the proxy wrote? (`the-proxy-opens-one-route.md`) |
| 5 | Is there no cross-referencing with another processing: no user identifier, no account, address or token sent, no import of external data, and a database no role of the application can read? (`tool-and-database-apart.md`) |
| 6 | Does no log outside the measurement tool record the IP address or the query string of a measurement request, including the web server's access log? |
| 7 | Does no third party receive the data, and is no third-party tool embedded? |
| 8 | Is there no tracking across sites: a cookie bound to the site's own host, no cross-domain linking, no fingerprinting? |
| 9 | Is the tracker's lifetime bounded and never extended by a later visit: a cookie's expiry (the regulator recommends no more than thirteen months), or, with no cookie, an identifier that changes on a stated schedule? |
| 10 | Is retention bounded (the regulator accepts at most twenty-five months)? |
| 11 | Is what the browser keeps exactly what the privacy policy lists, and does the policy say "no cookie" only for what is no cookie, never "no tracker" for a computed identifier? |
| 12 | Does the privacy policy inform the person: purpose, data, duration, recipients, rights, and does it call stored lines pseudonymous rather than anonymous? |
| 13 | Can the person object from the policy, does the objection last, and are browser signals honoured? (`opt-out-that-lasts.md`, `production-only-and-browser-signals.md`) |
| 14 | Are the features outside the frame switched off: marketing and campaign measurement, acquisition channels, cohorts, session replay, heatmaps, e-commerce, identification of a visitor; referrer reduced to its domain; browser and system reduced to a major version? |
| 15 | Is there no banner because nothing asks for consent, and nothing measured outside production? |

## Campaigns are outside the exemption

Measuring the effect of an advertisement through a campaign name or tag in the
address (`utm_*`, Matomo's `mtm_campaign`), even reduced to the name, is marketing
measurement and is not covered. What remains inside the frame is the number of
visits over time and the domain a visitor came from. Attribution per campaign needs
consent, which means a banner and a different specification. Write this refusal in
the specification, so the question is not reopened by each new advertising idea.

## No cookie is not no tracker

Article 82 of the French data-protection act, the national rule that transposes the
ePrivacy directive, covers any access to, or storage of, information on a person's
device. A tool that stores nothing but computes an identifier from the site's
identifier, the client address, the browser's user agent and a salt behaves like a
fingerprint, and the regulator ranks computing one, like reading local storage,
among the trackers. A measurement without a cookie is therefore still subject to
article 82, and the exemption is what spares it consent.

What the policy says follows:

- **"No cookie"** only where nothing is stored; never "no tracker", and never "no
  data".
- **"Anonymous"** only for the totals the dashboards show. The lines the database
  keeps carry a computed identifier and are **pseudonymous**, and so are the pages
  seen under one identifier, which most tools display. A dashboard source that reads
  lines can show the same; name it in the policy and in the specification as a
  deliberate gap, with who may open it and through what.
- The tool's identifier, its salt and its rotation are described in plain words:
  what goes into the calculation, what changes it, and that one period's identifier
  cannot be linked to the next.

Read the regulator's text again before writing these lines; it prevails.

## Anonymity of unsegmented reports

The self-assessment tool asks for reports rounded to the ten or, failing that, a
written analysis that the data is anonymous. State which one applies, and redo the
analysis when a dimension is added to the reports.

## Worked example: Umami

Umami stores no cookie and no address. It calculates the visitor's identifier from the
site, the address, the user agent and a salt derived from the period and from an
installation secret, and keeps a visit identifier that changes every hour. Settings
that carry the questions above, as read in the documentation and the source of the
version in use (read them again for a new one): telemetry, update checks and external
calls off, the salt rotating monthly, the client-address header and the geolocation
headers pointed at the proxy (`the-proxy-opens-one-route.md`), its own database
(`tool-and-database-apart.md`), the tool's own script never loaded, no `identify`
call, and a daily purge because the tool has no retention setting. The browser keeps
nothing, except for a person who objects: the `umami.disabled` marker in local
storage.

## Worked example: Matomo

Matomo ships a compliance mode for this exemption (from 5.9.0) and the regulator
publishes a configuration guide for it. Typical settings that carry the questions
above: visit log and visitor profile off, IP truncated by two bytes, user-ID plugin
off, e-commerce off, no cookie domain set, `setDoNotTrack(true)`, browser feature
detection disabled, a fixed visitor-cookie lifetime, and no access log of the
collection endpoint on the reverse proxy. Another product answers the same
questions with other settings; the questions do not change.

## Why

A measurement is exempt as a whole or not at all. One feature added for a
convenient figure is enough to take the entire processing back under consent, and
the people who see it first are the ones reading the privacy policy.
