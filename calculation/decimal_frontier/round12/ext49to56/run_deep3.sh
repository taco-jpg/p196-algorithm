#!/bin/bash
# r12e3: run_deep2.sh + (1) an atomic per-word claim (mkdir OUTDIR/T_word.lock), so several drivers can share one list without
# running a word twice; (2) an optional deadline: a word is only STARTED before START_BY (epoch s) and its time cap is
# min(SEC, END_BY - now) (skipped if < 300 s), so every run ends by itself.  Otherwise identical to run_deep2.sh / run_deep.sh:
# khxt -batch 4096 -exactset -top -v, root pattern with L = |word| for imprimitive words (Lemma K6), stderr kept per word.
# usage: run_deep3.sh LIST OUTDIR NWORK NODECAP SEC [START_BY_EPOCH END_BY_EPOCH]
cd ~/p196_run/r12e
LIST=$1; OUT=$2; NW=${3:-2}; NC=${4:-120000000}; SEC=${5:-900}; SB=${6:-0}; EB=${7:-0}
mkdir -p $OUT
awk '{print $1, $2}' $LIST | xargs -P $NW -L 1 bash -c '
  T=$0; w=$1; f='"$OUT"'/${T}_$w.out
  [ -s $f ] && exit 0
  S='"$SEC"'; now=$(date +%s)
  if [ '"$SB"' -gt 0 ]; then
    [ $now -ge '"$SB"' ] && exit 0
    R=$(( '"$EB"' - now )); [ $R -lt $S ] && S=$R; [ $S -lt 300 ] && exit 0
  fi
  mkdir '"$OUT"'/${T}_$w.lock 2>/dev/null || exit 0
  n=${#w}; r=$w
  for ((d=1; d<=n; d++)); do if (( n % d == 0 )); then u=${w:0:d}; s=""; for ((k=0;k<n/d;k++)); do s=$s$u; done; if [ "$s" == "$w" ]; then r=$u; break; fi; fi; done
  if [ "$r" == "$w" ]; then A="-g $w"; else A="-g $r -L $n"; fi
  echo "$(date -u +%FT%TZ) start $T $w root=$r sec=$S nodecap='"$NC"'"
  nice -n 10 ~/p196_run/r12e/bin/khxt 10 $A -batch 4096 -exactset -top -v -kmax 100000 -nodecap '"$NC"' -sec $S > $f.tmp 2> '"$OUT"'/${T}_$w.err
  echo "word=$w root=$r" >> $f.tmp; mv $f.tmp $f
  echo "$(date -u +%FT%TZ) end $T $w :: $(head -1 $f | cut -c1-220)"
'
echo "$(date -u +%FT%TZ) DEEP_DONE $LIST $OUT"
