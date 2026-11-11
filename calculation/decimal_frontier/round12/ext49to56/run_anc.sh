#!/bin/bash
# r12e: ancestry (core) runs: khxt -exactset to level K, then the ancestors of the final exact set at every level and their windows
# at level K-D (out/anc/NAME.anc).  Runs the jobs one after the other (one worker).
cd ~/p196_run/r12e; mkdir -p out/anc
run(){ NAME=$1; W=$2; L=$3; K=$4; D=$5; LA=""; [ -n "$L" ] && LA="-L $L"
  nice -n 10 ~/p196_run/r12e/bin/khxt_a 10 -g $W $LA -batch 4096 -exactset -kmax $K -nodecap 400000000 -anc $D out/anc/$NAME.anc > out/anc/$NAME.out 2>&1
  echo "$(date -u +%FT%TZ) $NAME done" >> out/anc/done.log; }
run p34_K2000 0001010101001001010101001010100101 "" 2000 1000
run p21sq_K1200 001001010101001010101 42 1200 600
run p47_K900 00010001000110001100010010001010100101000100011 "" 900 400
