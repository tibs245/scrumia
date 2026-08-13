#!/usr/bin/env bash
# Tests place-memory-write.sh against AC-14 of features/business/knowledge-placement/ —
# the write completes, the run is not interrupted, and the question arrives afterwards.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$HERE/../hooks/place-memory-write.sh"
HOOKS_JSON="$HERE/../hooks/hooks.json"
FAILURES=0
BASH=$(command -v bash)

check() {
  local name="$1" ok="$2" detail="${3:-}"
  if [ "$ok" = "true" ]; then
    echo "  ok   $name"
  else
    echo "  FAIL $name${detail:+: $detail}"
    FAILURES=$((FAILURES + 1))
  fi
}

command -v jq >/dev/null || { echo "jq is required to run these tests" >&2; exit 1; }

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

PROJECT="$WORKDIR/project"
mkdir -p "$PROJECT/.scrumia"
printf 'project:\n  name: "widgets"\n' > "$PROJECT/.scrumia/config.yaml"

write_payload() {
  jq -n --arg p "$1" --arg cwd "$PROJECT" \
    '{hook_event_name: "PostToolUse", tool_name: "Write", cwd: $cwd,
      tool_input: {file_path: $p, content: "x"}, tool_response: {filePath: $p}}'
}

edit_payload() {
  jq -n --arg p "$1" --arg cwd "$PROJECT" \
    '{hook_event_name: "PostToolUse", tool_name: "Edit", cwd: $cwd,
      tool_input: {file_path: $p, old_string: "a", new_string: "b"}, tool_response: {}}'
}

run_hook() {
  CLAUDE_PROJECT_DIR="$PROJECT" bash "$HOOK"
}

echo "== the reminder arrives, on both memory surfaces =="

ROLE_ENTRY="$PROJECT/.claude/agent-memory/scrumia-teams-scrumia-tech/a-lesson.md"
out=$(write_payload "$ROLE_ENTRY" | run_hook); status=$?
check "AC-14 a write to committed role memory exits 0" "$([ $status -eq 0 ] && echo true || echo false)" "exit $status"
check "AC-14 it answers on the event the write already happened on" \
  "$(echo "$out" | jq -r '.hookSpecificOutput.hookEventName == "PostToolUse"' 2>/dev/null || echo false)" "$out"
context=$(echo "$out" | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null)
check "AC-14 the reminder names the entry just written" \
  "$([[ $context == *"$ROLE_ENTRY"* ]] && echo true || echo false)" "$context"
check "AC-14 the reminder names the tree it sends to" \
  "$([[ $context == *scrumia-place* ]] && echo true || echo false)" "$context"

HARNESS_ENTRY="$HOME/.claude/projects/-Users-someone-widgets/memory/how-this-machine-is-set-up.md"
out=$(write_payload "$HARNESS_ENTRY" | run_hook)
check "AC-14 the harness's own memory surface is covered too" \
  "$(echo "$out" | jq -r --arg p "$HARNESS_ENTRY" '(.hookSpecificOutput.additionalContext // "") | contains($p)' 2>/dev/null || echo false)" "$out"

out=$(edit_payload "$ROLE_ENTRY" | run_hook)
check "AC-14 an Edit of an entry is a write to memory too" \
  "$(echo "$out" | jq -r '(.hookSpecificOutput.additionalContext // "") | length > 0' 2>/dev/null || echo false)" "$out"

REL_ENTRY=".claude/agent-memory/scrumia-teams-scrumia-tech/relative.md"
out=$(write_payload "$REL_ENTRY" | run_hook)
check "a relative path is read against the run's own directory" \
  "$(echo "$out" | jq -r --arg p "$PROJECT/$REL_ENTRY" '(.hookSpecificOutput.additionalContext // "") | contains($p)' 2>/dev/null || echo false)" "$out"

mkdir -p "$PROJECT/deep/dir"
out=$(jq -n --arg p "$ROLE_ENTRY" --arg cwd "$PROJECT/deep/dir" \
  '{tool_name: "Write", cwd: $cwd, tool_input: {file_path: $p}}' \
  | env -u CLAUDE_PROJECT_DIR bash "$HOOK")
check "with no project directory given, the composition is found by walking up" \
  "$(echo "$out" | jq -r '(.hookSpecificOutput.additionalContext // "") | length > 0' 2>/dev/null || echo false)" "$out"

echo "== it interrupts nothing =="

out=$(write_payload "$ROLE_ENTRY" | run_hook)
check "AC-14 the answer carries nothing that stops the run" \
  "$(echo "$out" | jq -r 'has("continue") or has("decision") or has("stopReason") | not' 2>/dev/null || echo false)" "$out"

