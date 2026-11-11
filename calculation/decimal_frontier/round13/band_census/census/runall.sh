#!/bin/bash
# run band census for the three decimal clocks, s=1..8, 8 threads, nice 10
cd ~/p196_run/r13a/census
for clk in 1000 10 00001110001; do
  for s in 1 2 3 4 5 6 7 8; do
    out=b${clk}_s$s.txt
    if [ -s b${clk}_s$s.done ]; then continue; fi
    /usr/bin/time -l nice -n 10 ./bandcensus 10 $clk $s 5 > $out 2> b${clk}_s$s.err
    echo "$(date -u +%H:%M:%S) clk=$clk s=$s bands=$(wc -l < $out)" >> runall.log
    echo done > b${clk}_s$s.done
  done
done
