#!/bin/bash
# r12b: khx over a word list (lines "p g ..." or "g"), N workers (round-robin), one output file per worker.
# usage: run_khx_list.sh LIST OUTPREFIX N "KHX_ARGS"
cd ~/p196_run/r12b
LIST=$1; OUT=$2; N=$3; ARGS=$4
tmp=$(mktemp -d /tmp/r12b_kl.XXXX)
awk '{print ($2!="" ? $2 : $1)}' $LIST > $tmp/w.txt
./rr_split.sh $tmp/w.txt $N $tmp/s
for f in $tmp/s*; do
  nice -n 10 ~/p196_run/r12b/bin/${KHXBIN:-khx} 10 -f $f $ARGS > ${OUT}_$(basename $f).out 2>/dev/null &
done
wait
rm -rf $tmp
echo "KHX_LIST_DONE $LIST"
