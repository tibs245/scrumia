# Web audience measurement — business rules

## Value

For whoever builds a public web app and wants to know how many people visit it, what they
use, and whether they follow a link to the app stores — without a consent banner. It
brings a short list of refusals that keep a measurement inside the authority's exemption,
and a checklist that turns "is this still exempt?" into questions with an answer. It
matters because the exemption is lost silently: one added event, one cookie, one campaign
tag takes the whole processing back under consent while the privacy policy still says
otherwise. Not instrumented today: nothing counts how many measured apps meet every
condition.

## Sources

| Source | What it provides |
|---|---|
| The authority's guidelines and recommendation on cookies and other trackers | The exemption itself, the lifetime and retention figures |
| The authority's self-assessment tool for an audience measurement exempt from consent (July 2025) | The conditions, the excluded features, the anonymity analysis |
| The authority's configuration guide for the product in use | The settings that carry the conditions, for Matomo |

The plugin paraphrases these. A paraphrase that has drifted from the text is rewritten
against the text, and the plugin says the regulator's current text prevails.

## The module's role

- **BR-1** — The module is generic. The product (Matomo) is a worked example and never a
  requirement; no rule names a setting a project cannot map onto another product.
- **BR-2** — What is measured is a closed list. The specification holds the catalogue as
  a table and the code holds it once as a typed constant; an event in the code and not in
  the table is a finding.
- **BR-3** — One module owns the tracker. Pages declare events by attribute; nothing
  outside the module reaches the tracker's queue or names the product.
- **BR-4** — The address sent is the path's template, with no query string and no
  fragment, and the referrer is reduced to its origin.
- **BR-5** — The site identifier is a build-time setting. Empty means nothing is rendered.
  The tracker is not loaded when the browser sends Global Privacy Control or Do Not Track.
- **BR-6** — The person can object from the privacy policy, in three stated states, and
  the objection outlasts the measurement cookie.
- **BR-7** — The exemption conditions are a checklist of closed questions. Campaign
  attribution is outside the exemption and is written as a refusal.
- **BR-8** — The module states which regulator it draws from, and a project under another
  authority replaces the checklist and keeps the structure.

## What the plugin contributes

| Register | Module that opens it | What it carries |
|---|---|---|
| `implement` | `scrumia-github-project` (via `scrumia-ticket`) | five refusals, the checklist, the audit method |
| `review` | `scrumia-github-project` (via `scrumia-review`) | the refusals a diff can break, and the checklist |

## Vocabulary

**"Exemption"** names the authority's allowance to measure without consent when its
conditions hold. **"Catalogue"** names the closed list of events and their values.
**"Template"** names an address with its variable segment replaced by a placeholder.
