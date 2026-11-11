#!/bin/bash
# chainZ (3-worker slot, replaces chains 5/6/8/9/10): after chain3's rot-epoch stage: centre sweeps N<=24; deep seam T=24 survivors Lj<=12; seam Nmul=2 for T<=12; R* clocks 10/p11; tau-scan T<=36.
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
dl() { date -j -u -f "%Y-%m-%d %H:%M" "2026-11-08 $1" +%s; }
until grep -q "chain3: L(T_rot epoch) for clock 1000 done" NOTES.md; do sleep 20; done
$PY gencentre.py 1000 24 6 jobs_centre1000b.txt --timeout 40 --budget 120
DEADLINE=$(dl 14:10) $PY $POOL ~/p196_run/r13a/jobs_centre1000b.txt 3 centre1000 > logs/pool_centre1000.out 2>&1
echo "$(date -u +%H:%M) chainZ: centre sweeps clock 1000 (N<=24) done" >> NOTES.md
# deep seam for T=24 survivors (no ALLUNSAT in L/R/R*)
$PY status_gen.py > /dev/null 2>&1
$PY - <<'PY2' > bands_T24surv.txt
import re
txt=open('~/p196_run/r13a/FINAL_status_auto.md').read()
m=re.search(r'clock 1000: \d+ survivors: (.*)\n',txt)
for it in m.group(1).split('; '):
    mm=re.match(r'\(([\d,]+)\) s=(\d+) T=(\d+) ',it.strip())
    if mm and int(mm.group(3))==24: print(mm.group(1))
PY2
wc -l bands_T24surv.txt
$PY genseam.py 1000 5,18,4,8,1,15,4,0,5 12 24 12 jobs_seam1000c.txt --timeout 60 --budget 240 --maxlcm 24
grep -F -f bands_T24surv.txt jobs_seam1000c.txt > jobs_seam1000c2.txt; wc -l jobs_seam1000c2.txt
# deeper: start at Lj=9 (Lj<=8 already covered)
sed -i '' 's/--Lmax 12/--Lmin 9 --Lmax 12/' jobs_seam1000c2.txt
DEADLINE=$(dl 14:22) $PY $POOL ~/p196_run/r13a/jobs_seam1000c2.txt 3 seam1000c > logs/pool_seam1000c.out 2>&1
echo "$(date -u +%H:%M) chainZ: deep seam T=24 survivors (Lj 9-12) done" >> NOTES.md
# seam at N=24 for T<=12 bands (Nmul=2), Lj<=6
grep -e "--Nmul 2" jobs_seam1000Nmul.txt > jobs_seam1000N2.txt
DEADLINE=$(dl 14:30) $PY $POOL ~/p196_run/r13a/jobs_seam1000N2.txt 3 seam1000N > logs/pool_seam1000N.out 2>&1
echo "$(date -u +%H:%M) chainZ: seam N=24 for T<=12 bands done" >> NOTES.md
# R* for clocks 10/p11 (bands R-PASS), T'<=36
grep -h "BANDRESULT R b=10 clock=10 " logs/bRresta/i*.log | grep "status=PASS" | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Rpass10.txt
grep -h "BANDRESULT R b=10 clock=00001110001 " logs/bRresta/i*.log | grep "status=PASS" | sed 's/.* V=\([0-9,]*\) .*/\1/' | sort -u > bands_Rpassp11.txt
$PY genband.py R 10 1 36 jobs_bRs10.txt --minM --comoving --timeout 100 --bands bands_Rpass10.txt --smax 8
$PY genband.py R 00001110001 1 36 jobs_bRsp11.txt --minM --comoving --timeout 100 --bands bands_Rpassp11.txt --smax 8
cat jobs_bRs10.txt jobs_bRsp11.txt > jobs_bRsrest.txt
DEADLINE=$(dl 14:40) $PY $POOL ~/p196_run/r13a/jobs_bRsrest.txt 3 bRsrest > logs/pool_bRsrest.out 2>&1
echo "$(date -u +%H:%M) chainZ: R* clocks 10/p11 T'<=36 done" >> NOTES.md
