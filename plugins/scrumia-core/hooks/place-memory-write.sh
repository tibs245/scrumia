#!/usr/bin/env bash
# PostToolUse, never Pre: the write completes and the run continues — knowledge-placement's BR-8.

set -uo pipefail

payload=$(cat)

# No jq, no reminder: a session must not break over one.
command -v jq >/dev/null || exit 0

file_path=$(printf '%s' "$payload" | jq -r '.tool_response.filePath // .tool_input.file_path // empty' 2>/dev/null) || exit 0
[ -n "$file_path" ] || exit 0

cwd=$(printf '%s' "$payload" | jq -r '.cwd // empty' 2>/dev/null)
if [ "${file_path#/}" = "$file_path" ]; then
  file_path="${cwd:-$PWD}/$file_path"
fi

# The path decides only whether to ask — what the entry is worth is the tree's answer, on
# its content (BR-4). Committed role memory and the harness's own both carry entries.
case "$file_path" in
  */.claude/agent-memory/*) ;;
  */.claude/projects/*/memory/*) ;;
  *) exit 0 ;;
esac

# The destinations are a composition's, so a session outside one has nothing to be told.
project_dir=${CLAUDE_PROJECT_DIR:-}
[ -n "$project_dir" ] || project_dir=$(git -C "${cwd:-$PWD}" rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -f "$project_dir/.scrumia/config.yaml" ] || exit 0

reminder=$(cat <<EOF
Agent memory was just written: $file_path

The write stands — this is a reminder, not a gate. Run \`scrumia-place\` on that path
before relying on the entry: it reads the entry itself and returns one destination, and
one of its answers is that memory was the right one.
EOF
)

# hookSpecificOutput is what reaches the model; a bare string reaches the transcript alone.
jq -n --arg context "$reminder" \
  '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $context}}'

exit 0
