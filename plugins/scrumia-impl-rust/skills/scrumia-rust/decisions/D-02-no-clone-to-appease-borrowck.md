# D-02: No `clone()` to silence the borrow checker

**Status**: Adopted
**Date**: 2026-08-07
**Impacts**: [guides/02-domain-types.md](../guides/02-domain-types.md)

## Context

`clone()` is the fastest way to make a borrow-checker error disappear: duplicate the value, and the conflicting borrows are no longer a conflict. That speed is exactly what makes it tempting to reach for instead of understanding what the checker is objecting to.

## Arguments For

- A clone is justified by semantics — two legitimate owners — not by a lost fight against the borrow checker.
- Three clones in the same place signal an ownership structure to rethink, not a style issue to fix line by line.
- Every unjustified clone is a duplicated source of truth: two copies of the same data can now drift, and a bug that "shouldn't be possible" becomes possible.

## Arguments Against (trade-offs accepted)

- Cloning is often the pragmatic fix under deadline pressure, and it compiles immediately — accepted cost: the pause to articulate real ownership instead of reaching for the fastest fix.
- For small, cheap-to-copy data the performance objection barely applies — the objection here is about design clarity, not runtime cost, and the rule is paid even when the clone itself is free.
- Redesigning ownership (borrowing, `Rc`/`Arc` where sharing is the real semantics, restructuring who holds what) costs more upfront time than a one-line `.clone()`.

## Verdict

`clone()` to escape a borrow-checker error is refused. A clone is acceptable when it expresses genuine shared ownership. Three clones clustered in one place is the threshold that triggers a redesign conversation rather than a fourth clone.
