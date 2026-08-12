# Acceptance criteria — Module authoring

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — What authoring produces passes the checker on the first run

```gherkin
Given a need with at least three distinct concerns and no module answering it
When the authoring pass runs to completion
Then the module it produced is accepted by the anatomy checker with no finding, without
  anything being edited between the pass ending and the check running
```

### AC-2 — The location follows the reach of the need

```gherkin
Given a need stated as belonging to this project alone
When the authoring pass decides where the module goes
Then it is created inside the project, and the pass states the reach it inferred so the
  human can contradict it
Given instead a need stated as belonging to anyone running ScrumIA
When the same pass runs
Then a marketplace is the location, and before creating anything the pass states the two
  obligations publishing carries — a version whose bumps `release-versioning` governs, and
  a deprecation window before a renamed thing disappears
```

### AC-3 — Promotion rewrites no file

```gherkin
Given a module created inside a project and since used by a second project
When it is promoted to a shared location
Then its location and the declarations naming it change, the content of every file it
  ships is byte-identical to what it was before, and the checker's verdict is the same
  after as before
```

This is the criterion that keeps the anatomy standard free of a local tier. It fails the
moment promotion needs to touch anything inside the module.

### AC-4 — Demotion is the same move, unceremonious

```gherkin
Given a published module that turns out to serve one project
When it is moved back into that project
Then the move succeeds with no file rewritten, and projects that had adopted it are told
  through the mechanism `features/business/release-versioning/` owns rather than through
  anything this pass invents
```

### AC-5 — Editing runs the same check as creating

```gherkin
Given an existing module that currently passes the checker
When any change is made to it through the authoring pass
Then the checker runs on the result, and a change that introduces a finding is reported
  before the pass reports success
Given instead an existing module that already has findings against it
When the pass opens it for editing
Then the pre-existing findings are surfaced first, and are not silently inherited as
  though the pass had produced them
```

### AC-6 — An edit names the commit signal, and derives no level

```gherkin
Given a change to a module that alters what one of its skills instructs an agent to do
When the authoring pass reports the change
Then it names the type and the scope the commit will carry, and points at
  `features/business/release-versioning/` for what follows from them
And it does not state a level — not "minor", not "major" — because the level is read off
  the commit there, and below `1.0.0` the same word names two different things
```

## Refusals

### AC-7 — A single rule does not become a module

```gherkin
Given a need that amounts to one standing rule
When the authoring pass is asked to create a module for it
Then no module is created, and the pass names the destination that fits, taken from the
  shapes `features/business/local-extension/` lists and chosen through
  `features/business/knowledge-placement/`'s tree — enumerating neither itself
```

### AC-8 — A new slot is refused unless a project would fill it differently

```gherkin
Given a proposed module described as needing a slot of its own
When the pass cannot state a real project that would fill that slot with a different
  module
Then the slot is refused, and the pass offers the two accepted alternatives — one more
  capability in an existing module, or a module filling no slot — rather than creating
  the slot and noting the doubt
```

### AC-9 — The pass writes no placeholder

```gherkin
Given a module whose need touches no register, reads no setting and exposes no script
When the authoring pass produces it
Then no file exists for any of the three, and no file it did write contains a heading
  with nothing under it or a marker to be filled in later
```

### AC-10 — A pass may end having created nothing

```gherkin
Given any input to the authoring pass
When the pass concludes that no module is warranted
Then it reports what it concluded and why, leaves the working tree unchanged, and this
  outcome is reported as a completed pass rather than as a failure
```

An authoring pass that can only succeed by creating a module will always create one.
