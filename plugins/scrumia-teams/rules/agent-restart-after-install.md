# Reaching a role requires a restart after install

The operational condition that is not optional, stated here so the skills that
spawn roles by their agent type (refinement, execution, sprint gather) carry
the rule rather than reach outside the module for it.

## The condition

The same definition serves three ways — delegated subagent, session main agent,
teammate in an agent team — and `docs/adr/0002-standing-roles.md` treats them as
interchangeable. They are, with one operational condition that is not optional:
**a module that ships agents is not usable until Claude Code restarts.** A hot
reload refreshes skills and leaves the registry of spawnable agent types stale.

This is specified rather than left to the tooling because of how it fails. The
roles are not degraded, they are unaddressable, and a caller that cannot reach
its reviewer falls back to a general agent whose verdict reads exactly like the
role's. One sprint measured the difference on the same five diffs: the
self-applied reviews returned five approvals and two reservations, the actual
roles one blocker and nine.

## What to do when the agent type does not resolve

The caller — the skill that would spawn the role by its agent type — names the
restart rather than falling back silently. The fallback to a subprocess that
prompts the role's `.md` on stdin is not the role: it returns `not_run` at the
gate, with cause "agent type did not resolve", and the verdict it can write is
not a role verdict. A fallback that reads as the real thing is worse than no
fallback, because nobody compensates for a gate they believe ran.

The restart is the fix; the skill that hits the symptom names it and reports
the verdict as `not_run`. A later skill — typically the sprint's gather — reads
the absence and triggers the review on that absence, since the symptom survives
the run only if the carrier does.

## Sources

Transcribed here rather than linked, so this module carries what its skills
apply. Open these to argue with the rule, never to apply it — what runs is the
text above.

| What it owns | Where |
|---|---|
| The condition, the failure mode, the measured difference | `features/business/agent-team/business.md` § *Reaching a role requires a restart after install* |
| Why the three call shapes are treated as interchangeable | `docs/adr/0002-standing-roles.md` |
| The verdict the gate reads when the type does not resolve | `rules/role-verdict-format.md` (in `scrumia-github-project`) |
| Acceptance criteria that close the rule | `features/business/agent-team/qa.md` AC-11 |

Those paths name files in the ScrumIA repository, which is not installed beside
this module. They are provenance: if one of them cannot be reached, nothing
above stops working. When one of them changes, this file is what has to be
brought back into line.
