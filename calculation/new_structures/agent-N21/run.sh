#!/bin/sh
set -eu
cd "$(dirname "$0")"
out=$(mktemp)
trap 'rm -f "$out"' EXIT HUP INT TERM
python3 packet_train.py > "$out"
diff -u trace.jsonl "$out"
python3 check_bigint.py
