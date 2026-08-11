# ADR-0020 — A skill is extended by data, and the table is computed when asked

**Status**: accepted — 2026-08-11

## Context

[ADR-0018](0018-modules-reach-by-name.md) closed the executable case and left the document
case open with only bad answers. A module can *run* another module's script by a published
name. It still cannot tell an agent to *read* another module's document: 0018's only two
exits are **inline it** — which is how `scrumia-specs-find` came to have one provider and
five prose copies, with the copies running — and **cite an absolute URL into this
repository**, which is meaningless in a consuming project that never had these files.

Every prose copy #184's audit measured is a module doing the only thing 0018 left it.

The gap is structural, not editorial. A skill that says *"apply SOLID, apply TDD, apply
the design system"* has to know which of those the project runs, which means either
naming them — and being wrong in every project that runs something else — or describing
them in prose that drifts from the module that owns them. The knowledge lives in one
place; the sentence that commands it lives in another; nothing keeps them equal.

Two mechanisms were reaching for the same job from opposite ends, and neither could finish
it. `scrumia-init` writes a generated region into `CLAUDE.md` — but everything between its
markers is replaced wholesale on the next run, so nothing durable can be added beside it,
and the only way to grow what a project is told is to grow the template for every project
at once. And a first design of this ticket built a per-action document tree, committed and
CI-gated — but its action vocabulary was closed by the kernel, so no module could declare
anything the kernel had not anticipated.

## Decision

**A main skill declares what it is for and stops. What it must apply is contributed by
other modules as data, and rendered into one table at the moment the skill asks for it.**

### A register is a named extension point

A module opens a register in `registers.json` at its own root — the register's name, the
main skill that consumes it, and its purpose. `implement`, `review`, `write-spec`,
`audit`, `convene` are registers this repository's modules open.

**The register vocabulary is open.** It is the union of what the installed modules open,
not a list the kernel hands out. A third-party module can introduce a register nobody had,
and `scrumia-extends --list` is the only honest answer to which registers exist in a given
project.

### An extension is a data file, and nothing else

A module contributes in `extends.json`, keyed by register, each entry carrying `name`,
`type`, `when`, `summary` and `read` — a path **inside the contributing module**.

**Nothing in that file names a consumer.** A module declares what it offers; it never
declares, and cannot encode, which skill will take it. That is what lets one fragment
serve implementation, review and audit without being written three times, and it is why
adding an implementation module does not require reopening every practice module.

**No executable is involved.** A module is discovered through `$PATH`: the harness
prepends `<pluginRoot>/bin` for every enabled plugin, with the install path — version
segment included — already resolved, so the parent of such an entry is a module root. This
generalises ADR-0018's mechanism 1 from *"the harness resolves a name I wrote"* to *"the
harness tells me which modules are here"*. An extension is therefore one JSON file: no
shim to publish, no logic to maintain, nothing that can be wrong except the data.

### What a module runs is declared, not inferred

`dependencies.jsonl` lists the published names a module executes, one per line — a flat
list, where a keyed object would wrap a single array in ceremony. The caller declares what
it calls — which is the provenance nobody had, and the reason a broken call site could
only ever be found by reading prose.

**Registers are not declared here.** A draft carried a second list naming the registers a
module consults; it was dropped before this ADR was accepted. Opening a register is
already the promise to consult it, so the two lists were the same set — and where they
differed, the shorter one hid the very defect the check exists for. The set that carries
the promise is `registers.json`, and it is the one the check runs over.

**A name is declared with its source**: `tibs245/scrumia:scrumia-board`. ADR-0018 records
that the session PATH is "one flat namespace shared with every other enabled plugin" and
answers it with a `scrumia-` prefix — a convention, which two marketplaces both following
it do not resolve. Qualifying the *declaration* makes the collision checkable: the check
resolves the bare name, finds the module that publishes it, and compares that module's own
declared source against the one the caller claimed.

**What is executed stays the bare name.** The qualification is a claim, not an invocation,
and ADR-0018's mechanism is untouched. Nothing looks a source up to decide what to run;
a mismatch is reported, never routed around — routing around it would be the capability
registry, arriving through the back door.

### The table is computed when asked, and stored nowhere

`scrumia-extends <register> [--app <name>|--path <file>]` reads the project's `extends`,
collects the contributions of the modules the project actually runs, and prints one table.

**There is no artefact.** Nothing is written, nothing is committed, nothing is gated for
drift, and nothing can be stale — which is the failure mode the alternative design spent
a digest, a `check` command and a CI job to contain.

