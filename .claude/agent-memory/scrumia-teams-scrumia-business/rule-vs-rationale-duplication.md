---
name: rule-vs-rationale-duplication
description: Review test for "is this rule duplicated" — check whether the two copies could ever command different behaviour, not whether their wording overlaps
metadata:
  type: project
---

**When reviewing a skill (or any consumer) that cites a spec's rule, the test for
duplication is not textual overlap — it is: could the two copies ever command different
behaviour?** A rule has a normative half (what must be done) and a trigger (what
condition fires it). Those are what must live in exactly one place. A copy that repeats
a spec's *premise* or *motivation* — a factual claim about the environment, from which no
one can be judged compliant or non-compliant — has not created a second rule: if the spec
later changes, the copy is left with a stale reason, never a wrong instruction.

**Why:** a skill carrying zero motivation gets skipped by an agent that never opens the
link, so demanding a bare pointer trades a real failure for a theoretical one.

**How to apply:** ask which sentences in the citing text are normative. Object to a
duplicated *trigger* or *obligation*; let a duplicated *reason* stand.
