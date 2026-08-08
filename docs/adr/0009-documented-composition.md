# ADR-0009 — Documented composition, no dynamic resolution

**Status**: accepted — 2026-08-07

## Context

ScrumIA is a set of replaceable modules, organized by slots: `specs`, `tracker`, `team`, `discovery`, `implementation`, `design`. What remained to be decided was how one module reaches another — how the tracker module creates a ticket without knowing whether specs are handled by this module or that one.

Two designs were on the table.

**Capability registry.** Each module declares the verbs it provides (`ticket.create`, `spec.read`). An agent calls a verb; the core resolves it to the plugged-in module. Modules never know each other.

**Documented composition.** `scrumia-init` reads the configuration and writes into `CLAUDE.md` a table saying which module occupies which slot. Agents read that table like any other project context. Modules cite each other by name.

## Decision

**Documented composition.**

`scrumia-init` generates, between markers in `CLAUDE.md`, a table of the plugged-in modules and a table of the app → implementation module mapping. Agents read it. There is no registry, no resolution, no indirection.

## Consequences

**What we gain**

- The agent reads a plain-English sentence rather than resolving an indirection. The cost is paid once at context load, not on every call.
- Nothing to debug between the call and its recipient: what the agent reads is what applies.
- The mechanism is inspectable by a human — a `CLAUDE.md` can be reread, a registry has to be inferred.
- Writing a module requires no knowledge of the core: three rules suffice.

**What we accept**

- *Modules cite each other by name.* Replacing the tracker module requires checking the other modules that mention it. Mitigated by a writing discipline: a module refers to the **slot** ("the tracker module") rather than the name whenever it can.
- *`CLAUDE.md` can diverge from the configuration.* This is the most likely flaw of this design: the config changes, the table does not, and agents follow a stale composition. The `scrumia-compose` skill makes it its first diagnostic point.
- *The table consumes context on every session.* A few dozen lines, versus a resolution on every call. The trade-off leans clearly the right way.

## Rejected alternative

**The capability registry.** Seductive on paper: complete decoupling, replacing a module without touching the others. The real cost is elsewhere — the agent must keep in mind that "creating a ticket" goes through a verb pointing to a module it cannot see. That burden is paid on **every** call, while the benefit only materializes on a slot change, which happens a few times in the life of a project.

The decoupling would also have been partial: a tracker module and a specs module share notions (a feature, an acceptance criterion) that no verb system makes interchangeable.

## To revisit

If a project ends up changing modules frequently on the same slot, or if the number of modules makes manually maintaining the references costly. Neither is in sight.
