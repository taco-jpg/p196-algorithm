#!/bin/bash
# chain2: (R1000 pool already running, 5 workers) wait for it; then controls; then L for clocks 10 and p11 (T<=60 first), then L* multi-epoch at clock 1000;
# then seam sweep T<=24; then the remaining L for clocks 10, p11 (60<T<=120).  Workers: 5 (the bL1000 pool keeps 3).
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
n=$(wc -l < jobs_bR1000.txt)
until [ "$(wc -l < logs/bR1000/done.txt)" -ge "$n" ]; do sleep 15; done
echo "$(date -u +%H:%M) chain2: R1000 done, starting controls" >> NOTES.md
$PY $POOL ~/p196_run/r13a/jobs_ctrl.txt 5 ctrl > logs/pool_ctrl.out 2>&1
echo "$(date -u +%H:%M) chain2: controls done, starting L clocks 10/p11 T<=60" >> NOTES.md
$PY genband.py L 10 1 60 jobs_bL10a.txt --timeout 100 --smax 8
$PY genband.py L 00001110001 1 66 jobs_bLp11a.txt --timeout 100 --smax 8
cat jobs_bL10a.txt jobs_bLp11a.txt | $PY -c "
import sys,re
lines=sys.stdin.readlines()
def key(l):
    m=re.search(r'--T (\d+)',l); v=re.search(r'--V ([\d,]+)',l).group(1); return (int(m.group(1)), v.count(','))
lines.sort(key=key)
sys.stdout.writelines(lines)
" > jobs_bLresta.txt
wc -l jobs_bLresta.txt
$PY $POOL ~/p196_run/r13a/jobs_bLresta.txt 5 bLresta > logs/pool_bLresta.out 2>&1
echo "$(date -u +%H:%M) chain2: L 10/p11 T<=60 done, starting L* 1000" >> NOTES.md
$PY gen2.py 1000 jobs_bLs1000.txt --Tgoal 96 --Tcap 120 --timeout 300
$PY $POOL ~/p196_run/r13a/jobs_bLs1000.txt 5 bLs1000 > logs/pool_bLs1000.out 2>&1
echo "$(date -u +%H:%M) chain2: L* 1000 done, starting seam sweep" >> NOTES.md
$PY genseam.py 1000 5,18,4,8,1,15,4,0,5 12 24 12 jobs_seam1000.txt --timeout 60 --budget 200 --maxlcm 24
$PY $POOL ~/p196_run/r13a/jobs_seam1000.txt 5 seam1000 > logs/pool_seam1000.out 2>&1
echo "$(date -u +%H:%M) chain2: seam sweep done" >> NOTES.md
