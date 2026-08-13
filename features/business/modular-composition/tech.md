# Modular composition — how the extension mechanism works

`business.md` states the rules; `docs/adr/0020-skill-extension-protocol.md` states the
decision and what it rejected. This file states the **mechanism**: what resolves what, in
which order, and what happens when a piece is missing.

The authoring reference — the exact fields of each data file, and how to open an extension
point in a skill — ships with the skill that teaches it, `scrumia-core`'s `scrumia-extend`.
It is deliberately not restated here: a consuming project must read the version that
matches the tooling it has installed, not whatever this repository's `main` branch carries
at the moment someone opens a link. What this file adds is what that skill cannot see —
how the pieces fit, and how the mechanism fails.

## The pipeline

Four inputs, one output, nothing stored in between.

```
  $PATH  (harness-provided)  ┌───────────────────────────┐
  $SCRUMIA_SHARED_DIR ──────▶│ 1. discover module roots  │
  .scrumia/modules/          │    three tiers, one pass, │
                             │    each root tagged with  │
                             │    the tier it came from  │
                             └─────────────┬─────────────┘
                                           │  module · root · location · source
                                           ▼
  .scrumia/config.yaml       ┌───────────────────────────┐
  modules: {…}        ──────▶│ 2. keep what this project │
  apps[].modules: {…} ──────▶│    runs, for this app     │
                             └─────────────┬─────────────┘
                                           │  the in-scope modules
                                           ▼
  <root>/extends.json        ┌───────────────────────────┐
  (one per module)    ──────▶│ 3. collect the rows for   │
                             │    the asked register     │
                             └─────────────┬─────────────┘
                                           │  rows, unordered
                                           ▼
  .scrumia/extends.json      ┌───────────────────────────┐
  (the project's own) ──────▶│ 4. order by scope, then   │
                             │    obligation, then name  │
                             └─────────────┬─────────────┘
                                           ▼
                                  one table, printed
                                  nothing written
```

**Step 1 is the load-bearing one**, and its marketplace tier is the load-bearing part of
it. The harness prepends `<pluginRoot>/bin` to the session PATH for every *enabled* plugin,
with the install path — version segment included — already resolved. That is the same fact
ADR-0018 relies on to run a published name; here it is read the other way round, to learn
which modules are present. It is what removes the need for any module to publish an
executable, or to know where any other module lives.

The other two tiers are plain directories, and which directory each is —
along with what binds a key to a root — is `features/business/local-extension/`'s
`tech.md`. All three are read in one pass; no tier is a fallback for another.

`$SCRUMIA_MODULE_DIR` replaces the **marketplace** tier with a directory of `<module>/`
checkouts, and stands in for it. This repository and CI use it, because no harness is
running there. The consequence is stated in ADR-0020 and repeated here because it is the
mechanism's blind spot: **CI can only ever exercise the override, never the product's own
path.** It is a blind spot on that tier alone — the two below it are directories in CI
exactly as they are anywhere else.

**Step 2 is what makes a module inert.** A module discovered in step 1 and named in no
`modules` mapping is dropped here — it is installed, and this project does not run it.

**Step 2 is also where a declaration becomes a root.** Step 1 yields a root, the tier it
came from, and a source derived from `plugin.json`'s `repository`/`homepage`, normalised to
`<owner>/<repo>`. A marketplace key binds only a root whose manifest claims that
repository; a `local:` or `shared:` key binds by name **within its own tier**, where a
manifest can say nothing useful about a location it does not know it is in. A declaration
no root answers is a declared absence (`features/business/local-extension/` BR-8); one that
two distinct roots answer is either the shadow BR-5 resolves or the conflict BR-7 refuses
to. Which, and why identity is the physical path, are that feature's `tech.md`.

Declaring a module in `.scrumia/config.yaml` does not put it on `PATH`. Both are required,
and they answer different questions — the harness decides what is *reachable*, the
configuration decides what is *run*. A module declared and not enabled is reported as a
declared absence rather than as a configuration error.

**Which shape step 2 reads.** Three have existed; the precedence is fixed and stated so a
half-migrated file cannot resolve to nothing:

| Present | Read | Warning |
|---|---|---|
| `modules:` | it, and only it | none |
| no `modules:`, `extends:` present | `extends:` | migrate to `modules:` (ADR-0021) |
| neither, `composition:`/`practices:` present | those | migrate to `modules:` |
| none of them | nothing | the composition is empty, said as such |

The last row is the one that must not be silent. A file carrying `modules:` and read by a
tool that only tests for `extends:` resolves to zero modules, and a register with no
contributions is an *answer* under BR-1 — so every table renders empty and nothing fails.
Testing the shapes in this order, and naming the empty composition, is what keeps that from
looking like a correct run.

**Which shape a module's own settings are read in.** ADR-0021 moves what `settings.<slot>`
held into that module's `params:`, so the same key exists in two shapes while a project
migrates. The resolver, not the consumer, reconciles them: a module names the nest its
configuration used to sit under when it asks, and every layer is **normalised to the
current shape before the layers combine**.

