#!/usr/bin/env bash
# Exact self-mirror absorbing row census; base 10, g=(01)^8, one 16-step return.
set -euo pipefail
CODE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/tmp/p196-agent11-p16-m8}"
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
g++ -O3 -std=c++17 -DLATTICE_M=4 "$CODE/agent11_p16_m8_rows.cpp" -o m4
nice -n 15 ./m4 m4.state m4.rows > m4.result 2> m4.progress
grep -Fxq 'COMPLETED m=4 p=16 selfmirror fixed rows=48 enumerated=14440' m4.result
g++ -O3 -std=c++17 -DLATTICE_M=8 "$CODE/agent11_p16_m8_rows.cpp" -o m8
nice -n 15 ./m8 m8.state m8.rows > m8.result 2> m8.progress
grep -Fxq 'COMPLETED m=8 p=16 selfmirror fixed rows=0 enumerated=10425680' m8.result
[[ ! -s m8.rows ]]
echo 'COMPUTED: decimal p16 m8 one-period self-mirror absorbing row cycle census EXHAUSTED (0 candidates)'
