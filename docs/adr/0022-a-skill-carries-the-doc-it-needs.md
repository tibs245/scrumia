# ADR-0022 — A skill carries the doc it needs, and `docs/` points inward

**Status**: accepted — 2026-08-16

## Context

[ADR-0018](0018-modules-reach-by-name.md) gave a reference leaving a module two
mechanisms, and only two: a name another module publishes under its `bin/`, or — for
"a document belonging to no module" — inlining, or an absolute URL into this repository.

That second mechanism was written for this repository's ADRs and features, which belong to
no module. It has since become the default answer to a different question: *what does a
skill do about a rule it needs that is written in `docs/` or `features/`?* Re-enumerated
against the tree, `plugins/` carries **50** markdown links into this repository's `docs/`
or `features/`, across eight modules, plus roughly twenty more of the same act written as
bare backticked paths. `#169`, `#223` and `#224` each opened on a slice of it and each
counted a different total, because each was scoped to one class in a couple of modules.

Two answers were weighed on `#224` before this decision, and both argued about the
reference's **form**:

- **Allow a relative path.** It resolves in this repository and nowhere else. Installed, a
  module sits at `~/.claude/plugins/cache/<marketplace>/<module>/<version>/`, whose parent
  holds only sibling modules — no `docs/`, no `features/`. The link is dead for every
  consumer.
- **Keep the absolute URL, restate the operative content inline, and let the link carry
  only provenance.** Better, and still wrong in one respect: the URL names `blob/main`, so
  a project reads whatever this repository's `main` says today rather than the version it
  installed. A module that ships versioned then depends on something that does not.

Neither addressed the reference's **direction**.

## Decision

**A document a skill needs to do its work is documentation internal to the module, and it
ships and versions with it.** Not cited, not restated with a link beside it: carried.

**The official documentation may point at a module's doc. A module pointing at `docs/` or
`features/` for something it needs is what this decision refuses.** The reference direction
is `docs/` → module, never module → `docs/`.

The test is what the reader loses when the target is unreachable:

| The target carries | Then |
|---|---|
| a rule, a method, a refusal the skill applies | it belongs to the module; move it in |
| the *reason* a rule is what it is, and the skill states the rule itself | it may stay outside, and the absolute URL is how it is cited |
| an external source nobody can vendor — MDN, W3C, a licence | it stays outside, cited with its licence |

**This is a rule about the act, not about link syntax.** A backticked path in prose and a
markdown link are the same act; ruling on the link alone would leave the act legal in the
form that is harder to see and would reach two modules instead of eight.

**What lands where.** `features/business/module-anatomy/` owns the rule, because it is the
feature that says what shape a module takes inside itself;
`features/business/module-authoring/` states none of it, as its own index already promises.
`scrumia-author` applies it when a module is written, and `scrumia-module check` is where it
becomes enforceable.

## Consequences

**What we gain**

- A module is complete on the machine it is installed on. What its skills apply travels
  with them, at the version the project chose.
- The versioning story stops having a hole in it. `features/business/release-versioning/`
  can promise what a bump means for a module's content, which it could not while part of
  that content lived on another repository's `main`.
- One rule covers the linked citations and the bare-path ones, which no form-shaped rule
  could.

**What we accept**

- **Duplication between a module's doc and this repository's.** Deliberate, and the
  direction is what keeps it honest: the module's copy is the one that runs, `docs/` points
  at it, and there is one authority rather than two texts drifting toward each other.
- **The 50 existing citations are debt, not a defect to fix in the change that names
  them.** Migrating them touches eight shipped modules and costs each a version bump; it is
  `#224`'s to sequence, and this ADR does not schedule it. Until it lands, the absolute URL
  remains the least-bad form for what has not moved yet, and `CLAUDE.md` says so.
- **Nothing enforces this on the day it is accepted.** Neither `tools/validate.py` — it
  skips relative-link resolution inside `plugins/` and delegates containment — nor
  `scrumia-module check` reports a reference leaving a module today, which was verified by
  planting one. The rule is written before its guard, and that order is stated rather than
  discovered.

## Rejected alternatives

**Allowing a relative path out of a plugin.** It resolves only in this repository. Every
consuming installation gets a dead link, and the failure is silent — nothing reads a
markdown link to check it.

**Keeping the absolute URL and restating operative content inline.** This was `#223`'s
shape and it is a real improvement over a bare link, but it leaves the module depending on
another repository's `main` for the half it did not restate, and it answers per-citation
what is one question about the module.

**Ruling on link syntax only.** Cheaper to enforce and it would have covered two modules of
the eight. The same act written as a backticked path would have stayed legal, which is the
form most of the debt is already in.

## Amends

This ADR **amends [ADR-0018](0018-modules-reach-by-name.md) on its second mechanism.** 0018
offers inlining or an absolute URL for "a document belonging to no module". That stands —
what this adds is the question asked first: *should* this document belong to no module? Where
a skill needs it, the answer is that it belongs to the module, and it moves rather than being
cited. 0018's first mechanism — a file another module ships is reached by a published name —
is untouched.

## To revisit

If a doc turns out to be needed, unchanged, by several modules at once, the copies become
the cost this decision accepted rather than the one it avoided. That is the point to ask
whether it is a module of its own — `features/business/module-authoring/`'s threshold
question — and not a reason to reopen the direction.
