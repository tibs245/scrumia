# Angle: index

**Mandatory in every feature, both strata.** The file is `index.md`.

## What this angle answers

Which files this feature carries, and when to open each. It is the only file an
agent or a human systematically reads before deciding what to read next, so it
must fit in one reading and everything in it must serve that one decision.

An index that carries a rule is not a richer index — it is a second place where
that rule lives, and the day the two disagree nobody knows which is current.

Read by: everyone, first.

## When it activates

Always, and it is written **last**: it lists the files present, so it cannot be
correct before they exist. Writing it first is the single most common source of a
`Files present` table that does not match the directory.

No configuration key can switch this angle off.

## The questions to explore it

1. What does this feature do, and for whom, in ten lines at most? If it does not
   fit, check the splitting criterion before writing a longer summary.
2. Is it `draft`, `active` or `deprecated` today — not what you intend it to be.
3. Where does it sit in the tree, and which links does that position oblige it to
   declare? See *The links* below, and `catalog.md` § *Disposition on disk* for
   the choice between a child and a sibling.
4. Which question does this feature defer to a `design/` or `docs/` file? That is
   an `Authority:` line, one line of key info, never the answer itself.
5. Which neighbouring feature owns something a reader might expect to find here?
   That is a `Boundary:` line — it prevents the same rule being written twice.
6. For each file present: what situation makes an agent open it? Not why it
   exists — the situation. That column is what lets an agent load `legal.md` only
   when it is needed rather than as a precaution.
7. For each catalog file **absent**: is its absence an assertion you are prepared
   to make? State the ones a reader would otherwise wonder about, in prose, under
   the table.

## The links

The vocabulary is fixed, so that a link can be resolved without interpretation.
Use these keys, and no invented ones:

Nine keys, in two groups.

**Structural — declared on both sides.** These two pairs describe where the
feature sits: in which stratum, and in which directory. A one-sided structural
link is a defect, and the missing side is the one nobody notices.

| Key | Its other half |
|---|---|
| `Business parent:` — App → its Business feature | `Implemented by:` |
| `Implemented by:` — Business → the App features that implement it | `Business parent:` |
| `Parent:` — child → the feature it sits inside | `Children:` |
| `Children:` — parent → the features that sit inside it | `Parent:` |

**Referential — one-sided by nature.** They record a use or point at an
authority. Nothing owes them a declaration back: the dependency itself is stated
by whoever depends, and a second mandatory copy would be one more thing to keep
in sync for no added truth.

| Key | Points at |
|---|---|
| `Consumes:` | a feature this one depends on |
| `Consumed by:` | a feature that depends on this one — a convenience for the reader arriving here first |
| `Defers to:` | another **feature** that owns a question this one raises and does not answer |
| `Authority:` | a file **outside** `features/` — a `design/` file, an ADR, a component spec |
| `Boundary:` | a neighbouring feature that owns an adjacent subject, with no dependency either way |

The line between `Defers to:` and `Boundary:`: if this feature would be wrong
without the other's answer, it defers; if a reader might merely look in the wrong
place, it is a boundary.

**A link is a path, not a story.** `features/business/<feature>/` or a relative
`standard/`, then at most one line saying what the other feature owns. What that
feature says is its own file's job.

An App feature with no `Business parent:` is suspect: either it is purely
technical — and this file says so explicitly, in one sentence — or the Business
feature is missing.

## Boundary

**Holds** — the summary in ten lines maximum; the status; the links; the list of
files present, one line each saying when to read it.

**May hold** — a one-line pointer to the file that elaborates a claim ("the
persona is in `business.md`"); the prose stating which absences are assertions.

**Must not hold**
- a rule → the file whose subject it is
- a decision or its rationale → the ADR or the tracker
- a ticket, issue or PR number → the tracker
- a fact a `design/` file or a component spec already states → cite it, one line
- history → `CHANGELOG.md`

**A rule, a decision or a rationale in an index is a defect**, whatever heading it
hides under.

## The section set

`In brief`, `Links`, `Files present` — those three, no others. The set is declared
by [`template.md`](template.md) and enforced from it, never from a second
hardcoded list. A section outside the set is detectable rather than a matter of
taste; a rule smuggled under a conformant heading is review's to catch.

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
