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

| Location | Reach |
|---|---|
| a marketplace | anyone who declares it |
| a directory of checkouts shared between a person's projects | that person's projects |
| inside the project | that project |

Resolution finds all three, and a module found in any of them is held to the anatomy
standard unchanged. There is no local tier and no relaxed variant: a module that would
fail the check in a marketplace fails it inside a project, and for the same reasons.

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
directives has extended ScrumIA correctly, and a checker must not report that project as
having a malformed module — there is no module there to be malformed.

Where a project-local directive sits relative to a module's, and which wins, is
`modular-composition`'s and is stated there.

## Where a module is found is stated, never guessed

Resolution reports the location a module came from. Two modules answering to the same
name in two locations is a conflict, and a conflict is reported naming both — never
resolved silently by whichever the search order reached first.

The failure this prevents is specific and expensive: a project that has a local copy of a
published module, diverging from it, with no indication anywhere that the local one is
the one running. The composition then describes a module nobody is executing.

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
  in each. Resolution finds all three.
- **BR-2** — A module resolved outside a marketplace is held to the anatomy standard
  unchanged. There is no local tier.
- **BR-3** — Local material that is not a module — a directive, a rules section, a skill
  — is legitimate as an end state, not as a stage before becoming one.
- **BR-4** — A project with local material and no local module is correctly extended, and
  nothing reports it as carrying a malformed module.
- **BR-5** — Resolution states the location each module came from.
- **BR-6** — Two modules answering to one name is a conflict, reported naming both
  locations. Nothing picks between them silently.
- **BR-7** — A capability reachable only from a location a clone cannot reach is reported
  as a declared absence, naming the module and its origin. It is never reported as
  present and never causes a failure.

## Vocabulary

- **Location** — where a module's files sit. Not a slot, not a source in a manifest: a
  module has one location and may fill zero or one slot.
- **Local material** — what a project adds without creating a module. Bounded to the
  three shapes above; anything larger is a module and is treated as one.
