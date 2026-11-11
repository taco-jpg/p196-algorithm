#!/bin/bash
# after the p11 s=8 census: run with 5 workers: R (clock 1000); controls + validations; seam sweep T<=48 (clock 1000);
# then L tests for clocks 10 and p11; then L* multi-epoch for clock 1000.
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until [ -s census/b00001110001_s8.done ]; do sleep 20; done
echo "$(date -u +%H:%M) chain1: census finished, starting R1000" >> NOTES.md
$PY $POOL ~/p196_run/r13a/jobs_bR1000.txt 5 bR1000 > logs/pool_bR1000.out 2>&1
echo "$(date -u +%H:%M) chain1: R1000 done, starting controls" >> NOTES.md
cat jobs_ctrlU3.txt jobs_val.txt > jobs_ctrl.txt
$PY $POOL ~/p196_run/r13a/jobs_ctrl.txt 5 ctrl > logs/pool_ctrl.out 2>&1
echo "$(date -u +%H:%M) chain1: controls done, starting seam sweep" >> NOTES.md
$PY genseam.py 1000 5,18,4,8,1,15,4,0,5 12 48 8 jobs_seam1000.txt --timeout 60 --budget 900 --maxlcm 48
$PY $POOL ~/p196_run/r13a/jobs_seam1000.txt 5 seam1000 > logs/pool_seam1000.out 2>&1
echo "$(date -u +%H:%M) chain1: seam sweep done, starting L for clocks 10, p11" >> NOTES.md
$PY genband.py L 10 1 120 jobs_bL10.txt --timeout 150 --smax 8
$PY genband.py L 00001110001 1 120 jobs_bLp11.txt --timeout 150 --smax 8
cat jobs_bL10.txt jobs_bLp11.txt | $PY -c "
import sys,re
lines=sys.stdin.readlines()
def key(l):
    m=re.search(r'--T (\d+)',l); v=re.search(r'--V ([\d,]+)',l).group(1); return (int(m.group(1)), v.count(','))
lines.sort(key=key)
sys.stdout.writelines(lines)
" > jobs_bLrest.txt
wc -l jobs_bLrest.txt
$PY $POOL ~/p196_run/r13a/jobs_bLrest.txt 5 bLrest > logs/pool_bLrest.out 2>&1
echo "$(date -u +%H:%M) chain1: L clocks 10/p11 done" >> NOTES.md