| Where the key sits | Read |
|---|---|
| at the top level of a layer | it — the current shape wins within its layer |
| only under that layer's retired `settings.<slot>` nest | it, for the deprecation window |
| both, in one layer | merged, the top-level key winning per key, never per block |
| both, in different layers | the later layer's, whichever shape carries it |

The last row is the one that has to be normalised for. A project migrates one key at a
time, and the layer it has not migrated is layer 3 — never committed, so nothing carries it
forward. Reconciled after the layers are merged, shape decides where BR-14 says the layer
does, and the per-machine layer is the one discarded. Reconciled within each layer first,
the merge order is the only thing left that can decide, which is what BR-14 states.

Merging per key rather than choosing a block is the other part that is not obvious: a
resolver that picked whichever block looked newer would drop every key the other still
carried onto the consumer's built-in defaults — a well-formed answer nobody configured,
which is BR-16's failure arriving through the migration meant to avoid it.

A nest no layer carries resolves clean and empty. A fully migrated project names one that
is gone, and a resolver that failed on it would stop every consumer the moment the
migration succeeded.

The retired nest's reading window is a deprecation like any other, and
`features/business/release-versioning/` decides when it closes. The release that removes it
is named where a project updating a module actually reads — that module's own changelog,
under `Deprecated` — because a feature carries no version to count releases from. It closes
in the consumers first and in the resolver last: the resolver cannot drop the mapping while
a module still names one.

**A key written with no value carries nothing, at any depth.** The merge propagates an
explicit null, so a key written bare would otherwise erase the layer it defers to — and
writing keys bare is what migrating one at a time produces. Nulls are dropped from every
layer before the layers combine, so the layer beneath answers, whether the bare key sits at
the top of a block or inside one. A layer left carrying nothing that way is not named among
the layers that answered: the provenance names what resolved, never what merely exists.

**What that costs a project configuring layer 3.** The layers add and overwrite; only one
thing subtracts. A key set to nothing defers rather than clears, and an empty block merges
rather than empties — so neither takes back what a lower layer carried. An empty **list**
does: lists replace where blocks merge, so writing `[]` is the one way a layer removes what
is beneath it, and it is also why a layer writing only `[]` counts as having answered.

| Written in a higher layer | What the lower layer keeps |
|---|---|
| a value | nothing — it is overwritten |
| a key with no value | the value, at any depth |
| an empty block | every key it held |
| an empty list | nothing — the list is replaced |

A project that needs a key genuinely absent removes it from the layer that carries it. A
module reaching a state where its configuration cannot be resolved is BR-16's, and it is
reached by no layer carrying the block — never by clearing one.

## Where each thing is resolved, and by what

| Question | Answered by | When |
|---|---|---|
| Which modules exist here? | the harness through PATH, plus the shared and local directories | every call |
| Which of them does this project run? | `.scrumia/config.yaml`'s `modules` | every call |
| Where does a `shared` or `local` module sit? | the directory each names, in `features/business/local-extension/`'s `tech.md` | when such a key is declared |
| Which app does this file belong to? | the longest `apps[].path` prefixing it | on `--path` |
| What does a module contribute? | its own `extends.json` | every call |
| Where is a fragment? | the module root, joined with `read` | at print time |
| Which module publishes a name? | its `bin/`, cross-checked against PATH | on `--check` only |

Nothing in that table is cached, and nothing in it is written down. That is the whole
reason there is no staleness class to detect: the answer is recomputed, and recomputing is
cheap because every input is a file already on disk.

## The order is computed, and it is the precedence

Scope is assigned in step 4, from *where a contributing module was named*, never from
anything the module says about itself:

| Scope | Source | Rank |
|---|---|---|
| project-local | `.scrumia/extends.json` | 0 |
| app | the app's own `modules` mapping | 1 |
| project-wide | the top-level `modules` mapping | 2 |

Then `required` before `optional`, then module name, then directive name — so two runs on
the same inputs print the same table, and a reader can check the order rather than trust it.

**Why scope rather than a `grain` field.** An earlier draft had each module declare whether
it was a technology module or a cross-cutting one, and ranked on that. It made every module
carry a claim about its standing relative to modules it has never heard of — unverifiable,
and wrong the first time someone writes a cross-cutting module that should win. Scope moves
the same judgement to the only place that has the information: the project, which decided
what to plug in where. A project that wants a different answer writes the row itself, in
`.scrumia/extends.json`, at rank 0.

## What fails, and what says so

The split is deliberate: **strict where the code is authored, tolerant where it is
consumed.** A consuming project must not be blocked by a third-party module's laxness, and
this repository must not ship one.

| Symptom | `scrumia-extends --check` | `tools/validate.py` |
|---|---|---|
| A fragment path leaves its module | — (not its job) | error |
| A fragment path names no file | — | error |
| A register names a skill the module does not ship | — | error |
| A `runs` name nothing publishes | error | error |
| A `runs` name published from another source | error | error |
| A `runs` name with no source at all | reported, passes | error |
| A publisher declaring no repository | reported, passes | warning |
| A contribution to a register nobody opens | error | — |
| Two modules opening one register | error | — |
| A register the module opens that no skill of its own asks for | — | error |
| A line of `dependencies.jsonl` that is not a name | — | error |
| A register nothing contributes to | nothing — an empty table is an answer | — |

