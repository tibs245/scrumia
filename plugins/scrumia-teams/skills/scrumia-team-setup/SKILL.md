---
name: scrumia-team-setup
description: Configures a project's agent team — which roles are active, on which models, with which escalation thresholds. Invoked by scrumia-init when this module fills the team slot, or by hand to adjust the team.
---

# Configuring the team

This module provides a **default** team, not an imposed one. Three roles cover most projects; a project can disable some, add some, or change their models.

## The default team

| Role | Model | Owns | Doesn't own |
|---|---|---|---|
| `manager` | `opus` | The board, splitting, routing, cadence | Business rules, architecture, merge |
| `business` | `fable` | Business rules, vocabulary, compliance | Architecture, stack, planning |
| `tech` | `fable` | Architecture, contracts, debt, quality | Business rules, priorities |

Those models live in each agent's frontmatter, not in `.scrumia/config.yaml` — the platform reads them at load time. The models used to **execute tickets** are a separate policy, set in Step 3.

The reasoning behind this split: each boundary is a **line of refusal**. Without it, the three roles converge toward the same generalist agent and the separation no longer serves any purpose.

It's not the only possible split. A solo project with no strong business stakes may enable only `tech`; a heavily regulated project may add a distinct `legal` role.

## Step 1 — Read the configuration

`scrumia-init` is the writer of this schema — it seeds `settings.team` in `.scrumia/config.yaml` at Step 3 of its own `SKILL.md`, in exactly the shape below. This module only reads and adjusts it; if the two shapes ever disagree, `scrumia-init`'s template is the one to fix.

```yaml
settings:
  team:
    roles:
      - name: manager
        enabled: true
      - name: business
        enabled: true
      - name: tech
        enabled: true
    execution:               # read by scripts/pick-model.sh — see Step 3
      unlabeled: sonnet
      unrated_risk: medium
      labels:
        scope_prefix: "scope/"
        risk_prefix: "risk/"
      matrix:
        S:  { low: fable,          medium: fable,          high: sonnet,        critical: opus }
        M:  { low: sonnet,         medium: sonnet,         high: opus,          critical: opus }
        L:  { low: sonnet,         medium: opus,           high: opus,          critical: opus }
        XL: { low: split_or_fable, medium: split_or_fable, high: split_or_opus, critical: split_or_opus }
    escalation:
      to_human:                    # what always escalates to the human
        - disagreement between roles
        - missing business rule
        - contract change consumed by another app
    sprint:
      max_tickets: 5               # beyond this, human review saturates
```

If `settings.team` is absent, propose these values and write them. There is no `sprint.parallel` key: every sprint runs one isolated worktree per ticket unconditionally (`scrumia-sprint`, Step 3) — a setting nothing reads is worse than no setting, so it isn't offered.

## Step 2 — Adjust the roles

Ask the user what they want to change, presenting the consequences rather than the options:

- **Disabling `business`** — no one keeps business rules consistent across features anymore; contradictions will surface at implementation or in production.
- **Disabling `tech`** — no more architecture review; acceptable on a single app, costly as soon as several apps share contracts.
- **Disabling `manager`** — the human takes back splitting, routing and sprint assembly.
- **Changing a standing role's model** — edit that role's agent file in `agents/`; the platform reads the frontmatter at load time and no config key overrides it. A smaller model costs less and misses more subtle contradictions; it's an arbitration, not a degradation. Don't confuse it with Step 3: this sets who reviews, that sets who executes.

Adding a role is possible: it takes an agent file in `agents/`, a scope that overlaps no existing role, and an explicit line of refusal. A role without a line of refusal is a duplicate.

## Step 3 — Set the execution policy

Standing roles have fixed models. The **executor of a ticket** does not: `scrumia-sprint` picks one per ticket, and `execution.matrix` is where that choice is written down instead of being improvised.

Two axes, both carried by the ticket's own labels: **scope** (how much work) and **risk** (what it costs to get wrong). They are independent — a one-line change to a payment rule is `scope/S` and `risk/critical`, and it deserves the strong model precisely because it is small enough to look harmless.

Nobody reads this matrix by hand, including you. `scripts/pick-model.sh <issue>` reads it and answers:

```bash
${CLAUDE_SKILL_DIR}/../../scripts/pick-model.sh 42
```

```json
{"scope":"S","risk":"critical","decision":"model","model":"opus",
 "instruction":"Execute this ticket on opus.","because":"scope=S risk=critical -> opus"}
```

Callers act on `instruction`. A skill that re-derives the decision from the YAML is a second implementation of the policy, and the two drift.

A cell holds a model, or `split_or_<model>`. The second form is a preference, not a verdict: **try to split, and if the work is genuinely indivisible, run it on the named model and say why the split was refused.** Oversized work is a reason to think again, not a dead end — which is why the fallback travels with the decision rather than leaving the caller stuck.

Two keys cover what the labels don't say. `unlabeled` is the model for a ticket carrying no scope label at all — it runs, and the answer asks for refinement rather than inventing an estimate nobody made. `unrated_risk` is the risk column assumed when only the scope is known; the answer flags the assumption so it can be contradicted.

If the project already labels its tickets, don't relabel it: set `labels.scope_prefix` and `labels.risk_prefix` to the prefixes in use, and map any vocabulary that differs.

```yaml
labels:
  scope_prefix: "size:"       # tickets carry size:S … size:XL
  risk_prefix: "risk:"
  risk_aliases: { red: critical, orange: high, yellow: medium, green: low }
```

## Step 4 — Set the escalation

`escalation.to_human` lists what escalates regardless of the autonomy level. Three entries deserve to be there by default:

- **A disagreement between roles** — that's exactly the case that requires human arbitration; blending it into an averaged opinion would destroy the information.
- **A missing business rule** — a rule invented along the way becomes everyone's reference without anyone having decided it.
- **A contract change consumed elsewhere** — the error isn't visible in the app that commits it.

## Step 5 — Provide its composition line

```markdown
| Team | `scrumia-teams` | Active roles: manager, business, tech. Call on a role when its answer changes the decision, not to cover a choice. |
```

Adapt the list to the roles actually enabled.

## Step 6 — Report back

The active roles and their models, those that were disabled and what the project loses, the escalation rules retained.

## On the permanence of roles

These roles are not running processes. They are agent definitions, whose continuity comes from two things: persistent memory at project scale (`memory: project`), and the state kept by the tracker module.

This has a practical consequence: any session rebuilds the context by reading the tracker. Two parallel sessions — one executing, the other scoping — therefore stay consistent without coordinating.
