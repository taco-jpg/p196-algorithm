#!/bin/bash
# r12g3: independent core (src/indep, genuine words) for rec2 orbits 0 and 1 up to K=20, then compare with kink7 files K=17..20
R=~/p196_run/r12g; D=$R/data/indep; L=$R/logs/g3
cd $D
/usr/bin/time -l $R/bin/indep_b core $D/rec2.rows 5 18 1 20 $D/g3core_rec2_o0 1 3 > $L/core_rec2_o0.log 2> $L/core_rec2_o0.err
for K in 17 18 19 20; do $R/bin/indep_b cmp $D/g3core_rec2_o0/core_$K.bin $R/data/k7/rec2_K${K}_o0.bin >> $L/cmp_rec2_o0.log 2>&1; done
/usr/bin/time -l $R/bin/indep_b core $D/rec2.rows 7 18 1 20 $D/g3core_rec2_o1 1 3 > $L/core_rec2_o1.log 2> $L/core_rec2_o1.err
for K in 17 18 19 20; do $R/bin/indep_b cmp $D/g3core_rec2_o1/core_$K.bin $R/data/k7/rec2_K${K}_o1.bin >> $L/cmp_rec2_o1.log 2>&1; done
echo DONE >> $L/cmp_rec2_o1.log
