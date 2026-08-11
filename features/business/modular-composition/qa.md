# Acceptance criteria — Modular composition

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — A slot exists independently of any module filling it

```gherkin
Given the seven slots named in `index.md` (`specs`, `tracker`, `team`,
  `discovery`, `implementation`, `practices`, `design`)
When a project has not chosen a module for one of them
Then `plugins/scrumia-core/scripts/compose-status.sh` still reports it rather
  than dropping it: for a project-wide slot, its `SLOTS` list still names the
  slot and the report still prints a row for it, labelled "empty on purpose"
  or "not declared"; for `implementation` or `practices`, which repeat per
  app, the affected app's row in the apps table still prints "none" for that
  column instead of omitting the app or the column
```

### AC-2 — A module fills a slot through configuration, not convention

```gherkin
Given a module's `.claude-plugin/plugin.json` and its own `SKILL.md`
When a project sets `composition.<slot>: <module-name>` in `.scrumia/config.yaml`
  and enables the plugin in `.claude/settings.json`
Then `scrumia-init` names that module for that slot in `CLAUDE.md`'s composition
  table, and agents read the table rather than inferring the slot from which
  plugins happen to be installed
```

## Edge cases

### AC-3 — An empty slot is a declared absence, not an oversight

```gherkin
Given a project that has not adopted a module for a given slot
When `.scrumia/config.yaml` is written or regenerated
Then the slot's key is present with value `null` — never omitted — so a reader
  can tell "not chosen yet" apart from "no key defined for this at all", and
  `CLAUDE.md` names the absence in prose beneath its composition table, which
  lists only the modules actually plugged in
```

The table carries no row for an empty slot on purpose: a row naming an absent
module sends an agent to a skill that does not exist. The declaration BR-2
requires lives in `.scrumia/config.yaml`'s explicit `null`; `CLAUDE.md` states
the same absence in the register a reader acts on — a sentence, not a dead row.

### AC-4 — A skill degrades by a named message when the module it needs is absent

```gherkin
Given a slot's module is absent at runtime — `CLAUDE.md`'s `## Specs contract`
  section (or the equivalent section for another slot) is missing because no
  module is plugged into that slot
When a skill that would consume that slot's capability runs — for example
  `scrumia-ticket` reaching its Step 1, needing the specs contract to load the
  parent feature
Then it states the gap with a specific, named message — "no specs module
  documented — ask the human or proceed without spec updates" — and continues
  the rest of its work in that degraded mode; it does not raise an error, and it
  does not silently guess a file layout that happens to work for one specs
  module
```

### AC-5 — A module is cited by name in prose, never resolved dynamically

```gherkin
Given two modules plugged into different slots that need to interoperate —
  for example the tracker slot's `scrumia-ticket` reading the specs slot's
  acceptance-file vocabulary
When one module's skill needs to reach a capability the other slot owns
Then it names the slot (or the specific module, where the sentence needs it) in
  its own prose, and reads whatever that slot's module documented in `CLAUDE.md`
  — there is no runtime call, verb, or registry that resolves the slot to a
  module on the agent's behalf
```

### AC-6 — A third-party module plugs in without joining the base repo

```gherkin
Given a slot with no ScrumIA-authored module answering a project's need — for
  example a tracker module for a system other than GitHub
When a project or a third party writes that module
Then it ships from its own repository, declared in `marketplace.json` through a
  `github`, `git-subdir`, `npm` or `archive` source instead of a relative path,
  and it still only needs to satisfy the three things any module owes (`SKILL.md`,
  scope, never assume another module is present) to be composable
```

### AC-7 — A module ships the standing role that guards its slot

```gherkin
Given a module filling a slot and providing a standing role for that slot's
  capability, whose definition lives in that module rather than in the team
  module's agents/ directory
When the composition is read to find out which roles are active
Then the role appears in the single settings.team.roles list, carrying a `from:`
  naming its provider, and routing needs no knowledge of where the definition lives
```

### AC-8 — The composition is reported from the file, and the two kinds of absence read differently

Sharpens AC-3: the declaration lives in `.scrumia/config.yaml`, and this is what
a human actually sees of it.

```gherkin
Given a project whose `.scrumia/config.yaml` names a module for some slots, sets
  one slot to `null`, and — as the defect BR-2 describes — omits another slot's
  key entirely
When `scrumia-core/scripts/compose-status.sh` runs, on its own or as the closing
  step of `scrumia-init` or `scrumia-compose`
Then it prints each slot with the module filling it; calls the `null` slot empty
  on purpose and names the module that would fill it; reports the omitted key as
  *not declared* instead, so an oversight never reads as a choice; drops colour
  when stdout is not a terminal or `NO_COLOR` is set to a non-empty value; keeps
  its columns readable in a narrow terminal; takes no argument in a configured
  repo; and writes nothing anywhere
```

The script reports `.scrumia/config.yaml` and stops there. Whether a module named
in it is actually enabled, and whether `CLAUDE.md` still matches, are AC-2's
territory and `scrumia-compose`'s job to diagnose around this output.

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
And the repository's validator fails on any reference whose resolved target
  leaves the module's root, so the rule is enforced rather than remembered
```

A reference that escapes resolves in the repository layout and nowhere else, so
neither a green validator nor a working session in the home repository is evidence
of anything. The layout it has to be checked against is the installed one.

## Out of scope

- **Module versioning and migration on a breaking change** — what a major, minor
  or patch bump means for a project already using a module, how long a renamed thing
  keeps working, and when that project finds out. Specified by
  `features/business/release-versioning/`; this feature only establishes that a module
  exists and can be composed, not how it evolves once adopted.
- **Any single module's own settings or file layout** — each module documents
  what it reads under `settings.<slot>` in its own `SKILL.md`; this feature does
  not duplicate any module's contract, only the shared rule that a contract must
  exist.
