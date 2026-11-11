#!/bin/bash
# Round 13, route band_census (agent r13a). Run from this directory; Python 3 with python-sat (kissat404, cadical195).
# The per-job command lines that produced logs.tar.gz are in jobs/jobs_*.txt (they call bandrun.py / bandjob.py /
# centrejob.py / seamjob.py / rootjob.py with the run-machine path ~/p196_run/r13a; replace it by this directory).
set -e
# 1. census (bitset F-iteration over all (2b-1)^s words), clocks 1000, 10, 00001110001, s = 1..8   [census/runall.log]
clang++ -O2 -std=c++17 -pthread census/bandcensus.cpp -o census/bandcensus
for clk in 1000 10 00001110001; do for s in 1 2 3 4 5 6 7 8; do
  census/bandcensus 10 $clk $s 5 > census/b${clk}_s$s.txt          # expect totals 265 / 284 / 161 BAND lines
done; done
# 2. encodings validated against genuine big-integer orbits (78 runs, jobs/jobs_val.txt): VALIDATE PASS
python3 bandval.py 11 --n 1 --T 36          # VALIDATE PASS (one of the 78 runs)
# 3. U3 control (30 words, T' = 40 and T = 120; jobs/jobs_ctrlU3.txt) and one L instance, e.g.
python3 bandjob.py L --b 10 --clock 1000 --V 18,9,0 --T 120 --Tprime 40 --R 12 --all --solver kissat404   # ALLUNSAT
# 4. the two non-trivial band centres (exact centre SAT, then direct replay)          [logs/centre1000/, centre_replay.out]
python3 centrejob.py --clock 1000 --V 11,8,5  --T 24 --Trot 8 --Lmax 6 --timeout 40 --budget 120   # CENTREBAND FOUND ... WITNESS_C [13, 2, 13]
python3 centrejob.py --clock 1000 --V 13,10,7 --T 24 --Trot 8 --Lmax 6 --timeout 40 --budget 120   # CENTREBAND FOUND ... tau=4
python3 centre_replay.py --V 5,11,8  --C 13,2,13 --N 24 --j 1      # EQUAL
python3 centre_replay.py --V 13,7,10 --C 5,16,5  --N 24 --j 1      # EQUAL
# 5. seams from the T12 exterior and rooted exteriors for these bands: jobs/jobs_seam1000*.txt, jobs/jobs_root*.txt
