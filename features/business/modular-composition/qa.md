# Acceptance criteria — Modular composition

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — An action's requirement exists independently of any module providing it

```gherkin
Given a project's declared steps and the actions they require
When no module has been configured to provide one of those actions
Then the action still exists as a requirement — asking "who provides this" stays a
  valid, answerable question, and nothing in the mechanism treats an unprovided
  action as though the requirement itself had disappeared
```

This asserts BR-1 at its own level of abstraction. What `compose-status.sh` actually
prints for an unprovided action is AC-8's territory, not this one's — coupling this
criterion to one script's exact output is the coupling defect this rewrite avoids
reintroducing.

### AC-2 — Coverage is derived from declared actions, counted by caller, not asserted

```gherkin
Given a module that declares it provides an action for a project's declared step
When nothing in the composed project actually reaches that module by name for that
  action
Then a coverage report names the action a hole — declared but uncalled — rather than
  counting it covered on the strength of the declaration alone
```

### AC-3 — A decision action has exactly one provider; a contribution action may have several

```gherkin
Given two modules both declaring the same action for the same step
When that action is a decision (BR-8) — moving a card, picking a model, settling a
  business rule
Then the composition reports a conflict at composition time, naming both modules,
  rather than picking one silently or letting `extends`'s list order arbitrate
Given the same situation
When that action is a contribution (BR-8) — reviewing a PR, applying a practice to a
  Build
Then both modules are accepted as legitimate providers and neither is reported as a
  conflict
```

### AC-4 — Three absence states report distinctly

```gherkin
Given a project's declared steps
When an action for one step has no module configured at all, another is explicitly
  `not-applicable`, and a third is explicitly `human`
Then a coverage report counts the first as a hole, excludes the second from the
  coverage denominator entirely, and counts the third as covered — the same input
  producing three different arithmetic outcomes rather than one absence reading as
  every other
```

### AC-5 — A coverage claim names the one recipient set it measures

```gherkin
Given the four recipient sets (run, kernel, adoption, authoring)
When a coverage report is produced
Then it states which set the numbers describe, and a claim covering `run` never
  presents its ratio as though it accounted for `kernel`, `adoption` or `authoring`
  as well
```

## Edge cases

### AC-6 — `practices` is declared per app, not project-wide

```gherkin
Given a monorepo with two apps, one needing TDD applied to its Build and one not
When each app declares its own `extends` list under `apps:`
Then the app that lists `scrumia-practice-tdd` gets it applied to its Build, the app
  that does not list it gets none, and no project-level `extends` entry can apply a
  practice module to an app that did not declare it
```

### AC-7 — Specific beats generic; a project override beats both

```gherkin
Given an implementation module and a practice module that contradict each other for
  the same app — the practice recommends a pattern the implementation module refuses
When an agent applies either while coding in that app
Then the implementation module's answer wins, and if the project has written
  `.scrumia/impl/<module>.md` or `.scrumia/practices/<module>.md` for the contested
  point, the project override wins over both
```

### AC-8 — An unprovided action is a declared absence, not an oversight

```gherkin
Given a project whose composition leaves some declared step's action without a
  provider
When `.scrumia/config.yaml` is written or regenerated
Then the gap is reported explicitly — never by a silently absent line — so a reader
  can tell "no provider yet" apart from "no report was ever run", and
  `scrumia-core/scripts/compose-status.sh` prints each declared step's actions with
  their provider, their absence state (missing / `not-applicable` / `human`), and
  drops colour when stdout is not a terminal or `NO_COLOR` is set to a non-empty
  value
```

### AC-9 — A module's references resolve inside it, in either layout

```gherkin
Given a module whose installed root carries a version segment the repository
  layout does not, and which needs a script another module ships, plus a
  rationale belonging to no module at all
When every reference it writes is resolved from its own root — the
  `${CLAUDE_SKILL_DIR}` paths in its skills and the relative links in its
  markdown
Then each one lands inside that root: the other module's script is reached by
  running the name that module publishes on PATH, with no path held by the
  caller, and the rationale is inlined or cited by absolute URL
```

A reference that escapes resolves in the repository layout and nowhere else, so
neither a green validator nor a working session in the home repository is evidence
of anything. The layout it has to be checked against is the installed one.

### AC-10 — A skill degrades by a named message when the action it needs is unprovided

```gherkin
Given an action a skill would consume has no provider in the current composition —
  for example `scrumia-ticket` reaching its Step 1, needing the specs contract an
  action nobody provides
When that skill runs
Then it states the gap with a specific, named message — "no specs module documented
  — ask the human or proceed without spec updates" — and continues the rest of its
  work in that degraded mode; it does not raise an error, and it does not silently
  guess a file layout that happens to work for one module
```

### AC-11 — A module is cited by name the harness resolves, never by a path