err=$(write_payload "$ROLE_ENTRY" | run_hook 2>&1 >/dev/null)
check "AC-14 it reports no failure the session did not have" \
  "$([ -z "$err" ] && echo true || echo false)" "$err"

event_keys=$(jq -r '.hooks | keys | join(",")' "$HOOKS_JSON")
check "AC-14 the hook is registered after the write and on nothing before it" \
  "$([ "$event_keys" = "PostToolUse" ] && echo true || echo false)" "$event_keys"
check "AC-14 it is registered on the tools that write an entry" \
  "$(jq -r '[.hooks.PostToolUse[].matcher] == ["Write|Edit"]' "$HOOKS_JSON" 2>/dev/null || echo false)" \
  "$(jq -r '[.hooks.PostToolUse[].matcher] | join(",")' "$HOOKS_JSON")"
check "the registered command is this script" \
  "$(jq -r '[.hooks.PostToolUse[].hooks[].command] | join(",") | test("hooks/place-memory-write.sh")' "$HOOKS_JSON" 2>/dev/null || echo false)" \
  "$(jq -r '[.hooks.PostToolUse[].hooks[].command] | join(",")' "$HOOKS_JSON")"

echo "== it stays silent everywhere else =="

out=$(write_payload "$PROJECT/src/widget.py" | run_hook); status=$?
check "an ordinary write draws no reminder" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

out=$(write_payload "$PROJECT/docs/memory-of-a-meeting.md" | run_hook)
check "a file merely named after memory draws none either" \
  "$([ -z "$out" ] && echo true || echo false)" "$out"

out=$(write_payload "$PROJECT/.claude/agent-memory/scrumia-teams-scrumia-tech/MEMORY.md" | run_hook)
check "the index is navigation, so it draws none" \
  "$([ -z "$out" ] && echo true || echo false)" "$out"

BARE="$WORKDIR/elsewhere"
mkdir -p "$BARE/.claude/agent-memory/some-agent"
out=$(jq -n --arg p "$BARE/.claude/agent-memory/some-agent/x.md" --arg cwd "$BARE" \
  '{tool_name: "Write", cwd: $cwd, tool_input: {file_path: $p}}' \
  | CLAUDE_PROJECT_DIR="$BARE" bash "$HOOK"); status=$?
check "outside a ScrumIA composition it says nothing" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

out=$(jq -n --arg p "$BARE/.claude/agent-memory/some-agent/x.md" --arg cwd "$BARE" \
  '{tool_name: "Write", cwd: $cwd, tool_input: {file_path: $p}}' \
  | env -u CLAUDE_PROJECT_DIR bash "$HOOK"); status=$?
check "with no project directory given and no composition above, it says nothing" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

NO_JQ="$WORKDIR/no-jq"
mkdir -p "$NO_JQ"
for tool in cat git; do ln -s "$(command -v "$tool")" "$NO_JQ/$tool"; done
out=$(write_payload "$ROLE_ENTRY" | PATH="$NO_JQ" "$BASH" "$HOOK"); status=$?
check "without jq it disables itself rather than the session" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

( cd "$WORKDIR" && jq -n '{tool_name: "Write", cwd: "a/relative/dir",
    tool_input: {file_path: ".claude/agent-memory/x/y.md"}}' \
  | env -u CLAUDE_PROJECT_DIR bash "$HOOK" > "$WORKDIR/walk.out" 2>&1 ) &
walk=$!
( sleep 5; kill -9 "$walk" 2>/dev/null ) >/dev/null 2>&1 &
watchdog=$!
wait "$walk"; status=$?
kill "$watchdog" 2>/dev/null
out=$(cat "$WORKDIR/walk.out")
check "a relative directory ends the walk instead of running forever" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

out=$(printf 'not json at all' | run_hook); status=$?
check "a payload it cannot read leaves the run alone" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

out=$(printf '' | run_hook); status=$?
check "an empty payload leaves the run alone" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

out=$(jq -n --arg cwd "$PROJECT" '{tool_name: "Write", cwd: $cwd, tool_input: {}}' | run_hook); status=$?
check "a payload with no path leaves the run alone" \
  "$([ -z "$out" ] && [ $status -eq 0 ] && echo true || echo false)" "exit $status, out: $out"

echo
if [ $FAILURES -eq 0 ]; then
  echo "all checks passed"
else
  echo "$FAILURES check(s) failed"
fi
exit $((FAILURES > 0))
