#!/bin/sh
# Fresh from-source build and exhaustive axiom audit for Agent #113's
# five-layer package. Usage:
#   ./build.sh <repo-root> [<new-empty-build-dir>] [<jobs, default 2>]
# Requires the official Lean 4.19.0 `lean` on PATH. No lake, no Mathlib.
# The 90 generated row modules are compiled `jobs` at a time (about 1.3 GB
# and 20 s each); everything else sequentially.
set -u
ROOT=$(cd "$1" && pwd)
PKG="$ROOT/proofs/contributions/agent-113/five-layer"
TWO="$ROOT/proofs/contributions/agent-113/two-digit-prefix"
B=${2:-$(mktemp -d)}
J=${3:-2}
mkdir -p "$B"
if [ -n "$(ls -A "$B")" ]; then echo "build dir $B not empty" >&2; exit 2; fi
cd "$B" || exit 2
cp "$ROOT/proofs/research/continuation/LychrelDigitSums.lean" .
cp "$ROOT/proofs/contributions/agent-104/seven-column-kernel/PalindromeBridge.lean" .
for m in TwoDigitProjection TwoDigitGrowth TwoDigitNumeric; do cp "$TWO/$m.lean" .; done
cp "$PKG"/*.lean .
lean --version > lean-version.txt
sha256sum *.lean > sources.sha256
PAT='\bsorry\b|\badmit\b|native_decide|^\s*axiom\b|@\[implemented_by|@\[extern'
if grep -nE "$PAT" FourColumn*.lean FiveLayer*.lean Audit5.lean; then
  echo "FORBIDDEN construct found" >&2; exit 3
fi
comp() {
  S=$(date +%s)
  LEAN_PATH="$B" lean -o "$1.olean" "$1.lean" > "$1.log" 2>&1
  rc=$?
  echo "$1 exit=$rc $(( $(date +%s) - S ))s" >> build-summary.txt
  return $rc
}
for m in LychrelDigitSums PalindromeBridge TwoDigitProjection TwoDigitGrowth \
    TwoDigitNumeric FourColumnProjection FourColumnChain FiveLayerData; do
  comp "$m" || { echo "FAIL $m"; exit 1; }
done
ls FiveLayerR[0-9]A*.lean | sed 's/\.lean$//' | \
  xargs -P "$J" -I{} sh -c 'S=$(date +%s); LEAN_PATH="'"$B"'" lean -o {}.olean {}.lean > {}.log 2>&1; echo "{} exit=$? $(( $(date +%s) - S ))s" >> build-summary.txt'
if grep -q "FiveLayerR.*exit=[^0]" build-summary.txt; then echo "row module failed"; exit 1; fi
for m in FiveLayerRows0 FiveLayerRows1 FiveLayerRows2 FiveLayerRows3 FiveLayerRows4 FiveLayer; do
  comp "$m" || { echo "FAIL $m"; exit 1; }
done
LEAN_PATH="$B" lean Audit5.lean > audit.log 2>&1
rc=$?
echo "Audit exit=$rc" >> build-summary.txt
grep -h "AUDIT-SUMMARY" audit.log >> build-summary.txt
grep -c "exit=0" build-summary.txt
tail -3 build-summary.txt
echo "build dir: $B"
exit $rc
