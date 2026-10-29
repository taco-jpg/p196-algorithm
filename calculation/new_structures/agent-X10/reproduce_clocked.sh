#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
a="$(mktemp /tmp/x10_hier_sym_XXXXXX)"
b="$(mktemp /tmp/x10_hier_int_XXXXXX)"
c="$(mktemp /tmp/x10_hier_clock_XXXXXX)"
trap 'rm -f "$a" "$b" "$c"' EXIT
g++ -std=c++17 -O3 -Wno-unused-function hierarchical_fusion_probe.cpp -o "$a"
g++ -std=c++17 -O3 -Wno-unused-function hierarchical_fusion_replay.cpp -o "$b"
g++ -std=c++17 -O3 -Wno-unused-function clocked_fusion_scan.cpp -o "$c"
"$c" 500 | cmp - clocked_fusion_scan.csv
for pair in 56:11964 110:12040 165:11971; do
  R="${pair%%:*}"
  q="${pair##*:}"
  "$a" "$R" 20000 | cmp - "clocked_symbolic_R${R}.txt"
  "$b" 20000 "$q" "$R" | cmp - "clocked_replay_R${R}.txt"
done
printf 'ALL X10 CLOCKED HIERARCHY 20K CHECKS PASSED\n'
