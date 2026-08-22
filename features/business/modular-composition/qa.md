# Acceptance criteria — Modular composition

One scenario per rule in `business.md`. Each scenario must be able to fail.

## Nominal

### AC-1 — A register nothing extends yields an answer, not a failure

```gherkin
Given a main skill that opens a register, in a project whose modules contribute
  nothing to it
When the skill asks for that register's directives
Then it receives an empty table, stated as such — no module the project runs speaks to
  this — and continues on its own criteria; it does not error, and nothing treats the
  absence as though the extension point had ceased to exist
```

This asserts BR-1 at its own level. What the empty table looks like on screen is the
tool's business; coupling this criterion to one script's exact wording is the coupling
defect this file exists to avoid.

### AC-2 — A module installed but named in no `extends` contributes nothing

```gherkin
Given a project with a module enabled in the harness and absent from every `extends`
  list, project-wide and per app
When any register that module contributes to is asked for
Then none of its directives appear, and the module is neither an error nor a warning —
  presence on disk is not participation
```

### AC-3 — A register is opened by exactly one main skill

```gherkin
Given two installed modules that both open the same register
When the composition is checked
Then the conflict is reported, naming both modules and the register, rather than one
  being picked silently or `extends`'s list order deciding
Given instead several modules contributing directives to one register
When the same check runs
Then all of them are accepted, because a register has as many contributors as the
  project runs and only one skill that consumes it
```

### AC-4 — A contribution names no consumer

```gherkin
Given a cross-cutting module contributing a principle that implementation, review and
  audit all need
When its contribution is written
Then it names the register and nothing else — no skill name, no module name, no
  condition about who is asking — and the same fragment is reachable from all three
  registers without being restated, so adding a new implementation module requires no
  edit to this one
```

### AC-5 — The directive table is rendered from data, in a stated order

```gherkin
Given a project whose composition has an app extending two modules, project-wide
  modules contributing to the same register, and a project-local `.scrumia/extends.json`
When the directives for that register are asked for, for that app
Then every contribution appears exactly once, carrying its name, its type, whether it
  is required, one line of what it says and the file to open — ordered project-local
  first, then the app's own modules, then the project-wide ones, required before
  optional within a tier — and the order rule is stated alongside the table rather than
  only applied to it
```

An order a reader cannot check is one that can invert without anything failing.

### AC-6 — Nothing is stored, so nothing can be stale

```gherkin
Given a project whose directive table was consulted, and whose composition has since
  changed — a module added to `extends`, or a module's own contributions edited
When the table is asked for again
Then it reflects the change immediately, with no build step, no artefact in the
  repository to regenerate, and no staleness to detect or refuse
```

## Edge cases

### AC-7 — An app's own module is declared per app, not project-wide

```gherkin
Given a monorepo with two apps, one needing TDD applied and one not
When each app declares its own `extends` list under `apps:`
Then the app that lists `scrumia-tdd` receives its directives, the app that
  does not receives none, and no project-level entry can apply a module to an app that
  did not declare it
```

### AC-8 — Specific beats generic; a project override beats both

```gherkin
Given an implementation module and a module refining it contributing to the same register
  for the same app, and a project that has written its own row for the contested point
When the directives are asked for
Then the project's own row is printed first, then the app's modules, then the
  project-wide ones — and no module has declared any ranking of itself against another
```

### AC-9 — A module's references resolve inside it, in either layout

```gherkin
Given a module whose installed root carries a version segment the repository
  layout does not, and which needs a script another module ships, plus a
  rationale belonging to no module at all
When every reference it writes is resolved from its own root — the
  `${CLAUDE_SKILL_DIR}` paths in its skills, the relative links in its markdown, and
  the fragment paths in its contributions
Then each one lands inside that root: the other module's script is reached by
  running the name that module publishes on PATH, with no path held by the
  caller, and the rationale is inlined or cited by absolute URL
```

