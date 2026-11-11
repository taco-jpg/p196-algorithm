#!/bin/bash
# r12b watchdog: every 5 s, sum RSS of all processes whose command line contains "r12b/bin/" (all r12b compute binaries are
# started with that path).  If one process exceeds PER_KB or the sum exceeds TOT_KB, kill the largest one (logged).
# Exits after IDLE_MAX seconds without any r12b process.   usage: watchdog.sh [TOT_GB=85] [PER_GB=40] [IDLE_MAX=1800]
TOT_KB=$(( ${1:-85} * 1024 * 1024 )); PER_KB=$(( ${2:-40} * 1024 * 1024 )); IDLE_MAX=${3:-1800}
LOG=~/p196_run/r12b/logs/watchdog.log; idle=0
echo "$(date -u +%FT%TZ) watchdog start pid=$$ tot=${1:-85}G per=${2:-40}G" >> $LOG
while true; do
  snap=$(ps -Ao pid=,rss=,command= | grep 'r12b/bin/' | grep -v grep)
  if [ -z "$snap" ]; then idle=$((idle+5)); [ $idle -ge $IDLE_MAX ] && { echo "$(date -u +%FT%TZ) watchdog idle exit" >> $LOG; exit 0; }; sleep 5; continue; fi
  idle=0
  tot=$(echo "$snap" | awk '{s+=$2} END{print s+0}')
  big=$(echo "$snap" | sort -k2 -nr | head -1)
  bpid=$(echo "$big" | awk '{print $1}'); brss=$(echo "$big" | awk '{print $2}')
  if [ "$brss" -gt $PER_KB ] || [ "$tot" -gt $TOT_KB ]; then
    kill $bpid 2>/dev/null; echo "$(date -u +%FT%TZ) KILL pid=$bpid rss_kb=$brss total_kb=$tot :: $(echo "$big" | cut -c1-200)" >> $LOG
  fi
  sleep 5
done
