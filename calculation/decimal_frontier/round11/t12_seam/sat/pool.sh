#!/bin/bash
# r11c: waits for census L12 (pid 14739) then runs seam SAT jobs, 6 at a time.
cd ~/p196_run/r11c
echo "pool start $(date)" >> sat/pool.log
cat sat/jobs.txt | xargs -P 3 -L 1 bash -c 'f=sat/seam_U$0_L$1.log; [ -s $f ] && grep -q RESULT $f && exit 0; nice -n 10 ~/p196_run/venv/bin/python seamsat.py seam --U $0 --Lj $1 > $f 2>&1; echo "$0 $1 $(tail -1 $f)" >> sat/pool.log'
echo "pool done $(date)" >> sat/pool.log
