#!/bin/bash
cd ~/p196_run/r9
for a in "24 0001 200000" "48 0001 100000" "72 0001 20000" "88 0001 20000" "96 0001 10000" "40 01 50000"; do set -- $a; ( time ./backdisk9 TEST 10 $1 $2 $3 $1 ) 2>&1 | grep -E "SELFTEST|real" | tr "\n" " " | sed "s/^/T=$1 clock=$2: /" >> logs/selftest.log; echo >> logs/selftest.log; done
for a in "88 0001 5000"; do set -- $a; ( time WIN=12 WINFILE=win/w12 ./backdisk9 TEST 10 $1 $2 $3 7 ) 2>&1 | grep -E "SELFTEST|real" | tr "\n" " " | sed "s/^/WIN12 T=$1: /" >> logs/selftest.log; echo >> logs/selftest.log; done
