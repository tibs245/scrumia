# Modular composition — business rules

## Value

For whoever adopts or extends ScrumIA — a project declaring which modules it runs, and
the modules themselves, written to be pluggable. It brings one flat declaration
(`modules`) a project edits to take exactly the capability it needs, so adopting one
module never requires taking the whole method. It matters because a project that forks
a monolithic method to adapt one part of it stops receiving updates to the rest, and the
composition is what lets the reference answers change without breaking a project's own
choices. Not instrumented today: nothing counts how many projects run with which
modules; the composition's shape is read from `.scrumia/config.yaml`, not aggregated.

## The composition is a routing mechanism first

An agent is effective when it reads the minimum it needs — but to read little it must
know **where** the essential of its task is. Declaring the modules exists to answer that,
across projects with disjoint contexts served by the same set of modules: a team inside a
large company, a for-profit monorepo, this plugin repository. Extension — a project
customising or adding to a module's behaviour — is a consequence of that routing, not
its object.

## `modules`

A mapping in `.scrumia/config.yaml`, keyed by each module's qualified source
([ADR-0021](../../../docs/adr/0021-modules-keyed-by-source.md)):

```yaml
modules:
  "tibs245/scrumia:scrumia-specs":
    params:
      root: features
  "tibs245/scrumia:scrumia-github-project": {}
  "local:acme-docs-rules": {}
apps:
  - name: api
    path: apps/api
    modules:
      "tibs245/scrumia:scrumia-impl-rust": {}
      "tibs245/scrumia:scrumia-practice-tdd": {}
```

**The key is `<source>:<module>`, always** — one grammar, no bare name. The source is a
marketplace (`<owner>/<repo>`), `shared` for a directory of checkouts shared between a
person's projects, or `local` for inside the project. A bare name would make the file's
meaning depend on what happens to be installed, which is what the qualified key removes.
The three sources are the three locations `features/business/local-extension/` defines,
and naming the source in the key is why no separate origin field exists to disagree with
it.

**The mapping is not ordered.** Any reader brings a last-wins reflex uninvited; this rule
exists to contradict it on first read. Order between modules decides nothing.

**A module installed and named nowhere is inert.** Presence on disk is not participation:
a project may have twenty modules enabled and run the five it names. That is what makes a
module safe to install before deciding to use it, and it is why the mechanism never asks
"is this slot filled" — only "does this project run it".

**A key names who runs, never what they contribute.** What each module offers is its own
`extends.json`, keyed by register. The two were deliberately not nested — ADR-0021 states
why, and BR-9 below is the rule it protects.

**A source is established, never chosen.** Whatever writes this file — an installer, a
migration off a shape that carried bare names — takes each source from what actually makes
the module resolvable: the repository the module's own manifest claims, the project's
module directory, or the shared tier. The marketplace a person happened to install it
through is a cross-check and not the answer; the two agree for a marketplace serving its
own repository and part company for a fork, where sourcing from the wrong one writes a key
that resolves to nothing while every table merely renders shorter.

**Reading may settle an ambiguous name for the length of one call; writing may not settle
it at all.** A bare name several tiers answer is a shadow: resolution picks the narrowest,
uses it, and says so every time it runs, which is safe because it is recomputed and
re-announced on the next call. Writing that same choice into a versioned key ends the
recomputation — the file now asserts on every machine what one machine's layout happened to
say. So an ambiguous name is reported and left out, and a person decides. This asymmetry
between resolving and recording is what the retired shapes' migration turns on.

## A module's configuration cascades, in a stated order

Three layers, each overriding the one before:

| Layer | Where | Versioned |
|---|---|---|
| 1 | `settings:` in `.scrumia/config.yaml` | yes |
| 2 | `modules[<key>].params:` | yes |
| 3 | `.scrumia/config.local.yaml` | **no** — gitignored |

**Layer 2 is where a module's own settings live.** A key one module reads belongs in that
module's `params:`, not in `settings:`. What stays in layer 1 is what is not a module's:
`settings.team.roles` declares the team, which `features/business/agent-team/` owns and
which three modules read.

