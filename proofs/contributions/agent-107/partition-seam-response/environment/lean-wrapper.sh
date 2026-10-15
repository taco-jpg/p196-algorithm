#!/bin/sh
set -eu
export LD_PRELOAD=/workspace/scratch/64704429df15/env107/readlink_self.so${LD_PRELOAD:+:$LD_PRELOAD}
exec /workspace/scratch/64704429df15/toolchain/lean-4.19.0-linux/bin/lean "$@"
