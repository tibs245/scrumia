#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat >&2 <<'EOF'
usage: detect-boundaries.sh [--json] [--window N] <path>...

Reports each .parse()/.safeParse() call and whether a trust-boundary marker
appears within N lines above it in the same file (default 25).

  --json      emit one JSON object per call instead of a table
  --window N  lines to look back for a boundary marker

Verdicts are heuristic: this reads text, not data flow. See
rules/validation-at-boundary.md.

exit 0  every call sits near a boundary marker
exit 1  the tool failed (unreadable input, missing dependency)
exit 2  bad usage
exit 3  at least one call looks internal
EOF
	exit 2
}

die() {
	printf 'detect-boundaries: %s\n' "$1" >&2
	exit 1
}

# Extending this list is how a project teaches the detector about its own client wrapper.
BOUNDARY_RE='fetch\(|axios\.|\.request\(|http\.(get|post|request)\(|XMLHttpRequest|'
BOUNDARY_RE+='readFile|readFileSync|createReadStream|'
BOUNDARY_RE+='req\.body|request\.body|\.formData\(|FormData|searchParams|URLSearchParams|process\.argv|'
BOUNDARY_RE+='\.subscribe\(|onMessage|consume\(|'
BOUNDARY_RE+='process\.env|JSON\.parse\('

JSON=0
WINDOW=25
PATHS=()

while [ $# -gt 0 ]; do
	case "$1" in
	--json) JSON=1 ;;
	--window)
		[ $# -ge 2 ] || usage
		WINDOW="$2"
		shift
		;;
	-h | --help) usage ;;
	-*) usage ;;
	*) PATHS+=("$1") ;;
	esac
	shift
done

[ ${#PATHS[@]} -gt 0 ] || usage
command -v awk >/dev/null 2>&1 || die "awk is required"

case "$WINDOW" in
'' | *[!0-9]*) usage ;;
esac

files=()
while IFS= read -r f; do
	[ -n "$f" ] && files+=("$f")
done < <(
	for p in "${PATHS[@]}"; do
		if [ -d "$p" ]; then
			find "$p" \( -name node_modules -o -name dist -o -name .git \) -prune -o \
				-type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' \) -print
		elif [ -f "$p" ]; then
			printf '%s\n' "$p"
		else
			die "no such file or directory: $p"
		fi
	done | sort
)

if [ ${#files[@]} -eq 0 ]; then
	exit 0
fi

findings=$(
	# Via the environment, not -v: awk unescapes a -v assignment and would eat the backslashes.
	BOUNDARY_RE="$BOUNDARY_RE" awk -v win="$WINDOW" -v json="$JSON" '
    BEGIN { bre = ENVIRON["BOUNDARY_RE"] }
    FNR == 1 { last = 0 }
    $0 ~ bre { last = FNR }
    /\.(safeParse|parse)\(/ {
      if ($0 ~ /^[[:space:]]*(\/\/|\*)/) next
      # JSON.parse is a boundary marker, not a Zod call site; a line may carry both.
      probe = $0
      gsub(/JSON\.parse\(/, "", probe)
      if (probe !~ /\.(safeParse|parse)\(/) next
      verdict = (last > 0 && FNR - last <= win) ? "boundary" : "internal-suspect"
      line = $0
      sub(/^[[:space:]]+/, "", line)
      gsub(/"/, "\\\"", line)
      if (json)
        printf "{\"file\":\"%s\",\"line\":%d,\"verdict\":\"%s\",\"heuristic\":true,\"code\":\"%s\"}\n", FILENAME, FNR, verdict, line
      else
        printf "%s:%d\t%s\t%s\n", FILENAME, FNR, verdict, line
      if (verdict == "internal-suspect") suspect = 1
    }
    END { exit (suspect ? 3 : 0) }
  ' "${files[@]}"
) && rc=0 || rc=$?

[ -n "${findings:-}" ] && printf '%s\n' "$findings"

if [ "$JSON" -eq 0 ] && [ "${rc:-0}" -eq 3 ]; then
	printf '\nVerdicts are heuristic. An "internal-suspect" call may cross a boundary\nthrough a helper this script cannot follow — verify before removing it.\n' >&2
fi

exit "${rc:-0}"
