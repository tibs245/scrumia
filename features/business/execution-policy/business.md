# Business rules — execution policy

Vocabulary: **scope** (how far a change reaches, carried by a `scope/*` label),
**risk** (what it costs if the change is wrong, carried by a `risk/*` label),
**cell** (the grid entry the two axes cross at), **decision** (what the policy
returns for a ticket: a model to run on, or a preference to split carrying a
fallback model), **deviation** (a run that did not happen the way the policy
preferred — a human override, or a split the executor refused).

## Two axes, and their independence is the point

Scope and risk answer different questions and are never collapsed into one number.

**A one-line change to a payment rule is `scope/S risk/critical`.** Nothing about how
much code moves predicts what it costs to get wrong, and the ticket small enough to
look harmless is exactly the one that gets executed casually. The reverse case is as
real and as common: a mechanical rename across two apps is `scope/L risk/low` — wide,
and cheap to revert.

A single axis would have to pick one of those two to serve and would mis-handle the
other. Two axes, set independently at refinement, are what let the grid spend
capability where the cost of error is, rather than where the diff is.

## The scope axis measures reach, not medium

`scope/*`'s spec clause reads a rule's **blast radius**, not a file's location.
"A business spec changes" means **a rule consumed beyond one feature or app changes**
— a contract another app depends on, a vocabulary another feature reads, an invariant
another feature enforces. A ticket that edits files under the specs root without
changing any rule another feature or app consumes does not reach `scope/L` on that
clause; it is judged on the axis's other questions — how many apps it touches, whether
it changes an interface contract.

