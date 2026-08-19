#!/usr/bin/env bash
# ScrumIA — prints the active composition: the modules the project runs, then app by app.
# Reads .scrumia/config.yaml. Writes nothing, anywhere.
#
# The site publishes this stdout verbatim and a fixture gates it, so a migration notice
# goes to stderr rather than into a published artefact.

# -f because every unquoted split below is over config text, never a path: a `*`
# in the config would otherwise print a file listing instead of the value.
set -fuo pipefail

CONFIG="${SCRUMIA_CONFIG:-.scrumia/config.yaml}"
CONFIG_LOCAL="${SCRUMIA_CONFIG_LOCAL:-.scrumia/config.local.yaml}"


die() { echo "compose-status.sh: $1" >&2; exit 1; }
# Folds like the report, because stderr and stdout share one terminal — a prefix on every
# line would leave nothing to fold into at 30 columns. Needs WIDTH.
note() {
  printf '%scompose-status.sh:%s\n' "$WARN" "${WARN:+$RESET}" >&2
  wrap '  ' "$WARN" "$1" >&2
}

usage() {
  cat >&2 <<'EOF'
compose-status.sh

Prints this project's ScrumIA composition — the modules it runs, then app by app.
A module is declared under `modules:`, keyed <source>:<module>; the retired `extends:`
list and the older `composition:`/`practices:` keys are still read, with a warning on
stderr. Takes no argument. Reads $SCRUMIA_CONFIG (default .scrumia/config.yaml) and
$SCRUMIA_CONFIG_LOCAL (default .scrumia/config.local.yaml), and writes nothing. Colour
is dropped when stdout is not a terminal, and when NO_COLOR is set to a non-empty value.
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

# Three shapes have existed; the precedence between them is fixed so that a half-migrated
# file cannot resolve to nothing and read as a project that runs no modules.
SHAPE=modules
if ! jq -e 'has("modules")' >/dev/null <<<"$CFG"; then
  if jq -e 'has("extends")' >/dev/null <<<"$CFG"; then
    SHAPE=extends
  elif jq -e 'has("composition") or has("practices")' >/dev/null <<<"$CFG"; then
    SHAPE=legacy
  else
    SHAPE=none
  fi
fi

case "$SHAPE" in
  extends) KEY=extends; HEADING="Modules this project extends"; APP_COL=Extends; APP_LABEL=extends
           note "warning: $CONFIG declares its modules under the retired 'extends:' — read for one more minor, migrate to 'modules:', keyed <source>:<module> (ADR-0021)" ;;
  legacy)  KEY=composition; HEADING="Modules this project extends"; APP_COL=Extends; APP_LABEL=extends
           note "warning: $CONFIG still uses the retired composition:/practices: keys — read for now, migrate to modules:" ;;
  # "declares", not "runs": this resolves nothing, so a heading claiming a `shared:` module
  # runs is how one tool reports present what the other reports absent (local-extension BR-6).
  *)       KEY=modules; HEADING="Modules this project declares"; APP_COL=Modules; APP_LABEL=modules ;;
esac

