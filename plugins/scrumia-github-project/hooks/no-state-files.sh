#!/usr/bin/env bash
# ScrumIA — project state lives in the tracker, not in the repo.

set -uo pipefail

# Must never break a session, even silently: no jq, no check, but say so.
command -v jq >/dev/null || { echo "scrumia guard: jq not found, state-file check skipped" >&2; exit 0; }

file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
[ -n "$file_path" ] || exit 0

project_dir=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -f "$project_dir/.scrumia/config.yaml" ] || exit 0

# Match --show-toplevel's symlink resolution, or a symlinked cwd (e.g. macOS /tmp) breaks the prefix match below.
resolved_dir=$(cd "$(dirname "$file_path")" 2>/dev/null && pwd -P) || resolved_dir=""
if [ -n "$resolved_dir" ]; then
  file_path="$resolved_dir/$(basename "$file_path")"
fi

case "$file_path" in
  "$project_dir"/*) rel_path=${file_path#"$project_dir"/} ;;
  *) rel_path=$file_path ;;
esac

case "$rel_path" in
  docs/*|.scrumia/*) exit 0 ;;
esac

basename_lower=$(basename "$file_path" | tr '[:upper:]' '[:lower:]')

case "$basename_lower" in
  sprint-status.md|sprint_status.md|backlog.md|sprint.md|roadmap-status.md|todo.md|tasks.md|plan.md|progress.md|status.md|board.md)
    cat >&2 <<EOF
ScrumIA blocks "$basename_lower": state lives in the tracker, not in a versioned file.

  - work to do / progress -> open an issue: gh issue create
  - spec-related state    -> see the specs contract in CLAUDE.md

Not state? Rename it, or place it under docs/ or .scrumia/ (exempt).
EOF
    exit 2
    ;;
esac

exit 0
