# Dev flow — brainstorming vs execution

**Status**: active
**Stratum**: business

## In brief

Two paths, kept deliberately apart:

- **Brainstorming** — human-led, agent-challenged. An idea gets questioned until it
  becomes a ticket carrying a verifiable acceptance criterion.
- **Execution** — agent-led. Once a ticket is scoped, agents implement and
  self-review; the human validates at the end, not mid-flight.

Mixing them is BMAD's failure mode: mobilizing the human uniformly, on the same
terms, whether the decision is still open or already made. Kept apart, validation
cost tracks where the decision actually happens — heavy while the idea is still
soft, light once it is a scoped ticket.

## This feature owns the code-cycle process

The execution path's mechanics — one worktree per ticket, one branch per ticket,
committing before a pause, review before merge, the three gates, `auto_merge` — are
**this feature's**. Ownership is settled; the wording is not all here yet — worktree
ownership and commit-before-pause land through #118 and #20, and until they do, no
other spec becomes their home. A tracker feature *traces* that
cycle: it says which concrete artefact each abstract step becomes on its tool, and it
never redefines the step itself.

`business.md` § *The code cycle* carries the ownership rule, the precedence when a
tracker feature disagrees, and the replacement test that files any given rule on
exactly one side.

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

## Files present

| File | Why it exists |
|---|---|
| `business.md` | who decides what on each path, where the human gate sits, and who owns the code cycle |
| `qa.md` | the refusal rule that keeps execution from running on a guessed intent, the autonomy gates, and what routes gate 2's review |
| `CHANGELOG.md` | history of this feature's changes, one entry per notable change |

## Open issues

- #3 — [EPIC] Spec the dev flow: brainstorming vs execution, gates, ceremonies (parent)
- #11 — Spec the human ceremonies: triggers, artefacts, cadence (this feature defers to it)
- #18 — The bootstrap case: a ticket whose deliverable is the parent feature is refused at Step 0
