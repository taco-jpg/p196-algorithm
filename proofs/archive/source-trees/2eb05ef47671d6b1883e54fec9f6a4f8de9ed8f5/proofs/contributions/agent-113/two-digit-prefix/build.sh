#!/bin/sh
# Fresh from-source build and exhaustive axiom audit for Agent #113's
# two-digit-prefix package. Usage:
#   ./build.sh <repo-root> [<empty-build-dir>]
# Requires the official Lean 4.19.0 `lean` on PATH. No lake, no Mathlib.
# Peak memory about 4 GB per certificate module; modules are compiled
# sequentially.
set -u
ROOT=$(cd "$1" && pwd)
PKG="$ROOT/proofs/contributions/agent-113/two-digit-prefix"
B=${2:-$(mktemp -d)}
mkdir -p "$B"
if [ -n "$(ls -A "$B")" ]; then echo "build dir $B not empty" >&2; exit 2; fi
cd "$B" || exit 2
cp "$ROOT/proofs/research/continuation/LychrelDigitSums.lean" .
cp "$ROOT/proofs/contributions/agent-104/seven-column-kernel/PalindromeBridge.lean" .
cp "$PKG"/*.lean .
lean --version > lean-version.txt
sha256sum *.lean > sources.sha256
# Forbidden constructs in this package's own sources (hard gate).
PAT='\bsorry\b|\badmit\b|native_decide|^\s*axiom\b|@\[implemented_by|@\[extern'
if grep -nE "$PAT" TwoDigit*.lean Audit.lean; then
  echo "FORBIDDEN construct found" >&2; exit 3
fi
# Imported dependencies: logged for inspection (their only hits are prose
# comments); the transitive axiom audit below is the hard gate for them.
grep -nE "$PAT" LychrelDigitSums.lean PalindromeBridge.lean > deps-forbidden-scan.txt
STATUS=0
for m in LychrelDigitSums PalindromeBridge TwoDigitProjection TwoDigitGrowth \
    TwoDigitNumeric TwoDigitCertificate \
    TwoDigitCert10 TwoDigitCert20 TwoDigitCert32 TwoDigitCert40 TwoDigitCert41 \
    TwoDigitCert60 TwoDigitCert64 TwoDigitCert65 TwoDigitCert76 TwoDigitCert80 \
    TwoDigitCert81 TwoDigitCert82 TwoDigitCert83 TwoDigitMain; do
  S=$(date +%s)
  LEAN_PATH="$B" lean -o "$m.olean" "$m.lean" > "$m.log" 2>&1
  rc=$?
  echo "$m exit=$rc $(( $(date +%s) - S ))s" | tee -a build-summary.txt
  if [ $rc -ne 0 ]; then STATUS=1; break; fi
done
if [ $STATUS -eq 0 ]; then
  LEAN_PATH="$B" lean Audit.lean > audit.log 2>&1
  rc=$?
  echo "Audit exit=$rc" | tee -a build-summary.txt
  grep -h "AUDIT-SUMMARY" audit.log | tee -a build-summary.txt
  [ $rc -ne 0 ] && STATUS=1
fi
echo "build dir: $B"
exit $STATUS
