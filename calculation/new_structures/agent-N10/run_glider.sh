#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 build_phase.py
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra -pedantic glider.cpp -o "$tmp/glider"
for core in 0 1 2 3; do "$tmp/glider" 300 20000 "$core" 1082; done
"$tmp/glider" 400 20000 0 1082
python3 glider_bigint.py 300 0 1400
python3 glider_bigint.py 300 2 1400