**Layer 3 is per-machine and never committed.** It is what lets one developer run a
different value without changing what the repository says. The cost is stated rather than
hidden: two machines can resolve different settings from one repository, so a composition
is reproducible in its *modules* — which the qualified key guarantees — and not necessarily
in its *values*. A reader who needs to know what a machine actually resolved asks the
tooling rather than reading the file.

The order is stated so it can be checked. An order only applied, never written, can invert
without anything failing.

**A module reads through the cascade, not out of the file.** The three layers are a rule
about resolution, and resolution happens somewhere. A module that opens
`.scrumia/config.yaml` itself and reads `settings:` sees layer 1 and nothing else, whatever
the table above promises: layers 2 and 3 are invisible to it, so a per-machine override is
a documented feature that changes nothing for the only thing that consumes it. Declaring
the layers and reading past them are two halves of one rule, and the second is the half
that can be absent without any of it failing.

**A module that cannot resolve its configuration stops.** It names what it was resolving
and for which module, proposes the next step — BR-3's obligation, which this does not
suspend — and answers nothing. Falling back to its own built-in defaults is worse than an
error, because the answer is well-formed: nothing fails, no one is told, and the module
runs on values a person never chose. That is how a migration of layer 1 breaks one
consumer loudly and another silently, and it is the silent one that costs.

**A key the layers do not carry is not the same as a value a module has an opinion
about.** A module may carry a default for a knob it can sensibly do without, and it says
when one stands in; what it may not do is carry a default for the thing it exists to
resolve, because there the default is indistinguishable from a resolved answer. Which of
its keys is which is the module's own to state, in its README — the rule here is only that
the second kind stops it and the first kind is said out loud.

## `practices` is retired as a named slot

`implementation` and `practices` were always two answers to the same question — how an
app is built — at two granularities. `practices` does not survive as its own key: a
practice module is declared in an app's own `modules`, alongside the implementation
module:

```yaml
apps:
  - name: api
    path: apps/api
    modules:
      "tibs245/scrumia:scrumia-impl-rust": {}
      "tibs245/scrumia:scrumia-practice-tdd": {}
  - name: prototype
    path: apps/prototype
    modules:
      "tibs245/scrumia:scrumia-impl-solidjs": {}
```

TDD applies to `api`, not to `prototype` next to it, because each app's `modules` mapping
is its own — the per-app axis the former `practices` slot carried is what makes this a
per-app declaration and not a single project-wide list.

**The one precedence rule the retired slot carried is unchanged: specific beats
generic, and a project override beats both.** What changes is where it is expressed: no
longer in prose a reader has to remember, but in the order the directive table prints —
project-local first, then the app's own modules, then the project-wide ones (§ *A skill
is extended by data*, below). A module never ranks itself.

Every other rule a practice module owes is unchanged: it refines a named point of the
implementation contract, it works on its own even without an implementation module
present, it ships a reference/audit/refactor skill trio, it documents the settings it
reads.

## What a module owes to be pluggable

Three things, no more:

1. **A `SKILL.md`** — the module's own entry point, and the place it documents its
   contract with the rest of the composition: the settings it reads, and the one
   sentence (`CLAUDE.md` line) that tells an agent what it must know about the module
   without opening it. A module with no `SKILL.md` cannot be composed — there is nothing
   for `scrumia-init` to point an agent to.
2. **The rule that it never assumes another module is present.** If a module needs a
   capability another module would provide, it checks for it rather than assuming it,
   and if nothing provides it, it names the gap and proposes the next step instead of
   failing outright or guessing a substitute behaviour.
3. **The rule that every reference it writes resolves inside itself** (§ *A module
   reaches nothing outside itself*, below).

A module that skips any of the three still runs, until the day a project composes it
with a different set of modules than the one it was written against — at which point it
breaks silently, which is the failure this rule exists to prevent.

The list admits an item only on that test — silent breakage. The extension data files
below are deliberately not a fourth entry: a module without them is fully composable, it
simply contributes nothing, and its silence is reported by name rather than discovered
later.

