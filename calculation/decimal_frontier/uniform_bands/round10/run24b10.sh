#!/bin/bash
cd ~/p196_run/r10
EARLY=1 WINCHECK=10 BFILT=1 WINDIR=wsets ROT=1 THREADS=20 nice -n 5 ./reachdisk_wc_r10 10 24 01 ALL wd/f24_w10 15000000000 0.18 >> logs/fwdB10_T24_01.log 2>&1
echo "run24b10 done $(date -u)" >> logs/fwdB10_T24_01.log
