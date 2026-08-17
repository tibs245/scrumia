# Review guard-rails: tech

## Does it say anything the code doesn't?

- The file lists files, functions or modules. That is a stale copy of the
  directory; delete it and state the reason the structure is what it is.
- A choice is recorded with no alternative rejected. "We use X" documents nothing —
  what was X chosen over, and why?
- A dependency is listed with no reason. Nobody will dare remove it later.
- The file paraphrases the framework's documentation.

## Debt

- Debt is stated with no exit condition. It stops being debt and becomes a
  permanent decision nobody revisits.
- Debt is stated with no date, so nobody can tell whether it has aged out.
- What is called debt is actually a deliberate design choice — or the reverse, a
  choice presented as permanent when the team knows it is temporary.

## Boundaries

- A data flow that crosses an app boundary is described here rather than in
  `archi.md`.
- A rule that constrains what the product promises — true whatever tool enacts it —
  is written here rather than in `business.md`. "Reads are filtered or they lie" is
  business; the flag that filters is tech.
- A schema another feature parses is defined here rather than in
  `api-contract.md`.
- A decision that will outlive this feature sits here instead of in an ADR. The
  test: if the feature is deleted, does this decision still matter?
- The file exists on a Business feature.

## Hygiene

- A ticket, issue or PR number appears.
- The former implementation is described alongside the current one.
- A benchmark result or an incident is narrated as justification. The current
  constraint belongs here; what happened belongs to the issue.
