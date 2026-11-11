#!/bin/bash
# r12g3 chain A2 (3 threads, now): indep fwd rec2 K=27 orbit 1 (kink7 Cyc(23) o1 + own TopCore(4), phi0=(7,14,1)),
# then step-by-step comparison with kfwd3 logs/fwd2/rec2_K27_k4_o1.log.
R=~/p196_run/r12g; L=$R/logs/g3; PY=~/p196_run/venv/bin/python; D=$R/data/indep
cd $R/data
/usr/bin/time -l $R/bin/indep_b fwd $D/rec2.rows 27 23 $R/data/k7/rec2_K23_o1.bin 4 $D/top/top_4.bin 7 14 1 3 8 27 3 > $L/ifwd_rec2_K27_o1.log 2> $L/ifwd_rec2_K27_o1.err
$PY $R/src/cmpsteps.py $R/logs/fwd2/rec2_K27_k4_o1.log $L/ifwd_rec2_K27_o1.log > $L/cmp_K27_o1.log 2>&1
echo DONE > $L/chain_g3a2.done
