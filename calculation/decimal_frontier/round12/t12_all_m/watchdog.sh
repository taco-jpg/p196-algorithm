#!/bin/bash
# r12f watchdog: sums RSS of every process whose command line contains "p196_run/r12f" (all r12f jobs are started
# with absolute paths under ~/p196_run/r12f).  If the sum exceeds LIMIT_KB (default 50 GB) it kills the largest
# job (python/solver process, never a pool script) and logs it.  Also logs a warning if more than 6 workers run.
# Exits when ~/p196_run/r12f/STOP_WATCHDOG exists or no r12f worker has run for 30 min.
LIMIT_KB=${LIMIT_KB:-50000000}
LOG=~/p196_run/r12f/logs/watchdog.log
idle=0
echo "$(date -u +%FT%TZ) watchdog start limit=${LIMIT_KB}KB pid=$$" >> $LOG
while [ ! -e ~/p196_run/r12f/STOP_WATCHDOG ]; do
  tot=$(ps -axo rss=,command= | grep "p196_run/r12f" | grep -v -e grep -e watchdog.sh | awk '{s+=$1} END {print s+0}')
  n=$(ps -axo pid=,command= | grep "p196_run/r12f" | grep -v -e grep -e watchdog -e "/usr/bin/time" -e "nice -n" -e xargs -e bash | wc -l | tr -d ' ')
  if [ "$n" -eq 0 ]; then idle=$((idle+1)); else idle=0; fi
  if [ $idle -ge 90 ]; then echo "$(date -u +%FT%TZ) idle 30min, exit" >> $LOG; exit 0; fi
  if [ "$n" -gt 6 ]; then echo "$(date -u +%FT%TZ) WARNING $n workers running" >> $LOG; fi
  if [ "$tot" -gt "$LIMIT_KB" ]; then
    victim=$(ps -axo pid=,rss=,command= | grep "p196_run/r12f" | grep -v -e grep -e watchdog -e "/usr/bin/time" -e "nice -n" -e xargs -e bash | sort -k2 -n -r | head -1)
    vpid=$(echo $victim | awk '{print $1}')
    echo "$(date -u +%FT%TZ) total_rss_kb=$tot > $LIMIT_KB: kill $victim" >> $LOG
    [ -n "$vpid" ] && kill -9 $vpid
  fi
  sleep 20
done
echo "$(date -u +%FT%TZ) STOP file, exit" >> $LOG
