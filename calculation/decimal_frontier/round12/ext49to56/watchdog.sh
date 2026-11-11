#!/bin/bash
# r12e watchdog: every 5 s, sum the RSS of all processes whose command line contains "r12e/bin/" (all r12e compute binaries
# are started with that path).  If one process exceeds PER_GB or the sum exceeds TOT_GB, kill the largest one (logged).
# Also logs a warning if the data volume has < 15% free.  Exits after IDLE_MAX seconds without any r12e process.
# usage: watchdog.sh [TOT_GB=80] [PER_GB=45] [IDLE_MAX=3600]
TOT_KB=$(( ${1:-80} * 1024 * 1024 )); PER_KB=$(( ${2:-45} * 1024 * 1024 )); IDLE_MAX=${3:-3600}
LOG=~/p196_run/r12e/logs/watchdog.log; idle=0; n=0
echo "$(date -u +%FT%TZ) watchdog start pid=$$ tot=${1:-80}G per=${2:-45}G" >> $LOG
while true; do
  snap=$(ps -Ao pid=,rss=,command= | grep 'r12e/bin/' | grep -v grep)
  if [ -z "$snap" ]; then idle=$((idle+5)); [ $idle -ge $IDLE_MAX ] && { echo "$(date -u +%FT%TZ) watchdog idle exit" >> $LOG; exit 0; }; sleep 5; continue; fi
  idle=0
  tot=$(echo "$snap" | awk '{s+=$2} END{print s+0}')
  big=$(echo "$snap" | sort -k2 -nr | head -1)
  bpid=$(echo "$big" | awk '{print $1}'); brss=$(echo "$big" | awk '{print $2}')
  if [ "$brss" -gt $PER_KB ] || [ "$tot" -gt $TOT_KB ]; then
    kill $bpid 2>/dev/null; echo "$(date -u +%FT%TZ) KILL pid=$bpid rss_kb=$brss total_kb=$tot :: $(echo "$big" | cut -c1-220)" >> $LOG
  fi
  n=$((n+1))
  if [ $((n % 120)) -eq 0 ]; then
    cap=$(df -k ~ | tail -1 | awk '{print $5}' | tr -d '%')
    echo "$(date -u +%FT%TZ) status total_rss_gb=$((tot/1024/1024)) nproc=$(echo "$snap" | wc -l | tr -d ' ') disk_used=${cap}%" >> $LOG
    [ "$cap" -gt 85 ] && echo "$(date -u +%FT%TZ) WARNING disk used ${cap}% > 85%" >> $LOG
  fi
  sleep 5
done
