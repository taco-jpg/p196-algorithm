#!/bin/bash
cd ~/p196_run/r13c
while pgrep -f "[k]hr_r3 10 01 8 24" > /dev/null; do sleep 20; done
nice -n 10 ~/p196_run/r13c/bin/khr_r3 10 0001 12 24 -kmax 6000 -nodecap 300000000 -sec 7200 -predict 1500 out/N24/pred.txt -deaths out/N24/deaths.txt > out/N24/pred.out 2>&1
LST=$(python3 -c "print(','.join(str(k) for k in list(range(10,100,10))+list(range(100,1500,20))))")
nice -n 10 ~/p196_run/r13c/bin/khp 10 -g 0001 -L 24 -batch 4096 -exactset -prim 12 -primk $LST -kmax 1480 -nodecap 400000000 -sec 7200 > ctrl/plain_N24.out 2> ctrl/plain_N24.err
echo DONE > ctrl/plain_N24.done
