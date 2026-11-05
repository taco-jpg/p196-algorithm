#!/bin/bash
cd ~/p196_run/r11g/src
for a in "3 10 11100" "3 20 11100" "4 6 100" "4 12 011001" "10 12 0001" "10 22 00001110001" "13 10 1010010000"; do
 for R in 0 1; do echo "== $a ROT=$R"; ROT=$R THREADS=4 nice -n 10 ./reachmt $a ALL 200000000 | grep -E "STREAM|TARGET|RESULT" | sed -E "s/; [0-9.]+ s;.*//"; done; done
