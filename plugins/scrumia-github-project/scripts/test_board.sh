#!/usr/bin/env bash
# Tests scrumia-board's cmd_read state handling — AC-1/AC-2/AC-4/AC-8, qa.md. `gh`
# is stubbed with a fixture: no network call, no dependency on the live board.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOARD_SH="$HERE/../bin/scrumia-board"
FAILURES=0

check() {
  local name="$1" ok="$2" detail="${3:-}"
  if [ "$ok" = "true" ]; then
    echo "  ok   $name"
  else
    echo "  FAIL $name${detail:+: $detail}"
    FAILURES=$((FAILURES + 1))
  fi
}

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

cat > "$WORKDIR/gh" <<'STUB'
#!/usr/bin/env bash
case "$1 $2" in
  "project item-list") cat "$FIXTURE_DIR/item-list.json" ;;
  "api graphql")       cat "$FIXTURE_DIR/states.json" ;;
  *) echo "unstubbed gh call: $*" >&2; exit 1 ;;
esac
STUB
chmod +x "$WORKDIR/gh"

mkdir -p "$WORKDIR/.scrumia"
cat > "$WORKDIR/.scrumia/config.yaml" <<'YAML'
project:
  repo: "acme/widgets"
settings:
  tracker:
    project_number: 1
    board:
      field_id: "FIELD"
YAML

# 201: closed, stuck in "Ready for dev" (the AC-8 gap). 202: open, same
# column. 203: closed, in "Done" — a normal merge, not the AC-8 gap.
cat > "$WORKDIR/item-list.json" <<'JSON'
{"totalCount": 3, "items": [
  {"content": {"number": 201, "type": "Issue"}, "title": "Stale ticket", "status": "Ready for dev", "labels": []},
  {"content": {"number": 202, "type": "Issue"}, "title": "Live ticket", "status": "Ready for dev", "labels": []},
  {"content": {"number": 203, "type": "Issue"}, "title": "Merged ticket", "status": "Done", "labels": []}
]}
JSON

cat > "$WORKDIR/states.json" <<'JSON'
{"data": {"repository": {
  "n201": {"number": 201, "state": "CLOSED"},
  "n202": {"number": 202, "state": "OPEN"},
  "n203": {"number": 203, "state": "CLOSED"}
}}}
JSON

FIXTURE_DIR="$WORKDIR"
export FIXTURE_DIR

OUT=$(PATH="$WORKDIR:$PATH" SCRUMIA_CONFIG="$WORKDIR/.scrumia/config.yaml" "$BOARD_SH" read --all 2>/dev/null)

live_states=$(jq -r '[.columns[].items[].state] | join(",")' <<<"$OUT")
check "AC-1: every live item carries the issue's own state" \
  "$([ "$live_states" = "CLOSED,OPEN" ] && echo true || echo false)" "got: $live_states"

in_live=$(jq '[.columns[].items[].number] | contains([201])' <<<"$OUT")
check "AC-2: closed-without-PR ticket is pulled out of the live columns" \
  "$([ "$in_live" = "false" ] && echo true || echo false)"

closed_count=$(jq -r '.closed_without_pr_count' <<<"$OUT")
check "AC-8: closed-without-PR is reported, not silently dropped" \
  "$([ "$closed_count" = "1" ] && echo true || echo false)" "got: $closed_count"

closed_number=$(jq -r '.closed_without_pr[0].number' <<<"$OUT")
check "AC-8: the flagged ticket is the right one" \
  "$([ "$closed_number" = "201" ] && echo true || echo false)" "got: $closed_number"

done_state=$(jq -r '.columns[] | select(.status=="Done") | .items[0].state' <<<"$OUT")
check "a closed ticket sitting in Done is a normal merge, kept and stated" \
  "$([ "$done_state" = "CLOSED" ] && echo true || echo false)" "got: $done_state"

# --- AC-4: a filtered, non-empty read confirms before it's trusted ---
WORKDIR2=$(mktemp -d)
trap 'rm -rf "$WORKDIR" "$WORKDIR2"' EXIT

