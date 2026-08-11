#!/usr/bin/env bash
# ScrumIA — prints the active composition, slot by slot then app by app.
# Reads .scrumia/config.yaml. Writes nothing, anywhere.

# -f because every unquoted split below is over config text, never a path: a `*`
# in the config would otherwise print a file listing instead of the value.
set -fuo pipefail

CONFIG="${SCRUMIA_CONFIG:-.scrumia/config.yaml}"

# `implementation` and `practices` are the two slots that repeat per app, so
# they belong to the apps table rather than to this list.
SLOTS="specs tracker team discovery design"

die() { echo "compose-status.sh: $1" >&2; exit 1; }

usage() {
  cat >&2 <<'EOF'
compose-status.sh

Prints this project's ScrumIA composition — slot by slot, then app by app.
Takes no argument. Reads $SCRUMIA_CONFIG (default .scrumia/config.yaml) and
writes nothing. Colour is dropped when stdout is not a terminal, and when
NO_COLOR is set to a non-empty value.
EOF
  exit 2
}

[ $# -eq 0 ] || usage

command -v jq >/dev/null 2>&1 || die "jq not found"

# Same loader as scrumia-board and scrumia-pick-model: one of the two YAML readers the
# machine already has, never a third dependency.
load_config() {
  [ -f "$CONFIG" ] || die "no $CONFIG — run /scrumia-core:scrumia-init first"
  if command -v yq >/dev/null 2>&1; then
    CFG=$(yq -o=json '.' "$CONFIG" 2>/dev/null)
  elif python3 -c 'import yaml' >/dev/null 2>&1; then
    CFG=$(python3 -c 'import sys,yaml,json; json.dump(yaml.safe_load(open(sys.argv[1])) or {}, sys.stdout)' "$CONFIG" 2>/dev/null)
  else
    die "need yq or python3+PyYAML to read $CONFIG"
  fi
  [ -n "${CFG:-}" ] || die "$CONFIG is empty or not valid YAML"
}

# A hint for an empty slot, not a claim that only this module could fill it.
reference_module() {
  case "$1" in
    specs)     echo "scrumia-specs" ;;
    tracker)   echo "scrumia-github-project" ;;
    team)      echo "scrumia-teams" ;;
    discovery) echo "scrumia-discovery" ;;
    design)    echo "scrumia-design" ;;
    *)         echo "" ;;
  esac
}

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  BOLD=$'\033[1m'; DIM=$'\033[2m'; WARN=$'\033[33m'; RESET=$'\033[0m'
else
  BOLD=""; DIM=""; WARN=""; RESET=""
fi

term_width() {
  local w="${COLUMNS:-}"
  if [ -z "$w" ] && command -v tput >/dev/null 2>&1; then
    w=$(tput cols 2>/dev/null) || w=""
  fi
  case "$w" in ''|*[!0-9]*) w=80 ;; esac
  [ "$w" -ge 20 ] || w=80
  echo "$w"
}

pad() { printf '%-*s' "$2" "$1"; }

