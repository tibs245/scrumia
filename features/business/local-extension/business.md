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
| inside the project | that project | `.scrumia/modules/<module>/`, beside the configuration that declares it |

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
  carry.
- **A skill** the project ships to itself, when the thing needed is a procedure and no
  register asks for it.

None of these is a degraded module. A project whose entire local extension is four
directives has extended ScrumIA correctly, and nothing may report that project as having a
malformed module — there is no module there to be malformed.

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
module comes from a shared checkout* is a fact about the project, and it is the fact AC-6
and AC-7 turn on. Where that checkout is, is a fact about the machine.

**The per-machine half lives in `.scrumia/.env.local`, as `SCRUMIA_SHARED_DIR`, and that
file is never committed.** One variable, `KEY=value`, naming the directory the `shared`
source resolves to; a module keyed `shared:acme-conventions` is looked for at
`$SCRUMIA_SHARED_DIR/acme-conventions`. Every reader that turns a declaration into a
location loads it — a resolver that skipped it would report a module absent that the
machine can reach, which is the same lie in the other direction. A reader that only
repeats what the configuration declares resolves nothing and needs nothing.

`SCRUMIA_SHARED_DIR` is an environment variable and not a setting. It carries no value a
module reads, it never appears under `settings:` or a module's `params:`, and it is
outside the cascade those layers form — the cascade configures modules, and this names
where one of them is. An environment already carrying the variable wins over the file, so
a caller can point one run at another checkout without editing a machine's state.

A repository that versions the file has reintroduced exactly the machine path this rule
removes, so its absence from version control is part of the rule and not an operational
detail. A clone arrives without it, which is the correct starting state: the composition
then reports declared absences rather than resolving paths that do not exist on this
machine.

## Where a module is found is stated, never guessed

Resolution reports the location a module came from. Where one declaration could be
answered by two different modules, that is a conflict, and a conflict is reported naming
both — never resolved silently by whichever the search order reached first.

The failure this prevents is specific and expensive: a project that has a local copy of a
published module, diverging from it, with no indication anywhere that the local one is
the one running. The composition then describes a module nobody is executing.

### One name reached twice is not automatically two modules

A rule that fired on the name alone would fire on the ordinary case this feature exists
to support. Someone promoting a module has the published copy installed and a checkout of
it beside them by construction, and `module-authoring`'s BR-3 only makes that move cheap
if having both at once is not a fault. Three situations wear the same name, and they are
three different answers:

| Situation | What it is | What happens |
|---|---|---|
| One module reached by two routes — a checkout symlinked into the project, the same directory named twice | one module | resolved, used, its location reported once |
| A copy in one location while another location holds the same name, and the composition declares which | a choice already made | the declared one resolves; the other is not run, because nothing declares it |
| One declaration answered by two distinct modules | a conflict | reported naming both, neither used |

The first is settled by identity, not by name: two routes reaching the same files are one
module. The second is settled by the declaration — a key states the location it comes
from, so a project running a checkout of a published module says `shared:` and the
published copy is simply a module it does not run. Only the third is undecidable from the
configuration, and it is the only one reported as a conflict.

That is what keeps the conflict rule from firing on promotion: the composition, not the
search, says which location a name comes from.

### A conflict blocks the module, not the composition

The declaration binds nothing — no directive of that module renders, in any register —
and the conflict is named on the error stream every time it is reached. Everything else in
the composition resolves and renders as usual.

It becomes a failure at the one surface whose job is to fail: the dependency check, where
an unresolvable declaration is an unmet dependency and exits non-zero. A conflict that
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
declared absence, naming the module and where it would come from — the same treatment an
empty slot already receives. It never reports it as present, and it never fails.

The consequence is worth stating plainly, because it is the argument against the shared
directory and it should be readable by whoever is choosing it: a module that lives only
on one machine is a module the project cannot be handed to someone else with.

## Business rules

- **BR-1** — A module lives in exactly one of three locations, and is the same artefact
  in each. Resolution finds all three in one pass; each location is a stated place, not a
  tree to search, and inside the project that place is `.scrumia/modules/<module>/`.
- **BR-2** — A module resolved outside a marketplace is held to the anatomy standard
  unchanged. There is no local tier.
- **BR-3** — Local material that is not a module — a directive, a rules section, a skill
  — is legitimate as an end state, not as a stage before becoming one.
- **BR-4** — A project with local material and no local module is correctly extended, and
  nothing reports it as carrying a malformed module.
- **BR-5** — Resolution states the location each module came from.
- **BR-6** — A module's location is its declaration's source, carried in the key rather
  than in a field beside it. Only the filesystem path a `shared` checkout resolves to is
  per-machine, read from `.scrumia/.env.local`, which is never committed and holds no
  setting. No versioned file names a path outside the project.
- **BR-7** — One declaration answered by two distinct modules is a conflict, reported
  naming both locations. Nothing picks between them silently. Two routes to the same
  files are one module, not a conflict, and a name present in a location the composition
  does not declare is not one either — the declaration already chose.
- **BR-8** — A capability reachable only from a location a clone cannot reach is reported
  as a declared absence, naming the module and its origin. It is never reported as
  present and never causes a failure.
- **BR-9** — A conflict blocks the declaration it applies to and nothing else: that
  module contributes no directive anywhere, every other module still resolves, and the
  dependency check exits non-zero on it.

## Vocabulary

- **Location** — where a module's files sit. Not a slot, not a source in a manifest: a
  module has one location and may fill zero or one slot.
- **Local material** — what a project adds without creating a module. Bounded to the
  three shapes above; anything larger is a module and is treated as one.
