#!/usr/bin/env bash
set -euo pipefail
AGENT102_RUNTIME_DIR="${1:-/workspace/scratch/fb513c1676b0/agent102-runtime}"
cd "$AGENT102_RUNTIME_DIR"
"$AGENT102_RUNTIME_DIR/lean-4.19.0-linux/bin/lean" --version | tee lean-version.log
"$AGENT102_RUNTIME_DIR/lean-4.19.0-linux/bin/lake" --version | tee lake-version.log
"$AGENT102_RUNTIME_DIR/lean-4.19.0-linux/bin/lean" -o smoke/Smoke.olean smoke/Smoke.lean 2>&1 | tee lean-smoke.log
"$AGENT102_RUNTIME_DIR/lean-4.19.0-linux/bin/lake" -d smoke build Smoke 2>&1 | tee lake-build.log
