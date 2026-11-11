#!/bin/bash
# r12b validation V2: independent exact check of khx deaths with bx3 -layered (layer-by-layer BFS, no global dedupe:
# layer d empty  <=>  no closed walk of length p in G_d).  Input lines "p g K wdone"; runs bx3 -layered K+1.
# usage: run_layered_check.sh LIST OUTPREFIX N
cd ~/p196_run/r12b
LIST=$1; OUT=$2; N=$3
tmp=$(mktemp -d /tmp/r12b_lc.XXXX)
sort -k3,3n $LIST > $tmp/sorted.txt
./rr_split.sh $tmp/sorted.txt $N $tmp/s
for f in $tmp/s*; do
  ( while read p g K w; do
      r=$(nice -n 10 ~/p196_run/r12b/bin/bx3 10 -g $g -layered $((K+1)) -lcap 60000000 -sec 900 | grep '^RES')
      echo "$p $g $K $w :: $r"
    done < $f > ${OUT}_$(basename $f).out ) &
done
wait
rm -rf $tmp
echo "LAYERED_DONE"
