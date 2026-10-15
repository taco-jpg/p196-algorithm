#!/bin/sh
# Fresh build of the Agent #117 cycle modules on top of Agent #104's accepted sources.
# usage: lean/build.sh <repo-root> <empty-build-dir>
# Requires the official Lean 4.19.0 toolchain (commit 6caaee842e94) on PATH.
set -eu
ROOT=$1; OUT=$2
mkdir -p "$OUT/olean" "$OUT/logs"
A104="$ROOT/proofs/contributions/agent-104/seven-column-kernel"
BASE="$ROOT/proofs/research/continuation/LychrelDigitSums.lean"
HERE="$ROOT/proofs/contributions/agent-117/remaining-prefix-cycles/lean"
lean --version | tee "$OUT/logs/toolchain.txt"
sha256sum "$BASE" "$A104/PrefixInverse.lean" "$A104/FastInverse.lean" "$A104/PrefixCertificate.lean" \
  "$A104/ActualPrefix.lean" "$HERE/PrefixCycle.lean" "$HERE"/witnesses/*.lean | tee "$OUT/logs/sources.sha256"
export LEAN_PATH="$OUT/olean"
build() { # module file
  echo "== $1"; lean -o "$OUT/olean/$1.olean" "$2" > "$OUT/logs/$1.log" 2>&1; echo "exit $?" | tee -a "$OUT/logs/$1.log"; }
build LychrelDigitSums "$BASE"
build PrefixInverse "$A104/PrefixInverse.lean"
build FastInverse "$A104/FastInverse.lean"
build PrefixCertificate "$A104/PrefixCertificate.lean"
build ActualPrefix "$A104/ActualPrefix.lean"
build PrefixCycle "$HERE/PrefixCycle.lean"
for f in "$HERE"/witnesses/*.lean; do m=$(basename "$f" .lean); build "$m" "$f"; done
grep -h "depends on axioms\|^exit" "$OUT"/logs/PrefixCycle.log "$OUT"/logs/Cycle*.log | tee "$OUT/logs/axioms.txt"
