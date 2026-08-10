# Tech memory — ScrumIA

What an entry here may hold, and what its frontmatter owes, is
`features/business/agent-team/business.md` § *What role memory may hold*.

- [Site motion invariants](site-motion-invariants.md) — .js gate semantics, reduced-motion delay blind spot, nth-child stagger coupling
- [Cross-skill claims go stale silently](pitfall-cross-skill-claims.md) — skills assert what siblings do; validate.py checks links, never truth
- [Site i18n guard invariants](site-i18n-guard-invariants.md) — why the unused-key guard stops at page-level keys; `mod_no_slot` is read programmatically
- [Scope axis: reach, entry vs exit](scope-axis-entry-exit.md) — ADR-0015's blast-radius test, the four surfaces that carry it verbatim, and when a label/diff gap is not a defect
- [Contract block names, never status](contract-block-carries-names-not-status.md) — ADR-0012's block is naming vocabulary; mandatoriness cannot be read off its key shape
- [gh search swallows a leading in:](pitfall-gh-search-in-qualifier.md) — the query returns every issue, exit 0; check any documented `gh search` against a negative control
- [Rule placement inside a SKILL.md](pitfall-rule-placement-in-skills.md) — a rule nested under Step N binds only from Step N; list the yield points above it
- [site/ and tools/ as peer apps](scope-rubric-vs-site-tools-coupling.md) — the two-app split mislabels every site-prose ticket; judge by blast radius and say so
- [Where format rules are restated](sweep-surface-format-rules.md) — the surfaces a specs-format sweep has to reach, two agent-executed and two generated
