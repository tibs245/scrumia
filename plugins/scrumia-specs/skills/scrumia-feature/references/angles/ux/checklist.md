# Review guard-rails: ux

## Design-system boundary

- A literal colour, spacing, radius or duration is written here. Every one of them
  belongs to `design/tokens.css`; a value no token supplies is a finding for
  `design/`, not a number typed into a spec.
- A component's anatomy or behaviour is described rather than cited. The component
  spec is the authority; a copy here will diverge from it.
- A mockup has become the permanent drawing of a screen that has no `design/`
  counterpart. A mockup is a seed — it converts into an exploration or a component
  spec, or it goes.

## States and copy

- Only the success state is described. Empty and error are the two that get
  skipped in the spec and invented at implementation time.
- A state is named without its copy, so the wording is decided by whoever writes
  the code.
- The loading state is missing on a screen that waits for anything.

## Accessibility

- A WCAG target that can pass or fail — a contrast ratio, a keyboard-trap check, an
  announcement — is written here as prose instead of as a tagged `qa.md` criterion.
- Prose here restates the mechanism of a criterion rather than citing it.
- Focus order, or what announces itself on change, is not stated at all on a screen
  with interactive elements.
- A non-textual element has no text alternative specified.

## Boundaries and hygiene

- A business rule or the intent behind the journey is stated here rather than in
  `business.md`. The tell: a sentence that would still be true if the screen were
  redesigned entirely.
- The file exists on a Business feature. A journey with screens is App stratum.
- A technical choice — a library, a rendering strategy — appears here rather than
  in `tech.md`.
- A ticket, issue or PR number appears.
- The screen's former layout is described alongside the current one.