A reference that escapes resolves in the repository layout and nowhere else, so
neither a green validator nor a working session in the home repository is evidence
of anything. The layout it has to be checked against is the installed one.

### AC-10 — A skill degrades by a named message when what it needs is absent

```gherkin
Given a capability a skill would consume with nothing providing it in the current
  composition — for example `scrumia-ticket` needing the specs contract when no specs
  module is documented
When that skill runs
Then it states the gap with a specific, named message — "no specs module documented
  — ask the human or proceed without spec updates" — and continues the rest of its
  work in that degraded mode; it does not raise an error, and it does not silently
  guess a file layout that happens to work for one module
Given instead the absent capability is the resolver the module's own configuration passes
  through
Then AC-19 governs and there is no degraded mode: the skill has no configuration to run
  the rest of its work on, so it stops
```

The exception is narrow on purpose. A skill missing a *collaborator* still knows what it
was configured to do; a skill missing the resolution of its own configuration knows
nothing, and every step it took anyway would be well-formed.

### AC-11 — A declared edge that nothing satisfies is reported by name

```gherkin
Given a module declaring the published names it runs, and opening one or more registers
When one of those names is provided by no installed module — the commonest cause being
  a plugin enabled without a session restart — or the module contributes to a register
  nobody opens, or it opens a register no skill of its own ever asks for
Then the check names each case and fails, and the absence is never read as "this module
  contributes nothing"
```

The three cases must not collapse. An absent name silently read as "no rules apply" is
well-formed, passes every gate, and tells every later agent that nothing governs the
work — which is the failure this criterion exists to catch.

### AC-12 — A name is depended on with its source, and the source is checked

```gherkin
Given two marketplaces whose modules both publish an executable of the same name, and a
  module that declares running that name qualified by the source it expects
When the composition is checked
Then the name is resolved to the module that actually publishes it, that module's own
  declared source is compared against the one claimed, and a mismatch is reported as a
  different command wearing the same name
Given the publishing module declares no source of its own
Then the check reports the claim as unverifiable, never as satisfied
Given a declaration that carries no source at all
Then this repository's own validator refuses it, while a consuming project's check
  reports it and continues — an author's laxness does not block someone else's project
```

The qualification is a claim, checked. What a skill invokes stays the bare name: a check
that resolved a source in order to decide what to run would be the capability registry
arriving through the back door.

### AC-13 — A module is cited by name the harness resolves, never by a path

```gherkin
Given two modules that need to interoperate — for example the tracker's ticket skill
  reading the specs module's acceptance-file vocabulary
When one module's skill reaches a capability the other provides
Then it names the other module in its own prose, in a form the harness resolves —
  never a relative path — and there is no runtime call, verb, or registry that
  resolves the name to a module on the agent's behalf
```

### AC-14 — The table arbitrates nothing

```gherkin
Given two modules whose directives, in prose, contradict each other on the same point
When both are printed for the same register
Then both rows appear, in the computed order, with nothing dropped and nothing marked
  as superseded — and resolving the contradiction is left to the person composing the
  project, because a generator does not read English
```

### AC-15 — A third-party module plugs in without joining the base repo

```gherkin
Given no ScrumIA-authored module answers a project's need
When a project or a third party writes that module
Then it ships from its own repository, declared in `marketplace.json` through a
  `github`, `git-subdir`, `npm` or `archive` source instead of a relative path; it may
  open a register no ScrumIA module had; and it only needs the three things any module
  owes (`SKILL.md`, never assume another module is present, every reference resolves
  inside itself) to be composable — the extension data files are a separate list, and a
  module that ships none is composable and contributes nothing
```

The two lists answer to different tests. The first admits an item only when skipping it
breaks silently; a module that contributes nothing is reported by name, so it cannot join
that list without weakening what membership in it means.

### AC-16 — A module ships the standing role that guards its capability

