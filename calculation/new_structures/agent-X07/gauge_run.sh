#!/bin/sh
set -eu
cd "$(dirname "$0")"
pyout=$(mktemp)
scalarout=$(mktemp)
cppq=/tmp/x07_gauge_scalar_$$
cppg=/tmp/x07_gauge_gmp_$$
trap 'rm -f "$pyout" "$scalarout" "$cppq" "$cppg"' EXIT
python3 gauge_preimages.py > "$pyout"
cmp "$pyout" gauge_counts.json
c++ -std=c++17 -O3 scalar_trace.cpp -o "$cppq"
"$cppq" 10 20000 > "$scalarout"
grep -q 'final_len=8277 digit_growth=8266 fnv64=882bbe1ad0ba698d' "$scalarout"
c++ -std=c++17 -O3 gmp_replay.cpp -lgmpxx -lgmp -o "$cppg"
"$cppg" 8278 20001
