#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 build_phase.py
python3 partial_guard.py
python3 partial_bigint_control.py
python3 guard_cycle.py 20000
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra -pedantic replay.cpp -o "$tmp/replay"
"$tmp/replay" 1031 20000 0
