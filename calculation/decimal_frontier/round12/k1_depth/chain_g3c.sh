#!/bin/bash
# r12g3 chain C (1 thread): direct fold check with the INDEPENDENT code (genuine addition) inside its own cores:
# rec2 K=20 orbits 0 and 1 (after g3_core_rec2.sh), rec0 K=17 orbit 0 (after chain B's core step).
# Compare with kink7: rec2 K20 o0 successors-in-Cyc 10,595,481, o1 8,737,601; rec0 K17 28,583,281; cycles 0.
R=~/p196_run/r12g; L=$R/logs/g3; D=$R/data/indep
cd $D
while ! grep -q DONE $L/cmp_rec2_o1.log 2>/dev/null; do sleep 20; done
for o in 0 1; do /usr/bin/time -l $R/bin/indep_b fold $D/rec2.rows 20 $D/g3core_rec2_o$o/core_20.bin 3 > $L/fold_rec2_K20_o$o.log 2> $L/fold_rec2_K20_o$o.err; done
while ! grep -q "core_17.bin" $L/cmp_rec0_o0.log 2>/dev/null; do sleep 30; done
/usr/bin/time -l $R/bin/indep_b fold $D/rec0.rows 17 $D/g3core_rec0_o0/core_17.bin 3 > $L/fold_rec0_K17_o0.log 2> $L/fold_rec0_K17_o0.err
echo DONE > $L/chain_g3c.done
