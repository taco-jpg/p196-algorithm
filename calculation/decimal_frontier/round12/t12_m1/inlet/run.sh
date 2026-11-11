#!/bin/bash
cd ~/p196_run/r12a
for spec in "0 112" "0 100" "6 112" "6 100" "13 112" "21 112"; do set -- $spec
 /usr/bin/time -l ~/p196_run/venv/bin/python ~/p196_run/r12a/rigid2.py Uinlet --U $1 --tmax $2 --cap 2 > inlet/Uinlet_U$1_T$2.log 2>&1
done