## A skill is extended by data

An agent that has to notice, in one module's prose, that a second module also speaks to
the task — then open it, and apply a precedence rule stated in a third place — is
performing a recomposition nothing checks. Prose copies of another module's content are
what that pressure produces, and a copy outlives the original it was taken from.

So a **main skill states its description and its goal, and stops.** What it must apply
is contributed by other modules, as data, and rendered into one table at the moment the
skill asks for it.

**A register is a named extension point.** A module opens one by naming it, the main
skill that consumes it, and its purpose. A register is opened by exactly one main skill:
two modules opening the same register leaves nothing to decide which skill consumes it,
and that is reported rather than arbitrated.

**A contribution names no consumer.** A module declares what it offers — a directive's
name, its type, whether it is required, one line of what it says, and the fragment to
open. It does not declare, and cannot encode, which skill will take it. That is what
lets one fragment serve implementation, review and audit without being written three
times, and it is why adding an implementation module does not reopen every practice
module.

**A contribution is data and nothing else.** No executable, no condition, no logic: a
module is discovered from the environment the harness already provides, so contributing
costs one file. What a module may not do is reach outside itself — a fragment path that
leaves the module is refused (BR-7).

**What a module runs is declared, not inferred**: the published names it executes. The
caller declaring its own edges is the provenance nothing had when a broken call site could
only be found by reading prose. Registers are not declared a second time here — opening one
is already the promise to consult it, and a module that consults one it does not open is
simply a caller of that register's tool, which needs no declaration to be checked.

**A name is declared with the source it comes from.** The session PATH is one flat
namespace shared with every enabled plugin, and a naming convention two marketplaces both
follow does not separate them. So a dependency on a name states *whose* — the marketplace
the publishing module ships from — which turns a collision from something nobody notices
into something a check reports. What is *executed* stays the bare name: the source is a
claim to verify, never something to look up in order to decide what to run. Register names
carry no source, because a register is a composition-local concept and not an entry in an
OS-wide namespace.

**The order is the composition's, never a module's.** Project-local first, then the
modules an app declares, then the project-wide ones; required before optional within a
tier. A module does not rank itself against modules it has never heard of.

**The table does not arbitrate.** Two directives whose prose contradicts each other are
both printed, in the stated order, because a generator cannot read English. What the
mechanism claims is that they are visible in one place, which they never were — and that
is the whole of the claim.

**Nothing is stored.** The table is computed when asked and thrown away. There is no
artefact to commit, no digest to verify, no drift to gate — and adding a module changes
what a skill applies with nothing to rebuild. The cost accepted in exchange is that the
answer depends on the environment at the moment of the call: a module enabled but not yet
restarted into contributes nothing, silently, until the check is run.

## The register vocabulary is open

A module may open a register nobody had. There is no kernel-owned list to bid from: the
vocabulary of a given project is the union of what its installed modules open, which is
why the only honest answer to "which registers exist here" is to ask the tool.

This is a deliberate reversal of the closed vocabulary an earlier version of this feature
carried. A closed list bounds the customisation promise — a project chooses who covers
what, never what the extension points are called — but it also means a third-party module
cannot declare anything the kernel did not anticipate without a `scrumia-core` release,
which is the opposite of what a plugin marketplace is for. The cost of opening it is that
a typo in a register name produces silence instead of an error; that is why an unmatched
contribution is a named finding of the check rather than something nobody mentions.

## Distribution is what makes composition cheap

A project adopts a module by declaring it, not by copying it. Two keys in a project's
own `.claude/settings.json` — `extraKnownMarketplaces` and `enabledPlugins` — are
enough; nothing is duplicated into the project repo. This rides on Claude Code's native
plugin marketplace rather than a bespoke installer, because ScrumIA deliberately targets
Claude Code alone (ADR-0001).

All of ScrumIA's own modules live in this one repo, which is also the marketplace
(ADR-0007). A cross-cutting change to the composition — this feature is one — fits in
a single, atomic PR instead of coordinating releases across several repos. A
third-party module remains possible without changing this structure: `marketplace.json`
accepts external sources (`github`, `git-subdir`, `npm`, `archive`) alongside the
relative paths used for ScrumIA's own plugins.

