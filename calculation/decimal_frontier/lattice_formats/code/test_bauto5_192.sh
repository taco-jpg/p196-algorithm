#!/bin/sh
# Reproduce the exact 192-bit admission boundary: p=48, 24 overflow entries,
# base 10 (2p + ceil(log2 10)*24 = 192).  A cap of one avoids a census.
set -eu
cd "$(dirname "$0")"
c++ -O3 -std=c++17 bauto5.cpp -o /tmp/bauto5_192_test
g=$(printf '10%.0s' $(seq 1 24))
out=$(/tmp/bauto5_192_test 10 48 48 -g "$g" -cap 1 2>&1)
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -q 'CAPPED p=48'
! printf '%s\n' "$out" | grep -q 'key too long'