```gherkin
Given two modules that need to interoperate — for example the tracker's ticket skill
  reading the specs module's acceptance-file vocabulary
When one module's skill reaches a capability the other provides
Then it names the other module in its own prose, in a form the harness resolves —
  never a relative path — and reads whatever that module documented in `CLAUDE.md`;
  there is no runtime call, verb, or registry that resolves the name to a module on
  the agent's behalf
```

A module reaching another by a relative path cannot be counted as a real edge by the
coverage calculation AC-2 depends on — this criterion is what makes AC-2 measurable,
not a separate concern from it.

### AC-12 — A third-party module plugs in without joining the base repo

```gherkin
Given no ScrumIA-authored module answers a project's need for some action — for
  example a tracker action for a system other than GitHub
When a project or a third party writes that module
Then it ships from its own repository, declared in `marketplace.json` through a
  `github`, `git-subdir`, `npm` or `archive` source instead of a relative path, and
  it still only needs to satisfy the three things any module owes (`SKILL.md`, the
  actions it provides, never assume another module is present) to be composable —
  the two things a module owes to join an assembly (`composition.json`, a
  `<module>-manifest` on its own `bin/`) are a separate list, and a module that ships
  neither is composable and contributes to no assembly
```

The two lists are separate because they answer to different tests. The first admits an
item only when skipping it breaks silently; a missing manifest is said out loud, so it
cannot join that list without weakening what membership in it means.

### AC-13 — A module ships the standing role that guards its capability

```gherkin
Given a module providing a capability and shipping the standing role that guards it,
  whose definition lives in that module rather than in the team module's agents
  directory
When the composition is read to find out which roles are active
Then the role appears in the single `settings.team.roles` list, carrying a `from:`
  naming its provider, and routing needs no knowledge of where the definition lives
```

### AC-14 — What an agent loads is assembled from declarations, not recomposed from prose

```gherkin
Given a project whose `extends` names several modules, at least two of which provide
  the same contribution action
When `scrumia-assemble build` runs
Then it writes one assembly per provided action, each naming every contributing module,
  the entry fragment to open inside it, and the name a person types to reach it — and
  the contributors are ordered by a rule the file states rather than by the order they
  appear in `extends`: project-local before app-level before project-wide, `technology`
  grain before `cross-cutting` within a tier, alphabetical within that
```

The order is stated in the artefact, not only applied to it: an order a reader cannot
check is one that can invert without anything failing.

### AC-15 — An assembly names a module and an inner path, never a machine's path

```gherkin
Given a built assembly that points at a file another module ships
When the artefact is committed and read on a different machine, or by CI
Then every fragment it names is a module name plus a path inside that module, and the
  file contains no absolute path and no harness variable — while
  `scrumia-assemble load <action>` resolves those pairs to real paths when it prints
```

### AC-16 — A module named in `extends` that cannot be reached stops the build

```gherkin
Given a project whose `extends` names a module whose `<module>-manifest` is not
  resolvable — the plugin is enabled but the session has not been restarted
When `scrumia-assemble build` runs
Then it fails, naming the module and the restart rule, and writes no assembly for the
  actions that module would have provided; a module that is reachable but ships no
  `composition.json` is reported as contributing nothing instead, by name
```

The two cases must not collapse into one. An empty assembly written because a name was
missing is well-formed, commits cleanly, passes CI, and tells every later agent that no
rules apply — which is the failure this criterion exists to catch.

### AC-17 — A built assembly is read, never recomputed, and says when it is stale

```gherkin
Given a project whose assemblies were built, and whose `.scrumia/config.yaml` has since
  changed
When `scrumia-assemble load <action>` runs
Then it refuses, naming the rebuild command, instead of printing either a stale answer
  or a freshly computed one; and when nothing has changed it prints the built file
  without consulting any module
```

A plugin version bump does not make an assembly stale: the artefact holds routing, not
prose, so a rewritten guide leaves it correct. A fragment that stops existing is caught by
`scrumia-assemble check` and by the missing file itself, never by wrong prose.

### AC-18 — An entry point changes the remedy, not the count

```gherkin
Given an action a plugged module provides, that no other module calls, and that a
  person can invoke by a slash command
When coverage is reported
Then the action still counts as a hole, and the row names the skill or command a person
  types — resolved to a file that exists — so the remedy offered is that invocation
  rather than "plug a module that provides it"
```

## Out of scope

- **Module versioning and migration on a breaking change** — what a major, minor or
  patch bump means for a project already using a module, how long a renamed thing
  keeps working, and when that project finds out. Specified by
  `features/business/release-versioning/`; this feature only establishes that a module
  exists and can be composed, not how it evolves once adopted.
- **Any single module's own settings or file layout** — each module documents what it
  reads under its own settings key in its own `SKILL.md`; this feature does not
  duplicate any module's contract, only the shared rule that a contract must exist.
- **The `x-<module>/<action>` opaque-prefix escape hatch for third-party action names**
  — reserved, not adopted, by `docs/adr/0019-extends-replaces-composition-and-practices.md`.
  No acceptance criterion exists for a mechanism this feature does not yet implement.
