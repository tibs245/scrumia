# Review guard-rails: business

Read `business.md` against this list before opening any other file of the feature.
Each line names a defect as it actually appears — if you recognise the shape, the
file needs work.

## The value

- **`## Value` describes how the feature works instead of what it brings and to
  whom.** The most frequent defect by a wide margin, and the easiest to miss
  because the text reads competently. Tell: the section can be summarised as "it
  does X" rather than "so that Y stops happening to Z". A sentence whose subject
  is the system, not a person, is the tell in one word.
- The audience is "the user", "the team", "everyone" — a placeholder, not a role.
- The gain is asserted without a loss it repairs: nothing goes wrong today if the
  feature never ships, and the section does not admit it.
- A measure is promised but not named, or a metric is invented that nothing in the
  project collects. "Not instrumented today" is a correct answer; a fabricated
  KPI is not.
- The value is stated for the whole EPIC in an App feature, instead of this app's
  share of it.

## The rules

- A rule is justified by a technical choice — "because the API returns 404" — when
  the promise it constrains would survive a change of tool.
- A rule that is not settled is written as if it were. Look for confident present
  tense on a question nobody has answered: it should read as an open question.
- The same rule appears here and in another feature, worded differently. Two
  authorities on one rule is the defect that surfaces months later as two
  behaviours.
- An App feature restates a rule its Business parent already states, instead of
  referencing it.
- An invariant is stated as a preference — "should", "ideally", "as much as
  possible". An invariant either always holds or is not one.

## The journey

- A step names a screen, a button, a field, a click path, a URL. Any of these
  moves the step to `ux.md`; what stays here is the intent it served.
- The journey is a sequence of system operations rather than actor intentions.
- A step exists that no persona listed above performs.

## Boundaries and hygiene

- A Given/When/Then scenario is written here rather than in `qa.md`.
- A schema, a payload, a field list another feature consumes appears here rather
  than in `api-contract.md`.
- A dependency, a library, a structural choice appears here rather than in
  `tech.md`.
- A ticket, issue or PR number appears anywhere in the file. Only `CHANGELOG.md`
  cites issues.
- History appears: "formerly", "since v2", "we used to", a struck-through
  paragraph, or a past-tense sentence explaining why a rule changed. The current
  rule alone belongs here; the why is in the issue.
- The vocabulary section defines a term that a neighbouring feature already
  defines differently, without either of them noticing.
- The file is over ~200 lines. Not a defect on its own — a signal to check the
  splitting criterion before it becomes one.
