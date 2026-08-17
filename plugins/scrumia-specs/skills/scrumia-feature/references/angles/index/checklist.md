# Review guard-rails: index

## The table

- `Files present` lists a file that is not on disk, or omits one that is. Both
  directions are defects; the second is the one a reader never notices.
- A child feature's directory is listed as if it were a file. A child is declared
  under `Links`, with `Children:`.
- The "read it when" column says why the file exists rather than the situation
  that makes someone open it. "The business rules" is a label; "when a ticket
  touches a rule" is an instruction.
- A mandatory file is missing from the table because it is obvious. Nothing is
  obvious to the agent deciding what to load.

## The links

- A link uses a key outside the fixed set — `Instances:`, `See also:`, `Related:`.
  The set exists so a link resolves without interpretation.
- A structural link is declared on one side only. Check the other feature's
  `index.md`: a `Parent:` with no matching `Children:`, or a `Business parent:`
  with no matching `Implemented by:`, is half a fact.
- A link points at a directory that does not exist.
- A link carries a paragraph explaining what the other feature says, instead of a
  path and one line on what it owns.
- An App feature declares no `Business parent:` and does not state, in one
  sentence, that it is purely technical.
- An `Authority:` line contains the answer instead of pointing at the file that
  holds it.

## The content

- A rule appears in the index — most often smuggled into `In brief` as "the
  feature must…". Whatever heading it hides under, it is a defect: move it to the
  file whose subject it is.
- A decision or its rationale appears. Those live in the ADR or the tracker.
- `In brief` runs past ten lines. Check the splitting criterion before rewriting
  it shorter.
- The status says what the feature is meant to become rather than what it is.
- A ticket, issue or PR number appears anywhere.
- History appears — "replaces the former…", "since the split". `CHANGELOG.md`
  owns that.
- A section heading outside `In brief`, `Links`, `Files present`.

## The absences

- No prose at all under the table, in a feature where a reader would reasonably
  expect `legal.md` or `security.md`. The absence is meant to be an assertion; an
  unstated absence is indistinguishable from an oversight.
- The prose asserts an absence the feature has not actually considered — a
  sentence written to satisfy the format rather than to record a judgement.