Two rows deserve their reason spelled out.

**"A contribution to a register nobody opens" is the silent one.** Those directives will
never be printed, by anything, ever — and no other signal exists. A register name is a free
string, so one typo turns a module's whole contribution into a file nobody reads. It is an
error for that reason alone.

**"A register the module opens that no skill of its own asks for"** is checked by
grepping that module's skills for the invocation. It catches the one failure a declaration
check structurally cannot: a skill that opens an extension point, reads as covered, and
applies nothing.

The set it runs over is `registers.json`, and that is deliberate. A draft of
`dependencies` carried a second list, `reads`, naming the registers a module consults.
It bought nothing — a module that opens a register already promises to consult it, so the
two lists were the same set — and where they *did* differ they hid the defect the check
exists for: `scrumia-specs` opened `find-spec`, `scrumia-specs-find` never asked, `reads`
did not list it, and a check scoped to `reads` said nothing. Two lists that must agree
eventually will not, so there is one, and it is the one that carries the promise.

## Why two formats

`registers.json` and `extends.json` are keyed: a register name is written once and groups
what belongs to it. `dependencies.jsonl` is a flat list, so it is one record per line.

The split is not stylistic. Converting `extends.json` to JSONL was measured on
`scrumia-impl-rust` and rejected: the register name would go from 3 occurrences to 11,
because every row would have to carry its own. That denormalises the one field whose typo
is already the silent failure above — eleven independent chances to orphan a directive
instead of three, for a 4% saving in bytes. A flat list has no such key, so it pays none of
that and keeps what a line-per-record file is good at: appending without touching the
neighbouring line, and diffing as exactly what changed.

## Constraints the implementation lives under

- **`bash` + `jq`, and nothing else.** `scrumia-extends` is reached the same way
  `scrumia-board` and `scrumia-pick-model` are, in sessions that may have no Python
  environment configured. The YAML is read by `yq` or by `python3` + PyYAML, whichever the
  machine already has — the same loader those two tools use, never a third dependency.
- **`/bin/bash` is 3.2 on macOS.** It mis-parses a `case` pattern's `)` inside a command
  substitution, which cost one debugging pass here; the affected code uses a suffix test
  instead, with the reason in a comment beside it.
- **The tool writes nothing, anywhere.** Not a cache, not a temp file, not a lock. That is
  what lets it be safe to call from inside any skill, at any point, including concurrently
  across the worktrees a sprint opens.
- **No answer about the composition carries meaning in the exit status.** Printing a table
  for a register nothing extends is success: an empty answer is an answer. The surfaces
  that do exit non-zero judge something else — a declared dependency nothing meets, and a
  sentence written about the composition that its reader cannot check; which those are, and
  what each refuses, is `local-extension`'s.

## Debt assumed

- **A directive's `summary` is prose about prose, and nothing checks it.** A summary that
  stops describing its fragment is invisible to every gate. What the mechanism buys is that
  the drift is now one line sitting beside the path it describes, instead of a paragraph in
  a different module. *Exit condition*: none planned — closing it means reading English.
- **`--check` is not run automatically in a consuming project.** A plugin enabled without a
  session restart contributes nothing, silently, until someone asks. *Exit condition*: a
  session-start hook, once the harness offers one that can report without blocking.
- **The grep that proves a skill runs the tool matches a string.** Renaming the tool, or
  invoking it through a variable, defeats it. *Exit condition*: none worth paying for — the
  check is a backstop, and a stricter one would fail on legitimate phrasing.
- **The debt each source's own location carries** — what is bound by name, and what a
  second route to one directory costs — is `features/business/local-extension/`'s
  `tech.md`, which is where that resolution is stated.

## Practices for writing an extension

- **One fragment, one scope.** A guide covering three principles can only be contributed
  whole, to every register at once, at whatever obligation fits the loosest of the three.
  Splitting is what buys the ability to say *this one is required for implementation, that
  one is optional for review*.
- **Write the `summary` as what the fragment says, not what it is about.** "One reason to
  change per unit" is usable without opening the file; "About the Single Responsibility
  Principle" is not, and an agent that has to open every row to find out which matter has
  gained nothing over reading the whole module.
- **`required` is a promise that every unit of work in scope obeys it.** A directive marked
  required that only applies sometimes teaches an agent to discount the column.
- **Contribute to `review` and `audit` separately, and differently.** The same fragment
  usually enters `implement` as a `norm` and `review` as a `refusal` — what to do, and what
  to look for. A module that contributes the identical row to three registers has probably
  not decided what each register is for.
- **Never encode a consumer.** No skill name, no module name, no "only when the app is
  Rust". If a directive should only reach some apps, that is the app's own `modules`, per
  app, doing its job — not a condition inside data that is supposed to hold none.
