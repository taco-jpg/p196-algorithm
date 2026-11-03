#!/bin/bash
cd ~/p196_run/r10
./wbuild 10 0001 10 wsets 4 > logs/build_0001_w10_again.log 2>&1 && ./bwin 10 0001 10 wsets 4 >> logs/build_0001_w10_again.log 2>&1
EARLY=1 WINCHECK=10 BFILT=1 WINDIR=wsets ROT=1 THREADS=4 nice -n 5 ./reachdisk_wc_r10 10 24 0001 ALL wd/pe24 15000000000 0.18 > logs/early_T24_0001.log 2>&1; rm -rf wd/pe24
echo "runpos2 done $(date -u)" >> logs/early_T24_0001.log
