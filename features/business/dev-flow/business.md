# Dev flow — business rules

## The two paths

**Brainstorming** — from an idea to a scoped ticket. **Execution** — from a scoped
ticket to a PR. A ticket is the boundary between them: it exists once it carries at
least one verifiable acceptance criterion and names the feature it belongs to (or,
for the bootstrap case, is what it produces — see #18).

## Who decides, on each path

**Brainstorming**

- The human decides whether the idea proceeds, its scope, its priority, and any
  business rule invented along the way to move it forward.
- The agent (`scrumia-discovery`, when plugged in) challenges: it questions the
  problem, the edge cases, the unstated assumptions, the legal exposure. It never
  decides in the human's place.
- If the discovery slot is empty, the human scopes by hand and says so rather than
  improvising a scoping pass. This is a degraded path, not a broken one.

**Execution**

- Agents decide the implementation, within the ticket's scope.
- The standing roles decide within what they own — `scrumia-tech` on architecture
  and implementation quality, `scrumia-business` on business-rule consistency —
  never outside it.
- Neither role settles a business rule found missing mid-execution: that stops the
  run and escalates instead, per `settings.team.escalation.to_human` in
  `.scrumia/config.yaml`.
- **An execution commits its in-flight work to the ticket's branch before the run
  yields control.** A yield is any pause that hands the next move to someone else —
  a role review, a sub-agent, a human verdict, a wait on a check. The rule is stated
  as the general case on purpose: it covers every yield point, including the ones no
  skill enumerates yet, because a pause added later is exactly the one an enumeration
  would leave uncovered.
- What carries an execution's output is **the branch**, not the working tree. The
  working tree belongs to whatever process happens to hold it, and that process can
  vanish while the run is paused; a branch survives it. Uncommitted work is therefore
  not work the run may assume it still has — and a reviewer asked for a verdict is
  reading the branch, so uncommitted work is also not under review.
- The human's unconditional decision point is the merge, per gate 3 below. Under
  `guided` autonomy the human also validates each ticket's transition into
  execution — a second decision, before any agent starts.

## Covering a criterion

An execution must show, for each acceptance criterion it is answerable for, **a test**:
an act of checking that could have come out the other way. A unit test is one form of
test, an integration test another. So are an automated check over the project's own
prose, an audit by an external agent, and a checklist walked case by case. What varies
between them is the executor and the failure mode — a failing assertion, a red CI check,
a **Blocked** verdict, a case that comes out wrong. The requirement never varies.

**The form follows the criterion's own subject, never the deliverable's overall
nature.** A ticket shipping code *and* a spec change owes each of its criteria the form
that criterion's subject calls for, in the same proposal, with no reading under which
either half escapes. Keying the form to the deliverable is what makes a mixed ticket
unsatisfiable: it would demand a unit test of a criterion whose subject is one sentence
in a markdown table.

### The forms, and what makes each fail

| Form | What it is | It fails when | Worked example in this repo |
|---|---|---|---|
| **Unit test** | code exercising one behaviour of the code | an assertion does not hold | `tools/test_build_site.py`'s `test_ac9_link_is_generated_not_hand_written` — it calls `module_link_specials()` with two invented module names and asserts the hrefs it returns were derived from them rather than hardcoded |
| **Integration test** | code standing a realistic whole up and running the real thing across it | an assertion does not hold, on the assembled system | `tools/test_validate.py`'s `test_broken_link_under_features_is_caught` — it builds a throwaway feature tree holding one dangling link, runs the real `check_doc_links()` over it, and asserts the gate reports it |
| **Automated check over the prose itself** | a program reading the project's own text and refusing a structure the rule forbids | the check reports an error and CI goes red | `tools/validate.py`'s `check_doc_links()` — it walks every relative markdown link under `docs/`, `plugins/` and `features/` and errors on one that resolves nowhere, on every pull request and every push to `main` |
| **Audit by an external agent** | a role reading the change against the question that role owns, and returning a verdict | the verdict is **Blocked**, with the failing case named | gate 2 on this very section: `scrumia-business` blocked its first wording, naming the case that wording made unsatisfiable — a mixed ticket owing a unit test for a sentence in a table (#31) |
| **External validation checklist** | the cases written out and walked one by one, by someone who did not write the change, each outcome reported and signed | a case comes out wrong | gate 3 on this very section: its claim that a rule is something *"where there is nothing to execute"* was walked against two mechanisms this repo runs daily — `tools/validate.py` and the gate 2 reviews — and came out false, which is what sent it back |
| **Self-validation checklist** | the same walk, run by the execution over its own diff, against a list stated in advance | a case comes out wrong | the execution's own self-review step, over its enumerated list: an uncovered criterion, an ignored error case, a contract changed without its file, an out-of-scope file |

The last is the weakest, because the author is the checker — and it is still a test: it
has cases stated in advance and a case can come out wrong. It is what remains when no
team module is plugged in, and a proposal says which one ran rather than letting a
self-check read as a review.

**This umbrella is this feature's, and a practice may narrow it.** Where a practice
plugged in through `apps[].practices` uses *test* in a narrower sense — a red test in
`scrumia-practice-tdd` is code exercising code — that narrower sense governs inside the
paths the practice covers, and a criterion there is not discharged by an audit or a
checklist. The forms above say what covers a criterion at gate 2; they never lower a
practice's own bar.

### Which form a criterion's subject calls for

Read this by the criterion's subject. Not by what tooling happens to exist, and not by
how strong a form one could imagine building.

| The criterion's subject | The form it calls for | Worked example |
|---|---|---|
| Behaviour of code the project runs | a unit or integration test | `features/app/site/module-pages/qa.md AC-9` — *the link is generated, not hand-written* — is behaviour of `tools/build_site.py`; `test_ac9_link_is_generated_not_hand_written` calls the function and fails the moment a URL stops being derived from the module's name |
| A property of the project's own text that a program can decide | an automated check over the prose, in the harness CI already runs | *every relative link resolves* is decidable by reading the tree, and `check_doc_links()` decides it — the artefact under test is markdown, and it is executed against |
| A judgement about a rule — is this wording consistent with another spec, is it ambiguous, would an agent reading it do the intended thing | an audit by the role that owns that judgement, at gate 2, returning a verdict on that criterion; a checklist walked against the criterion where no role owns the judgement | `qa.md` AC-13 — *the two acceptance namespaces stay two lists* — is a judgement about wording; `scrumia-business` owns spec vocabulary, and its verdict on the diff is the test |
| A property with finitely many cases that a reader must walk, because no program decides them | a validation checklist: the cases written out, walked, each outcome reported — external where the stakes justify it, the execution's own at minimum | `qa.md` AC-5's two `auto_merge` scenarios, walked against the paragraph that enumerates all three settings (`scrumia-review` Step 5, *Do not merge*), with `.scrumia/config.yaml` supplying the value in force |

**Whether a program can decide a property is settled by running the check, not by
imagining inputs.** A check decides a property when, run over the project's actual
content, it reports nothing a careful reader would not — which is exactly what makes it
shippable as an error rather than a warning. `tools/validate.py` carries both channels
and the choice between them *is* this distinction: `check_doc_links()` errors, because
on this repository's real tree it flags only links that genuinely resolve nowhere;
`check_french_leftovers()` warns, because it counts accented characters and flags a file
past three, which catches leftover French and also catches a page full of proper nouns.
A check that has to warn in order to stay quiet is an approximation: ship it where it
helps, and the criterion still owes the form its subject calls for. Hunting for a
pathological input some future check would mishandle is **not** this test — every
matcher has one, and treating that as disqualifying would empty this row.

**No form is owed merely because it is conceivable.** The mapping is read by subject and
returns one form; *"an automated check could be written for this"* is not a subject.
Read as "always take the strongest form imaginable", it would put a new checker in every
ticket — a cost this rule does not ask for and would not repay.

**Absence of tooling never reclassifies a subject.** Where the subject calls for a test
or a check and none exists, writing it is part of the work — for a behaviour criterion
first of all, and equally for a decidable property of the project's text. What a subject
*is* does not depend on what has been built.

### A section reference is not a form of coverage

Pointing at the section that satisfies a criterion is a claim of **location**, not an
act of verification. The same pointer gets written whether the section says what the
criterion demands or the opposite of it; nothing about it can come out the other way, so
it is not a test.

The location is still required, and the criterion-by-criterion mapping is where it
belongs — a reviewer has to be told where to look. So each line of that mapping carries
**both**: where what satisfies the criterion lives, *and* which form checked it, with
its outcome. "`business.md` § *Covering a criterion*" is half a line; "`business.md`
§ *Covering a criterion* — audited by `scrumia-business` at gate 2, which found the
subject→form mapping operable, Approved" is the line.

**An audit covers the criteria its verdict addresses, and no others.** A clean overall
verdict is not evidence about a criterion the reviewer never named: the form's whole
value is that it can fail on one criterion while passing on the rest, and a blanket
"Approved at gate 2" written against ten criteria restores exactly the property a
section reference had — it comes out the same whichever criterion it is placed beside.
So the audit is asked about the criterion, and the mapping line says what the reviewer
said about *it*. A checklist is read the same way: the case walked has to be that
criterion's case.

### No criterion is uncoverable

Where the first two rows of the mapping do not apply, the third or the fourth does. A
criterion whose subject is prose is not thereby exempt from being tested: it is tested
by an agent at gate 2 or by an executed checklist, and the mapping names **that form and
its verdict** — never a section standing in for one.

What is left over is a criterion no form can be applied to at all, because no concrete
case could contradict it. That is a defect in the criterion, not a gap in this list: it
is reworded, or reported as uncovered, whichever section it points at. It is the same
thing `qa.md` AC-1 refuses at the door.

**This is what *verifiable* means** in § *The two paths*, what `qa.md` AC-1 calls "an
acceptance criterion that can fail", and what ADR-0004 calls verifiable — one property
under three names, not three requirements.

**Which criteria an execution is answerable for**: the ticket's own, plus those it adds
to or amends in the feature's acceptance file. A criterion already standing in that
file and untouched by the ticket is not this execution's to re-cover; it was covered
when it was written.

**Not being answerable for a standing criterion is no licence to break one.** A
criterion the ticket contradicts without touching is a contradiction surfacing
mid-execution: the run stops and escalates under § *Who decides, on each path* →
**Execution**, `qa.md` AC-2's case. And the project's tests and linter run in every
case, whatever the execution is answerable for.

A ticket whose entire deliverable is the specification satisfies the spec-before-code
sequencing rather than waiving it: there is no second half to sequence against. Its
implementation step finding no code to write is a legitimate outcome, not a skipped
step.

## The ticket's criteria and the feature's are two namespaces

A ticket carries acceptance criteria and so does the feature it belongs to. The two
sets are complementary, and they are not interchangeable:

- **A ticket's criteria are a work order.** They say what this ticket must deliver,
  and they expire when it closes. "Remove the placeholder file" is a legitimate
  delivery criterion and will never be a standing guarantee.
- **A feature's criteria are a standing contract.** They say what the feature
  guarantees from now on, and they must keep holding long after every ticket that
  touched them is closed.

Their counts therefore need not match, and a difference between them is not a defect:
one delivery criterion can produce two standing guarantees, some standing guarantees
predate the ticket, and some delivery acts produce none at all. A 1:1 mapping is not
achievable and is not to be demanded.

**A reviewable proposal maps its delivery against the ticket's criteria** — the first
question a reviewer asks is whether the ticket delivered what it promised, and the work
order is what it promised. **It states separately, in its own list, which of the
feature's criteria it added or amended.** Two lists, two purposes, never merged.

**A criterion is cited with its namespace.** Both sets are numbered in the same format,
so a bare identifier means two different things depending on which document the reader
has open. A feature criterion is cited with its file (`dev-flow/qa.md AC-3`); a ticket
criterion is cited bare (`AC-3`). Naming a criterion without saying which namespace it
belongs to is the defect, whichever document does it.

## Where the human gate sits (ADR-0005)

The three-gate model governs the **execution** path. Brainstorming carries no gate
of its own, because the human is already the decision-maker throughout it.

| Gate | Path | Who | Blocks on |
|---|---|---|---|
| 1 — Automatic | Execution | CI, linter, tests | A red check |
| 2 — Agent | Execution | The roles, routed by the diff's actual scope | A **Blocked** verdict |
| 3 — Human | Execution | The human | The merge — always, unless `settings.autonomy.auto_merge` is set past `none` and the PR falls within what it covers |

`settings.autonomy.level` (`.scrumia/config.yaml`) widens or narrows how far into
execution the human reaches, without ever removing gate 3: `guided` adds a human
check on each ticket's scoping before execution starts; `assisted` and `autonomous`
don't. Only `autonomous`, and only where `auto_merge` reaches past its `none`
default, lets gate 3 itself go unattended — the conditions for that are ADR-0005's,
not re-decided here.

`auto_merge` is one scalar for the whole project, not a per-ticket category:
`none` (nothing merges unattended), `docs-only` (a PR touching documentation and
nothing else), or `all`. What exactly counts as docs-only, and what happens to a
PR mixing docs and code, is #17's to pin down.

## The code cycle: this feature is the process, a tracker feature is its trace

**This feature owns the code cycle.** How a scoped ticket becomes a reviewable
change — isolation per ticket, when work is committed, what must be reviewed and
when, what may merge unattended — is specified here, and only here. Not all of it is
written down yet: worktree ownership lands in this file through #20. When work is
committed is written above, under § *Who decides, on each path* → **Execution**.
Ownership is settled; the wording of what remains follows.

**A tracker feature owns the tracing and relaying of that cycle.** It states which
concrete artefact each abstract step becomes on its tool: that the reviewable
proposal is a GitHub PR opened this way, that entering execution shows up as a
column move, that a sprint is a milestone. It adapts to this feature; it does not
define it.

**Precedence, where the two disagree: this feature governs.** A tracker feature
found stating a different process rule is the one that must change — not this one,
and not "whichever was written last". A tracker materialises a process it does not
define, so a divergence is a defect on the tracker's side by construction. This is
part of the ownership decision, not a tie-break added after the fact.

That precedence is worth stating rather than leaving to inference, because both
features read as authoritative in isolation: each is a spec, written in the same
voice, and an agent that opens only one has no way to tell it is reading the
subordinate half.

### The replacement test — which feature does a rule belong to?

Apply it before filing any rule about how code ships, at refinement time and when
reviewing a spec change. Replace the tracker with a hypothetical
`scrumia-tracker-local` — a file-based tracker, no PR, no board:

- **The rule stays true, word for word → it belongs here.** One worktree per ticket,
  one branch per ticket, commit before the run yields control, review before merge,
  the three gates, `auto_merge`. None of them mentions a tracker to be stated.
- **The rule becomes meaningless → it belongs to the tracker feature.** Opening a PR
  and linking it to its issue, column transitions, milestone-as-sprint,
  epic-as-native-sub-issues, board reading discipline. Each names an artefact that
  ceases to exist.

Apply it to one atomic statement at a time. A rule that returns both answers is two
rules — splitting it is the first step, not a sign the test failed.

Every rule has exactly one answer, and a rule is written on one side only: this
feature states the abstract ("an execution ends in a reviewable proposal; gate 3
governs its merge"), the tracker feature binds it to the concrete ("that proposal is
a GitHub PR, opened this way"). Restating the abstract rule alongside its binding
creates a second copy that drifts — the same trap `scope/*` avoids by being
specified once in `features/business/execution-policy/` and restated by neither
consumer.

This is a question about **spec files**, not about modules.
`docs/adr/0013-tracker-stays-one-slot.md` decides something else — that the `tracker`
slot is not split into a `forge` slot — and assigns no ownership of specs. The
tracker module implementing the code cycle and this feature specifying it are both
true at once; they are different planes, and neither overrides the other.