```gherkin
Given a module providing a capability and shipping the standing role that guards it,
  whose definition lives in that module rather than in the team module's agents
  directory
When the composition is read to find out which roles are active
Then the role appears in the single `settings.team.roles` list, carrying a `from:`
  naming its provider, and routing needs no knowledge of where the definition lives
```

### AC-17 — A module is declared by source, and a bare name is not a declaration

```gherkin
Given a project declaring one module from a marketplace, one from a shared checkout and
  one from inside the project
When the composition is read
Then each is keyed `<source>:<module>`, each resolves from the location its source names,
  and the location reported for it is the one in its key
Given instead a configuration carrying a bare module name with no source
When the same read runs
Then it is reported as not a declaration, naming the key, rather than resolved against
  whichever module of that name happens to be installed
Given a configuration being written or migrated, carrying names with no source
When each name is sourced
Then the source comes from what establishes the module — the repository its own manifest
  claims, the project's module directory, or the shared tier that resolves it — and not
  from the marketplace it was installed through
Given instead a name nothing establishes, or one several tiers answer at once
When the same write runs
Then it is reported, naming the name and what answered, and left out of the written file,
  while every name that could be sourced is written
```

A bare name means one thing under `modules:` and another in the retired list shape, and
the migration turns on the difference; `business.md` § `modules` states it, and
`features/business/local-extension/`'s AC-11 governs the shadow it produces.

### AC-18 — A setting resolves through three layers, and reaches the module that reads it

```gherkin
Given a key present in `settings:`, overridden in a module's `params:`, and overridden
  again in the project's local layer
When the module reads it
Then the local layer's value wins, then the module's, then the base — and the order is
  stated where the layers are, not only applied
Given instead a key several modules write, present only in `settings:`
When each of them reads it
Then all of them see it, and nothing requires it to be moved inside one module's block
Given a module that opens `.scrumia/config.yaml` and reads `settings:` for itself
When the same key is overridden in layer 2 or layer 3
Then that module resolves the base value and neither override reaches it — the layers
  are consumed through the cascade, or they are decoration
```

### AC-19 — A module that cannot resolve its configuration says so, instead of defaulting

```gherkin
Given a module whose configuration cannot be resolved — the resolver is not reachable,
  it fails, or no layer carries the block that module reads
When the module runs
Then it names what it could not resolve and for which module, proposes the next step, and
  stops
And it does not fall back to its own built-in defaults, because an answer computed from
  defaults is indistinguishable from an answer computed from configuration — the caller
  cannot tell that the setting was never read, and neither can the person reading the
  output afterwards
Given instead a command whose whole purpose is to diagnose the composition
When the same configuration cannot be resolved
Then it reports the failure as one of its checks rather than stopping — a diagnostic that
  cannot run when the composition is broken diagnoses nothing
```

The two failures are not symmetric, and the asymmetry is the point. A consumer that dies
on a migrated key is fixed the day the migration lands; a consumer that quietly substitutes
its defaults keeps producing well-formed answers nobody has reason to doubt.

### AC-20 — Across the layers, the layer decides and the shape never does

```gherkin
Given one layer carrying a module's key under the retired `settings.<slot>` nest and
  another layer carrying the same key in the current shape
When the module reads it
Then the later layer answers whichever shape it wrote the key in
Given instead one layer carrying that key in both shapes at once
When the same read runs
Then the current shape wins, key by key, and the retired nest answers only for what the
  current shape does not carry
Given a module naming a retired nest that no layer carries
When the same read runs
Then the configuration resolves, carrying nothing on that nest's account — a project whose
  migration is finished is not a project whose modules stop resolving
```

### AC-21 — A key written with no value is an absence, at any depth

```gherkin
Given a key written bare in one layer, over a layer that carries a value for it
When the module reads it
Then the layer beneath answers, whether the bare key sits at the top of the block or
  inside one — a key written bare is a key not yet migrated, never a value
Given a layer whose every key is written bare
When the same read runs
Then that layer is not named among the layers that answered — naming a layer whose value
  is discarded is worse than naming none, on the one output whose whole job is to make the
  cascade checkable
Given a table a module reads by cell, one cell written bare in the layer above the one
  carrying the table
When the module reads that cell
Then the lower layer's cell answers, so a table has a hole where a layer leaves the cell
  out and never where a layer writes it empty — the two look alike in a file and mean
  opposite things
```

