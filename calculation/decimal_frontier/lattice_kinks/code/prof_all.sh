#!/bin/bash
# lifetime profile over all start phases: for w, find max H with survivors for each (t0,o); report global max
LAT=$1; W=$2; HLO=$3; HHI=$4
for H in $(seq $HLO $HHI); do
  tot=0
  for t0 in 0 1 2 3 4 5 6 7; do
    r=$(./surv $LAT $W 0 40 400 $H $t0 0 | grep TOTAL | sed 's/.*leaves=\([0-9]*\).*/\1/')
    tot=$((tot+r))
  done
  echo "w=$W H=$H total_leaves_over_all_phases=$tot"
  [ $tot -eq 0 ] && break
done