The file-location reading fails on a whole class of repository, and not rarely: where
the deliverable *is* specs, every ticket touches a spec file by construction, every
ticket is `scope/L`, and the axis stops discriminating. ScrumIA is such a repository.
The 2026-08-08 sprint overrode the resulting answer on all five of its tickets in the
same direction (#32), and the refinement of #34, #35 and #36 hit it again. An axis that
must be overridden systematically is not a strict axis — it is noise wearing a label.

**The test belongs to the axis, not to one of its readers.** `scope/*` has two: this
policy, which reads it for capability, and the manager's entry routing, which reads it
for who is asked while the ticket runs (`features/business/agent-team/business.md`).
It had a third until #130 — the review owed at exit — and that one now routes by the
diff's actual scope and reads no label at all (`docs/adr/0005-validation-gates.md`).
One label read two ways is two labels, and the second one drifts unobserved because
nothing names it.

`docs/adr/0006-ticket-routing.md` decided the axis and its three verifiable
questions — how many apps, does a spec change, and which one. This spec does not
replace them; it says what the second and third *measure*. The ADR's own table renders
them in the file-location wording, and an accepted ADR is never edited
(`docs/adr/README.md`), so aligning it is a superseding ADR's job — tracked in #78,
along with the plugin prose and the GitHub label descriptions that restate it.

## The grid is project data; what it must satisfy is not

Which model runs a given cell is a project's own call, and it changes on the vendor's
model-release cadence. The cells are therefore **not specified here**. What is
specified is the invariant any grid must satisfy:

> Along a capability order the project declares, **no cell is less capable than a cell
> it dominates**. Climbing either axis never descends the order.

The order is *declared*, not inferred: model names carry no ordering of their own, so a
grid can ship inverted, parse cleanly, pass every check and run — spending the weak
model where the risk is and the strong one where it is not. That is not hypothetical;
it shipped through a full sprint unnoticed (#47).

It is declared **once, in the project's configuration, beside the grid it governs**, so
that the two are read and edited together. It is deliberately not restated in this
spec: a second statement would go stale on a cadence this spec does not follow, and
would be exactly the duplicate the next section refuses.

**A cell preferring a split is not a placement on that order.** `split_or_<model>` names
the model taken *if* the split is refused; it is a fallback, not a rating. Comparing one
against a bare model in a neighbouring row is comparing two different kinds of statement,
and an invariant check that treats them as comparable reports a correct grid as broken —
which is worse than not checking, because it trains its reader to ignore it.

What that carve-out does **not** license is exempting those cells from the invariant.
Fallbacks are compared against fallbacks, along the same order: a row of split-preferring
cells whose fallback descends as risk climbs is inverted exactly the way a row of bare
models would be, and it is the more dangerous inversion because it is the one taken when
a split has already been refused. The rule is that the invariant compares like with like
— not that one kind is unchecked.

A grid whose configuration declares no capability order at all is not a grid with nothing
to violate: it is a grid the invariant cannot be checked against, and that is reported.
A check that silently does not run misleads its reader as surely as one that cries wolf,
and this is the state a project is in until it declares the order beside its grid.

## The order runs higher than the grid does

A capability order names every model the vendor sells, including ones a project is not
willing to spend on by default. So the project declares a **ceiling** beside the order,
and the invariant is that **no cell names a model above it** — not the bare cells, and
not the fallback a split-preferring cell carries.

The ceiling is a spending judgement, not a capability one. A cell above it bills at that
rate on every ticket it matches, indefinitely, and nobody re-reads a grid that is
working — which makes the top of the order precisely the place a default does the most
damage. Above the ceiling the choice is made per ticket, by the human who wants it there,
and it arrives the way every other departure from the policy's answer arrives: as a human
override, recorded as a deviation with its reason (below).

Which model is the ceiling is project data, declared beside the order in the same
configuration and for the same reason — the two are read, edited and go stale together.

## One reader, one decision

A caller asks the policy and acts on the **instruction it answers with**. It does not
open the grid and read the cell for itself, and it does not re-derive the decision from
the labels.

The reason is not convenience. A caller that re-derives is a second implementation of
the policy, and it will not carry what the first one carries — the fallback for a
missing label, the assumption stated out loud, the split preference, the refusal a
cell without a fallback expresses. The two answers agree on the easy cases and diverge
on exactly the ones the second implementation never considered. One reader means one
place to change when the policy changes, and one answer to disagree with when it is
wrong.

## Oversized is a preference with a fallback, not a verdict

A cell may say the ticket is too big to execute as it stands. That is a **preference,
not a refusal**: split first, and split properly — into tickets that can each ship on
their own, never into pieces that only make sense delivered together.

If, and only if, the work is genuinely indivisible — one migration, one contract that
cannot be delivered by halves — it runs on the fallback the cell names, and the refusal
of the split is recorded as a deviation (below). An oversized ticket is a reason to
think again, not a wall.

A cell may also refuse outright, naming no fallback. Then the ticket returns to
refinement, and no caller promotes that refusal into a fallback on its own authority:
the difference between the two is the grid's to state.

## A missing label is an assumption, and it is said out loud

Neither axis is guessed when its label is absent.

- **No `scope/*` label** — the ticket was never sized. The policy runs the configured
  unlabeled default and its answer says the ticket carried no scope label, so the caller
  asks for refinement instead of inheriting an estimate nobody made.
- **No `risk/*` label** — the risk was never rated. The policy assumes the configured
  default and its answer names the value it assumed, so a ticket that is in fact riskier
  can be flagged on the spot.
- **No cell for the pair** — the grid has a hole. Same treatment: the unlabeled default
  runs, and the gap is reported rather than papered over.

An assumption that is stated can be contradicted. An assumption applied silently reads
exactly like a rating somebody made, and that is the failure this rule exists to
prevent — not the wrong default, the invisible one.

## A project keeps its own words

A project that already labels its backlog does not relabel it to adopt this policy. Its
vocabulary is mapped onto the axes, in two steps, both configured:

- a **prefix** per axis, so a backlog using `size:` or `T-shirt/` is read without
  renaming a single label;
- an **alias table** per axis, mapping the project's values onto the axes' own —
  `size:S → S`, `risk:red → critical`.

Aliasing translates; it does not add levels. The axes keep four values each, because
the grid is defined over them and a fifth size would be a different grid, not a
different word. A project that needs one is asking to change the policy, and should say
so rather than smuggle it in through a synonym.

## A deviation records what was chosen, what ran, and why

Two events make a run deviate from the policy: a **human override** — the policy chose
one model, another ran — and a **refused split** — an oversized cell preferred a split,
and the ticket ran on the fallback instead. They are one kind of event for the only
reader who will ever ask about them, who has one question — *did this ticket run the
way the policy preferred, and if not, why?* — and must have one place to ask it.

What is recorded, for both: **what the policy chose, what actually ran, and the
reason.** The reason is the load-bearing part. Without it the record says only that
someone disagreed, which nobody can review, and which cannot be told apart from a
mistake. **A deviation recorded without its reason is non-compliant** — not an entry to
complete later.

Two moments, one mechanism:

- **At decision time**, the reason is stated by whoever decides the deviation, in the
  answer that announces it — the same pattern as a missing label's assumption, one step
  later in the chain. The policy's own answer cannot carry it: a deviation happens after
  the policy has spoken, which is why the policy's answer carries the *obligation* to
  state a reason rather than the reason itself. Stated there, it is contradictable while
  the decision is still being made.
- **Durably**, it lives wherever an override lives; split refusals are a second *kind*
  recorded there, not a second mechanism. Which venue that is — a label, a field, a
  structured comment — is chosen in #32, not here.

Repetition is what the record is for. Deviations leaning the same way on the same cell
are that cell asking to be adjusted, and a signal that only survives if it can be
queried. Five overrides written into five PR bodies in one sprint did not survive; that
is what produced #32.

The policy's answer stays the default. Recording a deviation makes it visible — it does
not make it a second way to pick a model.
