# Review guard-rails: devx

## Usability

- The example does not run. Paste it and check — an example that is a sketch is
  worse than none, because it is trusted.
- The example uses a name, an import path or a signature the code no longer has.
- No pitfall is listed. Either nobody has watched a first-time consumer, or the
  section was skipped; both mean the file has not done its job.
- What is exposed is described in prose without the actual names to import or
  invoke.

## Boundaries

- The internal why of the implementation is explained here rather than in
  `tech.md`. The tell: a sentence a consumer could not act on.
- The schema of data crossing a boundary is defined here rather than in
  `api-contract.md`.
- A business rule about what the thing means appears here.
- The file exists for something consumed only inside this feature.

## Stability

- Nothing is said about stability, so every consumer treats the whole surface as
  frozen — including the parts you meant to change next month.
- Something is marked stable that the team knows is about to move.
- What is deliberately unsupported is not stated, so it arrives as bug reports.

## Hygiene

- A ticket, issue or PR number appears.
- A deprecated usage is documented alongside the current one, with no indication
  of which is which.
