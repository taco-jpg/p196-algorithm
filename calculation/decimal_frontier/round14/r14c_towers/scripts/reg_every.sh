#!/bin/bash
# regression (sequential): plain memo DFS (ifb4) vs chunked tree DFS (ifd8) on a sample of towers (every N-th birth class) of a word
g=$1; L=$2; d0=$3; every=$4; alarm=${5:-3000}
cd ~/p196_run/r14c
perl -e "alarm $alarm; exec @ARGV" bin/ifb4 10 $g $L -word $d0 -every $every > ctrl/reg_${g}_${L}_a.out 2>/dev/null
perl -e "alarm $alarm; exec @ARGV" bin/ifd8 10 $g $L -word $d0 -tree -slots 4096 -every $every > ctrl/reg_${g}_${L}_b.out 2>/dev/null
ha=$(grep HIST ctrl/reg_${g}_${L}_a.out); hb=$(grep HIST ctrl/reg_${g}_${L}_b.out)
wa=$(grep IFB_WORD ctrl/reg_${g}_${L}_a.out | cut -c1-220); wb=$(grep IFB_WORD ctrl/reg_${g}_${L}_b.out | cut -c1-220)
echo "$wa"; echo "$wb"
if [ "$ha" == "$hb" ] && [ -n "$ha" ]; then echo "REG $g L=$L every=$every: HIST IDENTICAL"; else echo "REG $g L=$L every=$every: DIFFERENT or empty (a: $(echo $ha | cut -c1-100))"; fi
