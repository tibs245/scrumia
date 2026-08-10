# ADR-0016 — The specs contract gains a global index, and keys stop freezing values

**Status**: accepted — 2026-08-10 · supersedes [0012](0012-specs-contract.md)

## Context

`features/` holds thirteen features and no way to see them: no file lists what exists,
so an agent that was not handed a pointer discovers a feature only by walking the tree.
#9 asked whether a global index is needed; #193 measured the cost of not having one and
answered yes.

ADR-0012's contract has no name for such a file. Its vocabulary is six keys, declared
"this exact vocabulary and no other", and the block it shows carries the values inline —
which has been read as freezing the *values* too, so that changing the `catalog:` list
looked like it contradicted an accepted ADR. Those are two different kinds of change and
the contract never said so.

## Decision

ADR-0012's mechanism and reasoning stand unchanged — the specs module declares a
Composition block, `scrumia-init` copies it verbatim into `CLAUDE.md`, every consumer
reads it from there and hard-codes nothing. This ADR supersedes it only to state two
things that were missing.

**The vocabulary is seven keys:**

```
specs_root
feature_index
global_index
acceptance_file
ac_id_format
changelog
catalog
```

`global_index` names the file at the root of `specs_root` that lists every feature —
one line each: stratum, status, one-line brief. `scrumia-specs` declares
`global_index: index.md` and generates the file with a committed tool; its validation
fails on any drift between the tree and the index, which is what keeps the promise
"a feature is reachable without a pointer" true past the first sprint.

**Keys are the contract's shape; values are the module's declaration.** Adding,
removing or renaming a *key* changes what every consumer can ask for, and takes an ADR.
Changing a *value* — the files in `catalog:`, the identifier format — is the specs
module evolving its own declaration: it updates its Composition block, `CLAUDE.md`'s
copy is re-synced, and no ADR is involved.

## Consequences

**What we gain**

- A feature is discoverable without walking the tree or holding a pointer, and the
  file that makes it so has a contract name — a consumer says "the file named by
  `global_index`", not `features/index.md`.
- Catalog evolution stops looking like ADR violation. The `specs` module can add
  `security.md` or retire a file by updating its own block, visibly, without touching
  a frozen decision.

**What we accept**

- A generated file lives in the specs tree. It is derived state, and derived state can
  lag: the mitigation is the drift gate in CI, not discipline.
- One more key every replacement specs module must declare, or its consumers degrade —
  the same cost ADR-0012 already accepted, one key wider.
- Projects installed before this ADR carry a six-key block until `scrumia-init` is
  re-run; consumers must treat a missing `global_index` key as "no global index
  declared", not as an error.

## Rejected alternatives

**Status quo — discovery by walking the tree.** The cost is paid on every session by
every agent, and it grows with the tree. Thirteen features already make it the slowest
step of "what exists here?".

**A hand-written index.** It goes stale the first time someone adds a feature under
deadline, and a stale index is worse than none: it is believed. #193's inventory found
fourteen stale `Open issues` references across twelve indexes — the same failure mode,
measured, one level down.

**Listing the features in `CLAUDE.md`.** Wrong owner — the composition table documents
modules, not the specs module's content — and it loads the whole list into every
context whether the session needs it or not.
