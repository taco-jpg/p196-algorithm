#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
for L in rec0 rec1; do
  for o in 0 1 2 3; do
    ./mc13b run lat/$L.txt $o 46 8 > logs/${L}_o$o.log 2>&1
  done
done
echo done > logs/rec01.done
