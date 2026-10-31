#!/bin/sh
# One-command reproduction of the p12m9 (B0/W9) no-centre result and the rec0 counts.  ~10 minutes, < 2 GB.
set -e
cd "$(dirname "$0")"
echo "== 1. local rule vs genuine pair-word evolution (expect 0 mismatches; assertion error otherwise)"
python3 test_klib.py 3000
echo "== 2. bulk tables"
python3 export_tbl.py
g++ -O2 -o kink6 kink6.cpp
echo "== 3. p12m9 exact cyclic sets (expect accepting 684,1293,978,0,0 and exact cycles 0 at K=3..7)"
./kink6 lat_p12m9.tbl 3 full p12_3.bin 2>/dev/null
for K in 4 5 6 7; do ./kink6 lat_p12m9.tbl $K incr p12_$((K-1)).bin p12_$K.bin 2>/dev/null; done
echo "== 4. independent Python incremental step and exact-centre check from the K=4 set"
python3 bin2txt.py p12m9 4 p12_4.bin p12_4.txt
python3 incr.py p12m9 p12_4.txt 4 7
python3 bin2txt.py p12m9 5 p12_5.bin p12_5.txt
python3 exact_small.py p12m9 p12_5.txt 5
python3 exact_small.py p12m9 - 5 validate 3000
python3 validate_edges.py p12m9 p12_5.txt 6 200
echo "== 5. separate SAT encoding: K=5 period 72 SAT (replayed), K=6 periods 72 and 144 UNSAT in all three orbits"
python3 relsat.py p12m9 5 72 0
for o in 0 1 2; do python3 relsat.py p12m9 6 72 $o; python3 relsat.py p12m9 6 144 $o; done
echo "== 6. rec0 control: the relaxation does NOT close (accepting states stay > 0), no exact centre to depth 8"
./kink6 lat_rec0.tbl 3 full r0_3.bin 2>/dev/null
for K in 4 5 6 7 8; do ./kink6 lat_rec0.tbl $K incr r0_$((K-1)).bin r0_$K.bin 2>/dev/null; done
