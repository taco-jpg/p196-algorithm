#!/bin/bash
# generalized-lattice exterior census over bases; usage census4.sh bmin bmax pmax out
cd /home/claude/research/w3_formats/code
OUT=$4
echo "start $(date -u)" > $OUT
for b in $(seq $1 $2); do
  for p in $(seq 1 $3); do
    echo "### b=$b p=$p" >> $OUT
    timeout 120 ./bauto3 $b $p $p -cap 2000000 -maxscc 8 2>>$OUT.err | grep -v "nontrivial_sccs=0" | cut -c1-2500 >> $OUT
  done
done
echo "end $(date -u)" >> $OUT
