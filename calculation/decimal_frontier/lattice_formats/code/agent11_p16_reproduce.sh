#!/usr/bin/env bash
# Exhaustive decimal p=16 alternating neutral-exterior decision.
# Run: bash calculation/decimal_frontier/lattice_formats/code/agent11_p16_reproduce.sh /tmp/agent11-p16
# Needs g++ (C++17), ~3.2 GiB memory; private checkpoints/logs stay outside the repository.
set -euo pipefail
CODE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/tmp/agent11-p16}"
mkdir -p "$OUT"
cd "$OUT"
g++ -O3 -std=c++17 "$CODE/agent11_p16_controls.cpp" -o control
g++ -O3 -std=c++17 "$CODE/agent11_p16_stage1.cpp" -o stage1
g++ -O3 -std=c++17 "$CODE/agent11_p16_stage2.cpp" -o stage2
./control 13 1010010000 > control13.txt
grep -Fq 'b=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5' control13.txt
grep -Fq 'SCC min_depth=55 size=1' control13.txt
grep -Fq 'SCC min_depth=75 size=1' control13.txt
./control 9 1100011000 > control9.txt
grep -Fq 'b=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7' control9.txt
[[ $(grep -Fc 'SCC min_depth=61 size=4' control9.txt) == 2 ]]
echo 'MANDATORY_CONTROLS_PASSED'
export P16_CKPT="$OUT/checkpoint.bin"
ulimit -v 3700000
if [[ ! -e stage1.ok ]]; then
  nice -n 15 ./stage1 210000000 3600 > stage1.log 2> stage1.err
  grep -Fq 'STATUS CAPPED total=210365479 depth=366 wdone=365 acc=0' stage1.log
  touch stage1.ok
fi
if [[ ! -e stage2.ok ]]; then
  nice -n 15 ./stage2 300000000 3600 > stage2.log 2> stage2.err
  grep -Fq 'STATUS EXHAUSTED total=257093987 depth=592 wdone=591 acc=0' stage2.log
  touch stage2.ok
fi
echo 'COMPUTED EXHAUSTED p=16 g=0101010101010101 states=257093987 depth=592 accepted=0'
