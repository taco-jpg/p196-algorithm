#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -std=c++20 -O3 centre_sparse.cpp -o centre_sparse
for u in 0 1 2; do
 for L in 7 8 9 10; do
  case "$L" in 7) total=68590;; 8) total=130321;; 9) total=1303210;; 10) total=2476099;; esac
  offset=0
  while [ "$offset" -lt "$total" ]; do
   count=300000
   rem=$((total-offset))
   if [ "$rem" -lt "$count" ]; then count="$rem"; fi
   ./centre_sparse "$u" "$L" "$count" "$offset"
   offset=$((offset+count))
  done
 done
done
python3 verify_physical.py