A module may also ship the **standing role** that guards its capability, rather than
that role living in the team module. `scrumia-design` is the first to do so: a design
role in a project with no design system would have nothing to judge but taste. The role
registers in the same `settings.team.roles` list, so routing stays single-sourced — see
[ADR-0014](../../../docs/adr/0014-roles-ship-with-their-capability.md) and the
`agent-team` feature.

## How modules connect to each other

**Through documentation and data, never through a lookup that hides who answered.**

The `CLAUDE.md` table is what an agent needs **before** it knows what it is doing: which
modules are plugged in, and the one sentence about each that saves opening it. It is
written once, at composition time, and read as ordinary project context.

The **directive table** is what an agent needs **once the task is known**: for this
register, in this project, which fragments to open and which of them are required. It is
computed when asked, because the `CLAUDE.md` table cannot carry it without becoming the
document nobody reads.

The rejected alternative is still the capability registry: each module declaring verbs
that a core resolves to whichever module is plugged in. Its cost was the agent holding an
indirection in mind for something it could not see. Nothing here is invisible — every
contributing module and every file path is printed, and no verb resolves to a module,
because nothing selects a provider. What *is* amended, and stated as such in
[ADR-0020](../../../docs/adr/0020-skill-extension-protocol.md), is that the directive
table is computed at call time rather than written at composition time.

The rule that follows: **a module cites another by name in prose**, in its own
`SKILL.md` or `CLAUDE.md` line, never through a runtime lookup — and that name must be
one the harness resolves, never a relative path. Replacing a module means checking the
others that name it; that check is a few minutes of grep, done rarely.

## A module reaches nothing outside itself

BR-4 governs how a module **names** another. This governs how it **reaches** anything at
all, which is a different question: a reference written inside a module resolves inside
that module, or it does not resolve.

A module is installed at a path it does not choose. In this repository it sits at
`plugins/<name>/`; installed from a marketplace it sits one segment deeper, under a
version — and that version is neither knowable when the reference is written nor unique,
since two of them sit side by side in a cache. So a relative path climbing out of a
module's own root lands somewhere different in the two layouts, and nowhere at all in a
project that is not the module's home repository. It fails silently: a link nothing
opens, a script that is simply absent.

Two ways out for what crosses the module boundary — and a third, narrower one for a
`features/` rule the plugin owns in source but not at install time:

- **A file another module ships** — the owning module publishes it as a *named
  executable* under its own `bin/`, which the harness puts on the session's PATH with the
  install path already resolved. The caller runs the name and holds no path at all.
- **A document belonging to no module** — a rationale or a spec in the home repository.
  The module inlines what it needs, or cites an absolute public URL. A
  repository-relative link assumes a consuming project has a file it has never had.
- **A `features/` rule the plugin owns in source but not at install time** — once
  installed, the plugin is no longer its home-repo: the home-repo's `features/`
  directory belongs to the consumer's own `scrumia-specs` instance, which ships its
  own `features/` with the same path shape and content that may differ under the
  same name. A citation that drops a `features/` path or links out of the plugin root
  lands on whichever instance the runtime reads the same shape — possibly the
  consumer's `features/`, with different content. So the plugin restates the
  operative rule inline, and the citation is then a provenance pointer, not a
  load-bearing reference.

The same harness fact is what makes a contribution readable without an executable: the
modules present are the ones whose `bin/` the harness put on PATH, so the kernel's tool
discovers them without any module naming any other. That is a widening of the mechanism,
recorded in [ADR-0020](../../../docs/adr/0020-skill-extension-protocol.md) — and it is
what makes PATH load-bearing for the whole composition rather than for two call sites.

Running a name is not the dynamic resolution ADR-0009 rejected: the name is written down,
constant, and greppable — which a relative path is not — and nothing chooses *which*
module answers it. See [ADR-0018](../../../docs/adr/0018-modules-reach-by-name.md).

