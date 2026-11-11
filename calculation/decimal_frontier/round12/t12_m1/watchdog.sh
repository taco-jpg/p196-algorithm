#!/bin/bash
# r12a watchdog: sums RSS of every process whose command line contains "r12a"
# (all r12a jobs are started with absolute paths under ~/p196_run/r12a).
# If the sum exceeds LIMIT_KB, kills the most recently started heavy job and logs it.
# Exits when ~/p196_run/r12a/STOP_WATCHDOG exists or no r12a job has run for 15 min.
LIMIT_KB=${LIMIT_KB:-60000000}
LOG=~/p196_run/r12a/logs/watchdog.log
idle=0
echo "$(date -u +%FT%TZ) watchdog start limit=${LIMIT_KB}KB pid=$$" >> $LOG
while [ ! -e ~/p196_run/r12a/STOP_WATCHDOG ]; do
  tot=$(ps -axo rss=,command= | grep "p196_run/r12a" | grep -v -e grep -e watchdog.sh | awk "{s+=\$1} END {print s+0}")
  n=$(ps -axo pid=,command= | grep "p196_run/r12a" | grep -e python -e "/r12a/bin/" | grep -v -e grep -e watchdog.sh | wc -l)
  if [ "$n" -eq 0 ]; then idle=$((idle+1)); else idle=0; fi
  if [ $idle -ge 45 ]; then echo "$(date -u +%FT%TZ) idle 15min, exit" >> $LOG; exit 0; fi
  if [ "$tot" -gt "$LIMIT_KB" ]; then
    victim=$(ps -axo pid=,rss=,command= | grep "p196_run/r12a" | grep -e python -e "/r12a/bin/" | grep -v -e grep -e watchdog.sh -e pool | sort -k2 -n -r | head -1)
    vpid=$(echo $victim | awk "{print \$1}")
    echo "$(date -u +%FT%TZ) total_rss_kb=$tot > $LIMIT_KB: kill $victim" >> $LOG
    [ -n "$vpid" ] && kill -9 $vpid
  fi
  sleep 20
done
echo "$(date -u +%FT%TZ) STOP file, exit" >> $LOG
