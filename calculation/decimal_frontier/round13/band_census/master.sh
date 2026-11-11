#!/bin/bash
# master (5-worker slot): sequential steps
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
note() { echo "$(date -u +%H:%M) master: $*" >> NOTES.md; }
until [ "$(wc -l < logs/ctrl/done.txt)" -ge 168 ]; do sleep 20; done
note "controls done"
# step 2: L for clocks 10/p11 (T<=36 first, cheap), timeout 100 s per rotation
$PY genband.py L 10 1 36 jobs_bL10a.txt --timeout 100 --smax 8
$PY genband.py L 00001110001 1 33 jobs_bLp11a.txt --timeout 100 --smax 8
cat jobs_bL10a.txt jobs_bLp11a.txt | $PY -c "
import sys,re
lines=sys.stdin.readlines()
def key(l):
    m=re.search(r'--T (\d+)',l); v=re.search(r'--V ([\d,]+)',l).group(1); return (int(m.group(1)), v.count(','))
lines.sort(key=key); sys.stdout.writelines(lines)" > jobs_bLresta.txt
$PY $POOL ~/p196_run/r13a/jobs_bLresta.txt 5 bLresta > logs/pool_bLresta.out 2>&1
note "L clocks 10/p11 T<=36 done"
# step 3: seam sweep clock 1000, T<=24, Lj<=8 (N<=24 -> T | 24 and T not dividing 12 not yet swept in seam1000a)
$PY genseam.py 1000 5,18,4,8,1,15,4,0,5 12 24 8 jobs_seam1000b.txt --timeout 60 --budget 200 --maxlcm 24
$PY $POOL ~/p196_run/r13a/jobs_seam1000b.txt 5 seam1000b > logs/pool_seam1000b.out 2>&1
note "seam sweep clock 1000 T<=24 done"
# step 4: L* multi-epoch for clock 1000
$PY gen2.py 1000 jobs_bLs1000.txt --Tgoal 96 --Tcap 120 --timeout 240
$PY $POOL ~/p196_run/r13a/jobs_bLs1000.txt 5 bLs1000 > logs/pool_bLs1000.out 2>&1
note "L* 1000 done"
# step 5: R for clocks 10/p11 (T' <= 36)
$PY genband.py R 10 1 36 jobs_bR10a.txt --minM --timeout 100 --smax 8
$PY genband.py R 00001110001 1 33 jobs_bRp11a.txt --minM --timeout 100 --smax 8
cat jobs_bR10a.txt jobs_bRp11a.txt > jobs_bRresta.txt
$PY $POOL ~/p196_run/r13a/jobs_bRresta.txt 5 bRresta > logs/pool_bRresta.out 2>&1
note "R clocks 10/p11 T'<=36 done"
# step 6: L clocks 10/p11 36<T<=60
$PY genband.py L 10 37 60 jobs_bL10b.txt --timeout 100 --smax 8
$PY genband.py L 00001110001 34 66 jobs_bLp11b.txt --timeout 100 --smax 8
cat jobs_bL10b.txt jobs_bLp11b.txt > jobs_bLrestb.txt
$PY $POOL ~/p196_run/r13a/jobs_bLrestb.txt 5 bLrestb > logs/pool_bLrestb.out 2>&1
note "L clocks 10/p11 36<T<=60 done"
# step 7: R clocks 10/p11 for 36<T'<=120
$PY genband.py R 10 37 120 jobs_bR10b.txt --minM --timeout 100 --smax 8
$PY genband.py R 00001110001 34 120 jobs_bRp11b.txt --minM --timeout 100 --smax 8
cat jobs_bR10b.txt jobs_bRp11b.txt > jobs_bRrestb.txt
$PY $POOL ~/p196_run/r13a/jobs_bRrestb.txt 5 bRrestb > logs/pool_bRrestb.out 2>&1
note "R clocks 10/p11 36<T'<=120 done"
# step 8: seam sweep clock 10 (three lattice exteriors), T<=16
$PY - <<'PY2'
import json
d=json.load(open('~/p196_run/r13a/ctrl/p8_bands.json'))
for i,x in enumerate(d):
    open(f'~/p196_run/r13a/ctrl/E_p8_{i}.txt','w').write(','.join(map(str,x['V0'])))
PY2
for i in 0 1 2; do E=$(cat ctrl/E_p8_$i.txt); $PY genseam.py 10 $E 8 16 8 jobs_seam10_$i.txt --timeout 40 --budget 200 --maxlcm 48; done
cat jobs_seam10_0.txt jobs_seam10_1.txt jobs_seam10_2.txt > jobs_seam10.txt
$PY $POOL ~/p196_run/r13a/jobs_seam10.txt 5 seam10 > logs/pool_seam10.out 2>&1
note "seam sweep clock 10 done"
