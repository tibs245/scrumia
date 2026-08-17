# Changelog — agent team

Reverse-chronological. One entry per notable change, one category each.
The reasoning is in the issues; earlier history is in git and the tracker.

## 2026-08-17 — The verdict is posted by the role, with attribution, and `not_run` carries a cause
- Issue: #125
- Category: Added
- Breaking: yes — the verdict vocabulary is now `run` / `not_required` / `not_run`,
  and the verdict is read from the ticket's issue, not from the executor's report.
  A gather that does not know the new state cannot run.

## 2026-08-17 — Role consultation becomes a reflex with an artefact, not an invitation
- Issue: #121
- Category: Added
- Breaking: no

A refinement, execution or review now consults a role on stated conditions — a
business rule is ambiguous or missing, a change reaches beyond one feature or app,
two written statements disagree, or the same question blocks several tickets — and
its report names which roles were consulted and their answers, or states that none
was needed and why. AC-17 through AC-21 cover the four entry points; the rule
itself is stated once in `business.md § When a role must be consulted`, and the
skills cite it rather than restate it.

## 2026-08-16 — Sprint-loop writes are last-writer-wins, with no compare-and-swap
- Issue: #216
- Category: Added
- Breaking: no

## 2026-08-10 — Changelog rebuilt on Keep a Changelog's categories
- Issue: #213
- Category: Changed
- Breaking: no
