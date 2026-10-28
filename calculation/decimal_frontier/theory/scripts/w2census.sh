#!/bin/bash
# usage: w2census.sh b pmin pmax cap tag   -- complete exterior census over ALL counter-realizable gam necklaces of period p in [pmin,pmax]
# sequential, run inside ONE heavy call.  outputs out2/e4_<b>_<tag>.{txt,err,list}
b=$1; pmin=$2; pmax=$3; cap=$4; tag=$5
cd /home/claude/research/w2_theory/out2
../bin/gamlist $b $pmin $pmax emit > e4_${b}_${tag}.list
echo "streams: $(wc -l < e4_${b}_${tag}.list)" >&2
( ulimit -v 2400000; ../bin/bauto4 $b e4_${b}_${tag}.list -cap $cap > e4_${b}_${tag}.txt 2> e4_${b}_${tag}.err )
echo "done b=$b p=$pmin..$pmax cap=$cap accepts=$(grep -c ACCEPT e4_${b}_${tag}.txt) $(tail -1 e4_${b}_${tag}.err)" >&2
