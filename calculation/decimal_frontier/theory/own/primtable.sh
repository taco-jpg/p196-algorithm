#!/bin/bash
PM=$1; B1=$2; B2=$3
for b in $(seq $B1 $B2); do
  ./gamlist $b 1 $PM emit > /tmp/glp_$b.txt 2>/dev/null
  res=$( ( ulimit -v 1500000; timeout 20 ./bauto4 $b /tmp/glp_$b.txt -cap 200000 2>/dev/null ) | awk '{g=$4; sub("g=","",g); print g}' | sort -u | awk 'BEGIN{ORS=" "}{print}')
  cap=$(( ulimit -v 1500000; timeout 20 ./bauto4 $b /tmp/glp_$b.txt -cap 200000 2>&1 >/dev/null ) | grep -c "capped=1")
  echo "b=$b: $res  [capped streams: $cap]"
done
