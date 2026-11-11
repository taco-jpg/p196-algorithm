#!/bin/zsh
# r12g2: after the independent rec0 K=20 run: independent forward iteration (genuine addition, own packing for K > 25)
# rec2 K=27 orbit 0 with the kink7 Cyc(23) o0 file and the own TopCore(4), phi0 = (5,14,1), 3 threads
R=~/p196_run/r12g; D=$R/data/indep; L=$R/logs/indep
while ! grep -q -E "^(EMPTY|STABLE|UNDECIDED)" $L/ifwd_rec0_K20.log 2>/dev/null; do sleep 30; done
cd $D; /usr/bin/time -l $R/bin/indep_b fwd $D/rec2.rows 27 23 $R/data/k7/rec2_K23_o0.bin 4 $D/top/top_4.bin 5 14 1 3 8 27 3 > $L/ifwd_rec2_K27_o0.log 2> $L/ifwd_rec2_K27_o0.err
