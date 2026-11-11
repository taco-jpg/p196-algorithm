#!/bin/bash
# second pipeline (indep_scc, r13b rule + Kosaraju + genuine-addition fold) versus bin_mc14a runscc on sample lattices
cd ~/p196_run/r14a || exit 1
mkdir -p ctrl rows
# rows format: "Pp NB MM BS" header + same body
conv() { awk 'NR==1{print $2,$3,$4,$1; next} {print}' "$1" > "$2"; }
for L in 64_0 61_0 102_0 118_0 133_0; do conv latw/w$L.txt rows/w$L.rows; done
THR=${1:-8}
for job in "61_0 0" "61_0 1" "102_0 0" "102_0 3" "64_0 0" "118_0 0"; do
  set -- $job; w=$1; o=$2
  echo "== $w orbit $o $(date -u +%T)"
  ./bin_indep_scc rows/w$w.rows $o 1 45 ctrl/indep_$w $THR > ctrl/indep_w${w}_o$o.log 2>&1
  python3 - "$w" "$o" <<'PY'
import re,sys
w,o=sys.argv[1],sys.argv[2]
import glob,json
# find class id for this word
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
ok=True; bad=None
for k in sorted(ref):
    if k not in mine:
        print('K',k,'missing in indep'); ok=False; bad=k; break
    if ref[k]!=mine[k]:
        print('MISMATCH K',k,ref[k],mine[k]); ok=False; bad=k; break
print(f'class {cid} w{w} orbit {o}: {"ALL LEVELS EQUAL" if ok else "DIFFERENT"} levels compared {sorted(ref)[:1]}..{sorted(ref)[-1:]}, last ref {ref[max(ref)]}, indep has {sorted(mine)[-1:] if mine else None}')
PY
done
echo done
