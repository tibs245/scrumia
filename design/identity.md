# Identity

## What someone should feel in the first three seconds

**Summoned energy, pointed at one job.**

ScrumIA's whole argument is a shape: you state a task well, something appears that is enthusiastic and narrow, it does the one thing, it disappears. The site should feel like that — arriving, acting, leaving — rather than like documentation that sits there waiting to be read.

The corollary is the honest half of the argument: a vague brief makes that shape miserable. An agent asked to "improve the app" has nothing to converge on. The site should make that failure legible, not hide it — the method exists because the vague brief hurts.

## What it must never look like

**A neutral developer-tool landing page.** Grey cards on white, a system font, a hero gradient, four feature boxes, no motion. The current site is close to this, and it is the anti-reference: every value is defensible and the result belongs to nobody.

Concretely, in order of how badly each one hurts:

- Nothing moves. Nothing appearing or resolving on a site whose subject is agents appearing and resolving.
- The palette is a default violet on near-white. It carries no argument.
- The typography is the OS's. A site read by developers can afford a voice.
- Everything is emphasized equally, so the message — *compose a team from replaceable modules* — has to be read rather than seen.

## What already carries the identity

**The REX deck** (`tibs245.github.io/claude-code-rex`) is the strongest existing artifact, and the site should read as its sibling:

- Deep navy ground (`#000B1C`) with raised blue surfaces, not a white page with dark mode bolted on
- One cyan accent (`#73E3FF`) doing the pointing, used sparingly enough to still mean something
- Sora for display, Source Sans 3 for body, JetBrains Mono for code — a voice, not a fallback stack
- Diagrams built from labelled columns (INPUT → CONTEXT → QUERY → RESULT), which is how the deck explains mechanism instead of asserting benefit
- A narrative spine — the deck runs a day, `07:00 collect` to `20:00 close`, and the flow section of the site already wants that shape

**Claude Code's palette** is the second input: the warm coral (`#D97757`) and paper cream against the deck's cold navy. That contrast is the one worth building on — warm marks the human, cold marks the agent. The site already splits its flow into human steps and AI steps and currently colors them orange and blue by accident. Making that the deliberate rule turns a decoration into the argument.

**The summoned-helper reference** — the deck's own framing — is the tone: eager, single-purpose, cheerfully finite. Borrow the *idea* only. The character it comes from is someone else's property: no likeness, no name, no blue humanoid on a public page. What transfers is behaviour — appear on call, do one thing, resolve — expressible entirely in motion and copy.

## Decisions everything else follows from

1. **Cold ground, warm human.** Navy is the substrate the agents work on; coral marks every point where a human decides. A screen that uses coral for anything else breaks the argument.
2. **Motion means causality.** Things appear when summoned and resolve when done. Animation that does not stand for a state change is decoration, and gets cut.
3. **Mechanism over claim.** Show the pipeline, the columns, the slot filled or empty. The site's job is to make the composition legible, not to praise it.
4. **One accent.** Cyan points. If two things on a screen are pointing, neither is.

## Where this is not yet settled

The site ships French and English, and the voice above was written in English first. The French must carry the same tone rather than translate it literally — that is a real risk and it belongs to whoever writes the copy, not to the tokens.
