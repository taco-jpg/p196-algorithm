#!/bin/sh
set -eu
toolchain_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export LD_PRELOAD="$toolchain_dir/proc-self-compat.so${LD_PRELOAD:+:$LD_PRELOAD}"
exec "$toolchain_dir/lean-4.19.0-linux/bin/lean" "$@"
