---
name: review-head-vs-origin-vs-brief
description: On a gate 2 re-review, the brief's named commit, the worktree HEAD and origin/<branch> can all differ — check all three before judging
metadata:
  type: feedback
---

Before reviewing a branch, run `git log --oneline origin/<branch>..HEAD` and
`git status --short` in the worktree. Never trust the commit SHA the brief names as
the tip.

**Why:** on the #31 gate 2 re-review the brief named `dc725a5` as the amendment;
HEAD was actually `aec3665`, one commit further, and `aec3665` had already fixed a
factual error `dc725a5` carried. Meanwhile `origin/fix/31-spec-only-deliverable` was
still at `46b1858` — both amendment commits were unpushed, so the PR on GitHub showed
the version the human had already rejected. Reviewing the brief's SHA would have
produced findings the author had already fixed; reviewing without checking origin
would have let a re-review verdict land on a PR that did not contain the reviewed text.

**How to apply:** three reads at the start of every branch review — the diff at HEAD
(not at the named SHA), `git status --short` for uncommitted work, and
`origin/<branch>..HEAD` for unpushed work. Report an unpushed tip as a precondition
in the verdict: the verdict is meaningless until the human can read the same bytes.
