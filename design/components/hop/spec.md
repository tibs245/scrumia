# Hop

The mascot. Four segments and one eye — the same segments the flow diagrams are
built from, gathered into a body and let go again.

## Why it exists

The site's subject is agents that appear on call, do one narrow thing and
disappear. Hop *is* that sentence, drawn: summoning and resolving are one
animation played in two directions, and the thing that appears is visibly made
of the same parts as the diagrams around it.

That is also why it is not a sticker. Its single cyan eye is the site's
one-accent rule taking physical form, which makes Hop a layout device — the
thing on the screen that points — rather than decoration bolted to a corner.

The name is the motion instruction: **springy on arrival, flat on departure.**
Summoned things land. Finished things just stop.

## The four states

| State | Class | When |
|---|---|---|
| Summoned | `.hop-arrive` | the page, or the section, has just arrived |
| Present | `.hop-idle` | at rest; only the eye moves, and rarely |
| Resolved | `.hop-resolve` | the thing Hop stood for is done |
| Cycling | `.hop-loop` | demonstration only — never on a real page |

`.hop-loop` is for this preview and for nothing else. A mascot that loops forever
is an animation that stopped standing for a state change, which
[identity.md](../../identity.md) says gets cut.

## Sizes

`.hop-sm` (28px) beside the wordmark, default (96px) in a section, `.hop-lg`
(160px) once per page at most. Below 28px the segment gaps close up and Hop turns
into a smudge — use `mark.svg` there instead.

## When not to use it

- **As a bullet, an icon, or a list marker.** Hop is one per screen. A row of
  Hops is a row of things all pointing, which is a screen pointing nowhere.
- **To decorate an empty state.** An empty slot is *deliberately* empty; putting
  a mascot in it says someone is sorry about it, and nobody is.
- **Next to another animated element.** Whatever else moves will lose, and Hop
  will look like it is competing rather than announcing.

## What it refuses

- **A second eye.** One accent, one eye. Two eyes make a face, and a face makes
  it a character that needs a personality, a name in copy, and eventually a
  backstory the product does not have.
- **Anthropomorphism.** No limbs, no mouth, no expressions. It is not a tall thin
  humanoid with a rounded head and wide white eyes — that resemblance belongs to
  someone else, and beyond the legal question a borrowed personality cannot be
  changed when the product changes.
- **Anthropic's graphic identity.** Hop belongs to the Claude Code ecosystem
  through *colour only* — the coral on the human side of the flow. A mascot on a
  third-party plugin marketplace wearing Anthropic's identity would imply an
  affiliation that does not exist.
- **Motion under `prefers-reduced-motion`.** Hop stays assembled with its eye lit,
  and nothing travels. The mascot is a shape before it is an animation.
