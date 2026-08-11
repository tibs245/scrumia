---
name: scrumia-solid-principles
description: The ScrumIA SOLID reference — the five principles, each with its limit of application, in OO and functional alike. Load it before writing or designing code in an app where the SOLID practice is plugged in.
---

# Designing with SOLID — and knowing when to stop

This practice refines one point of the implementation contract: **which design principles**. It applies to apps that list it in their own `extends` in `.scrumia/config.yaml`. When an implementation module is plugged in, it situates these principles for its technology — and **specific beats generic**: if the implementation module restricts a principle, the module is right.

## The core contract

A principle without a limit of application becomes a reflex, and a reflex produces useless abstraction. The question is never "does this code comply with the principle?" but "**what varies here, and what must stay stable?**" — the principles are answers to real variation; without variation, they have nothing to say (why the audit weighs violations and over-applications equally: [D-01](decisions/D-01-over-application-audited-equally.md)).

- **S — One reason to change.** A module groups what changes together, for the same requester. → [guides/01-srp.md](guides/01-srp.md)
- **O — Open for extension, closed for modification.** Applies at *proven* variation points only. → [guides/02-ocp.md](guides/02-ocp.md)
- **L — Every implementer honors the entire contract.** The only one of the five with no over-application case. → [guides/03-lsp.md](guides/03-lsp.md)
- **I — Thin interfaces, cut to the consumer's measure.** Thin does not mean atomized. → [guides/04-isp.md](guides/04-isp.md)
- **D — Depend on the contract, not the concrete — at the boundaries.** Between two modules of the same domain, call directly. → [guides/05-dip.md](guides/05-dip.md)

In practice, on real code: **D at the boundaries** and **S on the hot files** give the most frequent, most profitable findings. **L** is rare but serious — it's a contract lie. **O** and **I** are handled when the variation is there, not before.

What we refuse, beyond each principle's own limit:

- **The single-implementer interface** created "just in case" — the day the second implementer arrives, the extraction costs ten minutes; that is the moment to pay it, not before. (rationale: [D-01](decisions/D-01-over-application-audited-equally.md))
- **The indirection layer without variation** — service → repository → DAO, three names for one behavior. → [guides/05-dip.md](guides/05-dip.md)
- **Inheritance to reuse code** — inheritance expresses a contract ("is substitutable for"), not a sharing of lines; to share, compose. → [guides/03-lsp.md](guides/03-lsp.md), [guides/02-ocp.md](guides/02-ocp.md)
- **The refactor "for SOLID" without a finding** — resolved one finding at a time by `scrumia-solid-refactor`, never for general compliance.

## Guides

| File | Use when you need to... |
|------|--------------------------|
| [01-srp.md](guides/01-srp.md) | Decide whether a module, function, or component groups the right things — or should split |
| [02-ocp.md](guides/02-ocp.md) | Add a case at a variation point without reopening the existing cases |
| [03-lsp.md](guides/03-lsp.md) | Check that every implementer of a contract can be substituted safely |
| [04-isp.md](guides/04-isp.md) | Size an interface, trait, or props surface to its actual consumer |
| [05-dip.md](guides/05-dip.md) | Decide whether a boundary needs an owned contract, or a direct call is fine |

## Routing table

```
"I'm splitting, merging, or naming a module/function/component"
  → 01-srp.md

"I'm adding a case to something that branches on a type"
  → 02-ocp.md

"I'm implementing, overriding, or mocking an existing contract"
  → 03-lsp.md

"I'm designing or reviewing an interface, trait, or component's props"
  → 04-isp.md

"I'm calling infrastructure (DB, HTTP, filesystem, clock, third-party) from domain code"
  → 05-dip.md

"I'm auditing a whole app for design findings"
  → 01 + 02 + 03 + 04 + 05 (see scrumia-solid-audit)

"I'm resolving one design finding"
  → the single guide matching that finding (see scrumia-solid-refactor)
```

## Dependencies between guides

```
01-srp  ← standalone, no dependencies
02-ocp  ← standalone, no dependencies
03-lsp  ← standalone, no dependencies
04-isp  ← standalone, no dependencies
05-dip  ← standalone, no dependencies
```

The five are independent lenses on the same code — none assumes another was read first. Real findings often combine two (a D violation on a file that is also an S violation); read whichever guides the finding names, in any order.

## Decisions

| D-NN | Decision | Related guide |
|------|----------|----------------|
| [D-01](decisions/D-01-over-application-audited-equally.md) | Over-application audited on equal footing with violations | all five guides |

## Settings

Under `settings.practices.scrumia-practice-solid` in `.scrumia/config.yaml`:

```yaml
settings:
  practices:
    scrumia-practice-solid:
      boundaries: []      # project-specific infrastructure boundaries where D applies
                          # e.g. ["stripe", "pdf-engine"] — added on top of the standard boundaries
```

## Project override

If `.scrumia/practices/scrumia-practice-solid.md` exists, its content takes precedence over this skill.

## Per-app scoping

This module applies to the apps that list it in their own `extends` in `.scrumia/config.yaml`. Within an app, `section.json`'s globs pick which guides are in scope; the default is all five (`**/*`).

## The module's two other skills

- `scrumia-solid-audit` — record violations **and** over-applications in an app.
- `scrumia-solid-refactor` — resolve a finding, in safe steps.
