# Review guard-rails: api-contract

## Drift

- The contract does not match the code. Check one field, one error case, one
  default against the implementation before trusting the rest — a diverged
  contract is worse than an absent one, because it is believed.
- The code changed in this same diff and this file did not.
- An example payload contradicts the schema above it.

## As a producer

- No stability statement. Every consumer will treat the whole thing as frozen, and
  be right to.
- Error cases are missing, so consumers invent their own handling.
- A field is described in prose without a type, or with a type the code does not
  enforce.
- An implicit limit — page size, maximum length, rate — exists in the code and not
  here.
- Nothing says what happens to existing consumers when the contract changes.

## As a consumer

- The producer's schema is copied rather than cited. The copy will drift, and the
  consumer will be debugged against a stale one.
- The assumptions section is missing or empty. It is the whole point of a consumer
  entry: what this feature relies on that the contract does not actually promise.
- The contract is cited by name with no path to the feature that owns it.

## Boundaries and hygiene

- An internal structure nobody outside the feature parses is documented here. That
  is `tech.md`'s.
- The meaning of the data — what a status value implies for the business — is
  explained here rather than in `business.md`.
- A ticket, issue or PR number appears.
- A deprecated version of the contract is kept alongside the current one. Only the
  current shape belongs here; the change belongs to `CHANGELOG.md`.
