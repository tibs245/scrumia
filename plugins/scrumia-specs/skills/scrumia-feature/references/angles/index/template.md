# <Feature name>

**Status**: draft | active | deprecated

## In brief

<What this feature does and for whom, in 10 lines maximum. If you can't manage
that, the feature is probably too big — see the splitting criterion. No rule,
no decision, no rationale here: the index indexes, and a claim that needs
elaborating gets a one-line pointer to the file that carries it.>

## Links

<Use only the fixed keys, and declare each link on both sides. The full table
is in the angle's `context.md` § The links.>

- Business parent: `features/business/<feature>/` — <App feature only>
- Implemented by: `features/app/<app>/<feature>/` — <Business feature only>
- Parent: `features/<stratum>/<feature>/` — <child feature only>
- Children: `<subdirectory>/` — <parent feature only; one line on what it is>
- Consumes: `features/<stratum>/<feature>/` — <what is depended on>
- Consumed by: `features/<stratum>/<feature>/` — <who depends on this>
- Defers to: `features/<stratum>/<feature>/` — <the question it answers for us>
- Authority: `<design/ or docs/ file outside features/>` — <one line of key info>
- Boundary: `features/<stratum>/<feature>/` — <what it owns, not restated here>

<Delete the lines that do not apply. The first four are structural and are
declared on both sides — the other feature's index.md gets its half in the
same change. The rest are pointers, one line each — which file answers which
question — never the answer itself.>

## Files present

| File | Read it when |
|---|---|
| `business.md` | <the situation that makes an agent open it, in one line> |
| `qa.md` | <in one line> |
| `CHANGELOG.md` | <in one line> |

<List only the files actually present. The mandatory files are always among
them; `index.md` does not list itself, and a child feature's directory is not
a file — it is declared under Links instead. For the rest, an absent file is
an assertion: nothing to say on this subject. The column answers "when do I
need to open this?" — the agent deciding what to load is this table's reader.

State in prose the absences a reader would otherwise wonder about: "No
`legal.md`: this feature processes no personal data."

No ticket number anywhere in this file: the tracker owns which issues concern
a feature, and is searched, not cached here.>
