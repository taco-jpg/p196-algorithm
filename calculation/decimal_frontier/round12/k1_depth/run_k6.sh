#!/bin/sh
# usage: run_k6.sh LAT K0 K1   (continues the chain in data/k6 from K0-1 to K1 with the original kink6)
L=$1; K0=$2; K1=$3
cd ~/p196_run/r12g/data/k6
for K in $(seq $K0 $K1); do
  /usr/bin/time -l ~/p196_run/r12g/bin/kink6 ../lat_$L.tbl $K incr ${L}_$((K-1)).bin ${L}_$K.bin > ~/p196_run/r12g/logs/k6_${L}_K$K.log 2> ~/p196_run/r12g/logs/k6_${L}_K$K.err
done