### AC-22 — A declared module absent from the runtime is reported by name

```gherkin
Given a project whose composition declares a module under `modules:` whose
  `<source>:<module>` key is not present in `claude plugin list --json`'s output —
  the entry is missing, `enabled: false`, scoped to another `projectPath`, or its
  `installPath` does not resolve on disk
When `compose-status.sh` runs
Then a one-line note naming the declared module, the source that should provide it,
  and the install command is emitted to stderr, and stdout is unchanged for any caller
  that gates on it
```

AC-22 covers the module itself; AC-11 covers a module that is present but whose declared
dependencies are unmet. The runtime read is what BR-6 admits: a declaration can name a
module whose install is absent, and nothing else surfaces the gap. The four signals are
read separately because each is a different failure mode — the predicate is in BR-6's
amendment and `scrumia-core`'s `compose-status.sh` is the kernel-level executor.

### AC-23 — A plugin citing its own home-repo's `features/` restates the operative rule inline

```gherkin
Given a plugin whose installed root is no longer its home-repo, and which cites a
  `features/` rule owned by its own home-repo — a document the plugin owns in
  source but not at install time, because the consumer's `scrumia-specs` instance
  ships its own `features/` with the same path shape and content that may differ
  under the same name
When the citation is read in a consumer's installation, in a session that has
  resolved neither the plugin's home-repo nor any plugin named for its `features/`
Then the plugin's own prose restates the operative rule inline, in a form a reader
  can apply without following the link; the citation is then a provenance pointer,
  not a load-bearing reference, and the reader's session is not asked to mediate
Given instead the reader is in the plugin's own home-repo, where the cited link
  resolves to the rule it was written against
When the same citation is read from there
Then the restate-inline form still holds — the operative rule restated inline is
  the same rule regardless of which installation the reader is in, so the inline
  statement and the cited content agree rather than relying on the reader's
  installation to mediate
```

The third case is narrower than BR-7's second bullet because the cited document
*is* the plugin's own rule in source — and that is exactly why the citation must
not be load-bearing. The wording is grounded on **text** (the consumer's
`scrumia-specs` ships its own `features/` with the same path shape and content
that may differ), not on path resolution: a load-bearing citation would resolve
to whichever instance the runtime sees, and the reader's installation would
mediate a rule it was never asked to mediate. The second scenario pins the
restate-inline obligation as not optional: the home-repo's installation is the
easiest reader for the inline statement to look redundant in, and the easiest for
it to be silently dropped from — exactly the failure the clause exists to forbid.

## The scrumia-kotlin-multiplatform-mobile lane

The Kotlin Multiplatform Mobile composition preset re-exports six satellites by
configuration. Its ACs are scoped to the lane so a reviewer reading the preset's
own rules can fail each one against the composition mechanism this feature
states.

### KMM-AC-1 — Declaring the preset reaches the pivot's rows alongside the satellites'

```gherkin
Given a project that declares
  `tibs245/scrumia:scrumia-kotlin-multiplatform-mobile` in `.scrumia/config.yaml`
  along with the six satellites (`scrumia-kotlin`, `scrumia-gradle`,
  `scrumia-ktor`, `scrumia-material3`, `scrumia-effect`,
  `scrumia-functional-programming`)
When `scrumia-extends implement` is run
Then the table prints the pivot's six rows in the project's own scope tier,
  followed by each satellite's rows in the order the project declared them, and
  the pivot's rows are not restatements of the satellites' rows
```

### KMM-AC-2 — The satellites work without the pivot

