# Angle: changelog

**Mandatory in every feature, both strata.** The file is `CHANGELOG.md`.

## What this angle answers

What moved in this spec, when, and where to dig for why. It is the only file of a
feature allowed to cite an issue — that is its entire reason to exist.

A spec holds only its current version. This file is what makes that affordable:
without it, the history has nowhere to go and starts leaking back into the rules.

Read by: everyone, to know what moved and where to dig.

## When it activates

Always, and it gains an entry on every notable change — including the change that
creates the feature. No configuration key can switch this angle off.

## The questions to explore it

Per change, in this order:

1. Is this change notable? A typo, a rewording that alters no rule, a reformatting
   is not. A rule added, altered, deprecated or removed is.
2. What is the change, in one line, stated as what the spec now says?
3. Which issue carries the why? That number goes in the entry. If no issue carries
   it, the reasoning has nowhere to live — open one rather than explaining here.
4. Which single category is it: `Added`, `Changed`, `Deprecated`, `Removed`? If
   two fit, it is two entries.
5. Is it breaking for something that consumes this spec — a ticket in flight, a
   test citing an `AC-<n>`, another feature referencing a rule? Say yes or no.

## The four categories

They are [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/)'s, minus
the two that have no referent in a document: a spec rule that turns out wrong is a
`Changed`, not a `Fixed`, and nothing in a spec is a `Security` issue.
`Deprecated` is what a feature citing a rule needs before that rule goes.

## The two rules that shape an entry

**An entry names only what exists when it is written.** The issue number does; a PR
number does not, because the entry ships inside the PR that would number it. The
tracker reaches the PR from the issue, so storing it here buys a placeholder and
nothing else.

**One entry, one category.** A change that both adds a rule and alters another is
two entries — a single label on it would be false about half the change.

## Boundary

**Holds** — one entry per notable change, reverse-chronological: date, one-line
title, issue, category, breaking or not.

**May hold** — a one-line pointer to a migration described in the issue.

**Must not hold**
- the reasoning behind the change → the issue. An entry that explains turns into a
  parallel spec, and that is exactly how a monolithic PRD re-forms
- a PR number, or any placeholder for one
- the former wording of the rule that changed → nowhere; git has it
- more than one category on one entry

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
