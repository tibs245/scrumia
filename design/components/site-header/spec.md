# site-header

The bar at the top of every page: Hop, the wordmark, the navigation, the language
pair and the theme toggle.

**Status: three candidates, none chosen.** The preview renders all three so the
decision can be made by looking. Once one wins, the other two come out of this
file — a design system that keeps its rejected options is a system that never
decided.

## The three candidates

| | Treatment | What its motion stands for | Costs |
|---|---|---|---|
| **A** | Assembly | Hop assembles on load; on scroll the bar compacts, its ground goes solid, a cyan rule fills to your position | The rule is a fourth thing competing for the accent |
| **B** | Scanline | a cyan sweep crosses on a slow loop | It moves when nothing happened — the one thing [identity.md](../../identity.md) says gets cut |
| **C** | Rail | one cyan rail slides to whatever you point at, and goes home when you stop | Invisible until the reader hovers; does nothing on touch |

A and C both pass the "motion means causality" test and B does not, which is an
argument rather than a verdict: B is the only one that is alive on a page nobody
has touched yet, and a site whose subject is agents doing work may want that.

A and C also compose — the rail is a navigation device and the progress rule is a
scroll device. Picking both is a real option, and the one to weigh against the
one-accent rule, since it puts two cyan marks in the same bar.

## What is settled, whichever wins

- **Hop sits at 26px, left of the wordmark**, and arrives once per page load. It
  never loops there. See [hop](../hop/spec.md).
- **The header is translucent over the ground**, not a solid band: the page runs
  underneath it, which is what makes the compaction in A legible at all.
- **The rail and the progress rule are the same cyan**, and only one of them may
  be on screen at a time if the one-accent rule is to survive.

## When not to use it

- **On a preview or a component page.** These render standalone, with no chrome;
  a header on them is a header pretending the component is a page.

## What it refuses

- **A second row.** Everything fits one line down to 640px, where the navigation
  scrolls horizontally rather than wrapping. A header that wraps has become a
  menu and should say so.
- **A call-to-action button.** The header routes; it does not sell. The hero owns
  the next step — see [button](../button/spec.md).
- **Hiding on scroll-down.** A header that disappears when you scroll is a header
  whose motion stands for nothing the reader asked for.
- **Motion the reader did not cause**, in A and C. B is the exception and knows
  it; that is precisely what the choice is about.
