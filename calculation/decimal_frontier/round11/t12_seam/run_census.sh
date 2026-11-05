#!/bin/bash
cd ~/p196_run/r11c
for L in 7 8 9 10 11 12; do /usr/bin/time -l nice -n 10 ./census $L 6 47 > census_L$L.txt 2> census_L$L.err; done