```gherkin
Given a project that declares only the six satellites (no
  `scrumia-kotlin-multiplatform-mobile`)
When `scrumia-extends implement` is run
Then the table prints each satellite's rows unchanged, the pivot's rows do not
  appear, and the pivot is not a prerequisite for any satellite
```

### KMM-AC-3 — The pivot duplicates no satellite's rule

```gherkin
Given the pivot's `extends.json` and each satellite's `extends.json`
When a reviewer reads them side by side, line by line
Then no rule in the pivot's `extends.json` restates a rule owned by a satellite —
  a Kotlin language rule belongs to `scrumia-kotlin`, a Gradle-the-tool rule
  belongs to `scrumia-gradle`, an HTTP rule belongs to `scrumia-ktor`, a UI
  rule belongs to `scrumia-material3`, an effect rule belongs to `scrumia-effect`,
  a paradigm rule belongs to `scrumia-functional-programming` — and any
  overlap is a finding
```

### KMM-AC-4 — The pivot lands and merges independently of the satellites

```gherkin
Given the pivot's own tree (`SKILL.md`, `extends.json`, `README.md`,
  `CHANGELOG.md`, `rules/`, the lane in `features/business/modular-composition/`)
When a reviewer greps the pivot's own code, docs, tests and fragments for any
  "X must be present" wording naming a satellite
Then no such wording is found — every rule is reachable without the pivot
  requiring a satellite to be active, including any wording in prose, in code,
  in tests, and in the fragments the rules resolve to
```

### KMM-AC-5 — The pivot contributes to the right registers and opens none named `init`

```gherkin
Given the pivot's `extends.json` and `scrumia-extends --list` before the pivot lands
When the pivot lands and `scrumia-extends --list` runs again
Then the pivot contributes rows to the `implement`, `review` and `find-spec`
  registers, the pivot does not open a register named `init`, and the list of
  register names is unchanged — the pivot adds no register and removes none
```

### KMM-AC-6 — Every fragment path resolves inside the pivot

```gherkin
Given the pivot's `extends.json`
When a reviewer reads each `read` path the pivot declares
Then every path resolves inside `plugins/scrumia-kotlin-multiplatform-mobile/`,
  no path climbs out of the module, and `tools/validate.py` exits clean
```

### KMM-AC-7 — The six KMP-specific rule families are all present, named and typed

```gherkin
Given the pivot's `extends.json` and the rules in `rules/`
When a reviewer reads the rule families the issue names — expect/actual across
  source sets, source-set layout (commonMain, androidMain, iosMain, JVM desktop),
  iOS/Android split (platform-specific tests and dependencies per target),
  Cocoapods and Swift interop, KMP target declaration, KMP-shaped Gradle wiring
Then each family is present as one directive with a `name`, a `type` from
  `{norm, refusal, method}`, a `when` from `{required, optional}`, and a `read`
  that lands on a self-contained fragment the pivot ships
```

### KMM-AC-8 — The dissociation is visible by file structure alone

```gherkin
Given the pivot's `extends.json` and each satellite's `extends.json`
When a reviewer reads them side by side without the prose
Then the pivot's `extends.json` lists no fragment under a satellite's root, and
  no satellite's `extends.json` lists a fragment under the pivot's root — the
  dissociation is visible from the file paths alone
```

## Out of scope

- **Module versioning and migration on a breaking change** — what a major, minor or
  patch bump means for a project already using a module, how long a renamed thing
  keeps working, and when that project finds out. Specified by
  `features/business/release-versioning/`; this feature only establishes that a module
  exists and can be composed, not how it evolves once adopted.
- **Any single module's own settings or file layout** — each module documents what it
  reads under its own settings key in its own `README.md` (`module-anatomy`); this
  feature does not
  duplicate any module's contract, only the shared rule that a contract must exist.
- **Whether a directive's one-line summary still describes its fragment.** Nothing
  checks it, and nothing can: it is prose about prose. The mechanism narrows the drift
  to one line sitting beside the path it describes, which is as far as this feature
  claims to go.

