#!/bin/bash
# r12e deep pass on census pass-1 survivors: khxt -batch 4096 -exactset -top (exact closed-walk sets; death level = khx3 death level),
# imprimitive words with the ROOT pattern and L = |word| (Lemma K6).  usage: run_deep.sh LIST OUTDIR NWORK NODECAP SEC
# LIST lines: "T word reason K type" (out/census/surv_T*.txt).  One output file per word: OUTDIR/T_word.out (skip if present).
cd ~/p196_run/r12e
LIST=$1; OUT=$2; NW=${3:-2}; NC=${4:-120000000}; SEC=${5:-1800}
mkdir -p $OUT
awk '{print $1, $2}' $LIST | xargs -P $NW -L 1 bash -c '
  T=$0; w=$1; f='"$OUT"'/${T}_$w.out
  [ -s $f ] && exit 0
  n=${#w}; r=$w
  for ((d=1; d<=n; d++)); do if (( n % d == 0 )); then u=${w:0:d}; s=""; for ((k=0;k<n/d;k++)); do s=$s$u; done; if [ "$s" == "$w" ]; then r=$u; break; fi; fi; done
  if [ "$r" == "$w" ]; then A="-g $w"; else A="-g $r -L $n"; fi
  nice -n 10 ~/p196_run/r12e/bin/khxt 10 $A -batch 4096 -exactset -top -kmax 100000 -nodecap '"$NC"' -sec '"$SEC"' > $f.tmp 2> /dev/null
  echo "word=$w root=$r" >> $f.tmp; mv $f.tmp $f
'
echo "$(date -u +%FT%TZ) DEEP_DONE $LIST"
