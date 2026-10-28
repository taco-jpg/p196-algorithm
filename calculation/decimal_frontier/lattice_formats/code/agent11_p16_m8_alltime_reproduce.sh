#!/usr/bin/env bash
# Complete base10 (01)^8 m8 all-time absorbing lattice symmetric-row graph.
set -euo pipefail
CODE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/tmp/p196-agent11-m8-alltime}"
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
# Independent dual-wrap carry engine reuses the already published second solver.
python3 - "$CODE/agent11_p16_m8_alltime.cpp" "$CODE/agent11_p48_m8_independent.cpp" "$OUT/independent.cpp" <<'PY'
from pathlib import Path
import sys
A=Path(sys.argv[1]).read_text();B=Path(sys.argv[2]).read_text()
a=A.index('static bool phi(');aa=A.index('static Row decode(',a)
b=B.index('static bool phi(');bb=B.index('static uint64_t ipow(',b)
Path(sys.argv[3]).write_text(A[:a]+B[b:bb]+A[aa:])
PY
for m in 4 8; do
    g++ -O3 -std=c++17 -DLAT_M="$m" "$CODE/agent11_p16_m8_alltime.cpp" -o "primary$m"
    g++ -O3 -std=c++17 -DLAT_M="$m" independent.cpp -o "independent$m"
    nice -n 15 "./primary$m" "primary$m.txt" > "primary$m.log" 2> "primary$m.progress"
    nice -n 15 "./independent$m" "independent$m.txt" > "independent$m.log" 2> "independent$m.progress"
    cmp "primary$m.txt" "independent$m.txt"
done
grep -Fxq 'GRAPH M=4 nodes=14440 live=13868 dead=572 lost_symmetry=0 duplicate_axes=358 cycles=70 cycle_members=106 primitive_cycles=64 primitive_cycle_members=96' primary4.txt
grep -Fxq 'GRAPH M=8 nodes=10425680 live=10364408 dead=61272 lost_symmetry=0 duplicate_axes=14226 cycles=622 cycle_members=4250 primitive_cycles=552 primitive_cycle_members=4144' primary8.txt
for row in '2 128' '6 232' '9 128' '10 16' '18 32' '38 16'; do read -r length count <<< "$row"; grep -Fxq "PRIMITIVE_CYCLE_LEN $length count=$count" primary8.txt; done
echo 'COMPUTED COMPLETE: decimal g=(01)^8, m8 selfmirror all temporal multipliers, 552 primitive cycles / 10425680 axis-labelled states; independent carry solvers agree'
