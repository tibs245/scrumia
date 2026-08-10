---
description: Create, update or audit a feature in the specs root — applying the contextual file catalog rather than a fixed template.
argument-hint: <feature name or what to specify>
---

Load the `scrumia-feature` skill and follow it.

$ARGUMENTS

The argument names the feature, or describes what needs specifying. Ask if it is unclear which feature is meant: writing a rule into the wrong feature is the defect that costs the most later, because two features then define the same rule differently.

Beyond `index.md`, `qa.md`, `CHANGELOG.md` and `business.md`, which this module requires of every feature — the last because every feature states its value — write the file the content calls for and no more. An absent optional file is information — it says the question does not arise — while an empty one says nobody looked.

A spec holds only its current version. History lives in git and in the tickets, and a spec cites no ticket — the changelog is the one file that points at them.
