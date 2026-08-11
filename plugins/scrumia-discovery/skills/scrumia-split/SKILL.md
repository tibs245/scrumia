---
name: scrumia-split
description: Splits a scoping into a ScrumIA feature tree (business then app) and creates the matching GitHub issues. Use it after a brainstorm, or to split an existing EPIC into features and tickets.
---

# Splitting into a feature tree

Turns a scoping into written specs (under `specs_root`, if a specs module is documented) and ready issues. This is what replaces the PRD.

Prerequisite: a completed scoping. If the problem and the expected outcome don't fit in three lines, go back to `/scrumia-discovery:scrumia-brainstorm`.

**Check the specs contract first.** Read `CLAUDE.md`'s `## Specs contract` section for the plugged specs module's vocabulary — `specs_root`, `feature_index`, `acceptance_file`, `ac_id_format`, `changelog`, `catalog` (`docs/adr/0012-specs-contract.md`). Never assume `scrumia-specs`'s own file names directly: a different module can occupy the `specs` slot, and steps 1–3 and 5 below must keep working unchanged.

**If the section is absent** — no specs module documented, or `scrumia-init` not yet run — say so: *"no specs module documented — ask the human or proceed without spec updates"*. Skip straight to step 4 (create the issues): tickets can still be scoped and created without written specs. Step 5 has nothing to commit in that case; say so in the report at step 6.

## The tree

```
EPIC (business feature)
├── business feature (unit of value)
│   ├── app/backend feature   (how the backend implements it)
│   └── app/frontend feature  (how the frontend implements it)
└── business feature
    └── ...
```

**Business first, always.** An App feature written before its Business parent ends up containing business rules that will live in the wrong place — and then be duplicated in every app.

## Flow

### 1. Identify the units of value

Split the scoping into units of value that are **independently verifiable**. The test: can you write a Given/When/Then scenario that validates this unit without depending on another unit in progress?

If not, it's not a Business feature — it's a piece of another one.

Apply the specs module's own splitting signals, documented in its writing skill — for `scrumia-specs`, roughly 200 lines in the feature's business-rules file, or a dozen scenarios in the file named by `acceptance_file`. A different specs module documents its own thresholds the same way, in its own main skill. No rules of its own and a single scenario stays the "it's a ticket" signal regardless of which module is plugged in.

### 2. Write the Business features

For each one, via the specs module's writing skill (`scrumia-feature` for `scrumia-specs`). That skill decides which files its module requires of every feature — do not derive that set from which keys sit outside `catalog`, since a key names a file without mandating it. Bring it the subject matter, and whichever `catalog` files the subject demands on top — compliance, cross-app architecture, and so on.

Write what was established during scoping. **Don't invent the missing rules.** A rule invented at this step becomes everyone's reference without anyone having decided it. When a rule is missing, write it as an open question in the file named by `feature_index` and create an issue.

### 3. Project onto the apps

For each Business feature, determine which apps implement it. Then one App feature **per app** — never an App feature covering two.

Each App feature references its parent and records only what is its own. It copies no business rules.

When two apps must talk to each other, the interface-contract file (from `catalog`) is written on the **producer** side; the consumer references it. One authority per contract.

### 4. Create the issues

**First check that a tracker module is plugged in** (the ScrumIA section of `CLAUDE.md`). Without one — or with `gh` unavailable — don't fail: write the ticket list to the scoping report and into the specs PR description instead, and say explicitly that no issue was created. Degraded, not broken.

One ticket per executable unit of work. Each issue carries:

- A title that states the expected outcome, not the task
- The feature it belongs to (path under `specs_root`, if a specs module is documented)
- The acceptance criteria involved (identifiers in `ac_id_format`, from the file named by `acceptance_file`, if a specs module is documented)
- The scope: which apps, which anticipated files
- A `scope/*` label — apply the Manager's grid: number of apps, spec modified or not, type of spec touched

A ticket without an acceptance criterion will not be executable. Create it anyway if needed, but leave it without a `scope/*` label: it will show up as unscoped in `scrumia-status`, which is exactly the intended signal.

### 5. Deliver on a branch, not on the main one

Scoping produces specs. They arrive like any other change: on a branch, in a PR.

```bash
git switch -c specs/<unit-of-value-slug>
```

Commit the written specs, open a PR that references the created issues, and leave it open. The human reviews the design in the same tool as the code — not in a conversation thread that will disappear.

It also provides an anchor point: tickets point to an already readable specs PR, and the refinement that follows starts from something frozen rather than from the memory of a discussion.

### 6. Report back

Show the tree produced, the issues created with their numbers, the specs PR, and **the remaining open questions**. The latter are the most useful part of your report: they are what will cost dearly if forgotten.

## What the split has to satisfy here

```bash
scrumia-extends split
```

Whatever the composition requires of a feature tree or of the tickets it produces arrives
here, from the module that owns the rule. An empty table means the checks below are the
whole obligation.

## Check before concluding

- Every App feature has a Business parent, or an explicit justification for being purely technical
- No business rule appears in two files
- Every feature has at least one verifiable acceptance criterion
- No App feature covers two apps
- No API contract has two authorities

## What you don't do

- No merge: the specs PR stays open, the human validates it.
- No implementation, no code skeleton.
- No empty "fill in later" files.
- No ticket refinement: that's the next step, carried by the tracker module.
