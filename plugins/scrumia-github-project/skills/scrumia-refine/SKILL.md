---
name: scrumia-refine
description: Refines a backlog ticket until it is ready for development — calls on the roles with the global view, splits into sub-issues when necessary, updates the specs. Use it to move a ticket from Backlog to Ready for dev.
---

# Refine a ticket

A backlog ticket carries an intent. Refinement turns it into something executable — or reveals that it must be split, or that a human decision is missing.

Usage: `/scrumia-github-project:scrumia-refine 42`

## What "ready for development" means

Four conditions, all verifiable:

1. A parent feature exists and is up to date
2. The acceptance criteria are written, identified in the format named by `ac_id_format`, and can fail
3. The scope is known: which apps, which anticipated files
4. No open question blocks the start

A ticket that doesn't meet all four stays in the backlog. Moving it forward anyway shifts the problem to execution, where it costs more.

## Step 1 — Read the intent

`gh issue view <n>`. Look for what the ticket wants to achieve, not how to do it. If the intent itself is vague, the ticket belongs to scoping: send it back to the scoping module rather than guessing.

Don't assume the card starts in `Backlog`. A card added to a board arrives with **no Status** — `gh issue create --project` does not place it in the first column, it places it in none. If `scrumia-board find <n>` shows a card with no status, set it (`scrumia-board move <n> Backlog`) before refining, so the transition at Step 7 moves it from a real state rather than from nothing.

**If `gh` fails** — not authenticated: say so and point to `gh auth login`; the human runs it, this skill doesn't. Network or API error: retry once, then report and stop, don't loop on a flaky call. No repo or no remote: name the missing prerequisite (`.git`, a GitHub remote) and stop. Refinement starts by reading the ticket — without it there's nothing to refine, so stop here rather than guess the intent from memory.

## Step 2 — Check against the specs

**Read `CLAUDE.md`'s `## Specs contract` section first** — it names the specs module's own vocabulary (`specs_root`, `feature_index`, `acceptance_file`, `ac_id_format`, `changelog`, `catalog`; `docs/adr/0012-specs-contract.md`). Never assume `scrumia-specs`'s own file names directly: a different module can occupy the `specs` slot with a different layout.

**If the section is absent** — no specs module documented, or `scrumia-init` not yet run — say so: *"no specs module documented — ask the human or proceed without spec updates"*, and skip to Step 3.

Through the plugged-in specs module: does the relevant feature exist? Does what the ticket asks contradict a rule already written? Is a rule missing to settle the question?

Three possible outcomes:

- **The spec already covers the need** → the ticket cites the existing identifier in `ac_id_format`
- **The spec must evolve** → refinement produces the spec update, not just the ticket
- **The spec contradicts the ticket** → escalate, don't settle it

## Step 3 — Call on the roles when it's useful

If the team module is plugged in, bring in a role **when its answer changes the ticket's content** — not to cover the decision.

| Situation | Role |
|---|---|
| A business rule is ambiguous or missing | Business |
| The ticket touches several apps, or an interface contract | Tech |
| Feasibility drives the splitting | Tech |

Without a team module plugged in, ask the human. It's slower and perfectly viable.

## Step 4 — Split if necessary

A ticket splits into sub-issues when:

- It touches several apps — one sub-issue per app, because the implementation context differs
- It mixes a spec change and an implementation
- Its parts can be delivered separately without breaking each other

It does **not** split because it looks big. A splitting that produces pieces that can't be delivered independently adds coordination without reducing risk.

Each sub-issue gets its feature, its identifier in `ac_id_format`, its scope and its label. The parent becomes the tracking point and carries the `epic` label.

Link them as **native sub-issues**, not as a checklist in the parent's body:

```bash
gh issue edit <parent> --add-sub-issue <child>,<child>
```

GitHub then computes the parent's progress itself (`subIssuesSummary`), which is what `scrumia-board epic <n>` reports. A checklist typed into the body is a second count that stops matching the moment a child is closed without someone ticking the box.

## Step 5 — Set the scope and the risk

