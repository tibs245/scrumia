# The role review verdict — venue and read-back

Where the verdict lives and how the gate reads it. The vocabulary and the format
are kept separately (`role-verdict-format.md`, beside it); this file states the
carrier and the read.

## The venue is a comment on the ticket's own issue

`features/business/dev-flow/` requires that a ticket at gate 2 carry the outcome
of its review as a record that survives the executor's death — one of `run`,
`not_required`, or `not_run` with a cause. Three properties no other carrier
has: **unfalsifiable by omission** (no role-signed comment = no review, whatever
the executor's report says), **survives the executor** between review and PR,
and **machine-readable** for the gather. Here is what that becomes on GitHub.

## Why an issue comment

A label is queryable and carries no verdict, and the verdict is the substance.
A Projects v2 field is structured but moves the record into board-side state,
against ADR-0009's "documented composition, no dynamic resolution". A structured
field in the agent's return dies with the session and is written by the
executor — exactly the failure mode the role-posted verdict exists to remove.
A comment carries the verdict, lives beside the ticket, survives the run, and
reuses a carrier the project already writes to rather than inventing a third.

## Who posts it

The reviewing role's agent, not the executor. The executor is the *convener* of
the review, and is not the reviewer — the roles are distinct agents with their
own definitions, and "the author reviews their own work" was never the defect.
The executor running a general agent handed the role's `agents/` file is not a
role review, and the verdict it could write is not a role verdict: the
`claude -p --agent` subprocess is `run` when it ran as the role, and `not_run`
when it did not. This is the substance the attribution clause names, and what
the substitution path closes.

## How it is read back

One ticket: `gh issue view <n> --json comments`, the same read a deviation
record uses. Across the project — which is what the gather needs:

```bash
gh search issues --repo <owner>/<repo> --match comments 'Verdict:' 'by scrumia-*'
```

The two terms are ANDed, and the `by scrumia-*` token is what discriminates a
role verdict from a comment that happens to match the prefix; without it, a
search over `Verdict:` alone returns every issue that quotes the word. The exact
failure mode if the qualifier is folded into the query string is the same as
the deviation record's: GitHub discards what it cannot parse and answers with
the whole repository, exit code 0, no warning.

## The PR body echoes it, and stops being the record

A PR whose ticket carries a role verdict restates it for a human reading the
diff, and that echo is a courtesy. The comment on the issue is what a later
reader queries, and the PR body is a copy of it. Five PR bodies were the whole
record once, in the sprint whose repeated overrides on the same cell went
uncounted for it; the comment is now the record and the PR is its copy.

## Sources

Transcribed here rather than linked, so this module carries what its skills
apply. Open these to argue with the rule, never to apply it — what runs is the
text above.

| What it owns | Where |
|---|---|
| The venue, why an issue comment, who posts it, the read-back query | `features/business/github-tracking/business.md` § *A role review verdict is a comment on the ticket's own issue* |
| Why the record must outlive the executor | `features/business/github-tracking/business.md` § *A deviation record is a comment on the ticket's own issue* |
| The vocabulary the carrier carries | `rules/role-verdict-format.md` (beside this file) |

Those paths name files in the ScrumIA repository, which is not installed beside
this module. They are provenance: if one of them cannot be reached, nothing
above stops working. When one of them changes, this file is what has to be
brought back into line.
