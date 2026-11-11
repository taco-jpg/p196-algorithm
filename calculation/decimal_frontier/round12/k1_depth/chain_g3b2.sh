#!/bin/bash
# r12g3 chain B2 (replaces chain B): after kfwd3 rec0 K=23 has finished (frees 4 threads):
#  (1) INDEPENDENT cores beyond the indep key limit (bin/indep_g3 corefrom = indep's own rule and trimming, kink key format
#      PS = 118 for K > 20): rec2 orbit 0 from its own Core(20) to K = 23, compared with kink7 rec2_K21..23_o0 (the filter of
#      the K = 27 run);
#  (2) indep core rec0 orbit 0 K = 1..17, compared with kink7 K = 15..17;
#  (3) indep fwd rec0 K=21 with its OWN Core(17) + own TopCore(4), phi0=(1,9,1), 4 threads (fully independent replication of
#      kfwd rec0 K=21) || corefrom rec2 orbit 1 from its own Core(20) to K = 23 (3 threads), compared with kink7 o1.
R=~/p196_run/r12g; L=$R/logs/g3; PY=~/p196_run/venv/bin/python; D=$R/data/indep
mkdir -p $D/g3core_rec0_o0 $D/g3core2_rec2_o0 $D/g3core2_rec2_o1; cd $D
while ! grep -q "^DONE" $R/logs/fwd2/rec0_K23_k4_o0.log 2>/dev/null; do sleep 30; done
# memory: corefrom K=23 peaks at ~32-37 GB (estimate), so also wait until chain A3 (rec2 K=24 runs) is done
while ! test -f $L/chain_g3a3.done; do sleep 30; done
/usr/bin/time -l $R/bin/indep_g3 corefrom $D/rec2.rows $D/g3core_rec2_o0/core_20.bin 20 23 $D/g3core2_rec2_o0 4 3 > $L/corefrom_rec2_o0.log 2> $L/corefrom_rec2_o0.err
for K in 21 22 23; do $R/bin/indep_b cmp $D/g3core2_rec2_o0/core_$K.bin $R/data/k7/rec2_K${K}_o0.bin >> $L/cmp2_rec2_o0.log 2>&1; done
/usr/bin/time -l $R/bin/indep_b core $D/rec0.rows 1 5 1 17 $D/g3core_rec0_o0 4 3 > $L/core_rec0_o0.log 2> $L/core_rec0_o0.err
for K in 15 16 17; do $R/bin/indep_b cmp $D/g3core_rec0_o0/core_$K.bin $R/data/k7/rec0_K${K}_o0.bin >> $L/cmp_rec0_o0.log 2>&1; done
if grep -q "core_17.bin.*=> EQUAL" $L/cmp_rec0_o0.log; then
  ( /usr/bin/time -l $R/bin/indep_b fwd $D/rec0.rows 21 17 $D/g3core_rec0_o0/core_17.bin 4 $D/top/top_4.bin 1 9 1 4 8 27 3 > $L/ifwd_rec0_K21.log 2> $L/ifwd_rec0_K21.err
    $PY $R/src/cmpsteps.py $R/logs/fwd/rec0_K21_k4_o0.log $L/ifwd_rec0_K21.log > $L/cmp_K21_rec0.log 2>&1 ) &
fi
/usr/bin/time -l $R/bin/indep_g3 corefrom $D/rec2.rows $D/g3core_rec2_o1/core_20.bin 20 23 $D/g3core2_rec2_o1 3 3 > $L/corefrom_rec2_o1.log 2> $L/corefrom_rec2_o1.err
for K in 21 22 23; do $R/bin/indep_b cmp $D/g3core2_rec2_o1/core_$K.bin $R/data/k7/rec2_K${K}_o1.bin >> $L/cmp2_rec2_o1.log 2>&1; done
wait
echo DONE > $L/chain_g3b2.done
