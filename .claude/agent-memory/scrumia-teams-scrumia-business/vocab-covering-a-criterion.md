---
name: vocab-covering-a-criterion
description: Coverage is keyed on the criterion's subject, never the deliverable — plus the two seams still open (practice narrowing, warn/error meaning)
metadata:
  type: project
---

Settled and specified (cite, don't re-litigate): *verifiable* / *can fail* /
*falsifiable* are one property under three names (dev-flow `business.md` § *No
criterion is uncoverable*); the scope of coverage is the ticket's own criteria plus
those it amends (dev-flow `qa.md` AC-12). **The load-bearing ruling to defend: the
form of coverage is keyed on the criterion's SUBJECT, never on the deliverable.**
Deliverable-keying ("this is a docs PR") makes a mixed ticket unsatisfiable — watch
for it re-entering through side doors.

**Still open — practice narrowing:** `scrumia-practice-tdd`'s `guides/03-ac-mapping.md`
Rule 1 keys on "every `AC-n` in scope", the business spec keys on "inside the paths
the practice covers"; the two scopings are not the same set.

**Still open — warn() vs error():** no doc defines the two channels, and the tree
uses `warn()` both for approximations and for decidable advisories. Any text claiming
the channel choice IS the decidable/approximate line must be checked against the tree
first (the tech role's memory holds the operable reading; the two entries disagree at
the edges — that disagreement is itself the open question).
