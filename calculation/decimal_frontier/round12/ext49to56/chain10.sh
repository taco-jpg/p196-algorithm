#!/bin/bash
# r12e: replace the last job of run_anc2.sh ((p21)^2 ancestry K=1200, too long for the remaining time) by K=800, D=400
cd ~/p196_run/r12e
until grep -q "n12x4 done" out/anc/done.log 2>/dev/null; do sleep 5; done
pkill -f "bash run_anc2.sh"; sleep 1; pkill -f "khxt_b 10 -g 001001010101001010101"; sleep 1
nice -n 10 ~/p196_run/r12e/bin/khxt_b 10 -g 001001010101001010101 -L 42 -batch 4096 -exactset -kmax 800 -nodecap 400000000 -anc 400 out/anc/p21sq_K800.anc > out/anc/p21sq_K800.out 2>&1
echo "$(date -u +%FT%TZ) p21sq_K800 done" >> out/anc/done.log
