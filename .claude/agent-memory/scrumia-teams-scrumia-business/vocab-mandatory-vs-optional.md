---
name: vocab-mandatory-vs-optional
description: The mandatory/optional vocabulary is owned by feature-format and ADR-0012 — this entry says only which trap a review keeps falling into
metadata:
  type: project
  topic: specs-mandatory-set
  source: human @tibs245 2026-08-09
  stale_when: ADR-0012 gains a contract key carrying mandatory/optional status, or feature-format restates the pair
  cites: features/business/feature-format/business.md, docs/adr/0012-specs-contract.md
---

The vocabulary pair and which files this project's specs module mandates are owned by
`features/business/feature-format/business.md`; the contract block's own vocabulary is
ADR-0012. Read them there — the ruling behind the wording is #25, a human decision of
2026-08-09.

**The trap a review keeps falling into:** inferring mandatoriness from the contract
block's *key shape* ("own key = mandatory, under `catalog` = optional"). The block is a
naming vocabulary. See [[../scrumia-teams-scrumia-tech/contract-block-carries-names-not-status]]
for the same trap from the tech side — the pair `topic: specs-mandatory-set` marks them as
speaking to one question.
