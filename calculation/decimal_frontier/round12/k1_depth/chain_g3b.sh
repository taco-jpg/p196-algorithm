#!/bin/bash
# r12g3 chain B: after kfwd3 rec0 K=23 has finished (frees 4 threads):
#  (1) independent core rec0 orbit 0 (phase (1,5,1)) K=1..17 with 4 threads (~20 GB at K=17), compare K=15..17 with kink7;
#  (2) independent forward iteration rec0 K=21 with its OWN Core(17) + own TopCore(4), phi0=(1,9,1), 4 threads
#      (fully independent replication of kfwd rec0 K=21), then step-by-step comparison with logs/fwd/rec0_K21_k4_o0.log.
R=~/p196_run/r12g; L=$R/logs/g3; PY=~/p196_run/venv/bin/python; D=$R/data/indep
mkdir -p $D/g3core_rec0_o0; cd $D
while ! grep -q "^DONE" $R/logs/fwd2/rec0_K23_k4_o0.log 2>/dev/null; do sleep 30; done
/usr/bin/time -l $R/bin/indep_b core $D/rec0.rows 1 5 1 17 $D/g3core_rec0_o0 4 3 > $L/core_rec0_o0.log 2> $L/core_rec0_o0.err
for K in 15 16 17; do $R/bin/indep_b cmp $D/g3core_rec0_o0/core_$K.bin $R/data/k7/rec0_K${K}_o0.bin >> $L/cmp_rec0_o0.log 2>&1; done
if grep -q "core_17.bin.*=> EQUAL" $L/cmp_rec0_o0.log; then
  /usr/bin/time -l $R/bin/indep_b fwd $D/rec0.rows 21 17 $D/g3core_rec0_o0/core_17.bin 4 $D/top/top_4.bin 1 9 1 4 8 27 3 > $L/ifwd_rec0_K21.log 2> $L/ifwd_rec0_K21.err
  $PY $R/src/cmpsteps.py $R/logs/fwd/rec0_K21_k4_o0.log $L/ifwd_rec0_K21.log > $L/cmp_K21_rec0.log 2>&1
fi
echo DONE > $L/chain_g3b.done
