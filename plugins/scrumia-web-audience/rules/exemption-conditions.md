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
| 4 | Is the IP address truncated before anything is stored, by at least its last byte? |
| 5 | Is there no cross-referencing with another processing: no user identifier, no account, address or token sent, no import of external data? |
| 6 | Does no log outside the measurement tool record the IP address or the query string of a measurement request, including the web server's access log? |
| 7 | Does no third party receive the data, and is no third-party tool embedded? |
| 8 | Is there no tracking across sites: a cookie bound to the site's own host, no cross-domain linking, no fingerprinting? |
| 9 | Is the tracker's lifetime bounded (the regulator recommends no more than thirteen months) and never extended by a later visit? |
| 10 | Is retention bounded (the regulator accepts at most twenty-five months)? |
| 11 | Are the cookies set exactly the ones the privacy policy lists? |
| 12 | Does the privacy policy inform the person: purpose, data, duration, recipients, rights? |
| 13 | Can the person object from the policy, does the objection last, and are browser signals honoured? (`opt-out-that-lasts.md`, `production-only-and-browser-signals.md`) |
| 14 | Are the features outside the frame switched off: marketing and campaign measurement, acquisition channels, cohorts, session replay, heatmaps, e-commerce; referrer reduced to its domain; browser and system reduced to a major version? |
| 15 | Is there no banner because nothing asks for consent, and nothing measured outside production? |

## Campaigns are outside the exemption

Measuring the effect of an advertisement through a campaign name or tag in the
address (`utm_*`, Matomo's `mtm_campaign`), even reduced to the name, is marketing
measurement and is not covered. What remains inside the frame is the number of
visits over time and the domain a visitor came from. Attribution per campaign needs
consent, which means a banner and a different specification. Write this refusal in
the specification, so the question is not reopened by each new advertising idea.

## Anonymity of unsegmented reports

The self-assessment tool asks for reports rounded to the ten or, failing that, a
written analysis that the data is anonymous. State which one applies, and redo the
analysis when a dimension is added to the reports.

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