**Order comes from the composition, never from a module ranking itself**: project-local
(`.scrumia/extends.json`) first, then the modules the app extends, then the project-wide
ones; `required` before `optional` within a tier. This is ADR-0010's "specific beats
generic, the project override beats both", expressed where the project can see it.

**The table does not arbitrate.** Two directives whose prose contradicts each other are
both printed. A generator cannot read English; what changed is that they are now in one
document, which they never were.

## Position against ADR-0009

This **amends ADR-0009**, and it is worth saying plainly rather than arguing around:
*the table is computed at call time.* 0009's "resolution at composition time, never at
call time" no longer holds for what a skill loads.

What 0009 actually rejected still stands, and is not what happens here. Its objection to
the capability registry was that **"the agent must keep in mind that 'creating a ticket'
goes through a verb pointing to a module it cannot see"** — the cost being an invisible
indirection paid on every call. Here:

- **No verb resolves to a module.** Nothing selects a provider. Every module the project
  runs contributes, and all of them are printed. There is nothing to keep in mind, because
  nothing is hidden: the table names each module and each file path.
- **The mechanism stays inspectable by a human**, which is 0009's own criterion for
  preferring a documented composition — `scrumia-extends --list`, `--check`, and the data
  files themselves are all readable, and there is no cache between them and the answer.
- **0009's stated most-likely flaw is removed, not mitigated**: *"`CLAUDE.md` can diverge
  from the configuration."* Nothing is copied into `CLAUDE.md` any more, so there is
  nothing there to diverge. The generated region names the tool; the tool reads the
  configuration.

The cost this buys back, honestly: the answer now depends on the environment at the moment
of the call. A plugin enabled but not restarted into is absent from `$PATH` and therefore
contributes nothing — silently, unless `--check` is run. That is the price of having no
artefact, and it is the one this decision accepts.

## Consequences

**What we gain**

- A skill's directives grow with the project's composition without the skill being edited,
  which is what neither the `CLAUDE.md` template nor a prose copy could do.
- One fragment, several registers: implementation, review and audit read the same file
  with a different obligation, instead of three copies drifting apart.
- An extension is data. Writing one requires no bash, no knowledge of install layout, and
  no knowledge of who consumes it.
- A missing dependency has a name and a check, where before it had neither.

**What we accept**

- **`$PATH` discovery is load-bearing for the whole mechanism**, not for two call sites.
  A harness that stops putting plugin `bin/` directories on `PATH` breaks every register
  at once. `$SCRUMIA_MODULE_DIR` is the documented override, and is what this repository
  and CI use — which also means CI can only ever exercise the override, never the
  product's own path. That is the same asymmetry ADR-0018 recorded, now wider.
- **A skill that opens a register and never runs the tool reads as covered and applies
  nothing.** No check can see it, because the check reads declarations, not behaviour.
- **Two modules opening the same register is ambiguity**, reported by `--check` and not
  resolved by the tool.
- **The table's freshness is real and its correctness is not.** A `summary` that no longer
  describes its fragment is invisible to everything — the same class of drift as before,
  moved from a paragraph into a field, where at least it is one line and beside the path
  it describes.

## Rejected alternatives

**A built, committed assembly per action** — the first design of this ticket. A tool wrote
one document per action into `.scrumia/assemblies/`, digest-stamped, with a `check`
command and a CI gate. Rejected for two reasons that compound: the action vocabulary had
to be closed by the kernel for the coverage arithmetic to mean anything, so no module
could declare anything unanticipated; and the artefact bought determinism the mechanism
did not need, at the cost of a staleness class that had to be detected, refused, explained
and re-run. Computing a table from data files is cheap enough that storing the result is
what creates the problem.

**Growing the `CLAUDE.md` template instead.** The generated region is replaced in full on
every `scrumia-init` run, so anything durable must live in the template — which means
every project gets it, whether it runs the module or not. That is the opposite of a
composition.

**Keying an extension by the skill it extends** (`scrumia-rust:implement`, or
`scrumia-rust`). Rejected on the module author's side: a cross-cutting practice would have
to enumerate every implementation skill that exists, and a new implementation module would
force every practice module to be reopened — which is the one-provider-five-copies defect
in a new spelling. A module declares what it offers; who takes it is not its business.

**Merging the fragments' content into one document rather than listing them.** Rebuilds
the monolith ADR-0011 rejected, and promotes the drifting-copy defect into a build output.

## To revisit

- If two modules opening the same register turns out to be a legitimate shape rather than
  a mistake, the check that reports it is what has to change first.
- If `type` and `when` being open vocabularies produces enough near-synonyms to make the
  table hard to read, close them — the checker is the only thing that would need to move.
