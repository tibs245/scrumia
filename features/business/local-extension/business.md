# Local extension — business rules

## Value

For a project that needs ScrumIA to do something no published module does, and for a
person who has the same house rules across every project they run. It brings three
declared places a module may live, one resolution that finds all three, and an explicit
answer to the question that precedes them: whether a module was needed at all. It matters
because the alternative to extending locally is forking the marketplace, and a fork stops
receiving everything it did not fork for. Measurable: the number of steps between having
a module on disk and having it appear in a register's table, which is expected to be one
declaration and nothing else.

## Three locations, one artefact

A module lives in exactly one of three places, and is the same thing in all three:

| Location | Reach | Found at |
|---|---|---|
| a marketplace | anyone who declares it | wherever the harness installed it, which it makes reachable |
| a directory of checkouts shared between a person's projects | that person's projects | one `<module>/` per entry in the directory the machine names |
| inside the project | that project | `modules/<module>/`, beside the configuration that declares it — `.scrumia/modules/` where the configuration is where it usually is |

Resolution finds all three **in one pass, not one instead of another**, and a module found
in any of them is held to the anatomy standard unchanged. There is no local tier and no
relaxed variant: a module that would fail the check in a marketplace fails it inside a
project, and for the same reasons.

The in-project location is a stated path rather than a place to search for one. A project
that had to be scanned for modules would answer differently depending on what else it
holds, and a module could be adopted by being copied somewhere — which is the opposite of
a composition that says what it runs.

This is what makes moving between locations free — the rule is `module-authoring`'s, and
it is only affordable because this feature refuses to make a local module a different
kind of thing.

## Not everything worth writing is a module

Most of what a project needs to add is smaller than a module, and creating one for it is
the expensive answer. Three shapes exist below it, and each is legitimate on its own
terms rather than as a stepping stone:

- **A directive** the project contributes to a register it did not open. It reaches every
  skill that consults that register, and it is data — no skill, no version, no
  installation.
- **A rules section** the project owns, when a topic has grown past what one file can
  carry. It is a fragment like any a module ships — `modular-composition`'s word for the
  file a directive points at — owned by the project and named by a project-local directive,
  so it needs no home of its own, and one no directive names is an ordinary document rather
  than a defect.
- **A skill** the project ships to itself, when the thing needed is a procedure and no
  register asks for it.

None of these is a degraded module. A project whose entire local extension is four
directives has extended ScrumIA correctly, and nothing may report that project as having a
malformed module — there is no module there to be malformed. The anatomy standard is a
property of a module's own tree, so a project holding none presents it nothing to judge:
the directory the configuration sits in is not a module, and no surface reads it as one.

This is the list `knowledge-placement` routes toward when its answer is "the project". It
is stated here and nowhere else.

Where a project-local directive sits relative to a module's, and which wins, is
`modular-composition`'s and is stated there.

## Declared by name, resolved by the environment

A module's origin is part of its name. The configuration keys each module
`<source>:<module>` — `<owner>/<repo>` for a marketplace, `shared`, or `local` — so the
three locations above are the three sources, and there is no second field that could
disagree with the first. The key's grammar is `modular-composition`'s
([ADR-0021](../../../docs/adr/0021-modules-keyed-by-source.md)); which locations exist is
this feature's.

What the key does **not** carry is where a `shared` checkout sits on a given machine.

| Declared, versioned, travels with the clone | Resolved per machine, never versioned |
|---|---|
| `local:acme-docs-rules` — name and source in one key | the filesystem path `shared` resolves to |

The split exists because both halves of the problem are real and they pull opposite ways.
A configuration that names an absolute path outside the project puts one machine's layout
into a versioned file, and is the runtime resolution [ADR-0009](../../../docs/adr/0009-documented-composition.md)
rejected. A configuration that names nothing leaves the composition unreadable: two
machines produce two different answers and neither file says so.

Naming the module and its origin gives a reader the composition's full intent — *this
module comes from a shared checkout* is a fact about the project, and it is the fact both
the declared absence and the honesty rule below turn on. Where that checkout is, is a fact
about the machine.

**The per-machine half lives in `.scrumia/.env.local`, as `SCRUMIA_SHARED_DIR`, and that
file is never committed.** One variable, `KEY=value`, naming the directory the `shared`
source resolves to; a module keyed `shared:acme-conventions` is looked for at
`$SCRUMIA_SHARED_DIR/acme-conventions`. Every reader that turns a declaration into a
location loads it — a resolver that skipped it would report a module absent that the
machine can reach, which is the same lie in the other direction.

A reader that only repeats what the configuration declares resolves nothing and needs
nothing, **and must not phrase its output as presence**. A list of declarations headed
*the modules this project runs* claims exactly what that reader did not check, and it is
how one tool comes to say a module runs while the other says it cannot be reached — which
is the asymmetry this rule exists to forbid, arriving through wording instead of through a
missing file. It says what it did: these are the modules this project **declares**.

