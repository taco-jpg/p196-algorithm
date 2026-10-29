#!/bin/sh
set -eu
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
c++ -std=c++17 -O3 collision_probe.cpp -o "$tmp/collision_probe"
python3 check_collision.py "$tmp/collision_probe" > "$tmp/observed"
diff -u collision_fixture.txt "$tmp/observed"
echo 'DECIMAL_MIXED_PHASE_COLLISION_PASS'
