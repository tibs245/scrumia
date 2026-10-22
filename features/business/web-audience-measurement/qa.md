# Acceptance criteria — Web audience measurement

One scenario per rule in `business.md`. Each scenario must be able to fail.

## The rules

### AC-1 — An event outside the catalogue is refused

```gherkin
Given a specification whose catalogue table lists `page-view` and `store-click`
And code that sends an event named `hero-hover`
When the audit's first question is answered
Then a finding names the file, the rule (`web-audience-measurement/BR-2`) and that the
  name is not in the specification's table
And a name present in both the table and the typed constant is not a finding
```

### AC-2 — A tracker call outside the measurement module is refused

```gherkin
Given a measurement module directory and a page outside it containing `_paq.push`
When `scripts/detect-direct-tracker-calls.sh --module <dir> <root>` runs
Then it prints that page and exits 3
And with no such page it prints nothing and exits 0
And a missing directory exits 1, and missing arguments exit 2
```

### AC-3 — A raw address sent to the measurement is refused

```gherkin
Given code that lets the tracker read the page's own address, or sends a path with its
  query string
When the audit's third question is answered
Then a finding names the file, the rule (`web-audience-measurement/BR-4`) and which of
  query, fragment, variable segment or full referrer was sent
```

### AC-4 — A site identifier written in source, or a tracker loaded after a browser signal, is refused

```gherkin
Given a literal site identifier in the source, or a tracker loaded although
  `navigator.globalPrivacyControl` is true
When the audit's fourth question is answered
Then a finding names the file and the rule (`web-audience-measurement/BR-5`)
And an empty identifier that renders no script, no configuration and no control is not a
  finding
```

### AC-5 — An opt-out shorter than the measurement cookie is refused

```gherkin
Given a refusal cookie whose lifetime is shorter than the measurement cookie's
When the audit's fifth question is answered
Then a finding names the rule (`web-audience-measurement/BR-6`) and both durations
And a missing control in the privacy policy is a finding of the same rule
```

### AC-6 — The checklist is answered question by question

```gherkin
Given a measured app and the rule `exemption-conditions.md`
When the audit's sixth question is answered
Then each of the fifteen questions is reported yes, no or not verifiable, with the file
  or setting that answered it
And a question about the server is answered from the server's configuration and the
  report says so
And a campaign tag kept from the address is reported as outside the exemption
```

## Plumbing

### AC-7 — The plugin is generic and passes the gate

```gherkin
Given the plugin's tree
When `scrumia-module check plugins/scrumia-web-audience` and `python3 tools/validate.py` run
Then both pass, naming no finding
And no file of the plugin names a project, a repository outside this one, or a ticket
And Matomo appears only as an example, never as a condition of a rule
And the plugin's entry in `site/modules.json` carries an emoji distinct from every other
  module's, with the prose for both `en` and `fr`
```
