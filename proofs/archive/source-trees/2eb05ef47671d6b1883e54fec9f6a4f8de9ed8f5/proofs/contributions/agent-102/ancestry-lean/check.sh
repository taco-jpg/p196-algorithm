#!/bin/sh
# Clean rebuild of the Agent #102 ancestry module from repository sources.
# Usage: LEAN=/path/to/lean-4.19.0-linux/bin/lean sh check.sh [empty-build-dir]
# Expects official Lean 4.19.0 (commit 6caaee842e94); Std only, no Mathlib.
set -eu
LEAN=${LEAN:-lean}
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../../.." && pwd)
OUT=${1:-$(mktemp -d)}
mkdir -p "$OUT"
"$LEAN" --version
cp "$REPO/proofs/research/continuation/LychrelDigitSums.lean" "$OUT/"
cp "$HERE"/RunAncestry.lean "$OUT/"
[ -f "$HERE/AncestryExtinction.lean" ] && cp "$HERE/AncestryExtinction.lean" "$OUT/"
cd "$OUT"
sha256sum *.lean
LEAN_PATH="$OUT" "$LEAN" -o LychrelDigitSums.olean LychrelDigitSums.lean > LychrelDigitSums.log 2>&1
LEAN_PATH="$OUT" "$LEAN" -o RunAncestry.olean RunAncestry.lean
if [ -f AncestryExtinction.lean ]; then
  LEAN_PATH="$OUT" "$LEAN" -o AncestryExtinction.olean AncestryExtinction.lean
fi
echo "PASS (build dir $OUT)"
