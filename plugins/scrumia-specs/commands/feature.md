---
description: Create, update or audit a feature in the specs root — applying the contextual file catalog rather than a fixed template.
argument-hint: <feature name or what to specify>
---

Load the `scrumia-feature` skill and follow it.

$ARGUMENTS

The argument names the feature, or describes what needs specifying. Ask if it is unclear which feature is meant: writing a rule into the wrong feature is the defect that costs the most later, because two features then define the same rule differently.

Beyond `index.md`, `qa.md`, `CHANGELOG.md` and `business.md`, which this module requires of every feature — the last because every feature states its value — write the file the content calls for and no more. An absent optional file is information — it says the question does not arise — while an empty one says nobody looked.

Each file is one angle's output, and each angle ships its own activation questions, template and review guard-rails. Answer the questions rather than deciding by feel, and report at the end which angles you declined and on which answer — an absence nobody can see was considered asserts nothing.

A spec holds only its current version. History lives in git and in the tickets, and a spec cites no ticket — the changelog is the one file that points at them.
