#!/bin/bash
# absorbing outer-band exterior census, base 10 (sequential, one process at a time)
cd /home/claude/research/w3_formats/code
OUT=../out/census1.log
echo "start $(date -u)" >> $OUT
run() { echo "### $*" >> $OUT; timeout 400 ./bauto2 10 "$@" >> $OUT 2>&1; echo "rc=$?" >> $OUT; }
run 9 10 -band 18 -cap 12000000
run 9 10 -band 0 -cap 12000000
run 2 8 -band 6,12 -cap 12000000
run 6 6 -band 2,4,8,16,14,10 -cap 12000000
run 6 12 -band 2,4,8,16,14,10 -cap 12000000
run 11 11 -band 18 -cap 12000000
run 11 11 -band 0 -cap 12000000
echo "end $(date -u)" >> $OUT
