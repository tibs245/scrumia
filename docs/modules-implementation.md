# Writing an implementation module

An implementation module answers a single question: **how we code in this app**.

It is the most personal slot in the composition. Two competent developers can hold opposite answers, and neither is wrong. That is exactly why it is a replaceable module rather than a kernel rule.

Two modules exist — [`scrumia-impl-rust`](../plugins/scrumia-impl-rust/skills/scrumia-rust/SKILL.md) and [`scrumia-impl-solidjs`](../plugins/scrumia-impl-solidjs/skills/scrumia-solidjs/SKILL.md). This document is the contract they follow, and the one yours should follow.

## What makes this slot particular

It accepts **several modules simultaneously**, one per app:

```yaml
apps:
  - name: web
    path: apps/web
    type: frontend
    implementation: scrumia-impl-solidjs
    practices: [scrumia-practice-tdd]
  - name: api
    path: apps/api
    type: backend
    implementation: scrumia-impl-rust
    practices: [scrumia-practice-tdd, scrumia-practice-solid]
```

An app without a module follows the neighboring code's conventions. That is normal behavior, not a gap — and often the right choice on a project whose conventions are already stable.

## The contract

An implementation module provides a main skill that the agent loads **before writing code** in the covered app. It covers four things:

### 1. How we test

The most structuring point, and the one that varies most. To cover:

- Which level of test for which type of change
- Where tests live, how they are named
- What gets simulated and what doesn't — that boundary decides the value of the whole suite
- How an acceptance criterion `AC-n` becomes a test, and how the link stays visible
- How to write a failing test first, if the module is TDD-oriented

### 2. Which design principles

Named and **situated**, not invoked. "We apply SOLID" guides nobody. What guides:

> Dependency inversion applies at infrastructure boundaries — database, HTTP, filesystem. It does not apply between two functions of the same module: the indirection there costs more than it earns.

A principle without an application limit becomes a reflex, and a reflex produces useless abstraction.

### 3. How the code is structured

The expected tree, what goes where, what is not allowed to depend on what. Precise enough that an agent places a new file without hesitating.

### 4. What we refuse

The most useful part, and the most often forgotten. The patterns this module rejects, with the reason for the rejection. An agent that knows what is refused corrects itself; an agent that only knows best practices applies them everywhere.

## Composing with the `practices` slot

Some answers are not stack-specific: TDD answers "how we test" the same way in Rust and SolidJS — only tooling and examples change. Those answers live in **practice modules** (`scrumia-practice-tdd`, `scrumia-practice-solid`), plugged app by app alongside the implementation module. See [ADR-0010](adr/0010-cross-cutting-practices.md).

An implementation module's part of the bargain is a **"With the practices" section**: for each practice it knows, a short conditional paragraph — "if this practice is plugged into the app, here is how it lands on this stack". Tooling, idioms, exceptions. A practice the module doesn't know still applies, just unsituated: degraded, not broken.

The one precedence rule: **specific beats generic**. Where the implementation module restricts a practice — `scrumia-impl-rust` refuses dependency inversion between modules of the same crate, whatever SOLID says — the implementation module wins. The project override wins over both.

## How an agent actually loads this

Being plugged in per app (`apps[].path`) is not the same as being read in full on every edit. An agent resolves the app from the file's path, then opens each plugged module's skill index — its `SKILL.md`, nothing more at that point — and loads only the reference guide(s) the index's routing table selects for the kind of change at hand, within the module's `section.json` globs for that app. A module says nothing about files outside its globs; neighboring conventions apply there.

`scrumia-init` can shortcut step one of this: a per-app `CLAUDE.md` stub at `apps[].path`, naming the app's modules and their index paths, picked up by Claude Code's native nested-`CLAUDE.md` loading before the agent even reaches the root composition table. Details in [docs/composition.md](composition.md#from-the-table-to-the-file-how-a-module-is-actually-consumed) and [ADR-0011](adr/0011-rules-hierarchy.md).

## Overriding without forking

A module must be adjustable by a project without being copied. Two mechanisms:

**Declared settings** — the module documents what it reads:

```yaml
settings:
  implementation:
    scrumia-impl-solidjs:
      test_runner: vitest
      coverage_threshold: 80
      strict_mode: true
```

**Project override file** — the module reads an optional file, `.scrumia/impl/<module>.md`, whose content wins over its own rules. A project adds a house convention this way without touching the module.

A module that provides neither will be forked at the first disagreement, and the fork will never receive updates.

## An audit skill

Both existing modules ship a second skill (`scrumia-rust-audit`, `scrumia-solidjs-audit`) that measures the gap between an existing app and the module's rules, finding by finding, without rewriting anything. It serves the moment that decides adoption: plugging the module into code that predates it. Ship one — a module that can only judge code born under its rules will never be plugged into anything real.

## Where the design system meets this contract

`scrumia-design` fills the `design` slot — see [modules.md](modules.md). It matters here because the two contracts touch and must not overlap: **the implementation module owns how a component is written** (file layout, props, tests), **the design module owns what it looks like**. A SolidJS component and a Rust-served template consume the same tokens.

So an implementation module does not answer "which blue", and the design module does not answer "where does this file go". Where they appear to disagree, they are answering different questions — re-read which one. A genuine conflict, such as an implementation module mandating a styling approach that cannot read the design tokens, is a composition problem to escalate, not a precedence call.

## Writing yours

1. Create `plugins/<name>/` with its `.claude-plugin/plugin.json`
2. One main skill, loaded before writing code, covering the four points of the contract
3. A "With the practices" section situating the known practices for your stack
4. An audit skill, for plugging into existing code
5. Document the settings read under `settings.implementation.<name>`
6. Provide for the project override
7. Add the marketplace entry, validate (`claude plugin validate`)
8. Plug it in app by app in `.scrumia/config.yaml`, then regenerate `CLAUDE.md` via `scrumia-init`

An implementation module is not meant to reach consensus. It is meant to be explicit — so that it can be replaced.
