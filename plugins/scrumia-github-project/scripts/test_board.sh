#!/usr/bin/env bash
# Tests scrumia-board's cmd_read and cmd_issues — the criteria are named per check. `gh`
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
modules:
  "acme/widgets:scrumia-github-project":
    params:
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

# --- AC-13: the `discussion` label is subtracted from the work, not dropped ---
WORKDIR3=$(mktemp -d)
trap 'rm -rf "$WORKDIR" "$WORKDIR2" "$WORKDIR3"' EXIT

cp "$WORKDIR/gh" "$WORKDIR3/gh"
mkdir -p "$WORKDIR3/.scrumia"
cp "$WORKDIR/.scrumia/config.yaml" "$WORKDIR3/.scrumia/config.yaml"

# 403 is closed: how a discussion normally ends, and it needs no PR to get there.
cat > "$WORKDIR3/item-list.json" <<'JSON'
{"totalCount": 3, "items": [
  {"content": {"number": 401, "type": "Issue"}, "title": "Real ticket", "status": "Backlog", "labels": ["scrumia"]},
  {"content": {"number": 402, "type": "Issue"}, "title": "A debate", "status": "Backlog", "labels": ["discussion"]},
  {"content": {"number": 403, "type": "Issue"}, "title": "A settled debate", "status": "Backlog", "labels": ["discussion"]}
]}
JSON
cat > "$WORKDIR3/states.json" <<'JSON'
{"data": {"repository": {
  "n401": {"number": 401, "state": "OPEN"},
  "n402": {"number": 402, "state": "OPEN"},
  "n403": {"number": 403, "state": "CLOSED"}
}}}
JSON

OUT3=$(PATH="$WORKDIR3:$PATH" FIXTURE_DIR="$WORKDIR3" \
       SCRUMIA_CONFIG="$WORKDIR3/.scrumia/config.yaml" "$BOARD_SH" read --all 2>/dev/null)

in_columns=$(jq '[.columns[].items[].number] | contains([402])' <<<"$OUT3")
check "AC-13: a discussion issue is not among what is waiting to be started" \
  "$([ "$in_columns" = "false" ] && echo true || echo false)"

work_kept=$(jq '[.columns[].items[].number] | contains([401])' <<<"$OUT3")
check "AC-13: the ticket beside it is untouched — the filter subtracts only its label" \
  "$([ "$work_kept" = "true" ] && echo true || echo false)"

disc_numbers=$(jq -r '[.discussions[].number] | sort | join(",")' <<<"$OUT3")
disc_count=$(jq -r '.discussion_count' <<<"$OUT3")
check "AC-13: both are returned in a group of their own, named and counted" \
  "$([ "$disc_numbers" = "402,403" ] && [ "$disc_count" = "2" ] && echo true || echo false)" \
  "got: numbers=$disc_numbers count=$disc_count"

stale_count=$(jq -r '.closed_without_pr_count' <<<"$OUT3")
check "AC-13: a settled discussion is not reported as a ticket abandoned without a PR" \
  "$([ "$stale_count" = "0" ] && echo true || echo false)" "got: $stale_count"

totals=$(jq -r '"\(.count)/\(.total_matching)"' <<<"$OUT3")
check "AC-13: the read's own totals still account for them — a subtraction is not a drop" \
  "$([ "$totals" = "3/3" ] && echo true || echo false)" "got: $totals"

# Numbers, not counts, so a substituted item cannot be absorbed by a balancing sum. Which
# group each lands in is `placement` below: this passes state-first too, by construction.
partition=$(jq -r '
  ([.columns[].items[].number] + [.closed_without_pr[].number] + [.discussions[].number]) as $all
  | if ($all | length) == ($all | unique | length) and ($all | sort) == [401,402,403]
    then "partitioned" else "not a partition: \($all|sort)" end' <<<"$OUT3")
check "AC-13: the three groups partition the read — every item in exactly one" \
  "$([ "$partition" = "partitioned" ] && echo true || echo false)" "got: $partition"

placement=$(jq -r '[.discussions[].number] as $d
  | if ($d | sort) == [402,403] then "right group" else "wrong group: \($d|sort)" end' <<<"$OUT3")
check "AC-13: and the labelled ones are the two in discussions, whatever their state" \
  "$([ "$placement" = "right group" ] && echo true || echo false)" "got: $placement"

# --- AC-10/AC-12 (knowledge-placement): the search is issues, in every state ---
WORKDIR4=$(mktemp -d)
trap 'rm -rf "$WORKDIR" "$WORKDIR2" "$WORKDIR3" "$WORKDIR4"' EXIT

cat > "$WORKDIR4/gh" <<'STUB'
#!/usr/bin/env bash
echo "$*" >> "$ARGS_LOG"
case "$1 $2" in
  "issue list") cat "$FIXTURE_DIR/issue-list.json" ;;
  *) echo "unstubbed gh call: $*" >&2; exit 1 ;;
esac
STUB
chmod +x "$WORKDIR4/gh"

mkdir -p "$WORKDIR4/.scrumia"
cp "$WORKDIR/.scrumia/config.yaml" "$WORKDIR4/.scrumia/config.yaml"

# 501 is closed — the case the board could never have answered, since a card leaves the
# board when its work does.
cat > "$WORKDIR4/issue-list.json" <<'JSON'
[
  {"number": 501, "title": "Settled long ago", "state": "CLOSED", "url": "u/501", "labels": [{"name": "discussion"}]},
  {"number": 502, "title": "Still open", "state": "OPEN", "url": "u/502", "labels": []}
]
JSON

ARGS_LOG="$WORKDIR4/gh-args"
OUT4=$(PATH="$WORKDIR4:$PATH" FIXTURE_DIR="$WORKDIR4" ARGS_LOG="$ARGS_LOG" \
       SCRUMIA_CONFIG="$WORKDIR4/.scrumia/config.yaml" \
       "$BOARD_SH" issues --search "settled" 2>/dev/null)

touched_board=$(grep -c "^project " "$ARGS_LOG" 2>/dev/null || true)
check "AC-12: the search never goes near the board" \
  "$([ "$touched_board" = "0" ] && echo true || echo false)" "got: $touched_board project calls"

state_flag=$(grep -c -- "--state all" "$ARGS_LOG" 2>/dev/null || true)
check "AC-12: it covers every state, and the flag is not the caller's to pass" \
  "$([ "$state_flag" = "1" ] && echo true || echo false)" "got: $state_flag"

closed_found=$(jq '[.issues[] | select(.state == "CLOSED") | .number] | contains([501])' <<<"$OUT4")
check "AC-10: a closed issue is reachable, so an existing one can be found before creating" \
  "$([ "$closed_found" = "true" ] && echo true || echo false)"

surface=$(jq -r '"\(.surface)/\(.states)"' <<<"$OUT4")
check "AC-12: the answer says which surface it read, so a board read cannot pass for this" \
  "$([ "$surface" = "issues/all" ] && echo true || echo false)" "got: $surface"

no_terms=$(PATH="$WORKDIR4:$PATH" FIXTURE_DIR="$WORKDIR4" ARGS_LOG="$ARGS_LOG" \
           SCRUMIA_CONFIG="$WORKDIR4/.scrumia/config.yaml" \
           "$BOARD_SH" issues 2>/dev/null | jq -r '.ok')
check "an unfiltered issue list is refused rather than answered as a search" \
  "$([ "$no_terms" = "false" ] && echo true || echo false)" "got: ok=$no_terms"

echo
if [ "$FAILURES" -eq 0 ]; then
  echo "All checks passed."
  exit 0
else
  echo "$FAILURES check(s) failed."
  exit 1
fi
