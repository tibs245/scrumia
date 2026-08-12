# scrumia-practice-solid

The practices slot for the SOLID design principles — single responsibility through
dependency inversion — each stated with its own limit of application, not only its rule.
Applies app by app, in object-oriented and functional code alike. (Design principles, not
the SolidJS framework — see `scrumia-impl-solidjs` for that.)

## What it answers

Whether a piece of code is under-abstracted, over-abstracted, or actually SOLID — five
guides, one per principle, an audit that reports violations and over-applications on
equal footing, and a refactor skill that closes one finding at a time.

## What it refuses

- No abstraction with a single implementer — an interface introduced "for later" is the
  over-application this module audits for, not a virtue.
- No violation fixed by a general "make it SOLID" pass. `scrumia-solid-refactor` resolves
  one audit finding at a time, in safe, tested steps.
- No principle applied past where an app's own implementation module already draws the
  line — where one is plugged in, its restriction on a principle takes precedence over
  the generic guide.

## What it ships

| Skill | Role |
|---|---|
| `scrumia-solid-principles` | The reference — five guides, one per principle, each with its limit of application. |
| `scrumia-solid-audit` | Measures an existing app against the five principles: violations and over-applications, both reported. |
| `scrumia-solid-refactor` | Resolves one audit finding at a time, in safe, tested steps. |

## Settings it reads

Under `settings.practices.scrumia-practice-solid` in `.scrumia/config.yaml`:
`boundaries`, the project-specific infrastructure edges added to the standard ones
(database, HTTP, filesystem, clock, randomness, third-party services) that Dependency
Inversion applies to.

## What it expects to find

An app that lists `scrumia-practice-solid` in its own `extends`. If `scrumia-practice-tdd`
is also plugged in, `scrumia-solid-refactor` defers to its refactor skill for the safety
net before touching code; otherwise it writes minimal characterization tests itself. An
optional `.scrumia/practices/scrumia-practice-solid.md` records house exceptions without
forking the module.

## Decisions

One so far: why an over-application is audited on equal footing with a violation, rather
than as a lesser note.
