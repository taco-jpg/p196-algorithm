#!/usr/bin/env bash
# Complete decimal g=(01)^8 spatial m4 all-temporal row-map functional graph.
set -euo pipefail
CODE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/tmp/p196-agent11-m4-alltime}"
mkdir -p "$OUT"
cd "$OUT"
g++ -O3 -std=c++17 "$CODE/agent11_p16_controls.cpp" -o control
./control 13 1010010000 > base13.txt
./control 9 1100011000 > base9.txt
grep -Fq 'b=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5' base13.txt
grep -Fq 'SCC min_depth=55 size=1' base13.txt
grep -Fq 'SCC min_depth=75 size=1' base13.txt
grep -Fq 'b=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7' base9.txt
[[ $(grep -Fc 'SCC min_depth=61 size=4' base9.txt) == 2 ]]
g++ -O3 -std=c++17 "$CODE/agent11_p16_m4_alltime.cpp" -o m4
nice -n 15 ./m4 > graph_cpp.txt
grep -Fxq 'COMPLETE states=130321 valid=128126 dead=2195 cycles=110 cyclic_states=210 max_cycle_blocks=3 mirrored_cycles=70 primitive_mirror_cycles=64 primitive_mirror_longer=16' graph_cpp.txt
PYTHONPATH="$CODE" nice -n 15 python3 "$CODE/agent11_p16_m4_alltime_check.py" > graph_python.txt
grep -Fq 'PYTHON_COMPLETE 130321 valid 128126 cycles 110 length_counts [(1, 60), (3, 50)] mirror 70 primitive_mirror 64 longer 16 cycle_members 210' graph_python.txt
echo 'COMPUTED: base10 p16 g=(01)^8, m4 functional-graph COMPLETE (60 fixed, 50 three-cycles)'
