#!/bin/sh
export LD_PRELOAD="/workspace/scratch/63e10b24caf2/runtime-audit/app-path-compat.so"
exec "/workspace/scratch/63e10b24caf2/runtime-audit/lean-4.19.0-linux/bin/lean" "$@"
