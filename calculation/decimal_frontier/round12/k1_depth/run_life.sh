#!/bin/zsh
# exact lifetimes of free top-K windows (no relaxation filter) at the four t=0 phase classes; compare with r12d survscan
cd ~/p196_run/r12g/data
for spec in "rec1 6" "rec1 7" "rec0 8" "rec1 8"; do
  L=${spec% *}; K=${spec#* }
  for ph in "0 0 0" "0 0 1" "0 1 0" "0 1 1"; do
    ~/p196_run/r12g/bin/kfwd lat_$L.tbl $K $K - ${=ph} 4000 6 > ../logs/life/${L}_K${K}_${ph// /}.log 2>&1
  done
done
