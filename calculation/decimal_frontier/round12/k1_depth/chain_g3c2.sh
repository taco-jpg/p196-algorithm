#!/bin/bash
# r12g3 chain C2 (1 thread): indep fold check (genuine addition, bin/indep_g3f = fold mode with the kink key format for K > 20) inside
# the independent cores K = 21..23 of rec2: orbit 0 now; orbit 1 after corefrom o1.  Compare with kink7: successors-in-Cyc o0 K21..23 =
# 17,079,408 / 27,736,184 / 44,301,524; o1 = 14,054,984 / 22,412,638 / 36,099,977; cycles 0.
R=~/p196_run/r12g; L=$R/logs/g3; D=$R/data/indep
cd $D
for K in 21 22 23; do /usr/bin/time -l $R/bin/indep_g3f fold $D/rec2.rows $K $D/g3core2_rec2_o0/core_$K.bin 3 > $L/fold_rec2_K${K}_o0.log 2> $L/fold_rec2_K${K}_o0.err; done
while ! [ "$(grep -c -E 'EQUAL|DIFFERENT' $L/cmp2_rec2_o1.log 2>/dev/null)" = "3" ]; do sleep 20; done
for K in 21 22 23; do /usr/bin/time -l $R/bin/indep_g3f fold $D/rec2.rows $K $D/g3core2_rec2_o1/core_$K.bin 3 > $L/fold_rec2_K${K}_o1.log 2> $L/fold_rec2_K${K}_o1.err; done
echo DONE > $L/chain_g3c2.done
