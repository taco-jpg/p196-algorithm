#!/bin/bash
# resume the all-phase windowed M1_P48 backward run whenever the disk has room (r6 heavy tasks come and go); stops on a final RESULT
cd ~/p196_run/r7
BD=~/p196_run/bands/backdisk
while true; do
  if grep -qE "^RESULT (REACHABLE|UNREACHABLE)|^RESULT TOO_BIG at layer [0-9]+: [0-9]+ states" logs/M1_P48_winphase8.log; then break; fi
  free=$(df -k /System/Volumes/Data | awk "NR==2{printf \"%d\", 100-\$5}")
  if [ "$free" -ge 28 ]; then
    WIN=8 ROT=1 THREADS=12 nice -n 10 $BD 10 48 0001 wd_wp8_48 4000000000 0.20 $(python3 specs.py 48) >> logs/M1_P48_winphase8.log 2>&1
  fi
  sleep 300
done
echo "resume loop ended $(date -u)" >> logs/M1_P48_winphase8.log
