# UX — Extends map

## Reading order

The section reads in three beats, and a reader who stops after the first has still
received the argument:

1. **The claim, in one line** — a skill says where it can be extended; any module answers;
   nothing is stored.
2. **The figure** — the mechanism, drawn.
3. **One real table** — the directives a register actually carries in this repository,
   with the module each came from.

The third beat is what keeps the second honest. A diagram of a mechanism nobody can see
running is a claim with a picture on it, and `design/identity.md` refuses exactly that.

## What the figure must make visible

Four things, or it is not showing the mechanism:

- a **skill** declaring a register, and not naming who fills it
- **several modules** contributing to that one register, none of them naming the skill
- the table being **computed at the moment it is asked for**, not read from anywhere
- the register carrying **nothing** as a legitimate outcome

The fourth is the one a diagram will drop first, and it is the one that distinguishes this
mechanism from a plugin registry. An empty register is an answer, not a failure — it is
`modular-composition`'s AC-1 — and a figure that only draws the populated case has drawn
something else.

**And nothing else.** The three locations a contributing module may live in —
`local-extension`'s — are deliberately absent from this figure. They are a second,
orthogonal mechanism, and a figure carrying two of those is how the fourth item above gets
dropped to make room. Where a module comes from belongs to `reference.html`; the section
points there and does not draw it.

## What it may not claim

**No invented module, no invented register.** Every name in the figure and in the table is
one this repository actually runs, read from the composition at the time the section is
written. An illustrative `scrumia-example` contributing to a `deploy` register would be
the same defect `slot-index` refuses with its "no eighth example" rule, and for the same
reason: the site's whole argument is that the thing shown is the thing running.

**No count that will silently rot.** A stated number of registers or of contributions is a
claim about the composition, and the composition changes. Either the number is generated
with the page or it is not written.

## States

**A register with no contribution is shown, in words.** At least one of this repository's
own registers currently carries nothing, and it appears as such — the empty case is not a
hypothetical to be illustrated, it is available for free and it is the more instructive
half of the mechanism.

**Nothing here opens or closes.** The section has no disclosure, no tab and no state
beyond what the page loads with. `slot-index` earns its `<details>` by having seven rows
whose answers are long; three beats and one figure do not.

## Constraints inherited from the rest of the site

- **No script.** The section is fully legible with JavaScript disabled, as every other
  section on this site is.
- **Both themes, through tokens.** The figure carries no literal colour. A diagram is the
  most common place a hard-coded stroke colour survives review, and it is the one that
  disappears in the other theme.
- **The figure scrolls inside itself, never the page.** A wide diagram is contained; the
  page body never scrolls horizontally.
- **The figure is not the only carrier.** Whatever it shows is also stated in the section's
  prose, so a reader who cannot see it receives the argument. The figure carries a text
  alternative describing the mechanism, not the shapes.
