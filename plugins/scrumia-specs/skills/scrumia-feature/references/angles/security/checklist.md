# Review guard-rails: security

## The activation

- The file is absent and one of the activation questions clearly answers yes — the
  absence asserts a judgement that was never made.
- The file is present and states no risk. Under the `context` default that is a
  file that should not exist; under `always` it must say so explicitly, with a
  date, not sit empty.

## The table

- A row names a threat and rates nothing. It decides nothing, and it will be read
  as covered.
- A rating is given with no mitigation and no acceptance — the sentence stops
  halfway.
- The rating does not match the scale's wording: something rated `low` that blocks
  a core flow, or `critical` used for an inconvenience. Check the rating against a
  comparable row in another feature, not against how the risk feels here.
- Two rows describe the same risk on two axes without saying so, so it gets counted
  twice or fixed once.
- An axis that the activation questions turned up has no row at all, and nothing
  says why.

## The acceptances

- A risk is accepted and nobody is named. "The team accepted it" is not an
  acceptance record.
- An acceptance has no revisit condition — it becomes permanent by default, which
  is exactly what the record exists to prevent.
- The reason for the acceptance is a restatement of the risk rather than why
  living with it is preferable.
- `legal.md` carries its own acceptance format instead of referencing this file's.
  The two will drift.

## Boundaries and hygiene

- An accessibility concern appears in the table. It belongs to `ux.md` and to a
  tagged `qa.md` criterion — "access" here means who may read the data, not who
  can operate the interface.
- A legal obligation appears here rather than in `legal.md`.
- A mitigation is designed rather than named — the implementation belongs to
  `tech.md`.
- A ticket, issue or PR number appears. Only `CHANGELOG.md` cites issues.
- The file narrates an incident that happened. The current risk belongs here; what
  happened belongs to the issue.
