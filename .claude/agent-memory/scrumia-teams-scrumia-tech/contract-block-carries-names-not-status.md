---
name: contract-block-carries-names-not-status
description: ADR-0012's Specs contract block is naming vocabulary only — it encodes no mandatory/optional status, and reading one into the key shape is a recurring over-claim
metadata:
  type: project
  topic: specs-mandatory-set
  source: agent
  stale_when: ADR-0012 gains a contract key carrying mandatory/optional status
  cites: docs/adr/0012-specs-contract.md, #25
---

`CLAUDE.md`'s `## Specs contract` block (ADR-0012) names files; it does not declare
which of them a feature must carry. `feature_index` / `acceptance_file` / `changelog`
are fixed vocabulary keys every conforming block fills, whether or not the module
behind it mandates those files — and a module mandating a fourth file has nowhere but
`catalog:` to name it. ADR-0012's "To revisit" already anticipates the vocabulary being
too narrow.

**Why:** reviewed on #25 (2026-08-09), where the spec of record inferred "own key =
mandatory, under `catalog` = optional" and generalised it to *any* specs module. True
for `scrumia-specs`, false as a contract property, and it makes an AC that cannot pass.

**How to apply:** a module-scoped statement ("this module mandates these three, and the
block names them") is sound — `scrumia-feature/SKILL.md` has said so for a while. A
statement about "whichever module fills the slot" needs either a new key in the contract
(ADR amendment) or nothing. Also check `scrumia-init` Step 5's template prose before
telling a consumer to "read it from `CLAUDE.md`": that prose names no mandatory set.
