#!/bin/sh
# Exact bauto5 SCC-status regression plus an independent Python graph oracle.
set -eu
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
c++ -O2 -std=c++17 bauto5.cpp -o "$tmp/bauto5"
python3 scc_oracle_b4.py > "$tmp/oracle"
grep -q '^states=957 edges=1012 nontrivial_sccs=4$' "$tmp/oracle"
"$tmp/bauto5" 4 6 6 -g 101100 -cap 10000 -maxscc 6 > "$tmp/default"
grep -q '^G p=6 g=101100 states=957 edges=1012 nontrivial_sccs=4 ' "$tmp/default"
test "$(grep -c '^SCCMIN p=6 ' "$tmp/default")" -eq 4
"$tmp/bauto5" 4 6 6 -g 101100 -cap 10000 -maxscc 1 -scccap 0 > "$tmp/capped"
grep -q '^SCCMIN_CAPPED p=6 g=101100 S=3 size=1 vertex_cap=0 status=UNDECIDED$' "$tmp/capped"
grep -q '^SCCMIN_SCOPE p=6 g=101100 nontrivial=4 examined=1 size_capped=1 omitted=3$' "$tmp/capped"
"$tmp/bauto5" 4 6 6 -g 101100 -cap 10000 -maxscc 0 > "$tmp/omitted"
grep -q '^SCCMIN_SCOPE p=6 g=101100 nontrivial=4 examined=0 size_capped=0 omitted=4$' "$tmp/omitted"
echo 'bauto5 SCC accounting: ALL TESTS PASSED'
