#!/usr/bin/env bash
# Fresh build of Agent #109 template-step bridge. Usage: ./build.sh <repo-root>
# Requires official Lean 4.19.0 (commit 6caaee842e94) on PATH.
set -euo pipefail
ROOT=$(cd "${1:-../../../..}" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
B=$(mktemp -d)
cp "$ROOT/proofs/research/continuation/LychrelDigitSums.lean" "$B/"
cp "$ROOT/proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean" "$B/"
cp "$ROOT/proofs/contributions/2026-10-15-agent8-complementary-bulk/ActualWordBridge.lean" "$B/"
cp "$HERE/TemplateStep.lean" "$HERE/Compat.lean" "$HERE/Audit.lean" "$HERE/IntegerEndpoints.lean" "$B/"
cd "$B"
lean --version
sha256sum *.lean
for m in TemplateStep LychrelDigitSums PeriodObstructions ActualWordBridge; do
  LEAN_PATH="$B" lean -o "$m.olean" "$m.lean" > "$m.log" 2>&1; echo "$m exit=$?"
done
LEAN_PATH="$B" lean Audit.lean; echo "Audit exit=$?"
LEAN_PATH="$B" lean -o Compat.olean Compat.lean; echo "Compat exit=$?"
LEAN_PATH="$B" lean IntegerEndpoints.lean; echo "IntegerEndpoints exit=$?"
if grep -n -E '\bsorry\b|\badmit\b|native_decide|ofReduceBool|^axiom ' TemplateStep.lean Compat.lean IntegerEndpoints.lean; then
  echo "FORBIDDEN TOKEN FOUND"; exit 1
fi
echo "token scan: no sorry/admit/native_decide/ofReduceBool/axiom in Agent109 sources"
