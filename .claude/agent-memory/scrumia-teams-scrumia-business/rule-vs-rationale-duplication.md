---
name: rule-vs-rationale-duplication
description: Business ruling — a skill repeating a spec's rationale is not "the rule written twice"; the drift test is whether two copies could command different behaviour
metadata:
  type: project
---

Ruled on 2026-08-09, on #118 / PR #173, against the criterion *"the rule is stated once
in `business.md` and the skill cites it rather than restating it — fails if the same rule
is written in two places."*

**The test is not textual overlap, it is: could the two copies ever command different
behaviour?** A rule has a normative half (what must be done) and a trigger (what
condition fires it). Those are what must live in exactly one place. A skill that repeats
a spec's *premise* or *motivation* — a factual claim about the environment, from which no
one can be judged compliant or non-compliant — has not created a second rule: if the spec
later changes, the skill is left with a stale reason, never a wrong instruction.

Corollary that decided the case: the skill kept the rationale sentence but explicitly
disclaimed holding the trigger — *"the rule, and what counts as yielding control, are
stated once in [business.md]"*. Trigger in one place, obligation in one place, premise
echoed — passes.

**Why:** a skill carrying zero motivation gets skipped by an agent that never opens the
link, so demanding a bare pointer trades a real failure for a theoretical one.

**How to apply:** when reviewing a skill that cites a spec, ask which sentences are
normative. Object to a duplicated *trigger* or *obligation*; let a duplicated *reason*
stand. See [[vocab-yield-vs-pause]] for the vocabulary this ruling sits on.
