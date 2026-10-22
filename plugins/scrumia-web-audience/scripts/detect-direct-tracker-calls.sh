#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat >&2 <<'USAGE'
usage: detect-direct-tracker-calls.sh [--queue NAME] --module <dir> <source-root>

Lists source files under <source-root> that mention the tracker's command queue
and sit outside the measurement module <dir>. The queue is `_paq` unless
--queue says otherwise.

exit 0  no file outside the module mentions the queue
exit 1  the tool failed (missing directory)
exit 2  bad usage
exit 3  at least one file outside the module mentions the queue
USAGE
	exit 2
}

QUEUE='_paq'
MODULE=''
ROOT=''

while [ $# -gt 0 ]; do
	case "$1" in
	--queue)
		[ $# -ge 2 ] || usage
		QUEUE="$2"
		shift
		;;
	--module)
		[ $# -ge 2 ] || usage
		MODULE="$2"
		shift
		;;
	-h | --help) usage ;;
	-*) usage ;;
	*) ROOT="$1" ;;
	esac
	shift
done

[ -n "$MODULE" ] && [ -n "$ROOT" ] || usage
[ -d "$MODULE" ] || { printf 'detect-direct-tracker-calls: no such directory: %s\n' "$MODULE" >&2; exit 1; }
[ -d "$ROOT" ] || { printf 'detect-direct-tracker-calls: no such directory: %s\n' "$ROOT" >&2; exit 1; }

module_abs="$(cd "$MODULE" && pwd)"
found=0

while IFS= read -r file; do
	file_abs="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"
	case "$file_abs" in
	"$module_abs"/*) continue ;;
	esac
	if grep -Fq -- "$QUEUE" "$file"; then
		printf '%s\n' "$file"
		found=1
	fi
done < <(
	find "$ROOT" \( -name node_modules -o -name dist -o -name .git \) -prune -o \
		-type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' -o -name '*.astro' -o -name '*.vue' -o -name '*.svelte' -o -name '*.html' \) -print | sort
)

[ "$found" -eq 0 ] || exit 3
