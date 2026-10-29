#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Positive t=0..13 exact overlap proof and dual independent controls.
bash ./overlap_reproduce.sh >/dev/null
sy="$(mktemp /tmp/x10_fused_symbolic_XXXXXX)"
re="$(mktemp /tmp/x10_fused_replay_XXXXXX)"
trap 'rm -f "$sy" "$re"' EXIT
g++ -std=c++17 -O3 -Wno-unused-function fused_20k.cpp -o "$sy"
g++ -std=c++17 -O3 -Wno-unused-function fused_20k_replay.cpp -o "$re"
"$sy" 20000 | cmp - fused_20k.txt
"$re" 20000 12002 | cmp - fused_20k_replay.txt
"$re" 20000 12003 | cmp - fused_20k_replay_q12003.txt
"$re" 1000 614 | cmp - fused_1000_replay_q614.txt
printf 'ALL X10 FUSED-CENTRE 20K CHECKS PASSED\n'
