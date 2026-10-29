#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -std=c++17 -O3 x01_pump.cpp -o /tmp/x01_pump
/tmp/x01_pump 49 59 4149 20000 > /tmp/x01_symbolic.txt
python3 x01_oracle.py 49 59 4149 20000 > /tmp/x01_integer.txt
grep '^STATE' /tmp/x01_symbolic.txt > /tmp/x01_a.txt
grep '^STATE' /tmp/x01_integer.txt > /tmp/x01_b.txt
diff -u /tmp/x01_a.txt /tmp/x01_b.txt
grep -F 'gamma1=8295 trims=11705 max_trim=1 pathhash=289024506' /tmp/x01_symbolic.txt
grep -F 'gamma1=8295 finalL=3 final_digits=16597 pathhash=289024506' /tmp/x01_integer.txt
echo 'X01 ALL LOCAL CHECKS PASSED'
