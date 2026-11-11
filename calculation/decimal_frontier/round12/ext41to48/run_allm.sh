#!/bin/bash
# r12b transfer analysis: for every primitive F1 root h (|h| <= 24): khx3p -allm (all multiples admissible: keep every cyclic SCC,
# no exact test) and print the SCC period multiset at the last complete level.  Output: one KHX line + one PERIODS line per word.
cd ~/p196_run/r12b
IN=$1; OUT=$2
while read h; do
  r=$(nice -n 10 ~/p196_run/r12b/bin/khx3p 10 -g $h -allm -periods -kmax 300 -nodecap 6000000 -sec 20 2>&1 | grep -E "PERIODS|KHX" | tail -2 | tr "\n" " ")
  echo "$h :: $r"
done < $IN > $OUT
echo ALLM_DONE $IN
