#!/bin/bash
# master.sh: sequential stages, each started when <= LOWLOAD r13c bin processes are running; nice 10; absolute paths.
# usage: master.sh STAGEFILE LOWLOAD
SF=$1; LOW=${2:-2}
R=~/p196_run/r13c
note(){ echo "- $(date -u +%FT%TZ) MASTER: $*" >> $R/NOTES.md; }
while IFS= read -r line; do
  case "$line" in \#*|"") continue;; esac
  TAG=$(echo "$line" | cut -d'|' -f1); NS=$(echo "$line" | cut -d'|' -f2); CMD=$(echo "$line" | cut -d'|' -f3-)
  # wait for low load
  while [ "$(pgrep -f '[/]p196_run/r13c/bin/' | wc -l | tr -d ' ')" -gt "$LOW" ]; do sleep 20; done
  mkdir -p $R/out/$TAG; note "START $TAG shards=$NS"
  pids=""
  for ((s=0;s<NS;s++)); do c=$(echo "$CMD" | sed "s/{S}/$s/g; s/{N}/$NS/g"); nohup nice -n 10 bash -c "$c" > $R/out/$TAG/s$s.out 2>&1 < /dev/null & pids="$pids $!"; done
  for p in $pids; do wait $p; done
  note "DONE $TAG"
  (cd $R; python3 py/collect.py $TAG >> out/collect_log.md 2>&1)
done < "$SF"
note "MASTER_END $SF"
