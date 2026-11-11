#!/bin/bash
cd ~/p196_run/r13c
B=~/p196_run/r13c/bin/khr_o
nice -n 10 $B 10 0001 12 12 -allL -kmax 60 -nodecap 80000000 -shard 1 2 > out/allL/n12_s1.out 2>&1
nice -n 10 $B 10 0001 12 12 -allL -kmax 60 -nodecap 80000000 -onlyif out/allL/if0.txt > out/allL/n12_if0.out 2>&1
nice -n 10 $B 10 01 8 8 -allL -kmax 60 -nodecap 80000000 > out/allL/g01.out 2>&1
echo DONE >> out/allL/side1.done
