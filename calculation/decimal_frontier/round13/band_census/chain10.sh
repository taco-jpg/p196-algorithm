#!/bin/bash
# chain10: 3-worker slot, after chain9: R* (comoving) for clocks 10/p11 (R-PASS bands, T'<=36), time box 14:35
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chain9: tau-scan 24<T<=36 done" NOTES.md; do sleep 30; [ $(date -u +%H%M) -gt 1425 ] && break; done
[ $(date -u +%H%M) -gt 1425 ] && exit 0
grep -h "BANDRESULT R b=10 clock=10 " logs/bRresta/i*.log | grep "status=PASS" | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Rpass10.txt
grep -h "BANDRESULT R b=10 clock=00001110001 " logs/bRresta/i*.log | grep "status=PASS" | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Rpassp11.txt
$PY genband.py R 10 1 36 jobs_bRs10.txt --minM --comoving --timeout 100 --bands bands_Rpass10.txt --smax 8
$PY genband.py R 00001110001 1 36 jobs_bRsp11.txt --minM --comoving --timeout 100 --bands bands_Rpassp11.txt --smax 8
cat jobs_bRs10.txt jobs_bRsp11.txt > jobs_bRsrest.txt
DEADLINE=$(date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 14:35" +%s) $PY $POOL ~/p196_run/r13a/jobs_bRsrest.txt 3 bRsrest > logs/pool_bRsrest.out 2>&1
echo "$(date -u +%H:%M) chain10: R* clocks 10/p11 T'<=36 done" >> NOTES.md
