#!/bin/bash
# r14c: restart of the three pass-2 towers with a real level cap (pass3 had none: default kmax=400).
cd ~/p196_run/r13c || exit 1
run() { nohup perl -e 'alarm 36000; exec @ARGV' bin/khr_r3 10 "$2" "$3" "$4" -runfile "$5" -kmax 1000000 -sec 35000 -nodecap 200000000 -batch 256 > ~/p196_run/r14c/logs/pass4_$1.out 2>&1 &
}
run L24_if7475 01 8 24 out/pass2/L24_if7475.txt
run CAP54a 001010101 9 54 out/pass2/CAP54a_list.txt
run CAP56b 00100101010101 14 56 out/pass2/CAP56b_list.txt
sleep 2
ps -axo pid,etime,rss,command | grep khr_r3 | grep -v grep | cut -c1-160
