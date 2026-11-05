#!/bin/bash
# r11d: like studio/run_stage.sh but with py/census_b.py, bin/bxb (wire + uniform-band acceptance), DB dir out/dbB, lists dir LISTS.
# usage: studio/run_stage_b.sh NAME "P1 P2 ..." CAP SEC LISTS [NSHARD=6]
set -u
cd "$(dirname "$0")/.."
NAME=$1; PS=$2; CAP=$3; SEC=$4; LISTS=$5; N=${6:-6}
BANDS="6,12;2,4,8,16,14,10;0;18"
DBDIR=${DBDIR:-out/dbB}
mkdir -p out/studioB logs $DBDIR
for p in $PS; do
  DBP=$DBDIR/b10_p${p}.jsonl; touch $DBP
  echo "== $(date +%T) stageB $NAME p=$p cap=$CAP sec=$SEC lists=$LISTS shards=$N bands=$BANDS"
  for ((i=0;i<N;i++)); do
    nice -n 10 python3 py/census_b.py 10 $p --cap $CAP --sec $SEC --bx bin/bxb --lists $LISTS --extra "-band $BANDS" --seed $DBP \
        --db out/studioB/${NAME}_p${p}_s${i}.jsonl --shard $i/$N > logs/B_${NAME}_p${p}_s${i}.log 2>&1 &
  done
  wait
  python3 py/merge_db.py $DBP $DBP out/studioB/${NAME}_p${p}_s*.jsonl
  python3 py/check_accepts.py $DBP | grep -E "NEW|accepted streams"
  python3 py/summarize.py 10 --files $DBP 2>/dev/null | sed -n 2,3p
  python3 -c "
import json,sys
n=0
for l in open('$DBP'):
    r=json.loads(l)
    if r.get('band'): n+=1; print('BANDHIT',r['g'],r['status'],r['band'])
print('band hits:',n)"
done
echo "== done $(date +%T)"
