#!/bin/bash
# runq.sh QUEUEFILE WORKERS : sequential queue of parallel shard jobs.
# Each line of QUEUEFILE: TAG S0 S1 ... (ignored)  format:  TAG|NSHARDS|command with {S}
# Lines starting with # are skipped. Waits for each batch to finish before starting the next. Logs to logs/runq.log.
Q=$1; LOG=~/p196_run/r13c/logs/runq.log
BASE=~/p196_run/r13c
while IFS= read -r line; do
  case "$line" in \#*|"") continue;; esac
  TAG=$(echo "$line" | cut -d'|' -f1); NS=$(echo "$line" | cut -d'|' -f2); CMD=$(echo "$line" | cut -d'|' -f3-)
  mkdir -p $BASE/out/$TAG
  echo "$(date -u +%FT%TZ) START $TAG shards=$NS" >> $LOG
  pids=""
  for ((s=0; s<NS; s++)); do
    c=$(echo "$CMD" | sed "s/{S}/$s/g; s/{N}/$NS/g")
    nohup nice -n 10 bash -c "$c" > $BASE/out/$TAG/s$s.out 2>&1 < /dev/null &
    pids="$pids $!"
  done
  for p in $pids; do wait $p; done
  echo "$(date -u +%FT%TZ) DONE $TAG" >> $LOG
done < "$Q"
echo "$(date -u +%FT%TZ) QUEUE_END $Q" >> $LOG
