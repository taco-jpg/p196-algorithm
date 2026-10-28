#!/usr/bin/env bash
# Base10 p48 alternating, primitive spatial m8 one-block selfmirror exact census.
set -euo pipefail
CODE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/tmp/p196-agent11-p48-m8}"
mkdir -p "$OUT"
cd "$OUT"
g++ -O3 -std=c++17 "$CODE/agent11_p16_controls.cpp" -o controls
./controls 13 1010010000 > control13.txt
./controls 9 1100011000 > control9.txt
grep -Fq 'b=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5' control13.txt
grep -Fq 'SCC min_depth=55 size=1' control13.txt
grep -Fq 'SCC min_depth=75 size=1' control13.txt
grep -Fq 'b=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7' control9.txt
[[ $(grep -Fc 'SCC min_depth=61 size=4' control9.txt) == 2 ]]
# Reuse the existing checkpointable first method, changing only its time period.
sed -e 's/static constexpr int M=LATTICE_M,B=10,P=16;/static constexpr int M=LATTICE_M,B=10,P=48;/' -e 's/COMPLETED m=%d p=16/COMPLETED m=%d p=48/' "$CODE/agent11_p16_m8_rows.cpp" > primary.cpp
g++ -O3 -std=c++17 -DLATTICE_M=4 primary.cpp -o primary4
g++ -O3 -std=c++17 -DLATTICE_M=8 primary.cpp -o primary8
g++ -O3 -std=c++17 -DLAT_M=4 "$CODE/agent11_p48_m8_independent.cpp" -o independent4
g++ -O3 -std=c++17 -DLAT_M=8 "$CODE/agent11_p48_m8_independent.cpp" -o independent8
nice -n 15 ./primary4 primary4.state primary4.rows > primary4.txt 2> primary4.progress
grep -Fxq 'COMPLETED m=4 p=48 selfmirror fixed rows=96 enumerated=14440' primary4.txt
nice -n 15 ./independent4 > independent4.txt
grep -Fxq 'INDEPENDENT m=4 p=48 seeds=14440 primitive_returns=96' <(tail -1 independent4.txt)
nice -n 15 ./primary8 primary8.state primary8.rows > primary8.txt 2> primary8.progress
grep -Fxq 'COMPLETED m=8 p=48 selfmirror fixed rows=0 enumerated=10425680' primary8.txt
[[ ! -s primary8.rows ]]
nice -n 15 ./independent8 > independent8.txt
grep -Fxq 'INDEPENDENT m=8 p=48 seeds=10425680 primitive_returns=0' independent8.txt
echo 'COMPUTED EXHAUSTED: base10 p48 g=(01)^24 primitive m8 one-period selfmirror 0/10425680, independent dual-wrap verifier agrees'
