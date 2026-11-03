#!/bin/bash
# r9u main: windowed backward cone (w=10 bitset windows + wrapped windows) for (T=32, clock 0000111000110001), targets = all uniform bands + all 9-wire streams
cd ~/p196_run/r9u
WIN=10 WRAP=1 WINDIR=wsets ROT=1 THREADS=14 nice -n 10 ./backdisk_r9u 10 32 0000111000110001 wd/main_T32 15000000000 0.22 bands allstreams >> logs/main_T32.log 2>&1
echo "run_main done $(date -u)" >> logs/main_T32.log
