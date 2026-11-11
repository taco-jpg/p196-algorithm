#!/bin/bash
# r12g3 chain A (<= 4 threads next to kfwd3 rec0 K=23): wait for indep rec2 K=27 o0 and the indep cores; then
#  (1) compare indep K=27 o0 with kfwd3; (2) base-9 planted control of the K > 25 path || indep rec2 K=21 orbit 1 (own Core(17));
#  (3) rec2 K=24 (Kb=20) both orbits: kfwd3 with kink7 Cyc(20) || indep with its OWN Core(20) (fully independent filters);
#  (4) indep fwd rec2 K=27 orbit 1 (kink7 Cyc(23) o1), the second orbit of the deepest rec2 result.
R=~/p196_run/r12g; L=$R/logs/g3; PY=~/p196_run/venv/bin/python; D=$R/data/indep
cd $R/data
while ! grep -q -E "^(EMPTY|STABLE|UNDECIDED)" $R/logs/indep/ifwd_rec2_K27_o0.log 2>/dev/null; do sleep 20; done
sleep 5
$PY $R/src/cmpsteps.py $R/logs/fwd2/rec2_K27_k4_o0.log $R/logs/indep/ifwd_rec2_K27_o0.log > $L/cmp_K27_o0.log 2>&1
while ! grep -q DONE $L/cmp_rec2_o1.log 2>/dev/null; do sleep 20; done
# (2)
$R/g3_b9_planted.sh &
/usr/bin/time -l $R/bin/indep_b fwd $D/rec2.rows 21 17 $D/g3core_rec2_o1/core_17.bin 4 $D/top/top_4.bin 7 18 1 2 8 27 3 > $L/ifwd_rec2_K21_o1.log 2> $L/ifwd_rec2_K21_o1.err
$PY $R/src/cmpsteps.py $R/logs/fwd/rec2_K21_k4_o1.log $L/ifwd_rec2_K21_o1.log > $L/cmp_K21_o1.log 2>&1
wait
# (3)
for o in 0 1; do
  $PY $R/src/select_phase.py $R/data/k7/rec2_K20_o$o.bin 20 48 4 $R/data/top/top_4.bin > $L/select_rec2_K20_o$o.log 2>&1
  set -- $(grep ^BEST $L/select_rec2_K20_o$o.log)
  t0=$2; j0=$3; p0=$4
  /usr/bin/time -l $R/bin/kfwd3 $R/data/lat_rec2.tbl 24 4 $R/data/k7/rec2_K20_o$o.bin $t0 $j0 $p0 4000 2 0 $R/data/top/top_4.bin 4 > $L/kfwd_rec2_K24_o$o.log 2> $L/kfwd_rec2_K24_o$o.err &
  /usr/bin/time -l $R/bin/indep_b fwd $D/rec2.rows 24 20 $D/g3core_rec2_o$o/core_20.bin 4 $D/top/top_4.bin $t0 $j0 $p0 2 8 27 3 > $L/ifwd_rec2_K24_o$o.log 2> $L/ifwd_rec2_K24_o$o.err
  wait
  $PY $R/src/cmpsteps.py $L/kfwd_rec2_K24_o$o.log $L/ifwd_rec2_K24_o$o.log > $L/cmp_K24_o$o.log 2>&1
done
# (4)
/usr/bin/time -l $R/bin/indep_b fwd $D/rec2.rows 27 23 $R/data/k7/rec2_K23_o1.bin 4 $D/top/top_4.bin 7 14 1 4 8 27 3 > $L/ifwd_rec2_K27_o1.log 2> $L/ifwd_rec2_K27_o1.err
$PY $R/src/cmpsteps.py $R/logs/fwd2/rec2_K27_k4_o1.log $L/ifwd_rec2_K27_o1.log > $L/cmp_K27_o1.log 2>&1
echo DONE > $L/chain_g3a.done
