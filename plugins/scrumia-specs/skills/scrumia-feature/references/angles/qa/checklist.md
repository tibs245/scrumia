# Review guard-rails: qa

## Falsifiability

- A criterion cannot fail. "The user has a good experience", "the page is fast",
  "the data is correct" — no state of the world makes them false, so they test
  nothing. This is the defect to look for first.
- The `Then` observes something no one can observe from outside: an internal
  variable, a call that was made, a state nobody can query.
- The `Given` describes a state nobody can set up, so the criterion can never be
  run.
- The criterion restates a business rule instead of testing it — same sentence,
  wrapped in Given/When/Then.

## Coverage

- Only the nominal case is written. A feature with one criterion is either
  under-specified or is a ticket rather than a feature.
- An edge case that plainly applies is missing — most often concurrency and
  insufficient permissions, in that order.
- An edge case is written as a heading with no scenario under it, left over from
  the template.
- A case is filled with "N/A" instead of being deleted.
- There is no *Out of scope* section, in a feature whose neighbours will
  reasonably be expected to cover something.
- On an App feature: no technical case at all — no timeout, no network error, no
  concurrent state — as if the implementation could not fail.

## Identifiers

- A criterion has no `### AC-<n>` heading, so no ticket and no test can cite it.
- Two criteria share the same number.
- A number was reused after a criterion was deleted, so an old ticket now cites a
  different behaviour. Numbers are not recycled.
- A criterion was renumbered on edit, silently invalidating every reference to it.

## Boundaries and hygiene

- The persona, or the value the criteria protect, is explained here rather than in
  `business.md`.
- How the implementation satisfies the criterion is described — that belongs to
  `tech.md`.
- An accessibility property stated in prose sits here untagged and untestable; the
  prose half belongs to `ux.md`, the testable half stays here, tagged.
- A ticket, issue or PR number appears. Only `CHANGELOG.md` cites issues.
- The file carries more than ~12 criteria. Not a defect on its own — a signal to
  check the splitting criterion.