`SCRUMIA_SHARED_DIR` is an environment variable and not a setting: it carries no value a
module reads, so it is outside the settings cascade entirely — what that cascade's layers
are is `modular-composition`'s BR-14 and is not counted here. The distinction worth
drawing is with its neighbour, because the two are easy to confuse and are gitignored for
the same reason:

| | Holds | Answers |
|---|---|---|
| `.scrumia/config.local.yaml` | this machine's values | what a module is configured with |
| `.scrumia/.env.local` | this machine's paths | where a module is |

An environment already carrying the variable wins over the file, so a caller can point one
run at another checkout without editing a machine's state. A file that sets nothing, or
names a directory that is not there, is reported — read as an empty location it would take
every `shared:` module with it, and every register would simply render shorter.

A repository that versions the file has reintroduced exactly the machine path this rule
removes, so its absence from version control is part of the rule and not an operational
detail. A clone arrives without it, which is the correct starting state: the composition
then reports declared absences rather than resolving paths that do not exist on this
machine.

## Where a module is found is stated, never guessed

Resolution reports the location a module came from. Where one declaration could be
answered by two different modules, that is a conflict, and a conflict is reported naming
both directories — never resolved silently by whichever the search order reached first.
Both may sit in one location, and often do: a fork checked out beside the module it
forked answers the same name from the same place.

The failure this prevents is specific and expensive: a project that has a local copy of a
published module, diverging from it, with no indication anywhere that the local one is
the one running. The composition then describes a module nobody is executing.

### One name reached twice is not automatically two modules

A rule that fired on the name alone would fire on the ordinary case this feature exists
to support. Someone promoting a module has the published copy installed and a checkout of
it beside them by construction, and `module-authoring`'s BR-3 only makes that move cheap
if having both at once is not a fault. Four situations wear the same name, and they are
four different answers:

| Situation | What it is | What happens |
|---|---|---|
| One module reached by two routes — a checkout linked into the project, the same directory reached twice | one module | resolved, used, its location reported once |
| A copy in one location while another location holds the same name, and the composition declares which | a choice already made | the declared one resolves; the other is not run, because nothing declares it |
| A declaration that names no location, answered in more than one location, one module each | a shadow | the narrowest location wins, is used, and is reported with the others |
| One declaration answered by two distinct modules in the location it names | a conflict | reported naming both directories, neither used |

The first is settled by identity, not by name: two routes reaching the same files are one
module. The second is settled by the declaration — a key states the location it comes
from, so a project running a checkout of a published module says `shared:` and the
published copy is simply a module it does not run. Only the last is undecidable, and it is
the only one reported as a conflict.

The third exists because a declaration is not always able to choose: the retired list shape
names modules without their source, and refusing to run one would punish a project for a
grammar it is being migrated off. **The narrowest location wins** — inside the project over
a shared checkout, a shared checkout over a marketplace — on the same "specific beats
generic" the composition uses everywhere else. It is stated rather than inherited from a
search, it is reported every time it applies, and the report names the fix: key the
declaration by source. A search order settles a name only where the composition declined
to, and never quietly.

### A conflict blocks the module, not the composition

The declaration binds nothing — no directive of that module renders, in any register —
and the conflict is named on the error stream every time it is reached. Everything else in
the composition resolves and renders as usual.

It becomes a failure at the surface that judges the composition: the dependency check,
where an unresolvable declaration is an unmet dependency and exits non-zero. No other
surface reading the composition fails on it — the reconciliation below refuses a sentence
someone wrote, which is a different object. A conflict that
only shortened a table would be a module silently missing from a register — the failure
mode this whole section exists to end — and one that stopped every skill would make an
ambiguity in one module a project that cannot be worked in.

## A clone without the local material must still be told the truth

Local material is, by construction, invisible to anyone who does not have it. A shared
checkout directory is on one machine; a module inside a project travels with the project,
a directive travels with the project, a person's shared directory travels with nobody.

What follows is a rule about honesty rather than about mechanism: **what a project's
`CLAUDE.md` claims must remain true for someone who clones it without any of it.** Where
a capability comes from a location a clone cannot reach, the composition reports it as a
declared absence, naming the module and the source its key states. It never reports it as
present, and it never fails.

Two comparisons carry that, and they answer different questions:

| What is compared | Against | Answers |
|---|---|---|
| every declaration the configuration makes | the roots resolution found | which capabilities this machine actually has |
| the text of each `CLAUDE.md` in the declaration's scope (the root file, or that app's stub) | the state each declaration resolved to | whether that file's claims are true for whoever is reading it |

The first is what makes a declared absence sayable at all. The second is what makes it
sayable about the one file an agent reads before it knows anything else — a file written
on one machine and read on every other, so its claims outlive the environment that made
them true. A row naming a capability by its bare name promises it; naming it by the
declaration key states the module and its source at once, which is the same fact the
absence report carries, and offers the reader an origin it can check rather than a
capability it cannot.

