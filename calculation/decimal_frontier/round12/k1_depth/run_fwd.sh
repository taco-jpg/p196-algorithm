#!/bin/zsh
# r12g2: usage run_fwd.sh LAT K k FILTER t0 j0 par0 THREADS TAG [TOPFILE Kt]   (kfwd3, absolute paths, log in logs/fwd2)
R=~/p196_run/r12g
L=$1; K=$2; k=$3; F=$4; t0=$5; j0=$6; p0=$7; T=$8; TAG=$9; TOP=${10:-$R/data/top/top_4.bin}; KT=${11:-4}
cd $R/data
/usr/bin/time -l $R/bin/kfwd3 $R/data/lat_$L.tbl $K $k $F $t0 $j0 $p0 4000 $T 0 $TOP $KT > $R/logs/fwd2/$TAG.log 2> $R/logs/fwd2/$TAG.err