## How the composition is reported

A composition an agent retypes is a composition that drifts, and the drift is invisible
because the prose still reads plausibly. So the skills that present the composition —
`scrumia-init` and `scrumia-compose` — end by running `scrumia-core`'s
`scripts/compose-status.sh`, which reads `.scrumia/config.yaml` and prints it: the
modules the project runs, and each app with the modules it declares. What a human reads is the
file, every time, rather than what one session remembered of it.

The script reads the config as the versioned artefact on stdout, and reads the runtime —
`claude plugin list --json` — as machine-local state on stderr. For each declared
module whose `<source>:<module>` key is not present in the runtime (entry missing,
`enabled: false`, scoped to another project, or `installPath` not resolving on disk),
one note names the module, the source that should provide it, and the install command.
stdout is unchanged for any caller that gates on it (the site publishes it verbatim;
`tests/fixtures/composition-output.txt` gates it).

This is reporting, not resolution. Nothing calls the script to find out who provides
anything; it resolves nothing on any agent's behalf, and BR-4 stands untouched. Reading
the runtime is the cross-check BR-6 admits: a declaration can name a module whose
install is absent, and that drift would not otherwise be visible to anyone who closes
by running the script. The four signals are read separately because each is a different
failure mode — a module not in the cache is one thing, a module disabled in the cache
is another, a module scoped to another project is a third, and a stale entry whose
`installPath` no longer resolves is a fourth.

## Business rules

- **BR-1** — A register is a question, not a module. An extension point exists
  independently of whether any installed module currently contributes to it; a register
  nothing extends yields an empty table, which is an answer and not a failure.
- **BR-2** — A module installed and named in no `modules` mapping is inert. Presence is
  never read as participation, and a project's `modules` is the only thing that decides which
  modules contribute.
- **BR-3** — A module never assumes another module's capability is present. It checks,
  and on finding the capability unprovided, it names the gap in a message a human or an
  agent can act on, and proposes the next step, rather than failing or silently
  changing behaviour.
- **BR-4** — A module cites another by name where the sentence needs the specific one,
  and that name is one the harness resolves, never a relative path. Nothing resolves a
  name to a module at runtime.
- **BR-5** — ScrumIA's own modules ship from a single repo, which is also the
  marketplace. A third-party module is not required to: it declares its own source in
  `marketplace.json`, at the adopting project's discretion.
- **BR-6** — The composition is reported by reading `.scrumia/config.yaml`, never from
  memory, and cross-checked against the runtime — what `claude plugin list --json`
  confirms is installed — before being printed. A skill that presents the composition
  closes by running the kernel's status script and does not paraphrase the table it
  prints. Reporting the composition is not resolving it: BR-4 still forbids resolving
  a name to a module at runtime.
- **BR-7** — Every reference a module writes resolves inside that module. A file
  another module ships is reached by running the name that module publishes on
  PATH — never by a path climbing out of the caller's own root — and a document
  belonging to no module is inlined or cited by absolute URL. Running a published
  name is not resolving a slot, so BR-4 stands: the name is constant and greppable,
  and nothing decides at runtime which module answers it. When the cited document is
  the plugin's own home-repo `features/` rule — a file the plugin owns in source but
  not at install time — the operative rule is restated inline before the citation;
  the citation is then a provenance pointer, not a load-bearing reference, because a
  load-bearing reference would resolve to whichever `features/` instance the
  consumer's `scrumia-specs` shipped, with content that may differ under the same
  path shape.
- **BR-8** — A register is opened by exactly one main skill, and may be extended by any
  number of modules. Two modules opening the same register is a conflict named by the
  check, never arbitrated by declaration order — `modules` carries no order to arbitrate by.
- **BR-9** — A contribution names no consumer. A module declares what it offers and to
  which register; it does not name, and may not encode, which skill takes it. A key that
  named a consumer would make every cross-cutting module enumerate the modules that could
  ever use it.
- **BR-10** — What a skill applies is contributed as data and rendered on demand, never
  recomposed by the agent from one module's prose about another, and never merged into
  the fragments' content. The table orders contributions; inside a module, that module's
  own routing table orders its files.
