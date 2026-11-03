#!/bin/bash
cd ~/p196_run/r9
for a in "72 0001 2000" "88 0001 2000" "96 0001 1000" "40 01 20000"; do set -- $a; ( time ./backdisk9 TEST 10 $1 $2 $3 $1 ) 2>&1 | grep -E "SELFTEST|real" | tr "\n" " " | sed "s/^/T=$1 clock=$2: /" >> logs/selftest.log; echo >> logs/selftest.log; done
( time WIN=12 WINFILE=win/w12 ./backdisk9 TEST 10 88 0001 1000 7 ) 2>&1 | grep -E "SELFTEST|real" | tr "\n" " " | sed "s/^/WIN12 T=88: /" >> logs/selftest.log; echo >> logs/selftest.log
