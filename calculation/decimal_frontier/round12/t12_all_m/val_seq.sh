#!/bin/bash
# r12f: genuine-orbit validations, run sequentially (one worker slot)
cd ~/p196_run/r12f
PY=~/p196_run/venv/bin/python; MD=~/p196_run/r12f/mdefect.py; MI=~/p196_run/r12f/mindep.py
run() { f=$1; shift; [ -e $f ] && return; /usr/bin/time -l nice -n 10 $PY "$@" > $f 2>&1; echo "$(date +%T) $f $(grep -o "'PASS': [A-Za-z]*" $f)" >> val/val.log; }
run val/seam_m3_U13.log   $MD validate  --U 13 --r 12 --m 3 --Lj 11 --seed 3 --solver kissat404
run val/centre_m3_U22.log $MD cvalidate --U 22 --r 4  --m 3 --Lj 9  --seed 4 --solver kissat404
run val/indep_genuine_m3_V13.log  $MI genuine  --V 13 --R 12 --m 3 --Lj 11 --seed 3 --solver kissat404
run val/indep_cgenuine_m3_V22.log $MI cgenuine --V 22 --R 4  --m 3 --Lj 9  --seed 4 --solver kissat404
run val/seam_m2_U26.log   $MD validate  --U 26 --r 12 --m 2 --Lj 9 --seed 5 --solver kissat404
run val/centre_m2_U8.log  $MD cvalidate --U 8  --r 6  --m 2 --Lj 9 --seed 6 --solver kissat404
run val/indep_genuine_m2_V26.log  $MI genuine  --V 26 --R 12 --m 2 --Lj 9 --seed 5 --solver kissat404
run val/indep_cgenuine_m2_V8.log  $MI cgenuine --V 8  --R 6  --m 2 --Lj 9 --seed 6 --solver kissat404
echo "$(date +%T) val_seq done" >> val/val.log