The second comparison runs once per file in the declaration's scope, not once per file at
all — the root file's claims are read against project-wide declarations, an app's stub
against that app's. An app stub names the modules the app extends, and the reader of that
stub is the app's reader, so what the stub claims is held against that app's declarations
and not against the project's. `scrumia-init` writes that stub; the reconciliation covers
it the same way it covers the root file.

Only one source needs that. A module comes from a marketplace anyone may install from, or
from inside the project where it arrives with the clone — and where one of those is missing
it is missing for every reader alike, author included, which is a module to restore rather
than a sentence to correct. A shared checkout is the location that travels with nobody, so
it is the only one whose absence is the reader's alone, and the only one where a bare name
in that file is a promise to a reader who has no way to keep it. That is the cost of the
location, arriving where it is least expected.

Neither comparison reads English, and neither is asked to. One matches names, the other
matches declarations against directories; the sentence a human writes around a module is
the human's, and no tool is trusted to grade it.

The consequence is worth stating plainly, because it is the argument against the shared
directory and it should be readable by whoever is choosing it: a module that lives only
on one machine is a module the project cannot be handed to someone else with.

## Business rules

- **BR-1** — A module lives in exactly one of three locations, and is the same artefact
  in each. Resolution finds all three in one pass; each location is a stated place, not a
  tree to search, and inside the project that place is `modules/<module>/` beside the
  configuration that declares it.
- **BR-2** — A module resolved outside a marketplace is held to the anatomy standard
  unchanged. There is no local tier.
- **BR-3** — Local material that is not a module — a directive, a rules section, a skill
  — is legitimate as an end state, not as a stage before becoming one. Material a
  module's contract in `CLAUDE.md` declares is not local material, and this feature's
  enumeration does not cover it: it lives by the contract that names it, and reading
  it is the contract's responsibility.
- **BR-4** — A project with local material and no local module is correctly extended, and
  nothing reports it as carrying a malformed module.
- **BR-5** — Resolution states the location each module came from. Where more than one
  answers a declaration that named none, the narrowest is the one used and the one
  reported, and the others are named alongside it.
- **BR-6** — A module's location is its declaration's source, carried in the key rather
  than in a field beside it. Only the filesystem path a `shared` checkout resolves to is
  per-machine, read from `.scrumia/.env.local`, which is never committed and holds no
  setting. No versioned file names a path outside the project. A reader that resolves
  nothing does not phrase its output as presence.
- **BR-7** — One declaration answered by two distinct modules is a conflict, reported
  naming both directories. Nothing picks between them silently. Three cases are not
  conflicts: two routes to the same files are one module; a name present in a location
  the composition does not declare is a module it does not run; and a declaration naming
  no location, answered by one module in each of several locations, is a shadow — the
  narrowest wins, is used, and is reported with the others and with the fix. Where the
  narrowest is itself ambiguous — two of the answers sharing a location — nothing is
  narrowest and it is a conflict again.
- **BR-8** — A capability reachable only from a location a clone cannot reach is reported
  as a declared absence, naming the module and its origin. It is never reported as
  present and never causes a failure. `CLAUDE.md` is held to the same rule by comparison
  rather than by prose: where this composition declares a module from a location a clone
  cannot reach, a file naming it by its bare name is a claim that reader cannot check, and
  the file states that module's source — its declaration key — or makes no claim about it.
  A module absent from a location every clone can reach is not that: there it is missing
  for every reader alike, which is a module to restore rather than a sentence to correct.
  What may fail is the reconciliation, and what it reports belongs to the file, never to
  the absence. The reconciliation runs once per file in the declaration's scope — the
  root file for project-wide declarations, the app's stub for that app's — and a
  declaration neither file mentions is a claim the composition makes that nobody has
  stated; the file in whose scope it sits is where it would have been said.
- **BR-9** — A conflict blocks the declaration it applies to and nothing else: that
  module contributes no directive anywhere, every other module still resolves, and the
  dependency check exits non-zero on it.
- **BR-10** — A declaration whose source resolves but whose module is no longer present
  at that source is a withdrawn declaration. The dependency check names the module, the
  source the declaration's key states, and the marketplace action — and exits non-zero,
  with the same consequence as an unresolvable declaration (BR-9). The notice is owed by
  `features/business/release-versioning/`, not invented here: that feature states what a
  withdrawn module owes at its last release and counts the window in published versions,
  and this feature states only the surface the declaration's resolution lands on.

## Vocabulary

- **Location** — where a module's files sit. Not a slot, not a source in a manifest: a
  module has one location and may fill zero or one slot.
- **Local material** — what a project adds without creating a module. Bounded to the
  three shapes above; anything larger is a module and is treated as one. Material a
  module's contract in `CLAUDE.md` declares — the `specs_root` `scrumia-specs`
  names, the `design_root` `scrumia-design` names, and any other contract-defined
  root — is not local material: its shape is the contract's, and the contract names
  the file the contract itself is filed in.
