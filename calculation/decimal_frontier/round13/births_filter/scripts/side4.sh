#!/bin/bash
cd ~/p196_run/r13c
while [ "$(pgrep -f '[/]p196_run/r13c/bin/' | wc -l | tr -d ' ')" -ge 8 ]; do sleep 20; done
exec nice -n 10 ~/p196_run/r13c/bin/khr_r3 10 01 8 24 -runfile out/pass2/L24_if7475.txt -kmax 20000 -sec 30000 -nodecap 1000000000 -batch 256 > out/pass2/L24_if7475.out 2>&1
