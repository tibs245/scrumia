# GitHub tracking — technical notes

How the tracking rules stated in `business.md` and tested in `qa.md` are actually
carried out. This file documents what the code cannot say for itself: which flag,
which field, which retry — not why the rule exists.

## Confirming a short read (AC-4)

A filtered, non-empty `scrumia-board` read confirms its own `totalCount` before returning
it: it re-issues the same query, backing off between checks, until two consecutive
reads agree or a small retry budget runs out. This is retry-with-backoff internal to
`scrumia-board`; it changes no output field — a caller reads the same JSON shape whether
the first read landed at rest or had to converge across a few retries.

## The `closed_without_pr` field shape (AC-8)

`scrumia-board read`'s items carry the issue's own `state` (`OPEN`/`CLOSED`), fetched in
one batched call rather than one per item. A closed card outside the `Done` column —
the only place a close is expected — is pulled out of the column it reports as live
work and returned instead under `closed_without_pr`, with a `closed_without_pr_count`
at the top level; a closed card sitting in `Done` is a normal merge and stays
reported as usual.

## The read partitions into three groups, label first (AC-8, AC-13)

`columns`, `closed_without_pr` and `discussions` are disjoint and together account for
every item the read returned — `count` and `total_matching` are unchanged by the split,
which is what makes it a subtraction rather than a drop.

**The `discussion` label is applied before the state split, and the order is the rule
rather than an implementation preference.** A discussion is normally closed once it is
settled, and it never had a pull request, so a state-first split files it under
`closed_without_pr` — reported as a ticket abandoned mid-flight, which is the opposite of
what it is, and precisely the item the label exists to set aside. Splitting by state first
would therefore leave the backstop correct on open discussions and wrong on the majority.

A consumer reading only `columns` gets what is waiting to be started, which is what both
readings that owe the subtraction want. One reporting counts adds all three.

## The deviation search command

Reading one ticket's record uses `gh issue view <n> --json comments`. Reading across
the project:

```bash
gh search issues --repo <owner>/<repo> --match comments 'Deviation:' 'cell L/low'
```

`--match comments` is not optional and not a convenience. Folding the qualifier into
the query string instead — `'in:comments "Deviation:" …'` — makes `gh` send the whole
rest of the string as the qualifier's *value*; GitHub discards what it cannot parse
and answers with **every issue in the repository**, exit code 0, no warning. That is
the mechanism behind `business.md`'s rule that a search folding the qualifier into the
query silently returns everything.

The two search terms are ANDed, and `L/low` does not collide with `XL/low` —
adjacency is preserved, which is what lets the `cell` token alone discriminate one
cell from another.
