#!/bin/bash
# sequential launcher: starts the next queued command when fewer than 8 of my processes run (budget 8 threads); not a scheduler/cron, ends when the queue is empty
cd ~/p196_run/r14c
Q=scripts/queue.txt; idx=0
n=$(wc -l < $Q)
while [ $idx -lt $n ]; do
  running=$(ps -axo command= | grep -cE "^bin/(ifb|ifc|ifd|ifw|khr)")
  # also count the waiter-launched N60_1 run as running via the same pattern
  if [ "$running" -lt 8 ]; then
    idx=$((idx+1)); cmd=$(sed -n "${idx}p" $Q)
    echo "$(date -u +%H:%M:%S) launch $idx: $cmd" >> logs/slot_runner.log
    nohup bash -c "$cmd" > /dev/null 2>&1 &
    sleep 30
  else
    sleep 60
  fi
done
echo "$(date -u +%H:%M:%S) queue done" >> logs/slot_runner.log
