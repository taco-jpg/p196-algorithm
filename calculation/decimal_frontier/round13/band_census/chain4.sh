#!/bin/bash
# chain4: after chain2: R for clocks 10 and p11 (T'<=120), then the remaining L for clocks 10/p11 (60<T<=120), each with 5 workers
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chain2: seam sweep done" NOTES.md; do sleep 30; done
echo "$(date -u +%H:%M) chain4: starting R for clocks 10, p11" >> NOTES.md
$PY genband.py R 10 1 120 jobs_bR10.txt --minM --timeout 150 --smax 8
$PY genband.py R 00001110001 1 120 jobs_bRp11.txt --minM --timeout 150 --smax 8
cat jobs_bR10.txt jobs_bRp11.txt > jobs_bRrest.txt
$PY $POOL ~/p196_run/r13a/jobs_bRrest.txt 5 bRrest > logs/pool_bRrest.out 2>&1
echo "$(date -u +%H:%M) chain4: R 10/p11 done, starting L 60<T<=120 for clocks 10/p11" >> NOTES.md
$PY genband.py L 10 61 120 jobs_bL10b.txt --timeout 120 --smax 8
$PY genband.py L 00001110001 67 120 jobs_bLp11b.txt --timeout 120 --smax 8
cat jobs_bL10b.txt jobs_bLp11b.txt > jobs_bLrestb.txt
$PY $POOL ~/p196_run/r13a/jobs_bLrestb.txt 5 bLrestb > logs/pool_bLrestb.out 2>&1
echo "$(date -u +%H:%M) chain4: done" >> NOTES.md
