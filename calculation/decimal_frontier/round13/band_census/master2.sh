#!/bin/bash
# master2 (5-worker slot, time-boxed): after the seam1000b pool: R 10/p11 T'<=36 -> L* 1000 -> L 10/p11 36<T<=60 -> seam clock 10 -> R 10/p11 36<T'<=120
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
note() { echo "$(date -u +%H:%M) master2: $*" >> NOTES.md; }
until [ "$(wc -l < logs/seam1000b/done.txt 2>/dev/null || echo 0)" -ge "$(wc -l < jobs_seam1000b.txt)" ]; do sleep 20; done
note "seam sweep clock 1000 T<=24 done"
# R for clocks 10/p11, T'<=36
$PY genband.py R 10 1 36 jobs_bR10a.txt --minM --timeout 100 --smax 8
$PY genband.py R 00001110001 1 33 jobs_bRp11a.txt --minM --timeout 100 --smax 8
cat jobs_bR10a.txt jobs_bRp11a.txt > jobs_bRresta.txt
DEADLINE=$(( $(date +%s) + 1500 )) $PY $POOL ~/p196_run/r13a/jobs_bRresta.txt 5 bRresta > logs/pool_bRresta.out 2>&1
note "R clocks 10/p11 T'<=36 done"
# L* multi-epoch clock 1000, time box until 13:55
$PY gen2.py 1000 jobs_bLs1000.txt --Tgoal 96 --Tcap 120 --timeout 240
DEADLINE=$(date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 13:55" +%s) $PY $POOL ~/p196_run/r13a/jobs_bLs1000.txt 5 bLs1000 > logs/pool_bLs1000.out 2>&1
note "L* 1000 done (time box 13:55)"
# L clocks 10/p11 36<T<=60, time box 14:20
$PY genband.py L 10 37 60 jobs_bL10b.txt --timeout 100 --smax 8
$PY genband.py L 00001110001 34 66 jobs_bLp11b.txt --timeout 100 --smax 8
cat jobs_bL10b.txt jobs_bLp11b.txt > jobs_bLrestb.txt
DEADLINE=$(date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 14:20" +%s) $PY $POOL ~/p196_run/r13a/jobs_bLrestb.txt 5 bLrestb > logs/pool_bLrestb.out 2>&1
note "L clocks 10/p11 36<T<=60 done (time box 14:20)"
# seam sweep clock 10 (rec0/rec1/rec2), T<=16, time box 14:40
$PY - <<'PY2'
import json
d=json.load(open('~/p196_run/r13a/ctrl/p8_bands.json'))
for i,x in enumerate(d):
    open(f'~/p196_run/r13a/ctrl/E_p8_{i}.txt','w').write(','.join(map(str,x['V0'])))
PY2
for i in 0 1 2; do E=$(cat ctrl/E_p8_$i.txt); $PY genseam.py 10 $E 8 16 8 jobs_seam10_$i.txt --timeout 40 --budget 200 --maxlcm 48; done
cat jobs_seam10_0.txt jobs_seam10_1.txt jobs_seam10_2.txt > jobs_seam10.txt
DEADLINE=$(date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 14:40" +%s) $PY $POOL ~/p196_run/r13a/jobs_seam10.txt 5 seam10 > logs/pool_seam10.out 2>&1
note "seam sweep clock 10 done (time box 14:40)"
