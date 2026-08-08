# Modular composition — business rules

## Why a composition rather than a method

A method that answers every project-steering question as one block forces a project
to take everything or leave everything. In practice a project takes it, adapts it,
diverges from it, and ends up on a fork that no longer receives updates.

ScrumIA separates the questions into slots (see `index.md`) and lets a project
answer each independently, by picking a module or leaving the slot empty. What is
meant to be reusable is this separation — not the specific answers the reference
modules give. See [ADR-0001](../../../docs/adr/0001-distribution-as-plugins.md),
[ADR-0007](../../../docs/adr/0007-single-base-repo.md) and
[ADR-0009](../../../docs/adr/0009-documented-composition.md).

## What a module owes to be pluggable

Three things, no more:

1. **A `SKILL.md`** — the module's own entry point, and the place it documents its
   contract with the rest of the composition: the settings it reads, and the one
   sentence (`CLAUDE.md` line) that tells an agent what it must know about the
   module without opening it. A module with no `SKILL.md` cannot be composed —
   there is nothing for `scrumia-init` to point an agent to.
2. **A scope** — the slot it fills, an existing one or a new one it defines and
   documents, plus the settings key(s) it owns under `settings.<slot>`. A module's
   authority stops at that boundary: it does not decide what another slot's module
   decides.
3. **The rule that it never assumes another module is present.** If a module needs
   a capability that lives in another slot, it checks for it rather than assuming
   it, and if the slot is empty or unfilled it names the gap and proposes the next
   step instead of failing outright or guessing a substitute behavior.

A module that skips any of the three still runs, until the day a project composes
it with a different set of modules than the one it was written against — at which
point it breaks silently, which is the failure this rule exists to prevent.

## Distribution is what makes composition cheap

A project adopts a module by declaring it, not by copying it. Two keys in a
project's own `.claude/settings.json` — `extraKnownMarketplaces` and
`enabledPlugins` — are enough; nothing is duplicated into the project repo. This
rides on Claude Code's native plugin marketplace rather than a bespoke installer,
because ScrumIA deliberately targets Claude Code alone (ADR-0001).

All of ScrumIA's own modules live in this one repo, which is also the marketplace
(ADR-0007). A cross-cutting change to the composition — this feature is one — fits
in a single, atomic PR instead of coordinating releases across several repos. A
third-party module remains possible without changing this structure:
`marketplace.json` accepts external sources (`github`, `git-subdir`, `npm`,
`archive`) alongside the relative paths used for ScrumIA's own plugins.

## How modules connect to each other

**Through generated documentation, never through dynamic resolution.**
`scrumia-init` reads `.scrumia/config.yaml` and writes, between markers in
`CLAUDE.md`, a table naming which module fills which slot and what an agent must
know about it before reading the module itself. Agents read that table like any
other project context.

The rejected alternative was a capability registry: each module declaring verbs
(`ticket.create`, `spec.read`) that a core resolves to whichever module is plugged
in. It would have decoupled modules completely, but at a cost paid on **every**
call — the agent holding an indirection in mind for something that changes a
handful of times in a project's life. Documented composition pays that cost once,
at context load, instead (ADR-0009).

The rule that follows from this choice: **a module cites another by name in
prose**, in its own `SKILL.md` or `CLAUDE.md` line — "the tracker module", or the
module's own name when the sentence needs it — never through a runtime lookup.
Replacing a module means checking the others that name it; that check is a few
minutes of grep, done rarely, not a per-call cost.

## How the composition is reported

A composition an agent retypes is a composition that drifts, and the drift is
invisible because the prose still reads plausibly. So the skills that present the
composition — `scrumia-init` and `scrumia-compose` — end by running
`scrumia-core`'s `scripts/compose-status.sh`, which reads `.scrumia/config.yaml`
and prints the slot table itself: the module in each slot, and, worded
differently from one another, the slots left empty on purpose and the keys
missing altogether. What a human reads is the file, every time, rather than what
one session remembered of it.

This is reporting, not resolution. Nothing calls the script to find out who fills
a slot; it resolves nothing on any agent's behalf, and BR-4 stands untouched. It
makes the answer BR-4 already documents legible in a terminal, which is a
different job from looking that answer up at runtime.

It stops there deliberately. It reads the config and only the config, so it
cannot tell whether a module named there is actually enabled, or whether
`CLAUDE.md` has gone stale against it. Those are diagnoses `scrumia-compose`
runs and reports around the script's output — a status printer that guessed at
them would be the least trustworthy output in the composition.

## Business rules

- **BR-1** — A slot is a question, not a module. The slot exists independently of
  whether any module currently fills it.
- **BR-2** — An empty slot is declared, not omitted. `.scrumia/config.yaml` sets it
  to `null` explicitly; a missing key is a configuration defect, not "no module".
- **BR-3** — A module never assumes another slot is filled. It checks, and on
  finding the slot empty or the module documenting it absent, it names the gap in
  a message a human or an agent can act on, and proposes the next step, rather than
  failing or silently changing behavior.
- **BR-4** — A module cites another by slot name where it can, by module name only
  where the sentence needs the specific one. Nothing resolves a slot to a module at
  runtime; the resolution is the `CLAUDE.md` table, generated once and re-read on
  every session.
- **BR-5** — ScrumIA's own modules ship from a single repo, which is also the
  marketplace. A third-party module is not required to: it declares its own source
  in `marketplace.json`, at the adopting project's discretion.
- **BR-6** — The composition is reported by reading `.scrumia/config.yaml`, never
  from memory. A skill that presents the composition closes by running the
  kernel's status script and does not paraphrase the table it prints. Reporting
  the composition is not resolving it: BR-4 still forbids resolving a slot to a
  module at runtime.

## Vocabulary

The word for a question is **slot**, never "area". "Slot" carries BR-1 in its name —
a question that exists whether or not anything currently answers it. "Area" reads as
a section heading and loses that: it suggests a fixed region of the project rather
than a question a project can leave open. Every table that names slots — including
the composition table `scrumia-init` writes into `CLAUDE.md` — uses "Slot" as its
header, not "Area", and "area" appears nowhere in this composition's vocabulary as a
synonym.
