---
name: vocab-mandatory-vs-optional
description: The specs vocabulary pair is mandatory/optional, declared per specs module; the Specs contract block does NOT encode mandatoriness
metadata:
  type: project
  topic: specs-mandatory-set
  source: human @tibs245 2026-08-09
  stale_when: ADR-0012 gains a contract key carrying mandatory/optional status, or #25's wording is superseded
  cites: docs/adr/0012-specs-contract.md, #25
---

Since issue #25 (human decision 2026-08-09), the feature-format vocabulary is
**mandatory** / **optional**, and "always" / "required" / "mandatory, everywhere"
are retired as competing terms.

- `scrumia-specs` mandates three files: `index.md`, `qa.md`, `CHANGELOG.md`.
  Rationale: a feature must be possible to follow over time (`CHANGELOG.md`) and
  possible to test (`qa.md`); `index.md` is the entry point.
- "Absence is information" governs the **optional** catalogue only. An absent
  mandatory file is a gap, not an assertion.
- The mandatory set is **whichever module fills the `specs` slot** declaring it,
  never a universal law of the format. Never write "every ScrumIA feature has a
  `qa.md`" — write that *this module* requires one.

**Why:** three texts had drifted into asserting two different rules (1 unconditional
file vs 3), and the human ruled that the conditionality must be visible in the wording.

**The trap — do not repeat it.** ADR-0012's Specs contract block is a **naming**
vocabulary only ("the file named by `acceptance_file`"). A key of its own does NOT
mean mandatory, and `catalog` does NOT mean optional. That the two happen to line up
is a coincidence of `scrumia-specs`'s own set: a module that carries a changelog
without mandating it still needs a `changelog:` key to name it. Any text claiming the
block's shape "carries the distinction" is overreaching, and any consumer told to
resolve the mandatory set from those three keys will be wrong for another module.
Expressing a mandatory set properly needs a new contract key — ADR-0012's "To revisit"
already licenses widening the vocabulary.

**The other side of the same seam (found on #25's fix pass).** Once the texts stop
claiming the contract carries the set, there is nowhere sanctioned left for a consumer
to read it: ADR-0012 rejected "dynamic runtime resolution" (reaching into the specs
module's own files at execution time), and `docs/composition.md` line 157 forbids a
module assuming another is present. So today a consumer *cannot* resolve the mandatory
set — the honest wording is that it must not guess one, not that it should go read
`references/catalog.md`. Do not let a text prescribe that reach as the fix.

**How to apply:** on any review touching the catalogue, the format docs, or the specs
contract — check both that mandatory/optional is used consistently and that no text
infers mandatoriness from the contract's key shape. See [[vocab-scope-label-readers]]
for the sibling habit of saying which reading you are counting.
