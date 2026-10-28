#!/bin/bash
OUT=$1; T=$2; shift 2
: > $OUT
for b in 10 11 20; do for s in 11 12 13 14 15 16 17 18; do ./cpp/lock3 $b 20 $s $T 6 16 | grep -v "^   " >> $OUT; done; done
