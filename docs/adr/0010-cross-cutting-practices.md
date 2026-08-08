# ADR-0010 — Cross-cutting practices as composable modules

**Status**: accepted — 2026-08-07

## Context

An implementation module's contract covers four points: how we test, which design principles, how the code is structured, what we refuse. While writing `scrumia-impl-rust` and `scrumia-impl-solidjs`, a finding: some answers are not specific to one technology. TDD answers "how we test" the same way in Rust and in SolidJS — only the tooling and the examples change. SOLID answers "which design principles" with the same need for application limits everywhere.

Duplicating those answers in every implementation module guarantees their divergence. What remained to be decided was how to share them.

Three designs were on the table.

**Child plugins with declared dependencies.** An implementation module declares it depends on `scrumia-practice-tdd`; installing it installs its children. This is the most visible composition, but it relies on a mechanism Claude Code plugins do not have — it would have had to be emulated in the install skills. Above all, it contradicts the founding prohibition: *a module never assumes another is present*.

**Deliberate duplication.** Each implementation module embeds its TDD section, its SOLID section. Simple, self-contained — and wrong from the second fix onward: an improvement to the TDD chapter would have to be propagated to N modules, and it will not be.

**A `practices` slot, multiple and per app.** A practice becomes an ordinary module, occupying a new slot under the same regime as `implementation`: several modules at once, plugged in app by app. The implementation module stays purely technological and **situates** the practice for its technology — a conditional section: "if `scrumia-practice-tdd` is plugged in on this app, here is how the cycle is tooled in Rust".

## Decision

**The `practices` slot**, multiple and per app.

```yaml
apps:
  - name: api
    path: apps/api
    implementation: scrumia-impl-rust
    practices: [scrumia-practice-tdd, scrumia-practice-solid]
```

`scrumia-init` carries the practices into the "Implementation per app" table of `CLAUDE.md`. The agent about to code loads the app's implementation module **and** its practices — that is the documented composition of ADR-0009, nothing more.

A practice module follows four rules:

1. **It refines a named point of the implementation contract** — "how we test" for TDD, "which design principles" for SOLID. A practice that answers everything is not a practice, it is a methodology.
2. **It works on its own** — on an app without an implementation module, the practice applies with the conventions of the surrounding code.
3. **It provides three skills**: the reference (loaded before writing code), the audit (finding the gaps), the refactor (closing a found gap).
4. **It documents its settings** under `settings.practices.<module>`.

And one precedence rule, the only one: **specific beats generic**. When an implementation module contradicts a practice — SOLID recommends dependency inversion, `scrumia-impl-rust` refuses it between modules of the same crate — the implementation module wins, because it knows the terrain. The project override (`.scrumia/impl/<module>.md`) beats both.

## Consequences

**What we gain**

- A practice is written and fixed in a single place; its audit and refactor skills serve on every technology.
- The choice stays per app: TDD on the API, not on the prototype next door. It is a documented trade-off, not a global setting.
- An implementation module stays short and purely technological — which is what makes it writable by a third party in one sitting.
- The mechanism invents nothing: it is the `implementation` slot regime, applied a second time.

**What we accept**

- *Implementation modules cite known practices by name*, in conditional sections — a few dead lines when the practice is not plugged in. That is the cost of ADR-0009, already accepted.
- *A practice unknown to the implementation module is not situated.* It then applies on its own, without technology-specific examples. Degraded behavior, not a failure.
- *One more axis in the config.* The `practices` line is added to each app. `null` or absent: no practice imposed, the implementation module's conventions suffice.

## Rejected alternatives

**Dependencies between plugins.** Besides the lack of native support, a dependency turns a choice into an obligation: installing the Rust module would impose TDD. And that is precisely the kind of coupling composition exists to undo — two competent developers can want the Rust module with and without TDD, and neither is wrong.

**Duplication.** Rejected on its maintenance record, but it has one merit the decision keeps: the "situating the practice" section of each implementation module keeps locally what is genuinely local — the tooling, the examples, the exceptions.

## To revisit

If the number of practices exceeds half a dozen, the implementation × practices matrix will become costly to situate. At that point, consider a "situation sheet" format that implementation modules would fill in mechanically.
