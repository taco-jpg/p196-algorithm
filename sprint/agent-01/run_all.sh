#!/usr/bin/env bash
# Reproduce every COMPUTED number in REPORT.md (sprint agent 01).
# Run from the repository root:  bash sprint/agent-01/run_all.sh [MAXK]
# MAXK defaults to 9.  Memory (allocated array sizes, not measured RSS): k<=7 < 3 GB, k=8 core
# ~2.6 GB, k=9 forward ~4.6 GB.  k=10 needs the 512 GB machine (see REPORT.md).
set -euo pipefail
cd "$(dirname "$0")"
MAXK=${1:-9}
CC=${CC:-cc}
OPT="-O3"
mkdir -p out
for p in fwdclosure peel sccchk layer witness backcore fullback orbit196; do
  $CC $OPT -o $p $p.c
done

# 0. cross-checks of the forward step against the Lean inverse (Python reference)
python3 check_ref.py

# 1. 196's projections at t = 100, 1000, 10^4, 10^5, 3*10^5
./orbit196 100 1000 10000 100000 300000 > out/orbit_states.txt
word() { grep "^t=$1 " out/orbit_states.txt | sed 's/.*q=//' | cut -d, -f1-$2; }

# 2. dense forward closures k=3..7 from t=100, infinite-history cores, SCC check
for k in 3 4 5 6 7; do
  ./fwdclosure $k out/F$k.t100 "$(word 100 $k)"
  ./peel $k out/F$k.t100.bits out/peel$k
  ./sccchk $k out/F$k.t100.bits "$(word 100 $k)" "$(word 1000 $k)" "$(word 10000 $k)" "$(word 100000 $k)" "$(word 300000 $k)"
done

# 3. layered width 8 (forward + core + dense bitset for width 9)
./layer 8 out/F7.t100.bits out/L8 fdsc "$(word 100 8)" "$(word 1000 8)" "$(word 10000 8)" "$(word 100000 8)" "$(word 300000 8)"

# 4. layered width 9 (forward only), from t=100 and from t=1000
if [ "$MAXK" -ge 9 ]; then
  ./layer 9 out/L8.bits out/L9 f "$(word 100 9)" "$(word 1000 9)" "$(word 10000 9)" "$(word 100000 9)" "$(word 300000 9)"
  ./layer 9 out/L8.bits out/L9from1000 f "$(word 1000 9)" "$(word 100 9)" "$(word 10000 9)" "$(word 100000 9)" "$(word 300000 9)"
  ./backcore 9 out/L8.bits 3537 3899 3984 4307 5838 6311 9123
  ./fullback 9 60000000 3537 3899 3984 4307 5838 6311 9123
fi

# 5. per-prefix table and forward-walk witnesses (Lean data source)
python3 table.py
./witness 7 out/F6.t100.bits "$(word 100 7)" out/walks7.tsv
./witness 8 out/F7.t100.bits "$(word 100 8)" out/walks8.tsv
python3 verify_walks.py 8 out/walks8.tsv "$(word 100 8)"

# 6. regenerate the Lean data modules (then: cd lean && lake build P196.Sprint.Agent01.W8Final)
python3 gen_lean_walks.py 8 out/walks8.tsv "$(word 100 8)" 25 8 ../../lean/P196/Sprint/Agent01
