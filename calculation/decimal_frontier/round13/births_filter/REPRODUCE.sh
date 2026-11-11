#!/bin/bash
# Round 13, route births_filter (agent r13c): Theorem B towers. Run from this directory.
# khr.cpp is the final source; the logs were produced by successive builds of it (bin/khr, khr_r2, khr_r3; khr_r3 = this source).
# Queue files scripts/q*.txt and scripts/stages*.txt hold the exact command lines of every run in out/ (run-machine paths).
set -e
mkdir -p bin out2
clang++ -O2 -std=c++17 -pthread src/khr.cpp -o bin/khr
clang++ -O2 -std=c++17 -pthread src/khp.cpp -o bin/khp
clang++ -O2 -std=c++17 -pthread src/kh3.cpp -o bin/kh3
# interface sets IF(d0) (Python and C++ agree): 22,601 / a0 = 87 (clock 01, d0 = 8); 22,657 / a0 = 70 (clock 0001, d0 = 12)
python3 py/ifsat.py 01 8; python3 py/ifsat.py 0001 12
# (01)^8, T = 16: all 68,520 births die, max level 526                                   [out/L16/s*.out]
for s in 0 1 2 3 4 5 6 7; do bin/khr 10 01 8 16 -kmax 6000 -nodecap 300000000 -sec 1800 -shard $s 8 > out2/L16_s$s.out; done
# (0001)^6, T = 24 and (0001)^9, T = 36: all births die (max 1369 / 107)                  [out/N24, out/N36]
bin/khr 10 0001 12 24 -kmax 6000 -nodecap 300000000 -sec 7200 > out2/N24.out
bin/khr 10 0001 12 36 -kmax 8000 -nodecap 400000000 -sec 1800 -bulk -rot2 > out2/N36.out
# (00010010111)^5, T = 55: all 1,240,956 rotation classes die, max level 345 (about 14 min) [out/CAP55a/s0.out]
bin/khr 10 00010010111 11 55 -kmax 8000 -nodecap 200000000 -sec 1500 -batch 256 -bulk -rot2 -shard 0 1 > out2/CAP55a.out
# controls: N12 at d0 = 4 (1 survivor = N12), base-9 certificate, period-8 lock, p11 at L = 22, 33, 44 (all die)
bin/khr  10 0001 4 12 -bulk -rot2 -kmax 800 -nodecap 100000000 -sec 900
bin/khr   9 11000 5 10 -bulk -rot2 -kmax 800 -nodecap 100000000 -sec 300
bin/khr  10 01 4 8 -bulk -rot2 -kmax 500 -nodecap 100000000 -sec 300
for L in 22 33 44; do bin/khr 10 00001110001 11 $L -bulk -rot2 -kmax 800 -nodecap 100000000 -sec 900; done
# validation of the reduction: plain K-head Rig(K) vs tower prediction (ctrl/plain_*.err, out/*/pred.txt): see scripts/side2.sh, side3.sh
# independent main-session program: main_check/ (mc13e.cpp, drive1.sh, drive2.sh)
