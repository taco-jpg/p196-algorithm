#!/bin/bash
# Round 13, route k1_fixed_period (agent r13b): E_acc(K,T) for the decimal period-8 lattices.
# Run from this directory. Times on a 24-core machine; memory peaks below 20 GB (rec2: about 30 GB at K = 24).
# Expected key lines are given after each command; the logs in logs/ are the original outputs.
set -e
mkdir -p bin out
clang++ -std=c++17 -O2 -pthread -DWORDS=4  -o bin/eset3     src/eset3.cpp
clang++ -std=c++17 -O2 -pthread -DWORDS=10 -o bin/eset3w10  src/eset3.cpp
clang++ -std=c++17 -O2 -pthread -DWORDS=3  -o bin/eset2     src/eset2.cpp
clang++ -std=c++17 -O2 -pthread            -o bin/indep_acc src/indep_acc.cpp
clang++ -std=c++17 -O2 -pthread            -o bin/foldlen   src/foldlen.cpp

# T = 80, rec0 and rec1, all four phase orbits (logs/acc_rec{0,1}_o{0..3}_T80.log; 2 min each)
for L in rec0 rec1; do for o in 0 1 2 3; do
  bin/eset3 tbl/lat_$L.tbl $o 1 48 out/acc_${L}_o${o}_T80 -threads 8 | tail -2   # expect: K=44 E=709 accepting=6; E(K=45) EMPTY
done; done
# T = 192, rec2, orbits 0 and 1 (orbits 2, 3 by the symmetry Phi; main_check/ computes them directly)
for o in 0 1; do
  bin/eset3w10 tbl/lat_rec2.tbl $o 1 120 out/acc_rec2_o${o}_T192 -threads 4 | tail -2  # expect: EMPTY at K = 40 (o0), 41 (o1)
done
# second pipeline (different rule implementation and closure algorithm; logs/indep_*.log)
bin/indep_acc tbl/rec0.rows 0 1 48 out/indep_rec0_o0 4 | tail -2              # expect: E_acc(K=45) EMPTY, counts = eset3
bin/indep_acc tbl/rec1.rows 0 1 48 out/indep_rec1_o0 1 | tail -2
bin/indep_acc tbl/rec2.rows 0 1 48 out/indep_rec2_o0 3 | tail -2              # expect: E_acc(K=40) EMPTY
# Python reference (needs ../../lattice_kinks/edge_relaxation/klib.py on PYTHONPATH; logs/pycheck_K10.log, logs/pylevels_*.log)
export PYTHONPATH=../../lattice_kinks/edge_relaxation:$PYTHONPATH
python3 src/pycheck_E.py rec0 0 10                                           # E and E_acc sets equal to eset2/eset3 files, K <= 10
python3 src/pylevels.py rec0 0 35 45 out/acc_rec0_o0_T80                     # SETS EQUAL K = 35..44, EMPTY at 45
# depth 0 (all-lattice orbit), K <= 3 exact orbits of E (logs/depth0.log)
for L in rec0 rec1 rec2; do for o in 0 1 2 3; do T=80; [ $L = rec2 ] && T=192; bin/eset2 tbl/lat_$L.tbl $o 1 3 out/e2_${L}_o$o -threads 2 | grep -o "exactOrbits=[0-9]*"; done; done
