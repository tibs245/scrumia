# scrumia-discovery

The discovery slot: scope an idea through challenge before it becomes a ticket, then split
it into the feature tree and the tracker issues that carry it.

## What it answers

Whether an idea is ready to be built, and what it looks like once it is: a validated scope
(problem, audience, outcome, edge cases) turned into a Business → App feature tree and the
tickets a project can actually pick up. Not a document — the point is the human dialogue
that produces shared understanding, not a written brief nobody rereads.

## What it refuses

- No brainstorm that skips the challenge. `scrumia-brainstorm` exists to push back on an
  idea, not to transcribe it.
- No feature tree without a prior scoping. `scrumia-split` works from a completed
  brainstorm or an existing EPIC — never from a raw idea.
- No hardcoded specs or tracker layout. Both skills read the specs and tracker contracts a
  project documents rather than assuming a specific module by name; missing either, they
  degrade rather than fail.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-brainstorm` | Scopes an idea through challenge until it is ready to be split — problem, audience, outcome, edge cases, the legal angle. |
| `scrumia-split` | Turns a completed scoping, or an existing EPIC, into a feature tree and the matching tracker issues, delivered on a `specs/<slug>` branch. |

## What it expects to find

A specs module documented in `CLAUDE.md`'s specs contract, for `scrumia-split` to write
features against — without one, it proceeds with no spec updates. A tracker module and an
authenticated `gh`, to create the issues it lists — without either, the tickets are listed
in the report only. Optionally, business and tech roles that `scrumia-brainstorm` can
delegate a question to.
