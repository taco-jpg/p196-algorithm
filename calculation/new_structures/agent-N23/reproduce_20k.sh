#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -std=c++17 -O3 protected_20k.cpp -o /tmp/n23_digit20k
c++ -std=c++17 -O3 protected_bigint.cpp -o /tmp/n23_limb20k
for q in 7000 7001 8000; do
  a=$(/tmp/n23_digit20k "$q" 20000)
  b=$(/tmp/n23_limb20k "$q" 20000)
  echo "$a"
  echo "$b"
  ah=$(echo "$a" | sed -n 's/.*checksum_mod1000000007=\([0-9]*\).*/\1/p')
  bh=$(echo "$b" | sed -n 's/.*checksum_mod1000000007=\([0-9]*\).*/\1/p')
  [[ -n "$ah" && "$ah" == "$bh" ]]
  expected=$(awk -F '\t' -v q="$q" 'NR>1 && $1==q {print $8}' seed20k.tsv)
  [[ "$ah" == "$expected" ]]
done
