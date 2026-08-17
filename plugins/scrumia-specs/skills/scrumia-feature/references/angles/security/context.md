# Angle: security

**Content-tested, both strata.** The file is `security.md`.

## What this angle answers

What can go wrong that nobody asked for, how bad it is on a comparable scale, and
whether the project mitigates it or knowingly accepts it.

Its output is a decision, not a survey. A threat listed without a rating decides
nothing, and a rating without a mitigation or a named acceptance decides nothing
either.

Read by: business (signs the acceptances), Technical Lead, devs.

## When it activates

The file exists when the feature has a meaningful risk surface on any of the four
axes below — which is a judgement, and the absence of the file asserts that the
judgement was made.

**By context.** Answer each, yes or no. One yes is enough to write the file.

| Question | Default when unsure |
|---|---|
| Does the feature read, write or move data that someone must not see? | yes → write it |
| Can it be silently wrong — produce a plausible result nobody detects? | yes → write it |
| Does a core flow depend on it being available? | no |
| Would a dispute about what happened need to be reconstructed afterwards? | no |
| Does it grant, check or bypass a permission? | yes → write it |
| Does it accept input from outside the project's own control? | yes → write it |

Defaulting to "yes → write it" on the first, second, fifth and sixth is
deliberate: those four are the ones a reader cannot verify was considered once the
file is absent.

**By configuration.** A project may take the judgement out of the writer's hands,
under this module's `params` in `.scrumia/config.yaml`:

```yaml
modules:
  "<source>:scrumia-specs":
    params:
      angles:
        security: always   # always | context | never
```

- `always` — every feature carries `security.md`, questions or not. For a project
  under an audit obligation, where an absent file is not an acceptable assertion.
- `context` — the default, and the behaviour when the key is absent: the questions
  above decide.
- `never` — the angle is off; the file is not written and its absence asserts
  nothing. For a project that handles this subject outside its specs.

Under `always`, a feature with no risk to state writes the file with an explicit
"no risk identified on any axis, considered on <date>" rather than an empty table.
That is the cost of the setting, and the reason `context` is the default.

## The questions to explore it

Per axis, and only for the axes the activation questions turned up:

**Availability** — If this fails, who is blocked, and for how long? Is there a
degraded mode, and does anyone notice it is degraded?

**Integrity** — If this is silently wrong, what breaks downstream? Is the error
detectable, by whom, and how long after the fact?

**Confidentiality (access)** — Who must not see this? What happens if they do —
and does the system record that they did?

**Traceability** — If this is disputed later, can the who, the when and the why be
reconstructed? From what, and for how long is it kept?

Then, for every risk found:

- What is its rating on the scale below, and what comparable risk in another
  feature did you check it against?
- Is it mitigated, or accepted? An unmitigated risk with no acceptance record is
  an unfinished sentence.
- If accepted: who accepts it, and what event or date invalidates the acceptance?

## The scale

One ordinal scale, so ratings compare across features:

- **low** — failure is cosmetic or self-healing; nobody is blocked
- **medium** — degraded for some, a workaround exists
- **high** — a core flow is blocked or silently wrong; recovery is manual
- **critical** — irreversible loss (data, money, trust) or no recovery path

## The acceptance record

For every risk assumed rather than mitigated — and reused by `legal.md` for
residual legal risks, stated once here and referenced from there so the two files
cannot drift:

the axis and rating · why it is accepted · who accepted it, named (a merge by the
project owner counts as the acceptance it records) · the revisit condition, the
event or date that invalidates the acceptance.

## Boundary

**Holds** — a risk table, one row per identified risk: the risk, its axis, its
rating, and its mitigation or its acceptance. The acceptance records.

**May hold** — a risk rated and explicitly accepted as out of this feature's
control, naming who owns it instead.

**Must not hold**
- an accessibility concern → `ux.md` and `qa.md`; it is not an "access" risk in
  this table's sense
- a legal obligation → `legal.md`
- a threat catalogue with no rated conclusion — a row that rates nothing decides
  nothing
- a mitigation's implementation detail → `tech.md`; here it is named, not designed

## Files

- Template: [`template.md`](template.md)
- Review guard-rails: [`checklist.md`](checklist.md)
