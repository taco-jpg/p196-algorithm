#!/bin/zsh
# usage: run_k7.sh LAT ORBIT K0 K1 PREV   -- kink7 chain for one phase orbit, K0..K1, starting from the Cyc(K0-1) file PREV
L=$1; O=$2; K0=$3; K1=$4; PREV=$5
D=~/p196_run/r12g/data/k7; mkdir -p $D
cd ~/p196_run/r12g/data
for K in $(seq $K0 $K1); do
  OUT=$D/${L}_K${K}_o$O.bin
  /usr/bin/time -l ~/p196_run/r12g/bin/kink7 lat_$L.tbl $K $PREV $OUT $O > ~/p196_run/r12g/logs/k7_${L}_o${O}_K$K.log 2> ~/p196_run/r12g/logs/k7_${L}_o${O}_K$K.err || break
  PREV=$OUT
done
