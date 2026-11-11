#!/bin/bash
cd ~/p196_run/r13c
nice -n 10 ~/p196_run/r13c/bin/khr_r3 10 0001 12 36 -kmax 3000 -nodecap 200000000 -sec 600 -batch 256 -predict 500 out/N36/pred.txt -deaths out/N36/deaths.txt > out/N36/pred.out 2>&1
LST=$(python3 -c "print(','.join(str(k) for k in list(range(10,200,10))+list(range(200,520,20))))")
nice -n 10 ~/p196_run/r13c/bin/khp 10 -g 0001 -L 36 -batch 4096 -exactset -prim 12 -primk $LST -kmax 500 -nodecap 400000000 -sec 3000 > ctrl/plain_N36.out 2> ctrl/plain_N36.err
echo DONE > ctrl/plain_N36.done
