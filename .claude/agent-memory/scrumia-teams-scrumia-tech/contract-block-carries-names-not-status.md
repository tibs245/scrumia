---
name: contract-block-carries-names-not-status
description: ADR-0012's contract block is naming vocabulary — the trap; the rule is owned by feature-format and ADR-0012
metadata:
  type: project
  topic: specs-mandatory-set
  source: agent
  stale_when: ADR-0012 gains a contract key carrying mandatory/optional status
  cites: docs/adr/0012-specs-contract.md, features/business/feature-format/business.md
---

The mandatory/optional vocabulary and which files this project's specs module mandates are
owned by `features/business/feature-format/business.md`; the contract block's own
vocabulary is ADR-0012. Read them there.

**The trap, reviewed on #25:** inferring status from the block's *key shape* — "own key =
mandatory, under `catalog` = optional". True of `scrumia-specs` by coincidence, false as a
contract property, and it makes an AC that cannot pass. A module mandating a fourth file
has nowhere but `catalog:` to name it. ADR-0012's "To revisit" already anticipates the
vocabulary being too narrow.

Its twin from the business side is
[[../scrumia-teams-scrumia-business/vocab-mandatory-vs-optional]] — the shared
`topic: specs-mandatory-set` is what makes the pair visible to the channel's check.
