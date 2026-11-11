#!/bin/bash
# chain5: after chain3 (the 3-worker slot): centre sweeps for clock 1000 bands (N<=48, Lc<=6), then seam sweep for T in (12,24] (Lj<=8)
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chain3: L(T_rot epoch) for clock 1000 done" NOTES.md; do sleep 30; done
$PY $POOL ~/p196_run/r13a/jobs_centre1000.txt 3 centre1000 > logs/pool_centre1000.out 2>&1
echo "$(date -u +%H:%M) chain5: centre sweep clock 1000 done" >> NOTES.md
