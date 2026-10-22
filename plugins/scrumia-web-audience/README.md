# scrumia-web-audience

Audience measurement for a web app that wants figures without asking visitors for
consent. It keeps the measurement inside the conditions a data-protection authority
sets for that exemption: a closed list of events, one module that owns the tracker,
addresses cleaned before they leave, nothing outside production, and an opposition
that lasts. Matomo is the worked example; no rule requires it.

## What it answers

How a web app measures its audience, and goes on changing that measurement, without
drifting out of the exemption one reasonable event at a time. Five refusals mark the
seams where it drifts, and a checklist of the exemption conditions turns "is this
still exempt?" into questions with a yes or a no.

## What it refuses

- An event name the specification does not list.
- A page, component or script that calls the tracker itself, or names the product.
- The page's real address sent to the measurement: query string, fragment, a token or
  a code in the path.
- A measurement that runs outside production, or loads after the browser said no.
- An opt-out that is missing, hidden outside the privacy policy, or shorter-lived
  than the measurement it refuses.
- Campaign attribution presented as exempt. It is marketing measurement and needs consent.

## What it ships

| What | Role |
|---|---|
| `rules/closed-event-catalogue.md` | The events are a table in the specification and a typed constant in the code. |
| `rules/one-module-declarative-markup.md` | One module owns the tracker; pages declare events by attribute. |
| `rules/cleaned-addresses.md` | The path template, no query, no fragment, the referrer as an origin. |
| `rules/production-only-and-browser-signals.md` | Build-time site identifier, empty means nothing, signals honoured. |
| `rules/opt-out-that-lasts.md` | The control, its three states, the cookie that outlasts. |
| `rules/exemption-conditions.md` | Fifteen conditions as closed questions, and what lies outside. |
| `web-audience-audit` (skill) | Six questions, one per rule, for an app that already measures. |
| `scripts/detect-direct-tracker-calls.sh` | Lists files outside the module that mention the tracker queue. |

The rules reach the `implement` and `review` registers through `extends.json`.

## Sources

The exemption conditions are paraphrased from the French data-protection authority
(CNIL): the guidelines and the recommendation on cookies and other trackers, the
self-assessment tool for an audience measurement exempt from consent (July 2025), and
the configuration guide it publishes for Matomo. They are read on cnil.fr, and the
paraphrase does not replace them: the regulator's current text prevails. A project
outside France takes the module's structure and replaces the checklist with its own
authority's conditions.

## What it expects to find

A web app with a build step that can read a build-time setting, a privacy policy page
the app controls, and a specification where the event catalogue can live. The rules
are about where things sit, not about which framework surrounds them.

## Not shipped yet

The checklist is a paraphrase kept by hand; nothing compares it with the regulator's
text. The detector reads text, so a tracker called through an alias is not found.
