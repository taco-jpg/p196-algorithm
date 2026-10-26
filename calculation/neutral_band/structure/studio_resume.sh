#!/bin/bash
# Resume the p=11 doubled C-job (k=2) on the Mac Studio with cauto_fast.
# Run from the directory that holds cauto.cpp / out/ (calculation/neutral_band/structure), after copying cauto_fast.cpp and cauto_done.py there.
set -e
NP=${NP:-30}
G=11100010000; E=10100110011

# 0. build (about 10 s).  Works with g++ or clang++ (needs unsigned __int128, i.e. any 64-bit build).
g++ -O2 -std=c++17 -o cauto_fast cauto_fast.cpp

# 1. stop the old job (its out/c_p11k2_*.err files are kept; only the patterns that were in progress are recomputed).
pkill -x cauto || true          # the 15 old processes are started as ./cauto
sleep 1

# 2. the done list.  Old format: every FINISHED pattern leaves one stderr line  "allm v=<22 chars of 0/1> jstar=.. period=.. mlo=.. ..."
#    in out/c_p11k2_<i>.err (stdout .txt only holds FEASIBLE / CAPPED / NOPERIOD lines).  cauto_fast reads the v=<pattern> strings
#    itself; a pattern that also appears in a CAPPED / NOPERIOD / FEASIBLE line is NOT treated as done.
cat out/c_p11k2_*.err out/c_p11k2_*.txt > out/done_p11k2.txt
python3 cauto_done.py indices ${E}${E} ${G}${G} out/c_p11k2_*.err out/c_p11k2_*.txt | wc -l      # number of finished patterns (indices 0..7314)

# 3. 30 processes, interleaved over the remaining patterns; -sym drops one pattern of every shift-equivalent pair (shift by 11).
for i in $(seq 0 $((NP-1))); do
  ./cauto_fast 10 ${E}${E} ${G}${G} 1 1 -vall -allm -w -cap 30000000 -sym -skip out/done_p11k2.txt -part $i $NP \
      > out/f_p11k2_$i.txt 2> out/f_p11k2_$i.err &
done
wait

# 4. result.  Empty output of the first command = no certificate for this stream (any C length).
grep -h "FEASIBLE\|NOPERIOD\|CAPPED" out/f_p11k2_*.txt | sort | uniq -c
grep -h "^DONE" out/f_p11k2_*.txt | wc -l                    # patterns run by the new binary
# 5. coverage proof: every one of the 7315 patterns is finished directly or by a shift-equivalent one, nothing flagged
python3 cauto_done.py coverage ${E}${E} ${G}${G} out/c_p11k2_*.err out/c_p11k2_*.txt out/f_p11k2_*.txt
