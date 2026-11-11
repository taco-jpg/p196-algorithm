#!/bin/bash
# r12e Task A: long khxt runs (exact closed-walk sets + TOP99/TOPUU closed-part test at every level + WL invariant per level)
# on the r12b UNDECIDED words.  usage: run_taskA.sh NAME WORD [L] [SEC]
cd ~/p196_run/r12e; mkdir -p out/taskA
NAME=$1; W=$2; L=${3:-}; SEC=${4:-15000}
LA=""; [ -n "$L" ] && LA="-L $L"
nice -n 10 ~/p196_run/r12e/bin/khxt 10 -g $W $LA -batch 4096 -exactset -top -inv -v -kmax 100000 -nodecap 400000000 -sec $SEC \
  > out/taskA/$NAME.out 2> out/taskA/$NAME.err
echo "$(date -u +%FT%TZ) $NAME finished" >> out/taskA/done.log
