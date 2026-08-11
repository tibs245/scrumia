#!/usr/bin/env bash
# ScrumIA — prints the active composition, slot by slot then app by app.
# Reads .scrumia/config.yaml. Writes nothing, anywhere.

# -f because every unquoted split below is over config text, never a path: a `*`
# in the config would otherwise print a file listing instead of the value.
set -fuo pipefail

CONFIG="${SCRUMIA_CONFIG:-.scrumia/config.yaml}"


die() { echo "compose-status.sh: $1" >&2; exit 1; }

usage() {
  cat >&2 <<'EOF'
compose-status.sh

Prints this project's ScrumIA composition — the modules it runs, then app by app.
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

# The list is flat, so there is no per-slot key to leave empty. What replaces the
# old three states is `actions:` — this project's own arbitrations and exclusions.
LEGACY=false
jq -e 'has("extends")' >/dev/null <<<"$CFG" || LEGACY=true

MODULES=$(jq -r '
  (.extends // ((.composition // {}) | to_entries | map(select(.value != null) | .value)))[]' <<<"$CFG")

MOD_ROWS="" MOD_W=6
for m in $MODULES; do
  [ -n "$m" ] || continue
  [ ${#m} -gt "$MOD_W" ] && MOD_W=${#m}
  MOD_ROWS="$MOD_ROWS$m"$'\n'
done

ACT_ROWS="" ACT_W=6 STATE_W=5
while IFS=$'\t' read -r a state; do
  [ -n "$a" ] || continue
  [ ${#a} -gt "$ACT_W" ] && ACT_W=${#a}
  [ ${#state} -gt "$STATE_W" ] && STATE_W=${#state}
  ACT_ROWS="$ACT_ROWS$a"$'\t'"$state"$'\n'
done < <(jq -r '(.actions // {}) | to_entries | .[] | [.key, (.value|tostring)] | @tsv' <<<"$CFG")

APP_ROWS="" APP_W=3 PATH_W=4 EXT_W=7
while IFS=$'\t' read -r app apath ext; do
  [ -n "$app" ] || continue
  [ -n "$apath" ] || apath="(no path)"
  [ ${#app} -gt "$APP_W" ] && APP_W=${#app}
  [ ${#apath} -gt "$PATH_W" ] && PATH_W=${#apath}
  [ ${#ext} -gt "$EXT_W" ] && EXT_W=${#ext}
  APP_ROWS="$APP_ROWS$app"$'\t'"$apath"$'\t'"$ext"$'\n'
done < <(jq -r '.apps // [] | .[] | [
    .name // "?",
    .path // "",
    ((.extends // ([.implementation] + (.practices // []) | map(select(. != null))))
      | if length == 0 then "none" else join(", ") end)
  ] | @tsv' <<<"$CFG")

# 28 is the width of the "Modules this project extends" heading, and 21 that of the
# action table's second column: a heading that overflows is as unreadable as a row.
MOD_TABLE_W=28
APP_TABLE_W=$((APP_W + 2 + PATH_W + 2 + EXT_W))
ACT_TABLE_W=0
[ -n "$ACT_ROWS" ] && ACT_TABLE_W=$((ACT_W + 2 + 21))
NARROW=false
for w in "$MOD_TABLE_W" "$APP_TABLE_W" "$ACT_TABLE_W"; do
  [ $((w + 2)) -gt "$WIDTH" ] && NARROW=true
done

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
  while IFS= read -r m; do
    [ -n "$m" ] || continue
    printf '  %s%s%s\n' "$BOLD" "$m" "$RESET"
  done <<<"$MOD_ROWS"
else
  printf '  %s%s%s\n' "$DIM" "Modules this project extends" "$RESET"
  printf '  %s%s%s\n' "$DIM" "$(rule 28 $((WIDTH - 2)))" "$RESET"
  while IFS= read -r m; do
    [ -n "$m" ] || continue
    printf '  %s\n' "$m"
  done <<<"$MOD_ROWS"
fi
[ -n "$MODULES" ] || wrap '  ' "$WARN" "Nothing is plugged in: extends is empty."

if [ -n "$APP_ROWS" ]; then
  echo
  if [ "$NARROW" = true ]; then
    while IFS=$'\t' read -r app apath ext; do
      [ -n "$app" ] || continue
      printf '  %s%s%s (%s)\n' "$BOLD" "$app" "$RESET" "$apath"
      wrap '    ' "" "extends: $ext"
    done <<<"$APP_ROWS"
  else
    printf '  %s%s  %s  %s%s\n' "$DIM" "$(pad App "$APP_W")" "$(pad Path "$PATH_W")" \
      "Extends" "$RESET"
    printf '  %s%s%s\n' "$DIM" "$(rule "$APP_TABLE_W" $((WIDTH - 2)))" "$RESET"
    while IFS=$'\t' read -r app apath ext; do
      [ -n "$app" ] || continue
      printf '  %s  %s  %s\n' "$(pad "$app" "$APP_W")" "$(pad "$apath" "$PATH_W")" "$ext"
    done <<<"$APP_ROWS"
  fi
fi

# Only what the config itself declares. Which action each module provides, and which
# are covered, is derived by scrumia-assemble — this script resolves nothing.
if [ -n "$ACT_ROWS" ]; then
  echo
  if [ "$NARROW" = true ]; then
    while IFS=$'\t' read -r a state; do
      [ -n "$a" ] || continue
      printf '  %s%s%s\n    %s\n' "$BOLD" "$a" "$RESET" "$state"
    done <<<"$ACT_ROWS"
  else
    printf '  %s%s  %s%s\n' "$DIM" "$(pad Action "$ACT_W")" "This project's answer" "$RESET"
    printf '  %s%s%s\n' "$DIM" "$(rule $((ACT_W + 2 + 21)) $((WIDTH - 2)))" "$RESET"
    while IFS=$'\t' read -r a state; do
      [ -n "$a" ] || continue
      printf '  %s  %s\n' "$(pad "$a" "$ACT_W")" "$state"
    done <<<"$ACT_ROWS"
  fi
fi

echo
if [ "$LEGACY" = true ]; then
  wrap '  ' "$WARN" "This config still uses the retired composition:/practices: keys."
  wrap '    ' "" "They are read for one more minor. Migrate to extends: with /scrumia-core:scrumia-compose."
  echo
fi
wrap '  ' "$DIM" "What each module provides, and what nothing covers: scrumia-assemble build."
wrap '  ' "$DIM" "Change any of this with /scrumia-core:scrumia-compose."
echo
