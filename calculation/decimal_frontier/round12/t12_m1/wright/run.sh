#!/bin/bash
# r12a: W right-defect sets (rigid2.py Wright): maximal W continuation B0 W0^14 W[0..j), letter at y=160+j != W_j,
# R free columns, FREE right port, exact rooted left, all columns return.  UNSAT for all j => third seam exclusion.
cd ~/p196_run/r12a
R=${R:-12}
for j in 0 1 2 3 4 5 6 7 8; do f=wright/Wright_j${j}_r${R}.log; [ -s $f ] && grep -q RESULT $f && continue
  /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/rigid2.py Wright --j $j --r $R > $f 2>&1
  echo "j$j R$R $(grep RESULT $f) $(grep "free columns" $f)" >> wright/run.log
done
