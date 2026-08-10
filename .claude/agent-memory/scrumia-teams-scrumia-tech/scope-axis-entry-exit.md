---
name: scope-axis-entry-exit
description: The scope/* axis measures reach (ADR-0015, owned by execution-policy/business.md); label routes entry, diff routes exit — and a gap between them is a scoping failure only when the axis itself would have answered higher
metadata:
  type: project
  topic: scope-axis
  source: agent
  stale_when: ADR-0015 is superseded, or #190 and #191 close
  cites: docs/adr/0015-scope-measures-reach.md, #78
---

Two invariants that every routing/labelling review in this repo runs into.

1. **`scope/*` measures a rule's blast radius, not a file's location** — ADR-0015
   supersedes 0006 (#78). The test has exactly one owner:
   `features/business/execution-policy/business.md` § *The scope axis measures reach,
   not medium*. Four surfaces apply it and must carry the shared wording **verbatim** —
   the clause in the spec's words, the four tier conditions in ADR-0015's:
   `scrumia-refine` Step 5, `scrumia-manager.md`'s routing table,
   `scrumia-project-setup`'s seeded `gh label create --description` block, and the
   live GitHub label descriptions. The seeded block is the one that outlives the repo
   it was copied from, so a change to the test that skips it re-seeds the drift with
   nothing in a diff to show for it.

   **The label description sets the wording for everyone.** It stops at 100 characters
   and spends 38 naming `features/business/execution-policy/`, so the tier conditions
   are compressed until they fit there and the roomier tables carry the compressed form
   anyway. `execution-policy/qa.md` AC-21 is what makes both halves — the owner
   reference and the verbatim carriage — checkable. Reviewing a change to the axis:
   diff the four renderings against each other, character for character, and check the
   live labels with `gh label list`, which no repo check can see.

2. **Label = entry, diff = exit.** Who is asked *during* execution comes from the
   label; who reviews the PR comes from the diff's path grid (ADR-0005), which reads
   no label — true since #130. Any prose implying a higher tier buys a reviewer is a
   regression (the `Handling` column wording was the recurring offender; the column is
   now called `Asked at entry`).

**The gap between them is not automatically a defect.** Under the old file-location
reading, label and diff agreed by construction: touching `features/business/**` forced
`scope/L`, so the entry set matched ADR-0005's exit set. The blast-radius reading
deliberately decouples them, so a legitimately-`scope/M` specs-only ticket routinely
draws a *business* reviewer at exit that its label did not imply. Reporting that as a
mislabel would fire on a whole class of correct ticket — same defect shape as #32, an
answer overridden systematically is not a strict answer. The narrowed rule now reads:
**a label/diff gap is a scoping failure only when the axis's own questions would have
answered higher.** Stated in ADR-0015 § Decision, tested by
`features/business/dev-flow/qa.md` AC-6 (three scenarios: the review always widens; the
gap is flagged when question 2 answers yes; it is not flagged when the rule stays inside
its feature and `scope/M` was correct), and applied in `scrumia-ticket` Step 6.
**`scrumia-review` gate 2 and `scrumia-manager` have not caught up — that is #191.**

**Why:** established reviewing #78, narrowed by the same PR after both roles found it.
**How to apply:** when reviewing anything that touches scope labelling, model routing
or gate 2, check whether the prose still ties the exit review to the label, and treat an
unqualified "label/diff gap = failed scoping" claim as a finding. Related:
[[pitfall-cross-skill-claims]] — ADR-0015 also leans on a feature's `index.md` naming
its consumers, which only `execution-policy` actually does; that is #190.
