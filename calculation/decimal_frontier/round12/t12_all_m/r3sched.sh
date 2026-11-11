#!/bin/bash
# r12f3 scheduler.  Queue r3queue.txt, one job per line: "<logpath> <estGB> <cmd args...>" (# = comment).
# Starts the first line whose log does not exist when fewer than MAXW r12f solver processes run and
# current r12f RSS + estimate <= MAXKB.  Re-reads the queue each time.  Stop: touch STOP_R3SCHED.
MAXW=${MAXW:-6}; MAXKB=${MAXKB:-46000000}; Q=~/p196_run/r12f/r3queue.txt; LOG=~/p196_run/r12f/r3/sched.log
echo "$(date -u +%FT%TZ) r3sched start MAXW=$MAXW MAXKB=$MAXKB pid=$$" >> $LOG
while [ ! -e ~/p196_run/r12f/STOP_R3SCHED ]; do
  n1=$(ps -axo pid=,command= | grep "p196_run/r12f" | grep -v -e grep -e watchdog -e "/usr/bin/time" -e "nice -n" -e xargs -e bash | wc -l | tr -d " ")
  n2=$(ps -axo pid=,command= | grep "r12f/r3run.sh" | grep -v grep | wc -l | tr -d " ")
  n=$(( n1 > n2 ? n1 : n2 ))
  if [ "$n" -lt "$MAXW" ]; then
    line=""
    while read -r l; do
      [ -z "$l" ] && continue
      case "$l" in \#*) continue;; esac
      set -- $l
      [ -e "$1" ] && continue
      tot=$(ps -axo rss=,command= | grep "p196_run/r12f" | grep -v -e grep -e watchdog.sh | awk "{s+=\$1} END {print s+0}")
      if [ $((tot + $2 * 1000000)) -gt $MAXKB ]; then line="WAIT"; break; fi
      line="$l"; break
    done < $Q
    if [ -z "$line" ]; then sleep 30; continue; fi
    if [ "$line" = "WAIT" ]; then sleep 20; continue; fi
    set -- $line; f=$1; est=$2; shift 2
    echo "$(date -u +%FT%TZ) start $f est=${est}GB workers_before=$n" >> $LOG
    nohup ~/p196_run/r12f/r3run.sh $f "$@" > /dev/null 2>&1 < /dev/null &
    sleep $((20 + 2 * est))
  else
    sleep 15
  fi
done
echo "$(date -u +%FT%TZ) STOP_R3SCHED, exit" >> $LOG
