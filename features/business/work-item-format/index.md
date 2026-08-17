# Work item format

**Status**: draft

## In brief

What any form of work item has to satisfy, whichever module supplies it and
whichever tracker renders it. A project declares the shape of its issues the
way it declares its specs: through a module, published as a contract other
modules read. The form supplies both the writing rules and the judgement that
tells whether an issue meets them; the tracker renders that form onto its own
tool and defines none of it.

This feature states the standard every form is held to. The form this
repository ships is one instance of it, and sits under `standard/`.

## Links

- Children: `standard/` — the form this repository ships. A second form would
  sit beside it, under this feature, rather than restating what both are held
  to.
- Implemented by: no App feature — purely technical, enacted by a module in
  the `work-item-form` position. Neither app in this repository is involved.
- Consumed by: whichever module fills the `tracker` slot, which renders the
  form and calls its judgement.
- Boundary: `execution-policy` owns what the classification axes mean,
  `github-tracking` owns the ticket's lifecycle, `dev-flow` owns the code
  cycle. None of the three is restated here.

## Files present

| File | Read it when |
|---|---|
| `business.md` | the rules any work-item form has to satisfy |
| `qa.md` | acceptance criteria for a correctly-applied form |
| `CHANGELOG.md` | history of changes to this spec |

No `legal.md`: a documentation convention processes no personal data, payment
or regulated content — a form may *require* a legal note through a contributed
rule, which is that contributing module's subject and not this one's. No
`archi.md`: this feature's own implementation touches no app. No
`api-contract.md`, `tech.md`, `ux.md`, `security.md`, `devx.md`: none applies
to a convention with no interface and no exposed library of its own.
