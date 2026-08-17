# When a role must be consulted

The condition under which a role is asked — not an invitation, a check — is stated
here rather than reached across modules, so the skills that apply it (refinement,
execution, review) do not have to leave this one to load the rule. Transcribed from
the feature spec that owns the rationale; the spec is the source of truth, this file
is what the skills read.

## Why it is a condition, not a courtesy

A role is asked because its domain owns the question, and a question left to the
caller is either answered on taste or carried to the human — both losses the team
exists to prevent. The skills that route to a role must therefore state **the
conditions under which a role is consulted** rather than invite one "when useful".
An invitation with no trigger is a role never called, and the evidence from a
single refinement pass is unambiguous: most tickets that came back blocked were
blocked on a question a role would have answered in three minutes.

## The condition, stated once

A role is consulted when any of the following holds:

- A business rule is ambiguous, missing, or contradicted by two written statements
- The change reaches beyond one feature or one app — the rule it changes is read elsewhere
- An interface contract changes, or two apps disagree on what the contract says
- The same question blocks several tickets — one consultation, referenced by all of them

That is the entire condition. It does not enumerate every case; it names the shape
the case has to take to be one. Anything narrower turns the role into an exception
list; anything broader turns it back into an invitation.

## The rule applies to every entry point

The same condition holds for refinement, for execution, and for review — not just
the skill that touches a ticket first. A refinement that consulted the right role
at entry and an execution that ran without one are both partial applications of
the rule, and the report's silence on which role was asked is what makes them
indistinguishable from a run that asked none.

A report — a refinement report, an execution's PR description, a review's verdict
— states **which roles were consulted, their answers, and where the answer is
recorded**, or states that no role was needed and names the condition that made
the call. A report that is silent on the question has not met the rule, regardless
of whether the role was asked.

## Unreachable roles

A role that cannot be reached is reported as such — the agent type does not
resolve, the module shipping it is not installed, the question lies outside every
declared role — and the report names the gap rather than substituting a general
agent in silence. A fallback that reads as the role is worse than no consultation,
because the role's absence is no longer visible to the reader of the report. The
agent-type case (a module that ships roles was installed or updated without a
restart) has its own rule, kept separately: a hot reload refreshes skills and
leaves the registry of spawnable agent types stale, and the role's apparent
absence is the symptom that misleads the fallback. The report carries every other
gap; the carrier for this one is the rule above.

## Repeated questions

A question that blocks several tickets is asked once. The first ticket that hits
the condition convenes the role; later tickets reference the answer rather than
asking the same role the same question again. A refinement that finds the answer
on the ticket cites it instead of re-asking, and an execution that needs the
answer reads it from the ticket it is closing rather than convening the role
independently. Repeated questions asked separately are repeated costs, and the
rule's point is to surface the team's domain — not its overhead.

## Sources

Transcribed here rather than linked, so this module carries what its skills apply.
Open these to argue with the rule, never to apply it — what runs is the text above.

| What it owns | Where |
|---|---|
| The condition, the four subsections, and the rationale | `features/business/agent-team/business.md` § *When a role must be consulted* |
| Why a role is asked by domain, not by invitation | `features/business/agent-team/business.md` § *Roles* |
| How a missing role degrades — measured on a single sprint | `features/business/agent-team/business.md` § *Reaching a role requires a restart after install* |
| Acceptance criteria that close the rule | `features/business/agent-team/qa.md` AC-17 to AC-21 |

Those paths name files in the ScrumIA repository, which is not installed beside
this module. They are provenance: if one of them cannot be reached, nothing above
stops working. When one of them changes, this file is what has to be brought back
into line.
