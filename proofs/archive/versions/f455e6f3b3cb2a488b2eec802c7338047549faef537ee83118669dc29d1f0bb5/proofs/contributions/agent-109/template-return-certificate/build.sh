#!/usr/bin/env bash
# Fresh from-source build of Agent #109 return-certificate soundness. Usage: ./build.sh <repo-root>
# Requires official Lean 4.19.0 (commit 6caaee842e94) on PATH.
set -euo pipefail
ROOT=$(cd "${1:-../../../..}" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
BR="$ROOT/proofs/contributions/agent-109/template-step-bridge"
B=$(mktemp -d)
cp "$ROOT/proofs/research/continuation/LychrelDigitSums.lean" "$B/"
cp "$ROOT/proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean" "$B/"
cp "$BR/TemplateStep.lean" "$BR/Compat.lean" "$B/"
cp "$HERE/ReturnCertificate.lean" "$HERE/CertCompat.lean" "$HERE/CertDemo.lean" "$HERE/CrossCheck.lean" "$B/"
cd "$B"
lean --version
sha256sum *.lean
for m in TemplateStep LychrelDigitSums PeriodObstructions Compat ReturnCertificate; do
  LEAN_PATH="$B" lean -o "$m.olean" "$m.lean" > "$m.log" 2>&1 || { echo "$m FAILED"; cat "$m.log"; exit 1; }
  echo "$m exit=0"
done
cat ReturnCertificate.log
LEAN_PATH="$B" lean CertCompat.lean; echo "CertCompat exit=$?"
LEAN_PATH="$B" lean CertDemo.lean; echo "CertDemo exit=$?"
LEAN_PATH="$B" lean CrossCheck.lean; echo "CrossCheck exit=$?"
if grep -n -E '\bsorry\b|\badmit\b|native_decide|ofReduceBool|^axiom ' TemplateStep.lean Compat.lean ReturnCertificate.lean CertCompat.lean; then
  echo "FORBIDDEN TOKEN FOUND"; exit 1
fi
echo "token scan: no sorry/admit/native_decide/ofReduceBool/axiom in Agent109 sources"
