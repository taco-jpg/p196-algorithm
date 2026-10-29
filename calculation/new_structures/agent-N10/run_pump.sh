#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 build_phase.py
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra -pedantic pump.cpp -o "$tmp/pump"
for core in 0 1 2 3; do "$tmp/pump" 300 20000 "$core"; done
python3 pump_bigint.py 300 1000
