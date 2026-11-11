#!/bin/bash
# r12g3 chain B4: after corefrom rec2 orbit 1 (chain B3) has finished: indep fwd rec0 K=22 with its OWN Core(18) (corefrom) + own
# TopCore(4), phi0=(1,9,1), 8 threads: the independent forward replication of the rec0 K=22 run (kfwd3 logs/fwd2/rec0_K22_k4_o0.log).
R=~/p196_run/r12g; L=$R/logs/g3; PY=~/p196_run/venv/bin/python; D=$R/data/indep
cd $D
while ! [ "$(grep -c -E 'EQUAL|DIFFERENT' $L/cmp2_rec2_o1.log 2>/dev/null)" = "3" ]; do sleep 20; done
/usr/bin/time -l $R/bin/indep_b fwd $D/rec0.rows 22 18 $D/g3core2_rec0_o0/core_18.bin 4 $D/top/top_4.bin 1 9 1 8 8 27 3 > $L/ifwd_rec0_K22.log 2> $L/ifwd_rec0_K22.err
$PY $R/src/cmpsteps.py $R/logs/fwd2/rec0_K22_k4_o0.log $L/ifwd_rec0_K22.log > $L/cmp_K22_rec0.log 2>&1
echo DONE > $L/chain_g3b4.done
