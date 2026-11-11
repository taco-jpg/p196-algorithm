#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
~/p196_run/venv/bin/python mklat_p12.py
./mc13b selftest lat/p12m9.txt 17 300000
./mc13b orbits lat/p12m9.txt
for o in 0 1 2; do
  ./mc13b run lat/p12m9.txt $o 60 8 1 > logs/p12m9_o$o.log 2>&1
done
echo done > logs/p12m9.done
