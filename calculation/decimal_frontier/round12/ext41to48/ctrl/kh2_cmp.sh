#!/bin/bash
# r12b V3: independent kh2 vs khx, level by level, on a sample of words.  Input: lines "p g ..." ; L = p.
#  (a) kh2 -scc kept counts must EQUAL khx -noexact kept counts at every level;
#  (b) kh2 -exact (exact closed-walk set) must die no later than khx (superset), and kept_exact <= kept_khx at every level.
cd ~/p196_run/r12b
IN=$1; KM=${2:-40}; NC=${3:-4000000}
while read p g rest; do
  a=$(bin/kh2 10 $g $p -scc $KM $NC | grep "^K=" | sed "s/ n=[0-9]*//" | tr "\n" " ")
  b=$(bin/khx 10 -g $g -kmax $KM -nodecap $NC -noexact -v 2>&1 >/dev/null | awk "{print \$1, \$3}" | tr "\n" " ")
  c=$(bin/kh2 10 $g $p -exact $KM $NC | tail -1 | awk "{print \$(NF-1), \$NF}")
  d=$(bin/khx 10 -g $g -kmax $KM -nodecap $NC | awk "{print \$5, \$6}")
  sccok=$([ "$a" == "$b" ] && echo SCC_EQUAL || echo SCC_DIFF)
  echo "$p $g :: $sccok :: kh2exact=[$c] khx=[$d]"
done < $IN
echo KH2CMP_DONE