- **BR-11** — A module declares the published names it runs, each qualified by the source
  that publishes it, and the check reports every one nothing satisfies — including a name
  whose actual publisher ships from another source. A name that is absent is never read as
  "this module contributes nothing": that reading turns a plugin awaiting a restart into a
  silent claim that no rules apply. Opening a register is itself the promise to consult it,
  so a register a module opens and never asks for is reported; it is not declared twice. A name that is absent is never read as "this module
  contributes nothing": that reading turns a plugin awaiting a restart into a silent claim
  that no rules apply. Qualifying a declaration is not resolving it: what a skill invokes
  is still the bare name, and nothing consults a source to decide what to run.
- **BR-12** — The directive table arbitrates nothing. Two contributions whose prose
  contradicts each other are both printed, in the computed order; resolving them is a
  composition decision a person makes, not one a generator may make silently.
- **BR-13** — A module is declared by a key of the form `<source>:<module>`, always. The
  source is a marketplace (`<owner>/<repo>`), `shared`, or `local`. A bare name is not a
  declaration, and no field beside the key restates the origin. Whatever **writes** such a
  key establishes the source from what makes the module resolvable — for a marketplace, the
  repository the module's own manifest claims — never from the marketplace it was installed
  through, and never from whichever module of that name happens to be installed. A name
  nothing establishes, or one several tiers answer at once, is reported and left unwritten:
  resolution may settle an ambiguous name for the length of one call, because it recomputes
  and re-announces it on the next; a versioned key settles it for every machine and every
  run, which is not the migration's to decide.
- **BR-14** — A module's configuration resolves from three layers in a stated order:
  `settings:`, then the module's own `params:`, then `.scrumia/config.local.yaml`, which is
  never committed. A key one module reads belongs in that module's `params:`; `settings:`
  holds what is no module's, and a composition is reproducible in its modules but not
  necessarily in its values. **The order is what decides**, and nothing about how a value
  is written may outrank it. A layer overrides with a value and never with an absence: a
  key written with no value carries nothing, at any depth, and the layer beneath answers.
  The cost is that no layer can subtract what a lower one carried — `tech.md` says what
  that leaves a project.
- **BR-15** — A module reads its configuration **through** that cascade, never out of the
  raw configuration file: reading `settings:` directly resolves layer 1 and silently
  discards the other two. While a module still reads keys under a retired `settings.<slot>`
  nest, it names that nest to the resolver when it asks: the cascade reconciles the two
  shapes, and it can only do so for a nest it has been told about.
- **BR-16** — A module that cannot resolve its configuration — the resolver absent, or no
  layer carrying the block it reads — names what it could not resolve, proposes the next
  step as BR-3 requires, and stops. It does not answer from its own defaults. BR-3 governs
  the message; what this rule adds is that a configuration one cannot resolve has no
  degraded mode to continue in, because every later answer would be well-formed and wrong.

## Vocabulary

**"Slot" names the question a project answers when composing** — it survives as the
word the human-facing composer uses to ask "which module fills this need", because
that is what a person actually answers, one question at a time. It is not the
mechanism's unit: nothing in the configuration or the tooling is keyed by slot.

**"Register" names an extension point** — what a main skill opens, what a module
contributes to, and the argument the kernel's tool takes. It is not a "slot": a slot has
one answer, a register has as many as the project runs. It is not a "hook" either — that
word belongs to the harness and names something that executes.

**"Directive" names one row of the table** — one principle, method, refusal or
reference, with the fragment that states it. **"Fragment" names the file** the directive
points at: one scope, one purpose, so the same file can be contributed to several
registers with a different obligation each time.

**"Extension" is not a coverage word.** A module contributes to a register exactly when
it declared something for it, which is *declaration*. A report that counted contributions
would be counting declarations with a new name on them.

"Area" appears nowhere in this vocabulary as a synonym for any of these: it reads as a
section heading and loses what "slot" and "register" carry — a question, or an extension
point, that exists whether or not anything currently answers it.
