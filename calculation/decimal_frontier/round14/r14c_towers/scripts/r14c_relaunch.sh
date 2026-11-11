#!/bin/bash
# main session: rerun r14c's time-capped towers with a 72 h cap (bin/ifd10, same logic as ifd7/ifd8, validated by r14c)
cd ~/p196_run/r14c
S=255000; A=259200
run() { # name clock L
  nohup perl -e "alarm $A; exec @ARGV" bin/ifd10 10 $2 $3 -runfile out/towers/$1.txt -tree -slots 4096 -sec $S > logs/main_$1.out 2> logs/main_$1.err < /dev/null &
}
run L32_C_1 01 32
run L32_C_3 01 32
run CAP54a 001010101 54
run N60_1 0001 60
run N60_2 0001 60
echo "$(date -u +%FT%TZ) main: r14c agent gone (Mac restart); relaunched its 5 time-capped towers L32_C_1, L32_C_3, CAP54a, N60_1, N60_2 with bin/ifd10 -tree, cap 72 h, logs r14c/logs/main_*.{out,err}" >> ~/p196_run/DECISIONS.md
