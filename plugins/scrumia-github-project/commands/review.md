---
description: Review an open PR by routing to the reviewers its diff actually calls for, and report each verdict with its source.
argument-hint: <PR number>
---

Load the `scrumia-review` skill and follow it.

$ARGUMENTS

The argument is the PR to review. Ask which one if none was given.

Route on what the diff touches, not on what the label claims — a label describes the intent, the diff describes the change.

If a role cannot be reached, say so where the verdict is reported. Handing a general agent the role's own definition is not that role, and a fallback that reads as the real thing is worse than one that names itself.

Approve nothing on the human's behalf.
