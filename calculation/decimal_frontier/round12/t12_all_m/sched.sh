#!/bin/bash
# r12f scheduler: starts the first not-yet-started line of queue.txt (run1.sh format: enc mode U R m solver outdir)
# whenever fewer than MAXW r12f worker processes run.  queue.txt is re-read every time (may be edited on the fly);
# a job counts as started when its log file exists (run1.sh naming).  Exit: STOP_SCHED file.
MAXW=${MAXW:-6}; MAXKB=${MAXKB:-45000000}; Q=~/p196_run/r12f/queue.txt; LOG=~/p196_run/r12f/logs/sched.log
# optional 8th field of a queue line: estimated peak RSS in GB (default 6); a job starts only if current r12f RSS + estimate <= MAXKB
cd ~/p196_run/r12f
echo "$(date) sched start MAXW=$MAXW pid=$$" >> $LOG
while [ ! -e ~/p196_run/r12f/STOP_SCHED ]; do
  n1=$(ps -axo pid=,command= | grep "p196_run/r12f" | grep -v -e grep -e watchdog -e "/usr/bin/time" -e "nice -n" -e xargs -e bash | wc -l | tr -d ' ')
  n2=$(ps -axo pid=,command= | grep "r12f/run1.sh" | grep -v grep | wc -l | tr -d ' ')
  n=$(( n1 > n2 ? n1 : n2 ))   # one run1.sh per job: counts jobs whose python has not started yet
  if [ "$n" -lt "$MAXW" ]; then
    line=""
    while read -r l; do
      [ -z "$l" ] && continue
      case "$l" in \#*) continue;; esac
      set -- $l
      f=$7/${1}_${2}_U${3}_r${4}_m${5}_${6}.log
      [ -e "$f" ] && continue
      est=${8:-6}
      tot=$(ps -axo rss=,command= | grep "p196_run/r12f" | grep -v -e grep -e watchdog.sh | awk '{s+=$1} END {print s+0}')
      if [ $((tot + est * 1000000)) -gt $MAXKB ]; then line="WAIT"; break; fi
      line="$l"; break
    done < $Q
    if [ -z "$line" ]; then sleep 30; continue; fi
    if [ "$line" = "WAIT" ]; then sleep 20; continue; fi
    echo "$(date +%T) start: $line (workers before: $n)" >> $LOG
    set -- $line
    nohup ~/p196_run/r12f/run1.sh $1 $2 $3 $4 $5 $6 $7 > /dev/null 2>&1 < /dev/null &
    set -- $line; sleep $((30 + 3 * ${8:-6}))
  else
    sleep 15
  fi
done
echo "$(date) STOP_SCHED, exit" >> $LOG
