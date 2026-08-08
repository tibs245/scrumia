# scrumia-rules

The rules-hierarchy format itself — not a topic, the shape every topic can take once it outgrows a single file. Fills no slot, exactly like `scrumia-core`: every other module can build on it, none has to.

## What it is

A section is an **index** an agent reads first and always, **guides** it loads only on demand — one concern each, with correct/incorrect examples — and **decisions** it never loads for code generation, only when a human is challenging a rule. A `section.json` declares the globs it governs. Module-shipped sections live inside the owning module's skill directory; project-local ones live under `.scrumia/rules/<section>/`, registered in the project's `CLAUDE.md`.

The full anatomy, the navigation rule, and the precedence between sections are in the `scrumia-rules` skill.

## When you need it

- A `conventions.md` has grown past the point an agent can afford to read it in full for every unrelated task.
- The same correction keeps coming up in review — that's a rule waiting to be written down, not enforced by memory.
- A module wants to ship topic-specific reference material (API conventions, a UI kit's usage rules) in a form agents can navigate instead of load wholesale.

You don't need it below roughly three distinct concerns on a topic. A section with one guide and one decision is a routing table that routes to itself — stay single-file until a real third concern shows up.

## What it refuses

- **No rule without a decision, no decision without its trade-offs.** A guide with no decision behind it is an opinion, not a rule — `scrumia-rules-update` will not touch one without either finding its decision or reconstructing it first. And a decision that only lists arguments for its own verdict hasn't been examined; Arguments Against is mandatory, `Proposed` decisions included.
- **No invented conventions.** `scrumia-rules-setup` harvests from code, lint configs and existing docs — a rule with no traceable source doesn't get written, it gets asked about.
- **No rewriting an adopted verdict in place.** A decision that reverses gets superseded by a new one; the old one stays, marked `Superseded by`. Same discipline this project holds its own ADRs to, and for the same reason: what was believed at the time stays visible.
- **No hierarchy for its own sake.** Below ~3 distinct concerns, this format is overhead over a single file. Splitting early produces ceremony, not clarity.

## Skills

| Skill | Role |
|---|---|
| `scrumia-rules` | The format reference — anatomy, navigation, precedence. Read first. |
| `scrumia-rules-setup` | Scaffolds a project-local section: interview, harvest, write, register in `CLAUDE.md`. |
| `scrumia-rules-update` | Evolves a rule: challenge the decision, refine or supersede, update the guide, log the change. |

## Format at a glance

```
<section>/
├── 00-index.md        # routing table — guides, quoted-need routing, dependency graph, decisions
├── guides/
│   └── NN-topic.md    # one concern, correct/incorrect examples
├── decisions/
│   └── D-NN-slug.md   # Status / Date / Impacts / Context / Arguments / Verdict
├── section.json       # { "globs": [...] }
└── CHANGELOG.md
```
