#!/bin/bash
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
dl() { date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 $1" +%s; }
n=$(wc -l < jobs_D1000.txt)
until [ "$(wc -l < logs/D1000/done.txt)" -ge "$n" ] || ! pgrep -f "pool.py ~/p196_run/r13a/jobs_D1000.txt" > /dev/null; do sleep 15; done
echo "$(date -u +%H:%M) chain3d: D1000 finished ($(wc -l < logs/D1000/done.txt) jobs); starting L(T_rot epoch) with deadline 14:00" >> NOTES.md
$PY genband.py L 1000 1 120 jobs_bLrotall1000.txt --rotepoch --timeout 120 --smax 8
DEADLINE=$(dl 14:00) $PY $POOL ~/p196_run/r13a/jobs_bLrotall1000.txt 3 bLrotall1000 > logs/pool_bLrotall1000.out 2>&1
echo "$(date -u +%H:%M) chain3: L(T_rot epoch) for clock 1000 done" >> NOTES.md
