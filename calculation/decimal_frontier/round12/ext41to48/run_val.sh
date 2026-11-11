#!/bin/bash
# r12b validation V1: khx (exact closure, kmax 15) on EVERY round-11 F1 word p=33..40 (5,400,712 words), compared with bx3.
cd ~/p196_run/r12b
N=${1:-10}
mkdir -p out/val/khx
for p in 33 34 35 36 37 38 39 40; do
  cut -f2 out/val/r11_p$p.tsv > out/val/w_p$p.txt
  ./rr_split.sh out/val/w_p$p.txt $N out/val/w_p${p}_s
  for f in out/val/w_p${p}_s*; do
    nice -n 10 ~/p196_run/r12b/bin/khx 10 -f $f -kmax 15 -nodecap 50000000 -sec 3 > out/val/khx/$(basename $f).out 2> /dev/null &
  done
  wait
  ~/p196_run/venv/bin/python py/val_cmp.py out/val/r11_p$p.tsv out/val/khx/w_p${p}_s*.out
  rm -f out/val/w_p${p}_s*
done
echo VAL_DONE
