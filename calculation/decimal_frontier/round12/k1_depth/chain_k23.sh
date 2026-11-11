#!/bin/zsh
# r12g2: wait for kink7 rec0 o0 K=19, the independent rec0 K=20 run and kfwd rec0 K=22, pick the cheapest phase,
# run kfwd3 rec0 K=23 (Cyc(19) + TopCyc(4)), 4 threads  (keeps r12g2 at <= 8 busy cores together with relsat)
R=~/p196_run/r12g
while ! grep -q "^K=19 orbit" $R/logs/k7_rec0_o0_K19.log 2>/dev/null; do sleep 30; done
~/p196_run/venv/bin/python $R/src/select_phase.py $R/data/k7/rec0_K19_o0.bin 19 20 4 $R/data/top/top_4.bin > $R/logs/fwd2/select_rec0_K19.log 2>&1
while ! grep -q -E "^(EMPTY|STABLE|UNDECIDED)" $R/logs/indep/ifwd_rec0_K20.log 2>/dev/null; do sleep 30; done
while ! grep -q "^DONE" $R/logs/fwd2/rec0_K22_k4_o0.log 2>/dev/null; do sleep 30; done
set -- $(grep ^BEST $R/logs/fwd2/select_rec0_K19.log)
$R/run_fwd.sh rec0 23 4 $R/data/k7/rec0_K19_o0.bin $2 $3 $4 4 rec0_K23_k4_o0
