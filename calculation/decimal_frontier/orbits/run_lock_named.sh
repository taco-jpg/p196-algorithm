#!/bin/bash
OUT=$1; T=$2; shift 2
: > $OUT
for s in "$@"; do echo "== seed $s" >> $OUT; ./cpp/lock2 10 n$s 0 $T 8 16 >> $OUT; done
