#!/bin/bash
# chainZ2 (3-worker slot): after the running centre pool (deadline 14:10): xchk of all ALLUNSAT -> deep seam T=24 survivors -> seam N=24 for T<=12 -> R* 10/p11 -> seam cadical cross-check
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
dl() { date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 $1" +%s; }
while pgrep -f "pool.py ~/p196_run/r13a/jobs_centre1000b.txt" > /dev/null; do sleep 15; done
echo "$(date -u +%H:%M) chainZ2: centre sweeps stage finished ($(wc -l < logs/centre1000/done.txt) jobs); starting xchk of ALLUNSAT" >> NOTES.md
$PY genxchk.py jobs_xchk6.txt > logs/genxchk6.out 2>&1
DEADLINE=$(dl 14:26) $PY $POOL ~/p196_run/r13a/jobs_xchk6.txt 3 xchk6 > logs/pool_xchk6.out 2>&1
echo "$(date -u +%H:%M) chainZ2: xchk6 done" >> NOTES.md
# deep seam for T=24 survivors
$PY status_gen.py > /dev/null 2>&1
$PY - <<'PY2' > bands_T24surv.txt
import re
txt=open('~/p196_run/r13a/FINAL_status_auto.md').read()
m=re.search(r'clock 1000: \d+ survivors: (.*)\n',txt)
for it in m.group(1).split('; '):
    mm=re.match(r'\(([\d,]+)\) s=(\d+) T=(\d+) ',it.strip())
    if mm and int(mm.group(3))==24: print(mm.group(1))
PY2
$PY genseam.py 1000 5,18,4,8,1,15,4,0,5 12 24 12 jobs_seam1000c.txt --timeout 60 --budget 200 --maxlcm 24
grep -F -f bands_T24surv.txt jobs_seam1000c.txt > jobs_seam1000c2.txt
sed -i '' 's/--Lmax 12/--Lmin 9 --Lmax 12/' jobs_seam1000c2.txt
echo "$(date -u +%H:%M) chainZ2: deep seam jobs: $(wc -l < jobs_seam1000c2.txt)" >> NOTES.md
DEADLINE=$(dl 14:38) $PY $POOL ~/p196_run/r13a/jobs_seam1000c2.txt 3 seam1000c > logs/pool_seam1000c.out 2>&1
echo "$(date -u +%H:%M) chainZ2: deep seam T=24 survivors done" >> NOTES.md
grep -h "BANDRESULT R b=10 clock=10 " logs/bRresta/i*.log | grep "status=PASS" | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Rpass10.txt
grep -h "BANDRESULT R b=10 clock=00001110001 " logs/bRresta/i*.log | grep "status=PASS" | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Rpassp11.txt
$PY genband.py R 10 1 36 jobs_bRs10.txt --minM --comoving --timeout 100 --bands bands_Rpass10.txt --smax 8
$PY genband.py R 00001110001 1 36 jobs_bRsp11.txt --minM --comoving --timeout 100 --bands bands_Rpassp11.txt --smax 8
cat jobs_bRs10.txt jobs_bRsp11.txt > jobs_bRsrest.txt
DEADLINE=$(dl 14:47) $PY $POOL ~/p196_run/r13a/jobs_bRsrest.txt 3 bRsrest > logs/pool_bRsrest.out 2>&1
echo "$(date -u +%H:%M) chainZ2: R* clocks 10/p11 done" >> NOTES.md
