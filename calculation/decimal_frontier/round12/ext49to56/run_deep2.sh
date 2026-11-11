#!/bin/bash
# r12e2: run_deep.sh with the per-level log kept (stderr -> OUTDIR/T_word.err, khxt -v) so that a run stopped by the watchdog
# still documents the level it reached.  Otherwise identical (khxt -batch 4096 -exactset -top, root pattern for imprimitive
# words with L = |word|, Lemma K6).   usage: run_deep2.sh LIST OUTDIR NWORK NODECAP SEC
cd ~/p196_run/r12e
LIST=$1; OUT=$2; NW=${3:-2}; NC=${4:-120000000}; SEC=${5:-900}
mkdir -p $OUT
awk '{print $1, $2}' $LIST | xargs -P $NW -L 1 bash -c '
  T=$0; w=$1; f='"$OUT"'/${T}_$w.out
  [ -s $f ] && exit 0
  n=${#w}; r=$w
  for ((d=1; d<=n; d++)); do if (( n % d == 0 )); then u=${w:0:d}; s=""; for ((k=0;k<n/d;k++)); do s=$s$u; done; if [ "$s" == "$w" ]; then r=$u; break; fi; fi; done
  if [ "$r" == "$w" ]; then A="-g $w"; else A="-g $r -L $n"; fi
  nice -n 10 ~/p196_run/r12e/bin/khxt 10 $A -batch 4096 -exactset -top -v -kmax 100000 -nodecap '"$NC"' -sec '"$SEC"' > $f.tmp 2> '"$OUT"'/${T}_$w.err
  echo "word=$w root=$r" >> $f.tmp; mv $f.tmp $f
'
echo "$(date -u +%FT%TZ) DEEP_DONE $LIST"
