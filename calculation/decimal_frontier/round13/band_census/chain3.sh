#!/bin/bash
# chain3: when the bL1000c pool ends (3 workers free): tau-scan (T<=24) and R* (comoving) for clock 1000, with 3 workers
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
n=$(wc -l < jobs_bL1000d.txt)
until [ "$(wc -l < logs/bL1000d/done.txt 2>/dev/null || echo 0)" -ge "$n" ]; do sleep 20; done
echo "$(date -u +%H:%M) chain3: bL1000d done, starting tau-scan + R* for clock 1000 (3 workers)" >> NOTES.md
$PY gentau.py 1000 24 jobs_tau1000.txt --timeout 60
grep -h "BANDRESULT R b=10 clock=1000" logs/bR1000/i*.log | grep "status=PASS" | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Rpass1000.txt
$PY genband.py R 1000 1 120 jobs_bRs1000.txt --minM --comoving --timeout 200 --bands bands_Rpass1000.txt
cat jobs_tau1000.txt jobs_bRs1000.txt > jobs_c3.txt
$PY $POOL ~/p196_run/r13a/jobs_c3.txt 3 c3 > logs/pool_c3.out 2>&1
echo "$(date -u +%H:%M) chain3: tau-scan and R* 1000 done" >> NOTES.md
# appended 11:32: rotating-epoch L test (epoch T_rot) for all twisted bands of clock 1000 (T_rot <= 120), 3 workers
cd ~/p196_run/r13a
$PY genband.py L 1000 1 120 jobs_bLrotall1000.txt --rotepoch --timeout 150 --smax 8
$PY $POOL ~/p196_run/r13a/jobs_bLrotall1000.txt 3 bLrotall1000 > logs/pool_bLrotall1000.out 2>&1
echo "$(date -u +%H:%M) chain3: L(T_rot epoch) for clock 1000 done" >> NOTES.md
