#!/bin/bash
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
dl() { date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 $1" +%s; }
echo "$(date -u +%H:%M) chain3c: starting D-type sweeps (R* for larger T stopped at c3: 167/195 done)" >> NOTES.md
DEADLINE=$(dl 13:55) $PY $POOL ~/p196_run/r13a/jobs_D1000.txt 3 D1000 > logs/pool_D1000.out 2>&1
echo "$(date -u +%H:%M) chain3c: D1000 done; starting L(T_rot epoch) for clock 1000" >> NOTES.md
$PY genband.py L 1000 1 120 jobs_bLrotall1000.txt --rotepoch --timeout 120 --smax 8
DEADLINE=$(dl 14:15) $PY $POOL ~/p196_run/r13a/jobs_bLrotall1000.txt 3 bLrotall1000 > logs/pool_bLrotall1000.out 2>&1
echo "$(date -u +%H:%M) chain3: L(T_rot epoch) for clock 1000 done" >> NOTES.md