# Calls 1/2/3 simulate the index catching up: 4 items, then 5, then 5 again
# — two consecutive equal counts is what cmd_read treats as "at rest".
cat > "$WORKDIR2/gh" <<'STUB'
#!/usr/bin/env bash
case "$1 $2" in
  "project item-list")
    n=$(( $(cat "$CALL_COUNTER" 2>/dev/null || echo 0) + 1 ))
    echo "$n" > "$CALL_COUNTER"
    [ "$n" -gt 3 ] && n=3
    cat "$FIXTURE_DIR/item-list-$n.json"
    ;;
  "api graphql") cat "$FIXTURE_DIR/states.json" ;;
  *) echo "unstubbed gh call: $*" >&2; exit 1 ;;
esac
STUB
chmod +x "$WORKDIR2/gh"

mkdir -p "$WORKDIR2/.scrumia"
cp "$WORKDIR/.scrumia/config.yaml" "$WORKDIR2/.scrumia/config.yaml"

cat > "$WORKDIR2/item-list-1.json" <<'JSON'
{"totalCount": 4, "items": [
  {"content": {"number": 301, "type": "Issue"}, "title": "A", "status": "Ready for dev", "labels": []},
  {"content": {"number": 302, "type": "Issue"}, "title": "B", "status": "Ready for dev", "labels": []},
  {"content": {"number": 303, "type": "Issue"}, "title": "C", "status": "Ready for dev", "labels": []},
  {"content": {"number": 304, "type": "Issue"}, "title": "D", "status": "Ready for dev", "labels": []}
]}
JSON
cat > "$WORKDIR2/item-list-2.json" <<'JSON'
{"totalCount": 5, "items": [
  {"content": {"number": 301, "type": "Issue"}, "title": "A", "status": "Ready for dev", "labels": []},
  {"content": {"number": 302, "type": "Issue"}, "title": "B", "status": "Ready for dev", "labels": []},
  {"content": {"number": 303, "type": "Issue"}, "title": "C", "status": "Ready for dev", "labels": []},
  {"content": {"number": 304, "type": "Issue"}, "title": "D", "status": "Ready for dev", "labels": []},
  {"content": {"number": 305, "type": "Issue"}, "title": "E", "status": "Ready for dev", "labels": []}
]}
JSON
cp "$WORKDIR2/item-list-2.json" "$WORKDIR2/item-list-3.json"

cat > "$WORKDIR2/states.json" <<'JSON'
{"data": {"repository": {
  "n301": {"number": 301, "state": "OPEN"}, "n302": {"number": 302, "state": "OPEN"},
  "n303": {"number": 303, "state": "OPEN"}, "n304": {"number": 304, "state": "OPEN"},
  "n305": {"number": 305, "state": "OPEN"}
}}}
JSON

CALL_COUNTER="$WORKDIR2/calls"
export FIXTURE_DIR="$WORKDIR2" CALL_COUNTER

OUT2=$(PATH="$WORKDIR2:$PATH" SCRUMIA_CONFIG="$WORKDIR2/.scrumia/config.yaml" \
       SCRUMIA_BOARD_RETRY_MAX=2 SCRUMIA_BOARD_RETRY_DELAY=0 \
       "$BOARD_SH" read --query "status:\"Ready for dev\"" 2>/dev/null)

ac4_count=$(jq -r '.total_matching' <<<"$OUT2")
check "AC-4: a filtered read confirms the count that GitHub's index was still catching up on" \
  "$([ "$ac4_count" = "5" ] && echo true || echo false)" "got: $ac4_count"

ac4_calls=$(cat "$CALL_COUNTER")
check "AC-4: the confirmation actually re-read the board rather than trusting the first pass" \
  "$([ "$ac4_calls" -ge 2 ] && echo true || echo false)" "got: $ac4_calls calls"

ac4_has_last=$(jq '[.columns[].items[].number] | contains([305])' <<<"$OUT2")
check "AC-4: the item missing from the first read is present in the final one" \
  "$([ "$ac4_has_last" = "true" ] && echo true || echo false)"

echo
if [ "$FAILURES" -eq 0 ]; then
  echo "All checks passed."
  exit 0
else
  echo "$FAILURES check(s) failed."
  exit 1
fi
