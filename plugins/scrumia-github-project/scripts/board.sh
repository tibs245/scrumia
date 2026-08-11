#!/usr/bin/env bash
# Deprecated shim: this path is unreachable from another module once installed (ADR-0018).
echo "board.sh: deprecated path — run 'scrumia-board' instead; this shim is removed two releases after the one that deprecated it" >&2
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")/../bin" && pwd)/scrumia-board" "$@"
