#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ulimit -v 8388608
tmp="$(mktemp -d)";trap 'rm -rf "$tmp"' EXIT
g++ -std=c++17 -O3 "$DIR/p21_head_primary.cpp" -o "$tmp/primary"
g++ -std=c++17 -O3 "$DIR/p21_head_checker.cpp" -o "$tmp/check"
: > "$tmp/primary_all"; : > "$tmp/check_all"
for k in 2 3 4; do
  nice -n 10 "$tmp/primary" "$k" "$tmp/primary$k.txt" | tee "$tmp/sum_primary$k.txt"
  nice -n 10 "$tmp/check" "$k" "$tmp/check$k.txt" | tee "$tmp/sum_check$k.txt"
  diff -u "$tmp/primary$k.txt" "$tmp/check$k.txt"
  diff -u "$tmp/sum_primary$k.txt" "$tmp/sum_check$k.txt"
  cat "$tmp/primary$k.txt" >> "$tmp/primary_all"
done
diff -u "$DIR/p21_head_phase0.txt" "$tmp/primary_all"
# Required positive controls from the same engine and standard known SCCs.
g++ -std=c++17 -O3 "$DIR/bauto5.cpp" -o "$tmp/bauto5"
nice -n 10 "$tmp/bauto5" 9 10 10 -cap 3000000 -maxscc 8 -g 1100011000 > "$tmp/b9"
nice -n 10 "$tmp/bauto5" 13 10 10 -cap 3000000 -maxscc 8 -g 1010010000 > "$tmp/b13"
grep -q 'states=956310.*nontrivial_sccs=7' "$tmp/b9"
grep -q 'minc=4 depth=61' "$tmp/b9"
grep -q 'states=250302.*nontrivial_sccs=5' "$tmp/b13"
grep -q 'cyclen=1 depth=55' "$tmp/b13"
grep -q 'cyclen=1 depth=75' "$tmp/b13"
echo "PASS exhaustive K2/K3/K4 finite graphs, independent SCC checker, b9/b13 controls"
