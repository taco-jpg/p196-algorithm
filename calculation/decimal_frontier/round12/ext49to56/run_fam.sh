#!/bin/bash
# r12e Task A (families, (01)^{4j}): khxt -exactset -top on pattern 01 with L=40 ((01)^20) and L=48 ((01)^24).
# TOP99 closed part at level K = all 9-wire exteriors of width <= K-2.  (N12^4 runs in run_anc2.sh.)
cd ~/p196_run/r12e; mkdir -p out/fam
run(){ NAME=$1; W=$2; L=$3; SEC=$4
  nice -n 10 ~/p196_run/r12e/bin/khxt 10 -g $W -L $L -batch 4096 -exactset -top -v -kmax 100000 -nodecap 400000000 -sec $SEC > out/fam/$NAME.out 2> out/fam/$NAME.err
  echo "$(date -u +%FT%TZ) $NAME done" >> out/fam/done.log; }
run h01_L40 01 40 ${1:-1500}
run h01_L48 01 48 ${2:-1500}
