#!/bin/bash
cd ~/p196_run/r11g/src
run(){ for R in 0 1; do echo "== $* RELAX=$R"; RELAX=$R ALLFITS=1 nice -n 10 ./reach_relax "$@" 300000000 | grep -E "BAND FITS|RESULT" | sed -E "s/; [0-9.]+ s;.*//"; done; }
BAND="1:1,0:2" PH=0 run 4 6 011001 BAND
BAND="1:1,0:2" PH=1 run 4 6 011001 BAND
BAND="0:8,1:4" PH=0 run 13 10 1010010000 BAND
BAND="0:8,1:4" PH=1 run 13 10 1010010000 BAND
for ph in 0 1; do BAND="0:6,1:2" PH=$ph run 10 8 01 BAND; done
for ph in 0 1 2 3 4 5; do BAND="0:2,0:4,0:8,1:6,1:4,1:0" PH=$ph run 10 12 0001 BAND; done
