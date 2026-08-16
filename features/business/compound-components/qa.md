# Acceptance criteria — Compound components

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Context over prop chains

### AC-1 — Children reach the parent through context, not props

```gherkin
Given a compound component whose children receive parent state through a
  prop chain of three or more levels
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`compound-components/BR-1`), and
  one line of what was not met — that context (or its framework equivalent)
  is the medium for parent-child state in a compound
And a chain of two levels is not subject to this rule; the threshold is
  the third
```

## Co-location

### AC-2 — Sub-components are co-located with the parent

```gherkin
Given a compound component `<Tabs>` whose `<Tab>` child is exported from a
  separate module path (a different file, a different directory, or a
  separate `index.ts`)
When the plugin's `implement` register contribution runs against it
Then a finding names the file, the rule (`compound-components/BR-2`), and
  one line of what was not met — that the public API is the parent, and
  its parts travel with it
```

## Framework coverage

### AC-3 — Documentation covers at least three of four frameworks

```gherkin
Given the plugin's documentation directory
When it is read for framework coverage
Then at least three of {React, Vue, Solid, Angular} are covered, each with
  an example in that framework's idiom, and the same principle stated
  in each
And a doc covering fewer than three frameworks is refused; coverage of one
  framework under four names does not satisfy it
```

## Sources

### AC-4 — The plugin cites patterns.dev

```gherkin
Given the plugin's README
When it is read for the pattern citation
Then `https://www.patterns.dev/react/compound-pattern/` is present
And a citation missing the URL is a finding
```

## Plumbing

### AC-5 — The plugin composes and passes the marketplace gate

```gherkin
Given the plugin's tree, with its `extends.json` declaring contributions to
  the `implement` register only
When `python3 tools/validate.py` runs from the repository root
Then the gate passes, naming the plugin once in its listing
And the plugin contributes no directive to the `review` register — the
  review register's table, printed by `scrumia-extends`, shows the plugin
  nowhere under `review`
And the plugin's entry in `site/modules.json` carries an emoji distinct
  from every other module's, and the i18n files for both `en` and `fr`
  carry the prose the marketplace page reads
```
