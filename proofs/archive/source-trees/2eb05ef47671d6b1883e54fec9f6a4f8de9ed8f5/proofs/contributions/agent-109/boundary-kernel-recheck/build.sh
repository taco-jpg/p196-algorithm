#!/usr/bin/env bash
# Fresh from-source build of Agent #109 kernel-only boundary recheck.
# Usage: ./build.sh <repo-root>   (official Lean 4.19.0, 6caaee842e94, on PATH)
# Memory: each lean process is capped at 6 GB virtual; at most 2 run concurrently.
set -euo pipefail
ROOT=$(cd "${1:-../../../..}" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
ORIG="$ROOT/proofs/research/main_existence_attempt/boundary_resume/lean"
B=$(mktemp -d)
cp "$ORIG"/{ReverseClosure,SoficProof,BoundaryData,BoundaryCertificate,ArithmeticBridge,BulkTargets,BulkDerivation}.lean "$B/"
cp "$HERE"/*.lean "$HERE"/run_chunks.py "$HERE"/chunk_modules.json "$B/"
cd "$B"
lean --version
sha256sum *.lean | sort -k2 > SOURCES.sha256; wc -l < SOURCES.sha256
mk() { ( ulimit -v 6000000; LEAN_PATH="$B" lean -o "$1.olean" "$1.lean" > "$1.log" 2>&1 ) || { echo "$1 FAILED"; tail -20 "$1.log"; exit 1; }; echo "$1 exit=0"; }
for m in ReverseClosure SoficProof BoundaryData BoundaryDataK SoficFast; do mk $m; done
LEAN_PATH="$B" lean TranscriptionCheck.lean; echo "TranscriptionCheck (compiled transcription control, not in proof chain)"
for p in "0 1" "2 3" "4 5" "6 7"; do set -- $p; mk FastData$1 & mk FastData$2 & wait; done
python3 run_chunks.py chunk_modules.json || {
  echo "retrying failed chunk modules sequentially (concurrency memory pressure)"
  for m in $(python3 -c "import json;print(' '.join(json.load(open('chunk_modules.json'))))"); do [ -f "$m.olean" ] || mk "$m"; done; }
for g in 0 1 2 3 4 5 6 7; do mk ProjK$g; cat ProjK$g.log; done
for m in BoundaryCertificate ArithmeticBridge BulkTargets BulkDerivation; do mk $m; done
for m in BoundaryCertificateK ArithmeticBridgeK BulkTargetsK BulkDerivationK; do mk $m; done
LEAN_PATH="$B" lean AuditK.lean; echo "AuditK exit=$?"
K="BoundaryDataK.lean SoficFast.lean FastData?.lean ProjK*.lean BoundaryCertificateK.lean ArithmeticBridgeK.lean BulkTargetsK.lean BulkDerivationK.lean AuditK.lean"
if grep -n -E '\bsorry\b|\badmit\b|native_decide|ofReduceBool|^axiom ' $K; then echo "FORBIDDEN TOKEN FOUND"; exit 1; fi
echo "token scan: no sorry/admit/native_decide/ofReduceBool/axiom in Agent109 K sources"
