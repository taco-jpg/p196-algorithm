#!/bin/bash
# chainW: last-minute cross-checks in the 3-worker slot after chainZ's R* step: seam T<=12 with cadical195 (deadline 15:00)
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chainZ: R\* clocks 10/p11" NOTES.md || [ $(date -u +%H%M) -gt 1450 ]; do sleep 20; done
sed 's/--budget 200/--budget 200 --solver cadical195/' jobs_seam1000a.txt > jobs_seam1000a_x.txt
DEADLINE=$(date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 15:00" +%s) $PY $POOL ~/p196_run/r13a/jobs_seam1000a_x.txt 3 seam1000ax > logs/pool_seam1000ax.out 2>&1
echo "$(date -u +%H:%M) chainW: seam T<=12 cadical cross-check done" >> NOTES.md
