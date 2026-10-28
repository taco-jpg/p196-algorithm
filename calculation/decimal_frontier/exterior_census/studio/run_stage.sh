#!/bin/bash
# usage: studio/run_stage.sh NAME "P1 P2 ..." CAP SEC [BX=bin/bx] [NSHARD=16] [GMIN=0] [GMAX=999]
#   For each p: NSHARD parallel shards of  py/census.py  (nice 19), each shard writing its OWN file out/studio/NAME_p<p>_s<i>.jsonl and reading the
#   per-p database out/db/b10_p<p>.jsonl as read-only seed (decisive words are skipped; capped words are retried only if CAP is larger than their old cap).
#   Words are processed smallest G first (shard i takes every NSHARD-th word of that order).  When the shards of a p are done they are merged into
#   out/db/b10_p<p>.jsonl (atomic replace), accepted streams are classified (py/check_accepts.py) and a funnel line is printed.
#   Memory per process is set by CAP (macOS ignores ulimit -v):  bx (16 B/key): CAP 3M -> 0.13 GB, 12M -> 0.5 GB, 48M -> 2.1 GB, 120M -> 4.3 GB (+50% while the table doubles)
#                                                                bx3 (24 B/key): CAP 3M -> 0.2 GB, 48M -> 3.2 GB, 100M -> 6.4 GB
#   bx supports p<=32 (use BX=bin/bx3 for p>=33).   Env DBDIR overrides out/db.
set -u
cd "$(dirname "$0")/.."
NAME=$1; PS=$2; CAP=$3; SEC=$4; BX=${5:-bin/bx}; N=${6:-16}; GMIN=${7:-0}; GMAX=${8:-999}
DBDIR=${DBDIR:-out/db}
mkdir -p out/studio logs $DBDIR
for p in $PS; do
  DBP=$DBDIR/b10_p${p}.jsonl; touch $DBP
  echo "== $(date +%T) stage $NAME p=$p cap=$CAP sec=$SEC bx=$BX shards=$N G=[$GMIN,$GMAX]"
  for ((i=0;i<N;i++)); do
    nice -n 19 python3 py/census.py 10 $p --cap $CAP --sec $SEC --bx $BX --seed $DBP \
        --db out/studio/${NAME}_p${p}_s${i}.jsonl --shard $i/$N --gmin $GMIN --gmax $GMAX \
        > logs/studio_${NAME}_p${p}_s${i}.log 2>&1 &
  done
  wait
  python3 py/merge_db.py $DBP $DBP out/studio/${NAME}_p${p}_s*.jsonl
  python3 py/check_accepts.py $DBP | grep -E "NEW|accepted streams"
  python3 py/summarize.py 10 --files $DBP | sed -n 2,3p
done
echo "== done $(date +%T)"
