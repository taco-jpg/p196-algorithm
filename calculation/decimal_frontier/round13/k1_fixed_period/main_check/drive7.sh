#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
# period-8 lattices: drift at most 1/5 (excludes the centre speed 1/4), and drift 0 alone
for L in rec0 rec2; do
  ./mc13d2 lat/$L.txt 5 10 8 > logs/${L}_budget5.log 2>&1
  ./mc13d2 lat/$L.txt 5 10 8 zero > logs/${L}_zero.log 2>&1
done
echo done > logs/p8budget.done
