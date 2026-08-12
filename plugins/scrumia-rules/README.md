# scrumia-rules

The rules-hierarchy format itself — not a topic, the shape every topic can take once it
outgrows a single file. Fills no slot: every other module can build on it, none has to.

## What it answers

When a `conventions.md`, a lint config or a repeated review comment has grown past what an
agent can afford to load in full for every unrelated task — and what to split it into: an
**index** it reads first and always, **guides** it loads only on demand, one concern each,
and **decisions** it loads only when a human is challenging a rule. A `section.json`
declares the globs a section governs. Module-shipped sections live inside the owning
module's own skill directory; project-local ones live under `.scrumia/rules/<section>/`,
registered in the project's `CLAUDE.md`.

## What it refuses

- No rule without a decision, no decision without its trade-offs. A guide with no decision
  behind it is an opinion, not a rule; a decision that only lists arguments for its own
  verdict has not been examined.
- No invented conventions. A section is harvested from code, lint configs and existing
  docs — a rule with no traceable source does not get written, it gets asked about.
- No rewriting an adopted verdict in place. A decision that reverses is superseded by a
  new one; the old one stays, marked `Superseded by`.
- No hierarchy below roughly three distinct concerns on a topic — splitting earlier
  produces ceremony, not clarity.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-rules` | The format reference — anatomy, navigation, precedence. Read first. |
| `scrumia-rules-setup` | Scaffolds a project-local section: interview, harvest, write, register in `CLAUDE.md`. |
| `scrumia-rules-update` | Evolves a rule: challenge the decision, refine or supersede, update the guide, log the change. |
