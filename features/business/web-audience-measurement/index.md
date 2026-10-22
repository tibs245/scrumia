# Web audience measurement

**Status**: draft

## In brief

Audience measurement on a web app that stays inside the conditions under which a
data-protection authority exempts it from consent: a closed event catalogue, one module
that owns the tracker, cleaned addresses, nothing outside production, an opposition that
lasts. The plugin that carries it (`scrumia-web-audience`) is generic — Matomo is the
worked example — and its exemption checklist is drawn from the French authority's
published conditions.

## Links

- Implemented by: `plugins/scrumia-web-audience/` — `extends.json` contributes rules to
  the `implement` and `review` registers, and an audit method to `implement`.
- Authority: the French data-protection authority's guidelines and recommendation on
  cookies and other trackers, and its self-assessment tool for an exempt audience
  measurement; named by title in the plugin's README.
- Defers to: `features/business/html-css-and-accessibility/` for the accessibility of
  the opt-out control; this feature states only the status region and the three states.

## Files present

| File | Read it when |
|---|---|
| `business.md` | deciding what the plugin refuses and which conditions it rests on |
| `qa.md` | writing or running the acceptance scenarios |
| `tech.md` | tracing how the plugin contributes to the `implement` and `review` registers |
| `CHANGELOG.md` | history of changes to this spec |

No `legal.md`: the plugin's authority is the regulator's text, which `business.md` names
and the plugin paraphrases; the specification of a project that adopts the plugin is
where the project's own legal file belongs.
