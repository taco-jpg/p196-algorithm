#!/bin/sh
set -eu
cd "$(dirname "$0")"
out=$(mktemp)
trap 'rm -f "$out"' EXIT HUP INT TERM
python3 binary_scattering.py > "$out"
diff -u binary_trace.jsonl "$out"
python3 check_binary_bigint.py