Two labels, two independent questions. Getting this wrong is not cosmetic: `scrumia-pick-model` reads both to decide which model executes the ticket. Who reviews the PR is **not** one of the consequences — gate 2 routes that by the diff's actual scope, not by this label ([`docs/adr/0005-validation-gates.md`](https://github.com/tibs245/scrumia/blob/main/docs/adr/0005-validation-gates.md)). A higher label buys a stronger model, never an extra reviewer.

One `scope/*` label, based on three objective questions: how many apps are touched, **does a rule consumed beyond one feature or app change**, and does an interface contract change.

| Label | Condition |
|---|---|
| `scope/S` | ≤1 app, no rule changes: it is already written |
| `scope/M` | ≤1 app, a rule changes, read only in its feature, or unclear |
| `scope/L` | ≥2 apps, a rule read beyond its feature, or interface contract |
| `scope/XL` | New value unit, pivot, data migration: back to scoping |

The second question is the one that gets misread, so read it as written: it measures **a rule's blast radius, not a file's location**. A rule read beyond its feature is a contract another app depends on, a vocabulary another feature reads, an invariant another feature enforces. A ticket that edits files under the specs root without changing any such rule has answered *no* to it. The label is then `scope/M`, or `scope/S` if no rule moved at all — unless question 1 or question 3 carries it to `scope/L` on its own.

That test is stated once, in [`features/business/execution-policy/business.md`](https://github.com/tibs245/scrumia/blob/main/features/business/execution-policy/business.md) § *The scope axis measures reach, not medium*, and this table applies it rather than defining it. The Condition cells are [ADR-0015](https://github.com/tibs245/scrumia/blob/main/docs/adr/0015-scope-measures-reach.md)'s, copied word for word — including their terseness, which exists so the same wording fits the `scope/*` label descriptions a fresh install seeds. Do not smooth them out here; a smoothed cell is a second definition. Where the deliverable *is* specs, the file-location reading this replaced made every ticket `scope/L` and the axis stopped discriminating.

When hesitating between two levels, take the higher one: one tier too high costs a stronger model than the ticket needed, one tier too low costs a botched ticket. Round up for capability, not to buy a reviewer — the diff decides that either way.

Then one `risk/*` label, answering a different question: **what does it cost if this is wrong in production?** Not how hard it is — how expensive the mistake is.

| Label | Condition |
|---|---|
| `risk/low` | Reversible in a commit, no data touched, no user-visible behaviour |
| `risk/medium` | Visible to users, but a revert restores the previous state |
| `risk/high` | Money, personal data, authentication, or a contract other apps consume |
| `risk/critical` | Irreversible: a migration that drops data, a payment, an outbound notification |

Size and risk are independent, and their independence is the point. A one-line change to a VAT rate is `scope/S risk/critical`; a thousand-line mechanical rename is `scope/L risk/low`. A ticket small enough to look harmless is exactly the one that gets executed casually — the risk label is what stops that.

If the ticket carries no risk label, execution assumes `execution.unrated_risk` and says so; the assumption is visible, not silent. Setting it here is still better than having it guessed.

## Step 6 — Decide whether the human must validate

Escalate to the human when:

- A business rule had to be invented to move forward
- The splitting changes the scope of what was asked
- The ticket is `scope/L` or touches a contract consumed by other apps
- A role gave an opinion with reservations

Otherwise, move the ticket to `Ready for dev` directly. The configured autonomy level (`settings.autonomy.level`) widens or narrows what you can decide alone: in `guided`, the human validates every transition; in `assisted` and above, only the cases above get escalated.

## Step 7 — Report back

On the issue: what was clarified, the specs updated, the sub-issues created, the scope chosen and why, the questions left open.

Then move the card to the `ready` step — or leave it in `Backlog` and say what's missing:

```bash
scrumia-board move <n> ready
```

`ready` is a flow step, not a column name; the mapping to this board's actual column lives in the config ([`projects-v2.md`](${CLAUDE_SKILL_DIR}/../scrumia-status/references/projects-v2.md)). If the move fails, continue and report it — a dead column is not a blocked ticket.

## What you don't do

- You don't implement anything.
- You don't decide a missing business rule: you escalate it.
- You don't close the parent ticket when you split it — it tracks its children.
