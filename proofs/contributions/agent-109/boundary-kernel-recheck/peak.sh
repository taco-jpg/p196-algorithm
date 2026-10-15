#!/usr/bin/env bash
# usage: peak.sh file.lean  -> runs lean with 6GB cap, reports peak RSS (VmHWM)
f=$1; start=$(date +%s)
( ulimit -v 6000000; exec env LEAN_PATH=. lean "$f" ) > peak.out 2>&1 &
pid=$!; hwm=0
while kill -0 $pid 2>/dev/null; do v=$(grep VmHWM /proc/$pid/status 2>/dev/null | awk '{print $2}'); [ -n "$v" ] && hwm=$v; sleep 0.5; done
wait $pid; rc=$?
echo "$f rc=$rc peakRSS=$((hwm/1024))MB $(( $(date +%s)-start ))s $(tail -c 200 peak.out | tr '\n' ' ')"
