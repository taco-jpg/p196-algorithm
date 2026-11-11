#!/bin/bash
# chain7: after chain4: seam sweeps for clock 10 against the p8 lattice exteriors rec0/rec1/rec2 (E rows from p8_scc.txt), T<=16, Lj<=8
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chain4: done" NOTES.md; do sleep 30; done
$PY - <<'PY2'
import json
d=json.load(open('~/p196_run/r13a/ctrl/p8_bands.json'))
for i,x in enumerate(d):
    open(f'~/p196_run/r13a/ctrl/E_p8_{i}.txt','w').write(','.join(map(str,x['V0'])))
PY2
for i in 0 1 2; do
 E=$(cat ctrl/E_p8_$i.txt)
 $PY genseam.py 10 $E 8 16 8 jobs_seam10_$i.txt --timeout 40 --budget 200 --maxlcm 48
done
cat jobs_seam10_0.txt jobs_seam10_1.txt jobs_seam10_2.txt > jobs_seam10.txt
$PY $POOL ~/p196_run/r13a/jobs_seam10.txt 5 seam10 > logs/pool_seam10.out 2>&1
echo "$(date -u +%H:%M) chain7: seam sweep clock 10 done" >> NOTES.md
