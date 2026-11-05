#!/bin/bash
# r11b positive controls for the level-family filter (HFILT): known exterior streams must survive.
# N12 (clock 0001, T=12 and T=24: stream at height 53) and p11 (clock 00001110001, T=11: stream at height 29).
cd ~/p196_run/r11b; mkdir -p vs vp wd
./lvl2 10 0001 8 vs 4 26; ./lvl2 10 0001 9 vs 4 27 8; ./lvl2 10 0001 10 vs 4 29 9; ./lvl2 10 0001 11 vs 4 31 10
./lvl2 10 00001110001 8 vp 4 26; ./lvl2 10 00001110001 9 vp 4 27 8; ./lvl2 10 00001110001 10 vp 4 29 9; ./lvl2 10 00001110001 11 vp 4 31 10
for w in 10 11; do
  for T in 12 24; do rm -rf wd/n${T}_h$w; THREADS=4 ROT=1 HWIN=$w HDIR=vs ./reachdisk_r11b 10 $T 0001 ALL wd/n${T}_h$w 3000000000 0.16 | grep -vE "^\[hcut|^height"; echo "CTRL (${T},0001) HWIN=$w done"; done
  rm -rf wd/p11_h$w; THREADS=4 ROT=1 HWIN=$w HDIR=vp ./reachdisk_r11b 10 11 00001110001 ALL wd/p11_h$w 3000000000 0.16 | grep -vE "^\[hcut|^height"; echo "CTRL (11,p11) HWIN=$w done"
done
echo CTRL_DONE
