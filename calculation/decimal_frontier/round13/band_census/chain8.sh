#!/bin/bash
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chain6: R=48 scan clock 1000 done" NOTES.md; do sleep 30; done
$PY $POOL ~/p196_run/r13a/jobs_seam1000Nmul.txt 3 seam1000N > logs/pool_seam1000N.out 2>&1
echo "$(date -u +%H:%M) chain8: seam N-multiple sweep (T<=12 bands, N=24,36,48) done" >> NOTES.md
