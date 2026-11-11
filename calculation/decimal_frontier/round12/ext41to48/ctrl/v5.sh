#!/bin/bash
# r12b V5: independent kh2 -exact on khx deaths (lines "p g K maxnodes"). SOUNDNESS check: kh2 must DIE at a level <= khx K
# (kh2 keeps EXACTLY the nodes on closed L-walks; if it still had nodes at the khx death level, khx would be wrong).
cd ~/p196_run/r12b
IN=$1
while read p g K mx; do
  r=$(perl -e 'alarm shift; exec @ARGV' 2400 nice -n 10 ~/p196_run/r12b/bin/kh2 10 $g $p -exact $((K+2)) 150000000 | tail -1)
  k2=$(echo "$r" | sed -n 's/.*DIES K=\([0-9]*\).*/\1/p')
  if [ -z "$k2" ]; then v="NO_VERDICT($r)"; elif [ "$k2" -le "$K" ]; then if [ "$k2" -eq "$K" ]; then v=SAME; else v=KH2_EARLIER; fi; else v=FAIL; fi
  echo "$p $g khxK=$K kh2K=${k2:-none} $v"
done < $IN
echo V5_DONE
