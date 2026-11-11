#!/bin/bash
# chain6: after chain5 (3-worker slot): L with larger R (R=48) for bands T<=48 of clock 1000 that passed at R=12
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chain5: centre sweep clock 1000 done" NOTES.md; do sleep 30; done
grep -h "BANDRESULT L b=10 clock=1000" logs/bL1000*/i*.log | grep "epochs=1 " | grep "status=PASS" | grep " tau=0 " | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Lpass1000.txt
$PY genband.py L 1000 1 48 jobs_bL1000_R48.txt --R 48 --timeout 120 --smax 8 --bands bands_Lpass1000.txt
$PY $POOL ~/p196_run/r13a/jobs_bL1000_R48.txt 3 bL1000R48 > logs/pool_bL1000R48.out 2>&1
echo "$(date -u +%H:%M) chain6: R=48 scan clock 1000 done" >> NOTES.md
