---
name: scrumia-solid-refactor
description: Resolves a design finding — SOLID violation or over-application — in safe, verifiable steps. Use it after scrumia-solid-audit, one finding at a time, never for a general compliance pass.
---

# Refactoring a design finding

This skill addresses **one finding** — from `scrumia-solid-audit` or stated by the user — not overall compliance. "Make the app SOLID" is not an executable request; "the domain imports the ORM in these four files" is.

## Step 0 — The safety net

A refactor without tests is a gamble. Check that the zone is covered:

- If the TDD practice is plugged into the app (listed in the app's own `extends` in the config), its `scrumia-tdd-refactor` skill provides the method for getting under test — apply it first.
- Otherwise, write the minimum of characterization tests on the zone's observable behavior, and say explicitly that this is the only safety net.

If no safety net is possible (code not runnable locally), stop and say why.

## Step 1 — Naming the move

Each type of finding has its standard move. Announce it before starting:

| Finding | Move | Guide |
|---|---|---|
| S violated — module with mixed responsibilities | Extract one responsibility at a time, the most autonomous first | [guides/01-srp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/01-srp.md) |
| O violated — duplicated case cascade | Centralize the variation in one place; open *or* close (exhaustive sum) depending on whether the cases are open or finite | [guides/02-ocp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/02-ocp.md) |
| L violated — implementer that lies | Fix the contract or the implementer — never the caller | [guides/03-lsp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/03-lsp.md) |
| I violated — obese interface | Cut one interface per consumer, migrate the callers one by one | [guides/04-isp.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/04-isp.md) |
| D violated — domain imports the infra | The domain declares the contract, the infra implements it, injection at the entry point | [guides/05-dip.md](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/guides/05-dip.md) |
| Over-application (any principle) — indirection without variation | **Inline.** Remove the single-implementer interface, unroll the delegation, bring it back home | the finding's guide, "Application limits" section; rationale: [D-01](${CLAUDE_SKILL_DIR}/../scrumia-solid-principles/decisions/D-01-over-application-audited-equally.md) |

The last one counts as much as the others: knowing how to remove an abstraction is half the practice.

## Step 2 — In small steps

- One move at a time, green suite between each step.
- A step that goes red gets undone; it is not fixed forward.
- No behavior change — if you discover a bug along the way, note it (an issue if a tracker module is plugged in), don't fix it in this diff.
- Stay within the finding's scope. The dubious neighbor becomes a finding for a next audit, not one more step.

## Step 3 — Report back

The starting finding, the move applied, the proof that behavior is intact (the suite, before/after), and what the refactor revealed without addressing it.

If the app's implementation module imposes structural conventions, check that the result complies with them — a refactor that "improves" the design while violating the app's structure will be undone at the next ticket.
