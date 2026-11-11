#!/bin/bash
# r12e2 V5-style check (as r12b section 3a): independent kh2 -exact on DEEP-pass deaths (khxt -exactset verdicts), smallest widest
# level first, until a total time budget is used.  Root pattern and L = |word| exactly as the deep pass (Lemma K6).
# SAME = kh2 dies at the same K; NOVERDICT = kh2 did not finish within TLIM s (no claim either way); DIFF* = disagreement.
# usage: kh2_deep.sh TAG MAXW TLIM BUDGET DIR [DIR ...]      output: ctrl/kh2_deep_TAG.out (one line per word + SUMMARY)
cd ~/p196_run/r12e
TAG=$1; MAXW=$2; TLIM=$3; BUDGET=$4; shift 4
OUT=ctrl/kh2_deep_$TAG.out; : > $OUT; t0=$(date +%s)
for d in "$@"; do for f in $d/*.out; do
  l=$(grep "^KHXT" $f); echo "$l" | grep -q " DIES " || continue
  mn=$(echo "$l" | sed 's/.*maxnodes=\([0-9]*\).*/\1/'); [ "$mn" -le "$MAXW" ] && echo "$mn $f"
done; done | sort -rn | while read -r mn f; do
  [ $(( $(date +%s) - t0 )) -ge $BUDGET ] && break
  grep -q "$(basename $f .out) " ctrl/kh2_deep_T49_54.out && continue
  l=$(grep "^KHXT" $f); K=$(echo "$l" | sed 's/.* DIES K=\([0-9]*\).*/\1/')
  w=$(grep -o "word=[01]*" $f | cut -c6-); r=$(grep -o "root=[01]*" $f | cut -c6-); n=${#w}
  res=$(perl -e "alarm shift; exec @ARGV" $TLIM nice -n 10 ~/p196_run/r12e/bin/kh2 10 $r $n -exact $((K+3)) 400000000 2>/dev/null | grep "^KH2" | tail -1)
  K2=$(echo "$res" | sed -n 's/.* DIES K=\([0-9]*\).*/\1/p')
  if [ -z "$res" ]; then v=NOVERDICT; elif [ -z "$K2" ]; then v=DIFF_SURVIVES; elif [ "$K2" == "$K" ]; then v=SAME; else v=DIFF; fi
  echo "$v $(basename $f .out) root=$r L=$n khxt_K=$K maxnodes=$mn kh2: $res" >> $OUT
done
echo "SUMMARY $TAG $(awk '{c[$1]++} END{for(k in c) printf "%s=%d ", k, c[k]}' $OUT)" >> $OUT
tail -1 $OUT
