# GitHub tracking — technical notes

How the tracking rules stated in `business.md` and tested in `qa.md` are actually
carried out. This file documents what the code cannot say for itself: which flag,
which field, which retry — not why the rule exists.

## Confirming a short read (AC-4)

A filtered, non-empty `board.sh` read confirms its own `totalCount` before returning
it: it re-issues the same query, backing off between checks, until two consecutive
reads agree or a small retry budget runs out. This is retry-with-backoff internal to
`board.sh`; it changes no output field — a caller reads the same JSON shape whether
the first read landed at rest or had to converge across a few retries.

## The `closed_without_pr` field shape (AC-8)

`board.sh read`'s items carry the issue's own `state` (`OPEN`/`CLOSED`), fetched in
one batched call rather than one per item. A closed card outside the `Done` column —
the only place a close is expected — is pulled out of the column it reports as live
work and returned instead under `closed_without_pr`, with a `closed_without_pr_count`
at the top level; a closed card sitting in `Done` is a normal merge and stays
reported as usual.

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