# wrap <indent> <colour> <text> — prose folds to the terminal; a command never
# does, since a wrapped command no longer survives a copy-paste.
wrap() {
  local indent="$1" colour="$2" text="$3" limit line='' word
  limit=$((WIDTH - ${#indent}))
  [ "$limit" -lt 20 ] && limit=20
  for word in $text; do
    if [ -z "$line" ]; then
      line="$word"
    elif [ $((${#line} + 1 + ${#word})) -le "$limit" ]; then
      line="$line $word"
    else
      printf '%s%s%s%s\n' "$indent" "$colour" "$line" "${colour:+$RESET}"
      line="$word"
    fi
  done
  [ -n "$line" ] && printf '%s%s%s%s\n' "$indent" "$colour" "$line" "${colour:+$RESET}"
}

rule() {
  local n=$1 max=$2 out=''
  [ "$n" -gt "$max" ] && n=$max
  while [ "$n" -gt 0 ]; do out="${out}─"; n=$((n - 1)); done
  printf '%s' "$out"
}

load_config
WIDTH=$(term_width)

NAME=$(jq -r '.project.name // "this project"' <<<"$CFG")
REPO=$(jq -r '.project.repo // empty' <<<"$CFG")

# Three states, not two: BR-2 makes an omitted key a configuration defect,
# which reads differently from a slot declared empty on purpose.
EMPTY="" UNDECLARED=""
SLOT_ROWS="" SLOT_W=4 MOD_W=6
declared=$(jq -r '.composition // {} | keys_unsorted[]' <<<"$CFG")
extra=$(comm -13 <(tr ' ' '\n' <<<"$SLOTS" | sort) <(sort <<<"$declared"))

for slot in $SLOTS $extra; do
  [ -n "$slot" ] || continue
  state=$(jq -r --arg s "$slot" '
    if (.composition // {} | has($s) | not) then "undeclared"
    elif (.composition[$s] == null) then "empty"
    else .composition[$s] end' <<<"$CFG")
  case "$state" in
    undeclared) UNDECLARED="$UNDECLARED $slot"; label="not declared" ;;
    empty)      EMPTY="$EMPTY $slot";           label="empty on purpose" ;;
    *)          label="$state" ;;
  esac
  [ ${#slot} -gt "$SLOT_W" ] && SLOT_W=${#slot}
  [ ${#label} -gt "$MOD_W" ] && MOD_W=${#label}
  SLOT_ROWS="$SLOT_ROWS$slot	$label	$state"$'\n'
done

APP_ROWS="" APP_W=3 PATH_W=4 IMPL_W=14 PRAC_W=9
while IFS=$'\t' read -r app apath impl practices; do
  [ -n "$app" ] || continue
  [ -n "$apath" ] || apath="(no path)"
  [ ${#app} -gt "$APP_W" ] && APP_W=${#app}
  [ ${#apath} -gt "$PATH_W" ] && PATH_W=${#apath}
  [ ${#impl} -gt "$IMPL_W" ] && IMPL_W=${#impl}
  [ ${#practices} -gt "$PRAC_W" ] && PRAC_W=${#practices}
  APP_ROWS="$APP_ROWS$app	$apath	$impl	$practices"$'\n'
done < <(jq -r '.apps // [] | .[] | [
    .name // "?",
    .path // "",
    (.implementation // "none"),
    ((.practices // []) | if length == 0 then "none" else join(", ") end)
  ] | @tsv' <<<"$CFG")

SLOT_TABLE_W=$((SLOT_W + 2 + MOD_W))
APP_TABLE_W=$((APP_W + 2 + PATH_W + 2 + IMPL_W + 2 + PRAC_W))
NARROW=false
{ [ $((SLOT_TABLE_W + 2)) -gt "$WIDTH" ] || [ $((APP_TABLE_W + 2)) -gt "$WIDTH" ]; } && NARROW=true

echo
if [ "$NARROW" = true ]; then
  wrap '' "$BOLD" "ScrumIA composition — $NAME"
  [ -n "$REPO" ] && wrap '' "$DIM" "$REPO"
elif [ -n "$REPO" ]; then
  printf '%sScrumIA composition — %s%s %s(%s)%s\n' "$BOLD" "$NAME" "$RESET" "$DIM" "$REPO" "$RESET"
else
  printf '%sScrumIA composition — %s%s\n' "$BOLD" "$NAME" "$RESET"
fi
echo

if [ "$NARROW" = true ]; then
  while IFS=$'\t' read -r slot label state; do
    [ -n "$slot" ] || continue
    case "$state" in
      undeclared|empty) printf '  %s%s%s\n    %s%s%s\n' "$BOLD" "$slot" "$RESET" "$WARN" "$label" "$RESET" ;;
      *)                printf '  %s%s%s\n    %s\n' "$BOLD" "$slot" "$RESET" "$label" ;;
    esac
  done <<<"$SLOT_ROWS"
else
  printf '  %s%s  %s%s\n' "$DIM" "$(pad Slot "$SLOT_W")" "Module" "$RESET"
  printf '  %s%s%s\n' "$DIM" "$(rule "$SLOT_TABLE_W" $((WIDTH - 2)))" "$RESET"
  while IFS=$'\t' read -r slot label state; do
    [ -n "$slot" ] || continue
    case "$state" in
      undeclared|empty) printf '  %s  %s%s%s\n' "$(pad "$slot" "$SLOT_W")" "$WARN" "$label" "$RESET" ;;
      *)                printf '  %s  %s\n' "$(pad "$slot" "$SLOT_W")" "$label" ;;
    esac
  done <<<"$SLOT_ROWS"
fi

if [ -n "$APP_ROWS" ]; then
  echo
  if [ "$NARROW" = true ]; then
    while IFS=$'\t' read -r app apath impl practices; do
      [ -n "$app" ] || continue
      printf '  %s%s%s (%s)\n' "$BOLD" "$app" "$RESET" "$apath"
      wrap '    ' "" "implementation: $impl"
      wrap '    ' "" "practices: $practices"
    done <<<"$APP_ROWS"
  else
    printf '  %s%s  %s  %s  %s%s\n' "$DIM" "$(pad App "$APP_W")" "$(pad Path "$PATH_W")" \
      "$(pad Implementation "$IMPL_W")" "Practices" "$RESET"
    printf '  %s%s%s\n' "$DIM" "$(rule "$APP_TABLE_W" $((WIDTH - 2)))" "$RESET"
    while IFS=$'\t' read -r app apath impl practices; do
      [ -n "$app" ] || continue
      printf '  %s  %s  %s  %s\n' "$(pad "$app" "$APP_W")" "$(pad "$apath" "$PATH_W")" \
        "$(pad "$impl" "$IMPL_W")" "$practices"
    done <<<"$APP_ROWS"
  fi
fi

echo
for slot in $EMPTY; do
  ref=$(reference_module "$slot")
  wrap '  ' "$WARN" "The $slot slot is empty on purpose."
  [ -n "$ref" ] && printf '    claude plugin install %s@scrumia --scope project\n' "$ref"
done
if [ -n "$UNDECLARED" ]; then
  list=""
  for slot in $UNDECLARED; do list="${list:+$list, }$slot"; done
  wrap '  ' "$WARN" "No key in $CONFIG for: $list."
  wrap '    ' "" "Add each one with an explicit null: a missing key reads as an oversight, not as a declared absence."
fi
[ -n "$EMPTY$UNDECLARED" ] && echo
wrap '  ' "$DIM" "Change any of this with /scrumia-core:scrumia-compose."
echo
