#!/usr/bin/env bash
# ScrumIA — turns a ticket's scope and risk into an execution decision.
# Callers act on `instruction`; they do not re-read the matrix themselves.

set -uo pipefail

CONFIG="${SCRUMIA_CONFIG:-.scrumia/config.yaml}"

die() { printf '{"ok":false,"error":%s}\n' "$(jq -Rn --arg m "$1" '$m')"; exit 1; }
warn() { echo "pick-model.sh: $1" >&2; }

usage() {
  cat >&2 <<'EOF'
pick-model.sh <issue-number>
pick-model.sh --scope S|M|L|XL [--risk low|medium|high|critical]

Reads settings.team.execution from .scrumia/config.yaml and returns the model
to run a ticket on — or, for oversized work, an instruction to split first.
EOF
  exit 2
}

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
  REPO=$(jq -r '.project.repo // empty' <<<"$CFG")
}

labels_of_issue() {
  local issue="$1" out
  [ -n "$REPO" ] || die "project.repo missing from $CONFIG"
  out=$(gh issue view "$issue" --repo "$REPO" --json labels,title 2>&1) \
    || die "issue #$issue unreadable: $out"
  echo "$out"
}

ISSUE="" SCOPE="" RISK="" TITLE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --risk)  RISK="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    [0-9]*)  ISSUE="$1"; shift ;;
    *) usage ;;
  esac
done
[ -n "$ISSUE" ] || [ -n "$SCOPE" ] || usage

command -v jq >/dev/null 2>&1 || die "jq not found"
load_config

SCOPE_PREFIX=$(jq -r '.settings.team.execution.labels.scope_prefix // "scope/"' <<<"$CFG")
RISK_PREFIX=$(jq -r '.settings.team.execution.labels.risk_prefix // "risk/"' <<<"$CFG")

# A project that already labels its tickets keeps its own words; the matrix
# speaks S/M/L/XL and low/high, so the vocabularies are mapped, not imposed.
alias_of() {
  jq -r --arg kind "$1" --arg v "$2" \
    '.settings.team.execution.labels[$kind + "_aliases"][$v] // $v' <<<"$CFG"
}

if [ -n "$ISSUE" ]; then
  command -v gh >/dev/null 2>&1 || die "gh not found — install the GitHub CLI"
  issue_json=$(labels_of_issue "$ISSUE")
  TITLE=$(jq -r '.title // ""' <<<"$issue_json")
  SCOPE=$(jq -r --arg p "$SCOPE_PREFIX" '[.labels[].name | select(startswith($p))][0] // "" | ltrimstr($p)' <<<"$issue_json")
  RISK=$(jq -r --arg p "$RISK_PREFIX" '[.labels[].name | select(startswith($p))][0] // "" | ltrimstr($p)' <<<"$issue_json")
fi

[ -n "$SCOPE" ] && SCOPE=$(alias_of scope "$SCOPE")
[ -n "$RISK" ] && RISK=$(alias_of risk "$RISK")

DEFAULT_RISK=$(jq -r '.settings.team.execution.unrated_risk // "medium"' <<<"$CFG")
UNLABELED=$(jq -r '.settings.team.execution.unlabeled // "sonnet"' <<<"$CFG")

SCOPE_RATED=true; RISK_RATED=true
[ -n "$SCOPE" ] || { SCOPE_RATED=false; }
[ -n "$RISK" ] || { RISK_RATED=false; RISK="$DEFAULT_RISK"; }

emit() {
  jq -n --arg issue "$ISSUE" --arg title "$TITLE" --arg scope "$SCOPE" --arg risk "$RISK" \
        --arg decision "$1" --arg model "$2" --arg instruction "$3" --arg because "$4" \
        --argjson scope_rated "$SCOPE_RATED" --argjson risk_rated "$RISK_RATED" '
    {ok: true,
     issue: (if $issue == "" then null else ($issue|tonumber) end),
     title: (if $title == "" then null else $title end),
     scope: (if $scope == "" then null else $scope end),
     risk: $risk,
     scope_rated: $scope_rated,
     risk_rated: $risk_rated,
     decision: $decision,
     model: $model,
     instruction: $instruction,
     because: $because}'
}

# No scope label means the ticket was never refined; guessing one would invent
# an estimate nobody made.
if [ "$SCOPE_RATED" = false ]; then
  warn "issue has no ${SCOPE_PREFIX}* label — falling back to execution.unlabeled"
  emit "model" "$UNLABELED" \
    "Run on $UNLABELED, and say in the PR that this ticket carried no ${SCOPE_PREFIX}* label. Ask for refinement rather than assuming a size." \
    "no ${SCOPE_PREFIX}* label -> execution.unlabeled"
  exit 0
fi

CELL=$(jq -r --arg s "$SCOPE" --arg r "$RISK" \
  '.settings.team.execution.matrix[$s][$r] // empty' <<<"$CFG")

if [ -z "$CELL" ]; then
  warn "no matrix cell for scope=$SCOPE risk=$RISK — falling back to execution.unlabeled"
  emit "model" "$UNLABELED" \
    "Run on $UNLABELED. The matrix in $CONFIG has no cell for scope=$SCOPE risk=$RISK — report this gap." \
    "matrix[$SCOPE][$RISK] undefined -> execution.unlabeled"
  exit 0
fi

RISK_NOTE=""
[ "$RISK_RATED" = false ] && RISK_NOTE=" Risk was not rated, so ${RISK_PREFIX}${RISK} was assumed — flag this if the ticket looks riskier."

# split_or_<model>: prefer splitting, but oversized is not a dead end. The
# caller judges feasibility, which is why the fallback travels with the verdict.
case "$CELL" in
  split_or_*)
    FALLBACK=${CELL#split_or_}
    emit "split_or_model" "$FALLBACK" \
      "First try to split this ticket into independently executable tickets. If — and only if — the work is genuinely indivisible, execute it on $FALLBACK and state in the PR why the split was refused. Do not split into tickets that cannot ship on their own.$RISK_NOTE" \
      "scope=$SCOPE risk=$RISK -> $CELL"
    ;;
  split)
    emit "split" "" \
      "Split this ticket before executing it. This cell allows no fallback model — return it to refinement.$RISK_NOTE" \
      "scope=$SCOPE risk=$RISK -> split"
    ;;
  *)
    emit "model" "$CELL" \
      "Execute this ticket on $CELL.$RISK_NOTE" \
      "scope=$SCOPE risk=$RISK -> $CELL"
    ;;
esac
