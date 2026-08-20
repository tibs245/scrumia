# ADR-0014 — A standing role ships with the module that gives it something to guard

**Status**: accepted — 2026-08-08

## Context

[ADR-0002](0002-standing-roles.md) settled that standing roles are subagent definitions, and put the three of them in the `team` slot's module. `docs/agents.md` went further and named what is deliberately *not* a role — including UX:

> A standing UX role would assume a continuous design flow, which is not the targeted use case.

Writing `scrumia-design` makes that sentence load-bearing. The module fills the `design` slot, and a project that plugs it in has, by definition, exactly the continuous design flow the sentence said was out of scope. So the question is no longer whether a design role is justified — it is **where it lives**.

## Considered

**A fourth role in `scrumia-teams`.** All roles in one directory, one place to look, `scrumia-team-setup` already configures them. The objection is what happens in the majority case: a project with `design: null` would inherit a role with no identity file, no tokens and no components to guard. `scrumia-designer` explicitly refuses to judge on taste — so in an empty-slot project it would either refuse every question, or quietly do the thing it refuses. It also makes the `team` slot promise a capability it does not provide.

**The role ships with `scrumia-design`.** The role exists if and only if the slot is filled, which is the same rule the rest of ScrumIA already runs on: an empty slot is a capability the project does not have. The objection is routing — `scrumia-manager` routes only to active roles, and it reads one list, `settings.team.roles`. A role defined in another module would be invisible to it.

**A `roles` slot of its own.** Rejected on [ADR-0013](0013-tracker-stays-one-slot.md)'s rule: no slot invented before a user needs it. One role from one module is not evidence of a slot.

## Decision

**A module that fills a slot may ship the standing role that guards that slot's capability. The role is contributed by that module — declared in its own `extends.json` under the `convene` register — and enabled by the project in `settings.team.roles`; the contract that decides whether the role convenes is the cross-check between the two surfaces, not a single list.**

The two surfaces are distinct facts about distinct things. The **contribution** surface lists which roles a composition offers: `scrumia-extends convene` is the union call, and every row carries an `extends:` list of `<source>:<module>` keys naming the sources that contribute this role. The **enablement** surface lists which of those roles this project wants — `settings.team.roles`, where each entry is `name + enabled + from:`, and `from:` is the full `<source>:<module>` key of one contributing module.

```yaml
roles:
  - name: manager
    enabled: true
    # no from: — contributed by the team slot's module
  - name: designer
    enabled: true
    from: tibs245/scrumia:scrumia-design    # full key, set-membership against the role's extends:
```

A role convenes when all three hold: it appears in the contribution surface with a non-empty `extends:`, it appears in `settings.team.roles` with `enabled: true`, and its `from:` is one of the keys in its `extends:` set. The three failure modes — contributed-but-disabled, enabled-but-not-contributed, `from:` outside `extends:` — are different findings, none of them silently reconciled. `scrumia-manager` reads what the cross-check produces, not one list, and a manager that asks the surface to reconcile them itself reintroduces the failure the split exists to prevent.

`scrumia-design-setup` writes the entry in `settings.team.roles` when it installs the slot, and the `extends:` field in its own `extends.json` names itself as the contributing source; removing the module means removing both.

`docs/agents.md` keeps its three roles: they are the `team` module's opinion. Its "not a role" section now says what it actually means — UX is not a role *of the team module*, and becomes one only through the module that brings a design system with it.

## Consequences

**What we gain**

- A role cannot outlive the capability that justifies it. No designer without a design system, and the failure mode of a role with nothing to guard disappears by construction.
- Modules stay self-contained: `scrumia-design` ships its skills and its role together, and plugging it in is one install.
- The rule generalizes without new machinery. A future `forge` or `analytics` module can ship a role the same way.

**What it costs**

- Roles are no longer all in one directory. Finding every active role means reading `settings.team.roles`, not listing `plugins/scrumia-teams/agents/`. The config is the authority; the directory is one provider among possibly several.
- `scrumia-team-setup` configures roles it does not define. It must not delete an entry carrying a `from:` it does not recognize — that would silently unplug another module's role.
- Two modules could one day ship a role with the same name. Nothing prevents it today; the collision would surface at `scrumia-init` and can be settled then, rather than designed against now.
