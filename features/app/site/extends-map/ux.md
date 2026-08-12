# UX — Extends map

## Where the section sits

After `#composer`, before `#modules`. That order is the argument: a visitor meets additions
as a *choice* in the composer, this section explains the mechanism behind the choice they
just made, then `#modules` shows what exists and `#install` closes.

**Not between `#slots` and `#composer`.** Their adjacency is load-bearing — the composer's
own intro reads "Same index as above", and `composer` AC-8 compares the two indexes' fills
on the rendered page. A dense figure wedged between them costs the composer its setup.

**Not folded into `#slots`.** That section is seven rows and one argument; a register figure
inside it makes it answer two questions and the index stops being the whole of it.

## Reading order

The section reads in three beats, and a reader who stops after the first has still
received the argument:

1. **The claim, in one line** — a skill says where it can be extended; any module answers;
   nothing is stored.
2. **The figure** — the mechanism, drawn.
3. **One real table** — the directives a register actually carries in this repository,
   with the module each came from. Three columns, not the five the tool prints: directive,
   what it says, which module it came from. The fragment's path is for an agent, not for a
   visitor deciding whether the tool bends to their project, and it is the column that
   would force the drag.

The third beat is what keeps the second honest. A diagram of a mechanism nobody can see
running is a claim with a picture on it, and `design/identity.md` refuses exactly that.

## What the figure makes visible, and what the invocation carries

The figure carries **three** facts; the fourth is temporal and no still frame states it.

The figure — three labelled columns, the deck idiom `design/identity.md` already names:

```
DECLARES              REGISTER                CONTRIBUTES
scrumia-github-       implement  ············  scrumia-impl-rust
project                                        scrumia-practice-tdd
                                               scrumia-specs
scrumia-teams         sprint     - - - - - - -  no contribution
```

- a **skill** declaring a register, and not naming who fills it
- **several modules** contributing to that one register, none of them naming the skill
- the register carrying **nothing** as a legitimate outcome

The first two are carried by the *absence* of an edge between the outer columns, which is
the honest drawing: neither side names the other, and nothing joins them but the register.
The third costs nothing to source — `sprint`, `design`, `scope-idea`, `split`,
`write-spec` and `find-spec` are all opened here and filled by nobody — and it is the fact
that distinguishes this from a plugin registry.

**The fourth fact is that the table is computed when asked, and stored nowhere.** That is
a negative temporal claim: a reader shown a table beside some modules concludes it was read
from somewhere, which is the opposite. So it is not drawn — it is carried by **position**.
Below the columns sits the invocation, `scrumia-extends implement`, and below that the real
table as its output. The table is downstream of the ask, not stored beside the modules, and
the reading order says so.

`identity.md` decision 2 makes causality motion's job: the columns arrive on `--stagger`,
the table arrives after the invocation. Without script it is a static figure that still
reads correctly — but a section whose central fact is temporal and in which nothing moves
is consistent, correct and mute, which this site treats as a defect rather than a
shortfall.

**And nothing else.** The three locations a contributing module may live in —
`local-extension`'s — are deliberately absent. They are a second, orthogonal mechanism, and
a figure carrying two of those is how the empty-register row gets dropped to make room.
Where a module comes from belongs to `reference.html`; the section points there and does
not draw it.

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

- **HTML and CSS, not SVG.** Inline SVG on this site means Hop — it is the mascot's
  medium, and the one mechanism figure that already exists, `#flow`'s run horizon, is marks
  on a hairline in HTML. Drawing this one in SVG would give the site two idioms for one job
  and make SVG mean both "the character" and "the diagram".
- **It turns, it does not scroll.** Below the width where three columns fit, the figure
  becomes a vertical list — register, then its contributors indented under it — same rows,
  same order, same words, nothing cut. `run-horizon`'s spec states the reason and this
  section inherits it: *four of seven columns in view is the ratio telling a lie until the
  reader drags*. Here the column that would fall off is the contributors, which is half the
  argument. Only the third beat's table may scroll inside itself, in the `.table-wrap` that
  already exists.
- **No script for the argument.** The section is fully legible with JavaScript disabled;
  motion is arrival only and its absence costs nothing but the temporal cue.
- **Both themes, through tokens, and no actor colour.** The figure carries no literal
  value. A register, a skill and a module are mechanism, not actors — neither `--agent` nor
  `--human` applies, and putting the agent's colour on a file is a mistake this site has
  already had to undo once. Columns in `--text` and `--text-soft`; `--accent` is spent on
  exactly one element, the invocation, which is the point the mechanism's own claim turns
  on.
- **The figure is not the only carrier.** Whatever it shows is also stated in the section's
  prose, so a reader who cannot see it receives the argument. The figure carries a text
  alternative describing the mechanism, not the shapes.
