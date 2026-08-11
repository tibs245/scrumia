---
name: scope-axis-entry-exit
description: scope/* measures reach (ADR-0015, owned by execution-policy); label routes entry, diff routes exit — and the verbatim carriage across four surfaces is AC-21's to check
metadata:
  type: project
---

Owned and specified: `features/business/execution-policy/business.md` § *The scope
axis measures reach, not medium* (ADR-0015 supersedes 0006); label = entry, diff =
exit (ADR-0005); a label/diff gap is a scoping failure only when the axis's own
questions would have answered higher (dev-flow `qa.md` AC-6). The four surfaces that
must carry the shared wording verbatim are enumerated by execution-policy `qa.md`
AC-21 — including the live GitHub label descriptions, which no repo check sees:
check them with `gh label list`.

**How to apply:** reviewing anything that touches scope labelling or gate 2, treat an
unqualified "label/diff gap = failed scoping" claim as a finding, and check the live
GitHub label descriptions too (`gh label list`) — they are one of AC-21's four surfaces
and no repo check sees them drift.
