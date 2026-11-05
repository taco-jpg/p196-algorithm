#!/bin/bash
# r11b validation with 2 threads (runs beside the w=11 build): level families on small bases + path checks; forward controls with HFILT.
cd ~/p196_run/r11b; mkdir -p vs wd
./val_small.sh
# forward controls, same binary as the main runs
THREADS=2 ROT=1 HWIN=10 HDIR=ls ./reachdisk_r11b 10 16 01 ALL wd/c16_h10 3000000000 0.16 | grep -vE "^\[hcut|^height" ; echo "(16,01) HWIN=10 done"
# clock 0001 families up to w=11, then (24,0001) and (12,0001)
./lvl2 10 0001 8 vs 2 26; ./lvl2 10 0001 9 vs 2 27 8; ./lvl2 10 0001 10 vs 2 28 9; NOBWD=1 ./lvl2 10 0001 11 vs 2 30 10
for w in 10 11; do for T in 12 24; do THREADS=2 ROT=1 HWIN=$w HDIR=vs ./reachdisk_r11b 10 $T 0001 ALL wd/p${T}_h$w 3000000000 0.16 | grep -vE "^\[hcut|^height"; echo "(${T},0001) HWIN=$w done"; done; done
echo VAL2_DONE
