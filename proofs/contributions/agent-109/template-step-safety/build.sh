#!/usr/bin/env bash
# Fresh from-source build of Agent #109 template-step safety. Usage: ./build.sh <repo-root>
# Requires official Lean 4.19.0 (commit 6caaee842e94) on PATH.
set -euo pipefail
ROOT=$(cd "${1:-../../../..}" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
BR="$ROOT/proofs/contributions/agent-109/template-step-bridge"
RC="$ROOT/proofs/contributions/agent-109/template-return-certificate"
B=$(mktemp -d)
cp "$ROOT/proofs/research/continuation/LychrelDigitSums.lean" "$B/"
cp "$ROOT/proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean" "$B/"
cp "$BR/TemplateStep.lean" "$BR/Compat.lean" "$RC/ReturnCertificate.lean" "$B/"
cp "$HERE/NoPalStep.lean" "$HERE/NoPalCompat.lean" "$B/"
cd "$B"
lean --version
sha256sum *.lean
for m in TemplateStep LychrelDigitSums PeriodObstructions Compat ReturnCertificate NoPalStep; do
  LEAN_PATH="$B" lean -o "$m.olean" "$m.lean" > "$m.log" 2>&1 || { echo "$m FAILED"; cat "$m.log"; exit 1; }
  echo "$m exit=0"
done
cat NoPalStep.log
LEAN_PATH="$B" lean NoPalCompat.lean; echo "NoPalCompat exit=$?"
if grep -n -E '\bsorry\b|\badmit\b|native_decide|ofReduceBool|^axiom ' NoPalStep.lean NoPalCompat.lean; then
  echo "FORBIDDEN TOKEN FOUND"; exit 1
fi
echo "token scan: no sorry/admit/native_decide/ofReduceBool/axiom in Agent109 sources"
