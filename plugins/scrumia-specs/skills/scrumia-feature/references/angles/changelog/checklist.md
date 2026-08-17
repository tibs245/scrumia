# Review guard-rails: changelog

## The entry

- The entry explains why the change was made. The why is in the issue; an entry
  that reasons is a spec starting to grow again.
- It carries a `PR:` field, or a `#NN` placeholder for one. An entry names only
  what exists when it is written.
- It carries two categories, or a category that is not one of `Added`, `Changed`,
  `Deprecated`, `Removed`. `Fixed` and `Security` have no referent in a document.
- A change that both adds and alters is written as one entry. It is two.
- `Breaking:` is missing, or answers something other than yes/no.
- The date is the date of the intent rather than of the change.
- The title describes the work done ("reworked business.md") instead of what the
  spec now says ("MFA required at login").

## The file

- The spec changed and no entry was added — the most common defect, and invisible
  unless you diff the feature.
- An entry was added and no spec file changed.
- Entries are chronological rather than reverse-chronological.
- The file has grown into a narrative, with paragraphs between entries.
- The former wording of a rule is quoted here "for reference". Git has it.

## Against the rest of the feature

- The entry cites an `AC-<n>` that no longer exists in `qa.md`.
- The entry announces something that is not actually in the tree — a rule said to
  be added that no file states. Check the claim against the files, not against the
  entry's confidence.
- A `Deprecated` entry exists and the rule it deprecates is already gone, so
  nothing had a chance to migrate.
