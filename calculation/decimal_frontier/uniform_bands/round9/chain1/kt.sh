#!/bin/bash
# round 9: K-tail cores (all periods at once) for the window-surviving alignments of the Agent6 port words, clock 0001
cd ~/p196_run/r9
for e in 01110101 11101010 0001000011101111 01000101 00101010 10111010 01011101; do
  THREADS=12 nice -n 10 ./ktail 10 0001 $e 24 400000000 > logs/kt_$e.log 2>&1
done
