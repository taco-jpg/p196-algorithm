#!/bin/bash
# r12e Task B check: independent kh2 (-exact) on the sampled census verdicts (and deaths with K >= 40) of out/census/samp_T{T}.txt.
# A pass-1 DIES at K must be reproduced by kh2 -exact at the same K (r12b V4a/V6: khx(-batch or default) death level = kh2 exact).
# usage: kh2_sample.sh T [MAXN=6000000] [TLIM=600]       output: ctrl/kh2_T{T}.out (one line per word) + summary line
cd ~/p196_run/r12e
T=$1; MAXN=${2:-6000000}; TLIM=${3:-600}
OUT=ctrl/kh2_T$T.out; : > $OUT
grep " DIES " out/census/samp_T$T.txt | while read -r l; do
  g=$(echo "$l" | sed 's/.* g=\([01]*\) .*/\1/'); K=$(echo "$l" | sed 's/.* DIES K=\([0-9]*\).*/\1/')
  r=$(perl -e "alarm shift; exec @ARGV" $TLIM nice -n 10 ~/p196_run/r12e/bin/kh2 10 $g ${#g} -exact $((K+3)) $MAXN 2>/dev/null | grep "^KH2" | tail -1)
  K2=$(echo "$r" | sed -n 's/.* DIES K=\([0-9]*\).*/\1/p')
  if [ -z "$r" ]; then v=NOVERDICT; elif [ -z "$K2" ]; then v=DIFF_SURVIVES; elif [ "$K2" == "$K" ]; then v=SAME; else v=DIFF; fi
  echo "$v T=$T g=$g khx_K=$K kh2: $r" >> $OUT
done
echo "SUMMARY T=$T $(awk '{c[$1]++} END{for(k in c) printf "%s=%d ", k, c[k]}' $OUT)" >> $OUT
tail -1 $OUT
