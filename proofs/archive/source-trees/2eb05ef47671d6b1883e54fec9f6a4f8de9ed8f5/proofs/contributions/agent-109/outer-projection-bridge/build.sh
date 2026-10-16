#!/usr/bin/env bash
# Fresh from-source build of Agent #109 outer-projection bridge. Usage: ./build.sh <repo-root>
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
cp "$HERE/agent7-deps/OuterFinite.lean" "$HERE/agent7-deps/OuterBounds.lean" "$B/"
cp "$HERE/OuterBridge.lean" "$HERE/OuterCompat.lean" "$B/"
cd "$B"
lean --version
sha256sum *.lean
echo "3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6  OuterFinite.lean
75ed5831f0cc1e9c6016672ebef83cf0f46da279432b3694ba075627cb973a76  OuterBounds.lean" | sha256sum -c
for m in TemplateStep LychrelDigitSums PeriodObstructions Compat ReturnCertificate OuterFinite OuterBounds OuterBridge; do
  LEAN_PATH="$B" lean -o "$m.olean" "$m.lean" > "$m.log" 2>&1 || { echo "$m FAILED"; cat "$m.log"; exit 1; }
  echo "$m exit=0"
done
cat OuterFinite.log OuterBounds.log OuterBridge.log
LEAN_PATH="$B" lean OuterCompat.lean; echo "OuterCompat exit=$?"
if grep -n -E '\bsorry\b|\badmit\b|native_decide|ofReduceBool|^axiom ' TemplateStep.lean Compat.lean ReturnCertificate.lean OuterBridge.lean OuterCompat.lean OuterFinite.lean OuterBounds.lean; then
  echo "FORBIDDEN TOKEN FOUND"; exit 1
fi
echo "token scan: no sorry/admit/native_decide/ofReduceBool/axiom in built sources"
