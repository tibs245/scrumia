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

This split is the backstop `business.md` describes, not the mechanism: a discussion issue is
filed without a card, so the only ones reaching it are those someone carded by hand.

**Within it, the `discussion` label is applied before the state split, and the order is the
rule rather than an implementation preference.** A discussion is normally closed once it is
settled, and it never had a pull request, so a state-first split files any of them outside
`Done` under `closed_without_pr` — reported as a ticket abandoned mid-flight, which is the
opposite of what it is. Splitting by state first would leave the backstop correct on open
discussions and wrong on the settled ones, which are most of them.

A consumer reading only `columns` gets the work, discussions excluded — which is what both
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

## The role-verdict search command

A role's verdict is found on the ticket's issue in the same carrier the deviation
record uses, with the same discipline on the qualifier. The verdict is a comment
carrying the `Verdict:` prefix and the `by scrumia-*` token — reading one ticket:

```bash
gh issue view <n> --json comments
```

Reading across the project — which is what the gather needs:

```bash
gh search issues --repo <owner>/<repo> --match comments 'Verdict:' 'by scrumia-*'
```

The two terms are ANDed. The `by scrumia-*` token is what discriminates a role
verdict from any comment that quotes the word "Verdict:"; without it, a search on
the prefix alone returns every issue that matches, in the same way the deviation
record's qualifier does. `--match comments` is the same flag the deviation record
needs — folding the qualifier into the query string sends the rest of the query
as the qualifier's value, and GitHub discards what it cannot parse and answers
with the whole repository, exit code 0, no warning.
