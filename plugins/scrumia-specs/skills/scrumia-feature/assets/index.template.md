# <Feature name>

**Status**: draft | active | deprecated

## In brief

<What this feature does and for whom, in 10 lines maximum. If you can't manage
that, the feature is probably too big — see the splitting criterion. No rule,
no decision, no rationale here: the index indexes, and a claim that needs
elaborating gets a one-line pointer to the file that carries it.>

## Links

<For an App feature:>
- Business parent: `features/business/<feature>/`
- Consumes: `features/app/<app>/<feature>/`
- Authority: `<design/ or docs/ file that answers a question this feature
  defers>` — <one line of key info>

<For a Business feature:>
- Implemented by: `features/app/<app>/<feature>/`

<Authority lines are pointers, one line of key info each — which file answers
which question — never the answer itself.>

## Files present

| File | Read it when |
|---|---|
| `business.md` | <the situation that makes an agent open it, in one line> |
| `qa.md` | <in one line> |
| `CHANGELOG.md` | <in one line> |

<List only the files actually present. The mandatory files are always among
them; `index.md` does not list itself. For the rest, an absent file is an
assertion: nothing to say on this subject. The column answers "when do I need
to open this?" — the agent deciding what to load is this table's reader.

No ticket number anywhere in this file: the tracker owns which issues concern
a feature, and is searched, not cached here.>