MODULES=$(jq -r --arg shape "$SHAPE" '
  if $shape == "modules" then (.modules // {} | to_entries[]
      | [ .key, ((.value // {}).params // {} | to_entries
                 | map(.key + "=" + (.value | tostring)) | join(", ")) ])
  elif $shape == "extends" then (.extends // [])[] | [., ""]
  elif $shape == "legacy" then
    ((.composition // {}) | to_entries | map(select(.value != null) | .value))[] | [., ""]
  else empty end | @tsv' <<<"$CFG")

# BR-13's grammar, spelled as scrumia-extends spells it: two readers of one key that
# disagree about what a declaration is are worse than either answer alone.
UNSOURCED=""
[ "$SHAPE" = modules ] && UNSOURCED=$(jq -r '
  def malformed:
    (test(":") | not)                                    # no source at all
    or startswith(":") or endswith(":")                  # one half missing
    or (sub(":[^:]*$"; "") | . != "shared" and . != "local" and (test("^[^/]+/[^/]+$") | not));
  [ (.modules // {} | keys[]), ((.apps // [])[] | .modules // {} | keys[]) ]
  | map(select(malformed)) | .[]' <<<"$CFG")

# BR-6's runtime cross-check on stderr: declared vs. installed. stdout is the
# published artefact, so a missing `claude` is a silent skip rather than a guess.
if command -v claude >/dev/null 2>&1; then
  RUNTIME_JSON=$(claude plugin list --json 2>/dev/null || true)
  if [ -n "${RUNTIME_JSON:-}" ] && printf '%s' "$RUNTIME_JSON" | jq -e 'type == "array"' >/dev/null 2>&1; then
    RUNTIME_PWD=$(pwd -P 2>/dev/null || pwd)
    while IFS=$'\t' read -r declared _; do
      [ -n "$declared" ] || continue
      module=${declared#*:}
      source=${declared%%:*}
      match=$(printf '%s' "$RUNTIME_JSON" | jq -r --arg mod "$module" --arg pwd "$RUNTIME_PWD" '
        [ .[]
          | select((.id // "") | startswith($mod + "@"))
          | select(.enabled == true)
          | .projectPath as $pp
          | select(
              (.scope // "") == "user"
              or ($pp // "") == $pwd
              or ($pp // "") != "" and ($pwd | startswith($pp + "/"))
            )
        ] | first // empty' 2>/dev/null)
      if [ -z "$match" ] || [ "$match" = "null" ]; then
        note "declared module '$declared' is not installed here — run \`claude plugin install $module@$source --scope project\` to install it"
      else
        ip=$(printf '%s' "$match" | jq -r '.installPath // ""' 2>/dev/null)
        if [ -z "$ip" ] || [ ! -d "$ip" ]; then
          note "declared module '$declared' has no installPath on disk — run \`claude plugin install $module@$source --scope project\` to repair it"
        fi
      fi
    done <<<"$MODULES"
  fi
fi

MOD_ROWS="" MOD_W=6
while IFS=$'\t' read -r m params; do
  [ -n "$m" ] || continue
  [ ${#m} -gt "$MOD_W" ] && MOD_W=${#m}
  MOD_ROWS="$MOD_ROWS$m"$'\t'"$params"$'\n'
done <<<"$MODULES"

APP_ROWS="" APP_W=3 PATH_W=4 EXT_W=${#APP_COL}
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
    ((if has("modules") then (.modules // {} | keys)
      elif has("extends") then (.extends // [])
      else ([.implementation] + (.practices // []) | map(select(. != null))) end)
      | if length == 0 then "none" else join(", ") end)
  ] | @tsv' <<<"$CFG")

# A heading that overflows is as unreadable as a row, and a key is longer than a name.
MOD_TABLE_W=${#HEADING}
[ "$MOD_W" -gt "$MOD_TABLE_W" ] && MOD_TABLE_W=$MOD_W
APP_TABLE_W=$((APP_W + 2 + PATH_W + 2 + EXT_W))
# The title carries the project name and repo, so it can be the widest line on the
# page; it folds on the same test as a table rather than being exempt from it.
TITLE_W=${#NAME}; TITLE_W=$((TITLE_W + 22))
[ -n "$REPO" ] && TITLE_W=$((TITLE_W + ${#REPO} + 3))
NARROW=false
for w in "$MOD_TABLE_W" "$APP_TABLE_W" "$TITLE_W"; do
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
  while IFS=$'\t' read -r m params; do
    [ -n "$m" ] || continue
    printf '  %s%s%s\n' "$BOLD" "$m" "$RESET"
    [ -n "$params" ] && wrap '    ' "$DIM" "$params"
  done <<<"$MOD_ROWS"
else
  printf '  %s%s%s\n' "$DIM" "$HEADING" "$RESET"
  printf '  %s%s%s\n' "$DIM" "$(rule "$MOD_TABLE_W" $((WIDTH - 2)))" "$RESET"
  while IFS=$'\t' read -r m params; do
    [ -n "$m" ] || continue
    printf '  %s\n' "$m"
    [ -n "$params" ] && wrap '      ' "$DIM" "$params"
  done <<<"$MOD_ROWS"
fi
[ -n "$MODULES" ] || wrap '  ' "$WARN" "Nothing is plugged in: $KEY is empty."

while IFS= read -r k; do
  [ -n "$k" ] || continue
  wrap '  ' "$WARN" "'$k' is not a declaration: a module is keyed <source>:<module> — <owner>/<repo>, 'shared' or 'local'. Nothing resolves for it."
done <<<"$UNSOURCED"

if [ -n "$APP_ROWS" ]; then
  echo
  if [ "$NARROW" = true ]; then
    while IFS=$'\t' read -r app apath ext; do
      [ -n "$app" ] || continue
      printf '  %s%s%s (%s)\n' "$BOLD" "$app" "$RESET" "$apath"
      wrap '    ' "" "$APP_LABEL: $ext"
    done <<<"$APP_ROWS"
  else
    printf '  %s%s  %s  %s%s\n' "$DIM" "$(pad App "$APP_W")" "$(pad Path "$PATH_W")" \
      "$APP_COL" "$RESET"
    printf '  %s%s%s\n' "$DIM" "$(rule "$APP_TABLE_W" $((WIDTH - 2)))" "$RESET"
    while IFS=$'\t' read -r app apath ext; do
      [ -n "$app" ] || continue
      printf '  %s  %s  %s\n' "$(pad "$app" "$APP_W")" "$(pad "$apath" "$PATH_W")" "$ext"
    done <<<"$APP_ROWS"
  fi
fi

echo
# On stderr for the same reason the migration notice is: this one is machine-local, and
# the report is a versioned artefact a fixture gates.
[ -f "$CONFIG_LOCAL" ] &&
  note "a local layer is in effect: $CONFIG_LOCAL overrides settings: and each module's params:. It is not versioned, so another machine resolves this composition's values differently."
wrap '  ' "$DIM" "What each module contributes, and to which register: scrumia-extends --list."
wrap '  ' "$DIM" "Change any of this with /scrumia-core:scrumia-compose."
echo
