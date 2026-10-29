#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
CXX="${CXX:-g++}"
"$CXX" -std=c++17 -O3 charged_fission_replay.cpp -o "$tmp/charged_fission_replay"
"$CXX" -std=c++17 -O3 charged_edge_classification.cpp -o "$tmp/charged_edge_classification"
"$CXX" -std=c++17 -O3 complement_front_probe.cpp -o "$tmp/complement_front_probe"
python3 charged_identity_control.py > "$tmp/charged_identity_control.txt"
cmp "$tmp/charged_identity_control.txt" charged_identity_control.txt
"$tmp/charged_edge_classification" 20000 > "$tmp/charged_edge_T20000.csv"
cmp "$tmp/charged_edge_T20000.csv" charged_edge_T20000.csv
"$tmp/complement_front_probe" 20000 > "$tmp/complement_front_20k.txt" 2> "$tmp/complement_front_20k_summary.txt"
cmp "$tmp/complement_front_20k.txt" complement_front_20k.txt
cmp "$tmp/complement_front_20k_summary.txt" complement_front_20k_summary.txt
"$tmp/charged_fission_replay" 20000 5976 88 49 4 > "$tmp/charged_fission_R5976.txt"
"$tmp/charged_fission_replay" 20000 5977 88 49 4 > "$tmp/charged_fission_R5977.txt"
"$tmp/charged_fission_replay" 20000 5993 88 75 4 > "$tmp/charged_fission_R5993.txt"
"$tmp/charged_fission_replay" 1000 305 88 49 4 > "$tmp/charged_fission_R305_T1000.txt"
"$tmp/charged_fission_replay" 1000 305 88 49 0 > "$tmp/charged_fission_R305_a0_T1000.txt"
for base in charged_fission_R5976 charged_fission_R5977 charged_fission_R5993 charged_fission_R305_T1000 charged_fission_R305_a0_T1000; do
  cmp "$tmp/$base.txt" "$base.txt"
done
printf 'ALL AGENT-X10 CHARGED FISSION CHECKS PASSED: 90 channels, 2,706 big-int identities, 3x20,001 and 2x1,001 independent full-word replays.\n'
