#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sy="$(mktemp /tmp/x10_nested_sy_XXXXXX)"
re="$(mktemp /tmp/x10_nested_re_XXXXXX)"
cl="$(mktemp /tmp/x10_nested_cl_XXXXXX)"
trap 'rm -f "$sy" "$re" "$cl"' EXIT
g++ -std=c++17 -O3 -Wno-unused-function nested_three_fusion_probe.cpp -o "$sy"
g++ -std=c++17 -O3 -Wno-unused-function nested_three_fusion_replay.cpp -o "$re"
g++ -std=c++17 -O3 -Wno-unused-function third_clock_scan.cpp -o "$cl"
"$cl" 56 500 | cmp - third_clock_scan_R56.csv
"$sy" 56 109 20000 | cmp - nested3_symbolic_20k.txt
"$sy" 56 161 20000 | cmp - nested3_symbolic_S161.txt
"$re" 20000 12014 56 109 | cmp - nested3_replay_q12014.txt
"$re" 20000 12015 56 109 | cmp - nested3_replay_q12015.txt
"$re" 1000 600 56 109 | cmp - nested3_replay_q600_t1000.txt
"$re" 20000 11977 56 161 | cmp - nested3_replay_S161_q11977.txt
printf 'ALL X10 NESTED THREE-FUSION 20K CHECKS PASSED\n'
