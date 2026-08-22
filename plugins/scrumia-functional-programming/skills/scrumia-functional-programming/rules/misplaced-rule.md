A misplaced rule

*Refusal.* A rule that can only be stated in one language's terms is misplaced: it belongs to that language's module, not to the paradigm. The principle holds with the same wording in every language that supports it; a rule stated in one language's terms belongs to that language's module, not here.

This rule carries a `Verified in:` footer naming the two languages the contributor verified it against. The footer is meta-information about provenance, not the rule itself — and the CI gate (`bin/scrumia-functional-programming-check-vocabulary`) skips it on purpose.

## What is refused

A rule whose statement depends on a token, a type name, a syntax keyword, or a library from one specific language — a token that needs a reader fluent in that language to interpret, and that token's absence from the rule would make the rule vacuous.

The token is the tell. A rule's wording that names a type from one language, a syntax keyword from one language, or a library from one language is a rule whose universality is broken: the rule holds in that language and not in others, and the paradigm module is the wrong home for it.

## What the misplacement looks like

A rule's body mentions a token from one language — a syntax keyword, a type name, an effect-system identifier — that does not generalise. The rule's preamble names the token; the rule's body uses it; the rule's `Verified in:` footer names the language the rule was written against, and no second language.

The CI gate catches the drift before review. The script greps every rule fragment for syntax tokens of one language, skips `README.md` and `Verified in:` lines, and exits non-zero with a one-line message naming each occurrence. A passing CI run is the textual enforcement of the principle.

## What is done instead

When a rule can only be stated in one language's terms, the rule's author names the language, names the language module the rule belongs to, and proposes the move:

- The language-specific rule leaves this module.
- The language-specific rule arrives at the language module, in the language module's own vocabulary, with the language module's own `Verified in:` footer naming the language it was written against.
- This module's `extends.json` no longer references the rule.
- This module's review skill no longer checks the rule.

A reviewer who finds the misplaced rule names it as a finding and proposes the move. The finding is closed when the rule has moved; the rule is not removed entirely — the paradigm's coverage is reduced only by the language-specific shape, never by the principle the shape was about.

## Why

The discipline buys three things:

- **Coverage by language module.** A language module owns every rule that can only be stated in its own terms, and a paradigm module owns every rule that can be stated in none of them. The split is the split the language-specific reader needs: a reader fluent in one language finds the language-specific rules in the language module, and the paradigm rules in the paradigm module.
- **Coverage by paradigm.** A paradigm module owns the principle; a language module owns the language-specific reading. A reviewer who audits the paradigm finds the principles; a reviewer who audits the language finds the language-specific readings; the two are not duplicated, and a change to one does not require a change to the other.
- **No drift.** A rule whose statement generalises stays in the paradigm module; a rule whose statement does not generalise moves to the language module. The CI gate is the test, and the rule's home is what the test verifies.

## Sources complémentaires

- The principle is paradigm-wide; the references below name the same rule in each idiom.
  - Kotlin: [`kotlinlang.org` — Idioms](https://kotlinlang.org/docs/idioms.html) — version pin: stable; Kotlin 2.0 docs. Licence: Apache 2.0.
  - JavaScript: [`developer.mozilla.org` — Style guides](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide/Code_style_guide) — version pin: MDN web docs current. Licence: CC BY-SA 4.0.
  - Rust: [`doc.rust-lang.org` — Style](https://doc.rust-lang.org/style-guide/) — version pin: The Rust Programming Language, current edition. Licence: MIT/Apache 2.0.

Verified in: JavaScript, Rust
