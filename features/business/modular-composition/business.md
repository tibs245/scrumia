# Modular composition — business rules

## Value

For whoever adopts or extends ScrumIA — a project declaring which modules it runs, and
the modules themselves, written to be pluggable. It brings one flat declaration
(`extends`) a project edits to take exactly the capability it needs, so adopting one
module never requires taking the whole method. It matters because a project that forks
a monolithic method to adapt one part of it stops receiving updates to the rest;
`extends` is what lets the reference answers change without breaking a project's own
choices. Not instrumented today: nothing counts how many projects run with which
modules; the composition's shape is read from `.scrumia/config.yaml`, not aggregated.

## `extends` is a routing mechanism first

An agent is effective when it reads the minimum it needs — but to read little it must
know **where** the essential of its task is. `extends` exists to answer that, across
projects with disjoint contexts served by the same set of modules: a team inside a
large company, a for-profit monorepo, this plugin repository. Extension — a project
customising or adding to a module's behaviour — is a consequence of that routing, not
its object.

## `extends`

A flat list of plugged modules in `.scrumia/config.yaml`, ESLint-shaped, replacing the
former `composition:` key:

```yaml
extends:
  - scrumia-specs
  - scrumia-github-project
  - scrumia-teams
apps:
  - name: api
    path: apps/api
    extends: [scrumia-impl-rust, scrumia-practice-tdd, scrumia-practice-solid]
```

**The list is not ordered.** ESLint's own `extends` carries last-wins semantics; this
one does not. Any reader brings the ESLint reflex uninvited; this rule exists to
contradict it on first read.

**A module installed but named in no `extends` is inert.** Presence on disk is not
participation: a project may have twenty modules enabled and run the five it names.
That is what makes a module safe to install before deciding to use it, and it is why
the mechanism never asks "is this slot filled" — only "does this project run it".

## `practices` is retired as a named slot

`implementation` and `practices` were always two answers to the same question — how an
app is built — at two granularities. `practices` does not survive as its own key: a
practice module is declared through `extends`, per app, alongside the implementation
module:

```yaml
apps:
  - name: api
    path: apps/api
    extends: [scrumia-impl-rust, scrumia-practice-tdd]
  - name: prototype
    path: apps/prototype
    extends: [scrumia-impl-solidjs]
```

TDD applies to `api`, not to `prototype` next to it, because each app's `extends` list
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

**What a module consumes is declared, not inferred**: the published names it runs and
the registers it reads. The caller declaring its own edges is the provenance nothing had
when a broken call site could only be found by reading prose.

**A name is declared with the source it comes from.** The session PATH is one flat
namespace shared with every enabled plugin, and a naming convention two marketplaces both
follow does not separate them. So a dependency on a name states *whose* — the marketplace
the publishing module ships from — which turns a collision from something nobody notices
into something a check reports. What is *executed* stays the bare name: the source is a
claim to verify, never something to look up in order to decide what to run. Register names
carry no source, because a register is a composition-local concept and not an entry in an
OS-wide namespace.

**The order is the composition's, never a module's.** Project-local first, then the
modules an app extends, then the project-wide ones; required before optional within a
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

Two ways out, and only two:

- **A file another module ships** — the owning module publishes it as a *named
  executable* under its own `bin/`, which the harness puts on the session's PATH with the
  install path already resolved. The caller runs the name and holds no path at all.
- **A document belonging to no module** — a rationale or a spec in the home repository.
  The module inlines what it needs, or cites an absolute public URL. A
  repository-relative link assumes a consuming project has a file it has never had.

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
modules the project runs, and each app with what it extends. What a human reads is the
file, every time, rather than what one session remembered of it.

This is reporting, not resolution. Nothing calls the script to find out who provides
anything; it resolves nothing on any agent's behalf, and BR-4 stands untouched.

It stops there deliberately. It reads the config and only the config, so it cannot tell
whether a module named there is actually enabled, or whether `CLAUDE.md` has gone stale
against it. Those are diagnoses `scrumia-compose` runs and reports around the script's
output — a status printer that guessed at them would be the least trustworthy output in
the composition.

## Business rules

- **BR-1** — A register is a question, not a module. An extension point exists
  independently of whether any installed module currently contributes to it; a register
  nothing extends yields an empty table, which is an answer and not a failure.
- **BR-2** — A module installed but named in no `extends` is inert. Presence is never
  read as participation, and a project's `extends` is the only thing that decides which
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
  memory. A skill that presents the composition closes by running the kernel's status
  script and does not paraphrase the table it prints. Reporting the composition is not
  resolving it: BR-4 still forbids resolving a name to a module at runtime.
- **BR-7** — Every reference a module writes resolves inside that module. A file
  another module ships is reached by running the name that module publishes on
  PATH — never by a path climbing out of the caller's own root — and a document
  belonging to no module is inlined or cited by absolute URL. Running a published
  name is not resolving a slot, so BR-4 stands: the name is constant and greppable,
  and nothing decides at runtime which module answers it.
- **BR-8** — A register is opened by exactly one main skill, and may be extended by any
  number of modules. Two modules opening the same register is a conflict named by the
  check, never arbitrated by list order — `extends` carries no order to arbitrate by.
- **BR-9** — A contribution names no consumer. A module declares what it offers and to
  which register; it does not name, and may not encode, which skill takes it. A key that
  named a consumer would make every cross-cutting module enumerate the modules that could
  ever use it.
- **BR-10** — What a skill applies is contributed as data and rendered on demand, never
  recomposed by the agent from one module's prose about another, and never merged into
  the fragments' content. The table orders contributions; inside a module, that module's
  own routing table orders its files.
- **BR-11** — A module declares the outward edges it depends on — the published names it
  runs, each qualified by the source that publishes it, and the registers it reads — and
  the check reports each one nothing satisfies, including a name whose actual publisher
  ships from another source. A name that is absent is never read as "this module
  contributes nothing": that reading turns a plugin awaiting a restart into a silent claim
  that no rules apply. Qualifying a declaration is not resolving it: what a skill invokes
  is still the bare name, and nothing consults a source to decide what to run.
- **BR-12** — The directive table arbitrates nothing. Two contributions whose prose
  contradicts each other are both printed, in the computed order; resolving them is a
  composition decision a person makes, not one a generator may make silently.

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
