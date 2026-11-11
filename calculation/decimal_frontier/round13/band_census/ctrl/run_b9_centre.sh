#!/bin/bash
PY=~/p196_run/venv/bin/python; CG=~/p196_run/r13a/centregen.py
cd ~/p196_run/r13a/ctrl
for w in "1,1,15,15" "1,15,15,1" "15,15,1,1" "15,1,1,15" "11,5,5,11" "5,5,11,11" "5,11,11,5" "11,11,5,5"; do
 for Lc in 0 1 2 3 4 5 6 7; do
  nice -n 10 $PY $CG --b 9 --clock 1100011000 --V $w --N 20 --j 1 --Lc $Lc --solver cadical195 2>&1 | grep -E "RESULT|WITNESS|Error|Traceback" | sed "s/^/$w Lc=$Lc: /"
 done
done
