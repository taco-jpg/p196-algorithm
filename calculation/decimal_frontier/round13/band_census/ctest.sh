#!/bin/bash
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
for spec in "6 8 1" "12 8 1" "2 24 3" "4 24 3"; do set -- $spec
 for Lc in 0 1 2; do
  echo -n "V=$1 N=$2 j=$3 Lc=$Lc: "; nice -n 15 $PY centregen.py --b 10 --clock 1000 --V $1 --N $2 --j $3 --Lc $Lc --solver cadical195 2>&1 | grep -E "RESULT|WITNESS" | tr '\n' ' '; echo
 done
done
