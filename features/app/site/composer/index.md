# Composer — the home page's build-your-composition section

**Status**: active
**Stratum**: app (`site`)

## In brief

The `#composer` section of the home page: the same seven slots the `slot-index`
feature *reports*, offered as choices. The visitor answers each slot — or leaves
it empty on purpose — and takes away two artifacts: the install commands for the
modules they picked, and the `.scrumia/config.yaml` that declares the
composition.

It is the only place on the site where a visitor does something rather than
reads, which is why it is drawn as a composition assembling rather than as a
form being filled.

## Where the authority sits

| Question | Answered by |
|---|---|
| What is a slot, and which seven exist? | `features/business/modular-composition/index.md` |
| How is a slot row drawn? | `design/components/slot-index/spec.md` |
| What does an empty slot cost? | `features/business/modular-composition/business.md` (BR-2, AC-4) |
| What consumes the emitted config? | `plugins/scrumia-core/skills/scrumia-init/SKILL.md` |
| Which values may be used? | `design/tokens.css` |

## The rules this feature owns

**One drawing of a slot, in a third state.** The composer does not draw its own
slot. It reuses `slot-index`'s row — `sign · name · question · leader · fill` —
and adds *choosable* as a third state alongside filled and empty. A second
drawing of a slot would undo the ruling #61 landed on.

**The two indexes are told apart by colour, not by shape.** `#slots` reports
this repo's composition and its fills are `--text-soft`; `#composer` records the
visitor's decisions and its fills are `--human`, because choosing is the one
human act in the section. That is `design/identity.md`'s decision 1 applied, not
a decoration.

**Choosing needs no JavaScript.** `<details name="composer-slot">` owns what is
open, native radios and checkboxes own what is chosen, and CSS `:has()` owns
which fill the row reports. Script owns exactly one thing: writing the two
takeaway artifacts. With scripting off the index still opens, still chooses and
still reports — and the artifacts are pre-rendered in the template to match the
default composition, so the page never shows a stale or empty takeaway.

**Empty is an offered option, never an unasked one.** Every slot carries a
`leave it empty` choice whose description states what the absence costs, in the
voice of `modular-composition`'s AC-4: named degradation, work continuing. No
sentence may imply the agents break. A slot the visitor was never asked must not
be emitted as a decided `null` — which is why `design` is a question here and
not a silent default.

**The consequence survives the copy.** An empty slot's cost is stated three
times, each in the idiom of where it sits: in the option's description at
decision time, in the open row's gap line after the fact, and as a comment on
the `null` in the emitted YAML — the only one of the three that survives being
pasted into a repo.

**`implementation` and `practices` are per app.** They are the two slots that
repeat, so they are checkbox rows, and a practice attaches only to the app types
it applies to. Assigning a frontend data-fetching practice to a backend app is
the bug this rule exists to prevent.

**The install claim is the real one.** No one-liner consumes a generated config;
claiming one would be the promise `modular-composition`'s BR-3 forbids modules
from making, and the site gets no exemption. What the composer claims is what is
true: commit the file, install the modules, run `scrumia-init` — which finds an
existing `.scrumia/config.yaml` and verifies it instead of proposing one.

**The emitted YAML matches init's schema.** `project:` with `name` and `repo`,
all five `composition:` keys spelled even when `null`, and `apps[]` carrying
`name`, `path`, `type`, `implementation`, `practices`. The composer never
fabricates a `settings:` block: those are each module's setup skill to write,
and init filling them in later is not drift.

## Files present

| File | Why it exists |
|---|---|
| `qa.md` | The criteria the composer must keep passing |
| `CHANGELOG.md` | History of changes to this spec |

No `business.md`: the rules about slots and absence are
`modular-composition`'s. No `ux.md`: the row anatomy and the interaction are
fully specified by `design/components/slot-index/spec.md`, and a second copy is
what the design contract exists to prevent.

## Open issues

- The `aria-live` delta line announces the slot and its new fill. Whether it
  should also announce the artifacts changing is untested with a real screen
  reader — noted for a follow-up, not guessed at here.
- `--human` on `--ground` is a new contrast pair: the composer is the first
  place a fill carries the human hue. It belongs in `tools/check_contrast.py`.
