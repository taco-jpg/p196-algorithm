#!/usr/bin/env bash
set -euo pipefail
AGENT102_RUNTIME_DIR="${1:-/workspace/scratch/fb513c1676b0/agent102-runtime}"
mkdir -p "$AGENT102_RUNTIME_DIR"
cd "$AGENT102_RUNTIME_DIR"
curl --fail --location --connect-timeout 20 --max-time 60 \
  --output lean-4.19.0-linux.tar.zst.part \
  --write-out '\nhttp_code=%{http_code} bytes=%{size_download}\n' \
  'https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst'
mv lean-4.19.0-linux.tar.zst.part lean-4.19.0-linux.tar.zst
sha256sum --check <<'AGENT102_CHECKSUM'
6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe  lean-4.19.0-linux.tar.zst
AGENT102_CHECKSUM
tar --zstd --no-same-owner -xf lean-4.19.0-linux.tar.zst > extract.log 2>&1
bash "$AGENT102_RUNTIME_DIR/verify-runtime.sh" "$AGENT102_RUNTIME_DIR"
