#!/bin/sh
exec /workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false "$@"
