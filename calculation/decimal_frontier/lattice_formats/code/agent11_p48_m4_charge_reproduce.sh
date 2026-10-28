#!/usr/bin/env bash
# Full exact p48 charge-and-target obstruction with mandatory controls.
set -euo pipefail
CODE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/tmp/p196-agent11-p48-charge}"
mkdir -p "$OUT"
cd "$OUT"
g++ -O3 -std=c++17 "$CODE/agent11_p16_controls.cpp" -o controls
./controls 13 1010010000 > base13.txt
./controls 9 1100011000 > base9.txt
grep -Fq 'b=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5' base13.txt
grep -Fq 'SCC min_depth=55 size=1' base13.txt
grep -Fq 'SCC min_depth=75 size=1' base13.txt
grep -Fq 'b=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7' base9.txt
[[ $(grep -Fc 'SCC min_depth=61 size=4' base9.txt) == 2 ]]
PYTHONPATH="$CODE" nice -n 15 python3 "$CODE/agent11_p48_m4_charge.py" > charge.txt
grep -Fxq 'PAPER_CHECK_OK base10 temporal=48 overflow=(01)^24 spatial=4 cycles=16 rows=48 cut_states=192 charged_3=96 charged_6=96 root_charge=0 column_equalities=9216' charge.txt
cat charge.txt
