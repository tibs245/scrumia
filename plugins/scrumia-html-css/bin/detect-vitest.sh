#!/usr/bin/env bash
set -uo pipefail

CONFIG="${SCRUMIA_CONFIG:-.scrumia/config.yaml}"
if [ -f "$CONFIG" ]; then
  ROOT=$(dirname -- "$CONFIG")
else
  ROOT="."
fi

[ -f "$ROOT/package.json" ] || exit 1

if ! grep -q '"vitest"\s*:' "$ROOT/package.json" 2>/dev/null; then
  exit 1
fi

# Skip caches and VCS so a stray fixture under node_modules does not count.
if find "$ROOT" \
     \( -name node_modules -o -name .git -o -name dist -o -name build -o -name .next \) \
     -prune -o \( -name '*.test.ts' -o -name '*.test.tsx' \) -print \
     -quit 2>/dev/null | grep -q .; then
  exit 0
fi

exit 1
