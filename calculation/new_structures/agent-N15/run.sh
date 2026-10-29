#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 monoid.py
python3 folded_relations.py
python3 dyadic.py
python3 radius.py
python3 independent.py 9 1000
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
g++ -std=c++17 -O3 -Wall -Wextra replay.cpp -o "$tmp/replay"
"$tmp/replay" 20000 9
"$tmp/replay" 20000 11
printf 'AGENT_N15_ALL_LOCAL_CHECKS_PASSED\n'
