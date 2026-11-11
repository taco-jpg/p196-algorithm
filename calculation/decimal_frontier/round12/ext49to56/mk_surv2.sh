#!/bin/bash
# r12e3: deep-2 candidates of period T = deep-1 outputs out/deep5556/T_*.out with a verdict line that SURVIVE without any
# TOP99/TOPUU hit and whose root is not 01 ((01)^{4j}: G_K(01) keeps 8-periodic closed walks at every K, Theorem K can never
# apply).  Same rule as chain14b.sh.   usage: mk_surv2.sh T  > list   (lines "T word")
cd ~/p196_run/r12e; T=$1
for f in out/deep5556/${T}_*.out; do
  [ -e "$f" ] || continue
  grep -q "^KHXT" "$f" || continue
  if grep -q SURVIVES "$f" && ! grep -Eq "top99_first=[0-9]|topUU_first=[0-9]" "$f"; then
    w=$(grep -o "word=[01]*" "$f" | cut -c6-); r=$(grep -o "root=[01]*" "$f" | cut -c6-)
    [ "$r" == "01" ] && continue
    echo "${#w} $w"
  fi
done
