#!/bin/bash
# watch.sh LOG RSS_GB MAX_SEC STOP_REGEX -- cmd...   : runs cmd (stdout+stderr >> LOG), kills it if RSS > RSS_GB, time > MAX_SEC, or LOG matches STOP_REGEX
LOG=$1; LIM=$2; MAXS=$3; STOP=$4; shift 5
"$@" >> "$LOG" 2>&1 &
P=$!; t0=$(date +%s)
while kill -0 $P 2>/dev/null; do
  sleep 10
  r=$(ps -o rss= -p $P 2>/dev/null | tr -d " "); r=${r:-0}
  if [ $r -gt $((LIM*1048576)) ]; then echo "WATCHDOG: RSS ${r}KB > ${LIM}GB, killed $(date -u)" >> "$LOG"; kill $P; fi
  if [ $(( $(date +%s) - t0 )) -gt $MAXS ]; then echo "WATCHDOG: time limit ${MAXS}s, killed $(date -u)" >> "$LOG"; kill $P; fi
  if [ -n "$STOP" ] && grep -qE "$STOP" "$LOG"; then echo "WATCHDOG: stop pattern reached, killed $(date -u)" >> "$LOG"; kill $P; fi
done
wait $P; echo "watch exit $? $(date -u)" >> "$LOG"
