#!/bin/bash
# Mac Studio run book.  Needs: g++ (clang ok), python3, the repo mirror (MIRROR=/path/to/p196-algorithm/calculation).
# 0. build (seconds)
g++ -O2 -o bauto bauto.cpp && g++ -O2 -o cauto cauto.cpp && g++ -O2 -o cmatch cmatch.cpp
export MIRROR=${MIRROR:-$HOME/p196-algorithm/calculation}
NP=${NP:-30}

# 1. Sanity (about 1 min): must print CYCLE ... cycleOK = True for base 11.
python3 pipeline.py 11 3 1 2 | head -5

# 2. Base-10 B-cycles, every period up to 20, any |B|.  Output: ACCEPT lines with g (gam stream), e (carry stream), B_t witnesses.
#    (estimate: p<=15 minutes; p=16,18 are the hard ones; RAM per process <= ~10 GB at the 150M-state cap)
mkdir -p out
for i in $(seq 0 $((NP-1))); do ./bauto 10 11 20 -w -part $i $NP -cap 300000000 > out/b10_part$i.txt 2> out/b10_part$i.err & done; wait
cat out/b10_part*.txt | grep ACCEPT | sort -u > out/b10_streams.txt
grep -h "state cap" out/b10_part*.err | sort -u > out/b10_capped.txt   # any line here = that g pattern is undecided

# 3. C decision for every B-stream, ALL C lengths (-allm), k=1 and k=2 repetitions (sum g must be even).
#    Known open jobs: p=12 stream g=100010001000 (k=2, P=24) and p=11 stream k=2 (P=22).  Parallel over the 55..~700 trim patterns v.
G=100010001000; E=$(grep "g=$G " out/b10_streams.txt | head -1 | sed 's/.* e=\([01]*\).*/\1/')
for i in $(seq 0 $((NP-1))); do ./cauto 10 $E$E $G$G 1 1 -vall -allm -w -cap 30000000 -part $i $NP > out/c_p12k2_$i.txt 2> out/c_p12k2_$i.err & done; wait
grep -h "FEASIBLE\|NOPERIOD\|CAPPED" out/c_p12k2_*.txt | head      # empty = no base-10 certificate for this stream

# 4. Full automatic pipeline for any base (stages B -> C -> mirror replay -> EDGES list), one part per process:
#    python3 pipeline.py 10 20 1 2 NP part      (CAP=30000000 env var sets the cauto cap)
for i in $(seq 0 $((NP-1))); do CAP=30000000 python3 pipeline.py 10 16 1 2 $NP $i > out/pipe10_$i.txt 2>&1 & done; wait
grep -h "CYCLE\|EDGES\|B_0\|C_0" out/pipe10_*.txt | head
