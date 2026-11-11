#!/bin/bash
# one comparison job: indep_scc vs bin_mc14a runscc log; usage: ctrl_indep2.sh WORD ORBIT THREADS
cd ~/p196_run/r14a || exit 1
w=$1; o=$2; thr=${3:-2}
mkdir -p ctrl rows
echo "== $w orbit $o threads $thr $(date -u +%T)"
./bin_indep_scc rows/w$w.rows $o 1 45 ctrl/indep_$w $thr > ctrl/indep_w${w}_o$o.log 2>&1
python3 - "$w" "$o" <<'PY'
import re,sys,json
w,o=sys.argv[1],sys.argv[2]
t=json.load(open('class/classes.json'))
cid=None
for r in t:
    if r['rep'].endswith('w'+w+'.txt'): cid=r['id']
log=f'logs/sw_scc_c{cid}_o{o}.log'
ref={}
for l in open(log):
    if l.startswith('K '):
        p=l.split(); ref[int(p[1])]=(int(p[3]),int(p[5]),int(p[9]))
mine={}
for l in open(f'ctrl/indep_w{w}_o{o}.log'):
    m=re.search(r'K=(\d+) .*E_acc=(\d+) acceptingInEacc=(\d+) exactOrbits=(\d+)',l)
    if m: mine[int(m.group(1))]=(int(m.group(2)),int(m.group(3)),int(m.group(4)))
ok=True
for k in sorted(ref):
    if k not in mine:
        print('K',k,'missing in indep'); ok=False; break
    if ref[k]!=mine[k]:
        print('MISMATCH K',k,ref[k],mine[k]); ok=False; break
print(f'class {cid} w{w} orbit {o}: {"ALL LEVELS EQUAL" if ok else "DIFFERENT"} levels compared {sorted(ref)[:1]}..{sorted(ref)[-1:]}, last ref {ref[max(ref)]}, indep last {sorted(mine)[-1:] if mine else None}')
PY
