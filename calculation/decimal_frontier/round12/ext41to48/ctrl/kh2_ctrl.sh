#!/bin/bash
cd ~/p196_run/r12b
for a in "10 00001110001 11" "10 0001 16" "10 0001 20" "10 0001 28" "10 01 36" "10 01 8" "13 1010010000 10" "4 011001 6" "10 000100010001 12"; do
  set -- $a
  r2=$(bin/kh2 $1 $2 $3 -exact 30 3000000 | tail -1); r3=$(bin/kh2 $1 $2 $3 -scc 30 3000000 | tail -1)
  r1=$(bin/khx $1 -g $2 -L $3 -kmax 30 -nodecap 3000000 | cut -d" " -f5-6); r4=$(bin/khx $1 -g $2 -L $3 -kmax 30 -nodecap 3000000 -noexact | cut -d" " -f5-6)
  echo "$a :: kh2-exact: ${r2#*$3 } | khx: $r1 || kh2-scc: ${r3#*$3 } | khx-noexact: $r4"
done
