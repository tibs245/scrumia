---
name: scope-axis-entry-exit
description: The scope/* axis measures reach (ADR-0015, owned by execution-policy/business.md); label routes entry, diff routes exit — and the "gap = scoping failure" rule now false-positives on every specs-only ticket
metadata:
  type: project
---

Two invariants that every routing/labelling review in this repo runs into.

1. **`scope/*` measures a rule's blast radius, not a file's location** — ADR-0015
   supersedes 0006 (#78). The test has exactly one owner:
   `features/business/execution-policy/business.md` § *The scope axis measures reach,
   not medium*. Four surfaces apply it and must carry that section's own words rather
   than paraphrase: `scrumia-refine` Step 5, `scrumia-manager.md`'s routing table,
   `scrumia-project-setup`'s seeded `gh label create --description` block, and the
   live GitHub label descriptions. The seeded block is the one that outlives the repo
   it was copied from, so a change to the test that skips it re-seeds the drift with
   nothing in a diff to show for it.

2. **Label = entry, diff = exit.** Who is asked *during* execution comes from the
   label; who reviews the PR comes from the diff's path grid (ADR-0005), which reads
   no label — true since #130. Any prose implying a higher tier buys a reviewer is a
   regression (the `Handling` column wording is the recurring offender).

**Known false-positive introduced by (1), not yet ticketed as of 2026-08-10.** Under
the old file-location reading, label and diff agreed by construction: touching
`features/business/**` forced `scope/L`, so the entry set matched ADR-0005's exit set.
The blast-radius reading deliberately decouples them, so a legitimately-`scope/M`
specs-only ticket now routinely gets a *business* reviewer at exit that its label did
not imply. ADR-0015 § Decision and `features/business/dev-flow/qa.md` AC-6 still say
that gap "is flagged as a scoping failure" — which is now systematically wrong for a
whole class of correct ticket, and teaches readers to ignore the signal. Same defect
shape as #32 (an answer overridden systematically is not a strict answer).

**Why:** established reviewing #78. The decoupling is the point of ADR-0015; the
flagging rule was carried over from 0006 unexamined.
**How to apply:** when reviewing anything that touches scope labelling, model routing
or gate 2, check whether the prose still ties the exit review to the label, and treat
a "label/diff gap = failed scoping" claim as needing the specs-only carve-out. Related:
[[pitfall-cross-skill-claims]] — ADR-0015 also claims "a feature's index.md Links
section names its consumers", which only `execution-policy` actually does.
