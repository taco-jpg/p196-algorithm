#!/bin/bash
# chain9 (3-worker slot, after chain8): tau-scan for 24<T<=36 (clock 1000), then xchk of new ALLUNSAT results
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
POOL=~/p196_run/r13a/pool.py
until grep -q "chain8: seam N-multiple" NOTES.md; do sleep 30; done
$PY gentau.py 1000 36 jobs_tau1000b.txt --timeout 60
$PY - <<'PY2'
import re
lines=[l for l in open('jobs_tau1000b.txt')]
keep=[l for l in lines if int(re.search(r'--T (\d+)',l).group(1))>24]
open('jobs_tau1000b.txt','w').writelines(keep)
print(len(keep))
PY2
$PY $POOL ~/p196_run/r13a/jobs_tau1000b.txt 3 tau1000b > logs/pool_tau1000b.out 2>&1
echo "$(date -u +%H:%M) chain9: tau-scan 24<T<=36 done" >> NOTES.md
