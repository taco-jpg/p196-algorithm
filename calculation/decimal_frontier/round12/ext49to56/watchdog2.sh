#!/bin/bash
# r12e2 watchdog (= r12e watchdog.sh + protected pids): every 5 s, sum the RSS of all processes whose command line contains
# "r12e/bin/".  If one process exceeds PER_GB, kill it (protected or not).  If the sum exceeds TOT_GB, kill the largest process
# that is NOT protected (the two long single runs: the decisive attempt and the (p21)^2 confirmation), or the largest one if only
# protected processes are left.  Logs to logs/watchdog.log (same file).  Disk check as before.  Exits after IDLE_MAX s idle.
# usage: watchdog2.sh TOT_GB PER_GB IDLE_MAX "PID PID ..."
TOT_KB=$(( ${1:-80} * 1024 * 1024 )); PER_KB=$(( ${2:-45} * 1024 * 1024 )); IDLE_MAX=${3:-3600}; PROT=" ${4:-} "
LOG=~/p196_run/r12e/logs/watchdog.log; idle=0; n=0
echo "$(date -u +%FT%TZ) watchdog2 start pid=$$ tot=${1:-80}G per=${2:-45}G protected:${PROT}" >> $LOG
while true; do
  snap=$(ps -Ao pid=,rss=,command= | grep 'r12e/bin/' | grep -v grep)
  if [ -z "$snap" ]; then idle=$((idle+5)); [ $idle -ge $IDLE_MAX ] && { echo "$(date -u +%FT%TZ) watchdog2 idle exit" >> $LOG; exit 0; }; sleep 5; continue; fi
  idle=0
  tot=$(echo "$snap" | awk '{s+=$2} END{print s+0}')
  big=$(echo "$snap" | sort -k2 -nr | head -1); bpid=$(echo "$big" | awk '{print $1}'); brss=$(echo "$big" | awk '{print $2}')
  if [ "$brss" -gt $PER_KB ]; then
    kill $bpid 2>/dev/null; echo "$(date -u +%FT%TZ) KILL(per-process) pid=$bpid rss_kb=$brss total_kb=$tot :: $(echo "$big" | cut -c1-220)" >> $LOG
  elif [ "$tot" -gt $TOT_KB ]; then
    cand=$(echo "$snap" | sort -k2 -nr | awk -v P="$PROT" 'index(P, " " $1 " ") == 0' | head -1)
    [ -z "$cand" ] && cand=$big
    cpid=$(echo "$cand" | awk '{print $1}'); crss=$(echo "$cand" | awk '{print $2}')
    kill $cpid 2>/dev/null; echo "$(date -u +%FT%TZ) KILL(total) pid=$cpid rss_kb=$crss total_kb=$tot :: $(echo "$cand" | cut -c1-220)" >> $LOG
  fi
  n=$((n+1))
  if [ $((n % 120)) -eq 0 ]; then
    cap=$(df -k ~ | tail -1 | awk '{print $5}' | tr -d '%')
    echo "$(date -u +%FT%TZ) status total_rss_gb=$((tot/1024/1024)) nproc=$(echo "$snap" | wc -l | tr -d ' ') disk_used=${cap}%" >> $LOG
    [ "$cap" -gt 85 ] && echo "$(date -u +%FT%TZ) WARNING disk used ${cap}% > 85%" >> $LOG
  fi
  sleep 5
done
