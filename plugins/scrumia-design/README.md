# scrumia-design

The design slot: identity, tokens and components that live in the repo, sync with a
claude.ai/design project, and a standing `designer` role that guards both — the person
deciding what a user sees, not the agent writing the markup.

## What it answers

What a user actually sees — hierarchy, colour, motion — and whether it is still the same
product across every screen it appears on. One vocabulary (`identity.md`, `tokens.css`,
one directory per component) that an interface reads from instead of inventing a value
inline.

## What it refuses

- No inline value. A colour, a spacing or a duration that is not a token is a finding the
  audit raises, not a style choice.
- No component judged on consistency alone. Consistent-but-forgettable ("mutedness")
  weighs the same as an invented value ("drift") — the audit reports both on equal
  footing, never drift-only.
- No opinion on copy or performance. Those belong to the business and tech roles; the
  designer owns what is seen, not what is said or how fast it loads.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-design-system` | The reference — where identity, tokens and components live, and how to consult them before writing an interface. Read first. |
| `scrumia-design-setup` | Installs the `design/` tree, registers the designer role, optionally links a Claude Design remote. |
| `scrumia-design-audit` | Audits an existing interface: drift and mutedness, on equal footing. |
| `scrumia-design-sync` | Syncs local components with a claude.ai/design project, component by component, never a wholesale replace. |
| `scrumia-designer` (agent) | The standing role — guards identity and consistency, reviewing hierarchy → identity → consistency → reuse → accessibility → motion, in that order. |

## Settings it reads

Under `settings.design` in `.scrumia/config.yaml`: `root`, `remote` (`claude-design` or
`none`), `project_id` once linked. It also appends its `designer` entry to
`settings.team.roles` when a team module is present.

## What it expects to find

`CLAUDE.md`'s own `## Design contract` section, written there by `scrumia-init` from this
module's composition block — every consumer reads the contract there, never a hardcoded
path into `design/`. `scrumia-design-sync` additionally needs a linked claude.ai/design
project.

## Decisions

One so far: why the audit reports drift and mutedness on equal footing, rather than as a
drift-only linter.
