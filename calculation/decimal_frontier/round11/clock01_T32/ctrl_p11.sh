#!/bin/bash
# r11b positive control p11 (clock 00001110001, T=11, stream 00111010011 at height 29) with the level family at w=8 and w=9.
cd ~/p196_run/r11b; while pgrep -f ctrl.sh >/dev/null; do sleep 60; done
./lvl2 10 00001110001 8 vp 4 28; ./lvl2 10 00001110001 9 vp 4 30 8
for w in 8 9; do rm -rf wd/p11_h$w; THREADS=4 ROT=1 HWIN=$w HDIR=vp ./reachdisk_r11b 10 11 00001110001 ALL wd/p11_h$w 3000000000 0.16 | grep -vE "^\[hcut|^height"; echo "CTRL (11,p11) HWIN=$w done"; done
echo CTRLP11_DONE
