#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 build_phase.py
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra -pedantic replay.cpp -o "$tmp/replay"
for centre in 0 1 2 3; do "$tmp/replay" 300 20000 "$centre"; done
for copies in 301 320 400 2100; do "$tmp/replay" "$copies" 20000 0; done
python3 independent_bigint.py 300 2000
