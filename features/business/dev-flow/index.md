# Dev flow — brainstorming vs execution

**Status**: active

## In brief

Two paths, kept deliberately apart: brainstorming turns an idea into a scoped
ticket, human-led and agent-challenged; execution turns a scoped ticket into a
reviewable PR, agent-led with the human validating at the end. This feature
owns the code-cycle process that execution runs on; a tracker feature only
traces it onto its own tool. `business.md` carries who decides on each path,
the mechanics of the cycle, and the ownership rule against a tracker feature.

## Links

- Implemented by: none — this business feature is enacted directly by the plugin
  composition (`scrumia-discovery`, `scrumia-github-project`, `scrumia-teams`), not
  by app code.
- Defers to: `features/business/execution-policy/` for which model executes a scoped
  ticket. This feature says the human validates at the end of execution, not which
  model does the executing.
- Traced by: `features/business/github-tracking/` — it binds this feature's abstract
  cycle to GitHub's concrete artefacts (a PR, a column, a milestone). Whichever
  feature fills the tracker slot plays that role; none of them redefines the process.
- Defers to: `features/business/ceremonies/` for what happens beside the ticket path —
  which occasions are admitted, on what trigger, and what each leaves behind. This
  feature owns the gates, which are decision points inside the path and not ceremonies.

## Files present

| File | Read it when |
|---|---|
| `business.md` | need who decides what on each path, where the human gate sits, or who owns the code cycle |
| `qa.md` | need the refusal rule, the autonomy gates, or what routes gate 2's review, as falsifiable scenarios |
| `CHANGELOG.md` | need history of this feature's changes |

