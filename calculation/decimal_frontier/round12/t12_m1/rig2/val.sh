#!/bin/bash
# r12a: soundness controls for the free-port rigidity encoding (rigid2.py validate / Wleft)
cd ~/p196_run/r12a
PY=~/p196_run/venv/bin/python
$PY ~/p196_run/r12a/rigid2.py Wleft --r 9 --pin > rig2/wleft_r9_pin.log 2>&1
for spec in "0 12 3 1" "13 12 3 2" "1 12 6 3" "24 15 9 4" "7 20 12 5" "28 9 6 6"; do
  set -- $spec
  /usr/bin/time -l $PY ~/p196_run/r12a/rigid2.py validate --U $1 --Lj $2 --r $3 --seed $4 > rig2/val_U$1_L$2_r$3_s$4.log 2>&1
done
echo done > rig2/val.done
