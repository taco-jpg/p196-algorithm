#!/bin/bash
# r11b: size of BB_8 per target class (clock 01, base 10)
cd ~/p196_run/r11b
one() { tag=$1; shift; rm -rf cls/$tag; mkdir -p cls/$tag; env "$@" ./lvlx 10 01 8 cls/$tag 8 27 | grep LEVEL | sed "s/^/[$tag] /"; }
# one all X=0 (done)
one band NOWIRE=1
# one wire NOBAND=1 (= all at w=8, round 10 notes)
for u in 0000 010101 000000; do one av$u WAVOID=$u; done
echo CLS_DONE
