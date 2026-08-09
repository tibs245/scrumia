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

## Links

- Implemented by: none — this business feature is enacted directly by the plugin
  composition (`scrumia-discovery`, `scrumia-github-project`, `scrumia-teams`), not
  by app code.
- Defers to: `features/business/execution-policy/` for which model executes a scoped
  ticket. This feature says the human validates at the end of execution, not which
  model does the executing.

## Files present

| File | Why it exists |
|---|---|
| `business.md` | who decides what on each path, and where the human gate sits |
| `qa.md` | the refusal rule that keeps execution from running on a guessed intent, the autonomy gates, and what routes gate 2's review |

## Open issues

- #3 — [EPIC] Spec the dev flow: brainstorming vs execution, gates, ceremonies (parent)
- #11 — Spec the human ceremonies: triggers, artefacts, cadence (this feature defers to it)
- #18 — The bootstrap case: a ticket whose deliverable is the parent feature is refused at Step 0
